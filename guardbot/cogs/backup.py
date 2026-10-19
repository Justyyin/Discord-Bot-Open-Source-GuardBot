# Copyright (c) Justyn
import asyncio
import io
import json
import re
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import CREDIT

NAME_RE = re.compile(r"[\w-]{1,40}")


def snapshot(guild):
    roles = [
        {"id": r.id, "name": r.name, "color": r.color.value, "hoist": r.hoist, "mentionable": r.mentionable, "permissions": r.permissions.value}
        for r in sorted(guild.roles, key=lambda r: r.position)
        if not r.is_default() and not r.managed
    ]
    channels = []
    for c in sorted(guild.channels, key=lambda c: (isinstance(c, discord.CategoryChannel) is False, c.position)):
        ow = []
        for target, o in c.overwrites.items():
            if isinstance(target, discord.Role):
                allow, deny = o.pair()
                ow.append({"role": target.id, "allow": allow.value, "deny": deny.value})
        channels.append({
            "id": c.id,
            "name": c.name,
            "type": c.type.name,
            "category": c.category_id,
            "topic": getattr(c, "topic", None),
            "nsfw": getattr(c, "nsfw", False),
            "slowmode": getattr(c, "slowmode_delay", 0),
            "bitrate": getattr(c, "bitrate", None),
            "user_limit": getattr(c, "user_limit", None),
            "overwrites": ow,
        })
    return {
        "meta": {"generator": CREDIT, "format": 1, "guild": guild.name, "created": discord.utils.utcnow().isoformat()},
        "roles": roles,
        "channels": channels,
    }


class Backup(commands.Cog):
    grp = app_commands.Group(name="backup", description="Backup and restore roles and channels", default_permissions=discord.Permissions(administrator=True), guild_only=True)

    def __init__(self, bot):
        self.bot = bot

    def folder(self, gid):
        p = Path(self.bot.settings.get("data_dir", "data")) / "backups" / str(gid)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @grp.command(name="create", description="Save roles and channel structure")
    @app_commands.describe(name="Name of the backup (default: date)")
    async def b_create(self, it: discord.Interaction, name: str = ""):
        name = name or discord.utils.utcnow().strftime("%Y-%m-%d_%H-%M")
        if not NAME_RE.fullmatch(name):
            return await it.response.send_message("Use only letters, numbers, - and _ (max 40).", ephemeral=True)
        data = snapshot(it.guild)
        (self.folder(it.guild_id) / f"{name}.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
        await it.response.send_message(f"Backup '{name}' saved: {len(data['roles'])} roles, {len(data['channels'])} channels.", ephemeral=True)

    @grp.command(name="list", description="List backups")
    async def b_list(self, it: discord.Interaction):
        files = sorted(self.folder(it.guild_id).glob("*.json"))
        await it.response.send_message("\n".join(f.stem for f in files) or "No backups yet.", ephemeral=True)

    @grp.command(name="download", description="Download a backup file")
    async def b_download(self, it: discord.Interaction, name: str):
        p = self.folder(it.guild_id) / f"{name}.json"
        if not NAME_RE.fullmatch(name) or not p.exists():
            return await it.response.send_message("Backup not found.", ephemeral=True)
        await it.response.send_message(file=discord.File(io.BytesIO(p.read_bytes()), filename=p.name), ephemeral=True)

    @grp.command(name="delete", description="Delete a backup")
    async def b_delete(self, it: discord.Interaction, name: str):
        p = self.folder(it.guild_id) / f"{name}.json"
        if not NAME_RE.fullmatch(name) or not p.exists():
            return await it.response.send_message("Backup not found.", ephemeral=True)
        p.unlink()
        await it.response.send_message("Deleted.", ephemeral=True)

    @grp.command(name="restore", description="Recreate missing roles and channels from a backup (nothing is deleted)")
    async def b_restore(self, it: discord.Interaction, name: str):
        p = self.folder(it.guild_id) / f"{name}.json"
        if not NAME_RE.fullmatch(name) or not p.exists():
            return await it.response.send_message("Backup not found.", ephemeral=True)
        await it.response.defer(ephemeral=True)
        data = json.loads(p.read_text(encoding="utf-8"))
        guild = it.guild
        rmap = {}
        made_r = made_c = 0
        for r in data["roles"]:
            role = discord.utils.get(guild.roles, name=r["name"])
            if role is None:
                try:
                    role = await guild.create_role(name=r["name"], colour=discord.Colour(r["color"]), hoist=r["hoist"], mentionable=r["mentionable"], permissions=discord.Permissions(r["permissions"]), reason="Backup restore")
                    made_r += 1
                    await asyncio.sleep(0.4)
                except discord.HTTPException:
                    continue
            rmap[r["id"]] = role

        def overwrites(items):
            out = {}
            for o in items:
                role = guild.default_role if o["role"] == data_everyone else rmap.get(o["role"])
                if role:
                    out[role] = discord.PermissionOverwrite.from_pair(discord.Permissions(o["allow"]), discord.Permissions(o["deny"]))
            return out

        data_everyone = guild.default_role.id
        cmap = {}
        for c in data["channels"]:
            if c["type"] != "category":
                continue
            cat = discord.utils.get(guild.categories, name=c["name"])
            if cat is None:
                try:
                    cat = await guild.create_category(c["name"], overwrites=overwrites(c["overwrites"]), reason="Backup restore")
                    made_c += 1
                    await asyncio.sleep(0.4)
                except discord.HTTPException:
                    continue
            cmap[c["id"]] = cat
        for c in data["channels"]:
            if c["type"] == "category":
                continue
            parent = cmap.get(c["category"])
            pool = parent.channels if parent else guild.channels
            if any(x.name == c["name"] and x.type.name == c["type"] for x in pool):
                continue
            kw = {"category": parent, "overwrites": overwrites(c["overwrites"]), "reason": "Backup restore"}
            try:
                if c["type"] in ("text", "news"):
                    await guild.create_text_channel(c["name"], topic=c["topic"], nsfw=c["nsfw"], slowmode_delay=c["slowmode"], **kw)
                elif c["type"] == "voice":
                    await guild.create_voice_channel(c["name"], user_limit=c["user_limit"] or 0, **kw)
                elif c["type"] == "stage_voice":
                    await guild.create_stage_channel(c["name"], **kw)
                elif c["type"] == "forum":
                    await guild.create_forum(c["name"], topic=c["topic"] or "", nsfw=c["nsfw"], **kw)
                else:
                    continue
                made_c += 1
                await asyncio.sleep(0.4)
            except discord.HTTPException:
                pass
        await it.followup.send(f"Restore finished: {made_r} roles and {made_c} channels created. Existing items were left untouched.")


async def setup(bot):
    await bot.add_cog(Backup(bot))
