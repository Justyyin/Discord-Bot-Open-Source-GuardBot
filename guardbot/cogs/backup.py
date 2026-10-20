"""Backup and restore of roles, channels, emojis, webhooks and member roles."""

import base64
import gzip
import io
import json
import logging
import re
import time
from pathlib import Path
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ..utils import CREDIT, bulk

log = logging.getLogger(__name__)

NAME_RE = re.compile(r"[\w-]{1,40}")
EXT = ".json.gz"


def pack_ow(channel):
    """Convert the permission overwrites of a channel to plain dicts."""
    out = []
    for target, o in channel.overwrites.items():
        allow, deny = o.pair()
        kind = "role" if isinstance(target, discord.Role) else "member"
        out.append({"type": kind, "id": target.id, "allow": allow.value, "deny": deny.value})
    return out


async def snapshot(guild, include_members=True, include_emojis=True):
    """Collect roles, channels, emojis, webhooks and member roles of a server into one dict."""
    roles = [
        {"id": r.id, "name": r.name, "color": r.color.value, "hoist": r.hoist, "mentionable": r.mentionable, "permissions": r.permissions.value, "position": r.position}
        for r in sorted(guild.roles, key=lambda r: r.position)
        if not r.is_default() and not r.managed
    ]
    channels = []
    for c in sorted(guild.channels, key=lambda c: (not isinstance(c, discord.CategoryChannel), c.position)):
        channels.append({
            "id": c.id, "name": c.name, "type": c.type.name, "category": c.category_id, "position": c.position,
            "topic": getattr(c, "topic", None), "nsfw": getattr(c, "nsfw", False), "slowmode": getattr(c, "slowmode_delay", 0),
            "bitrate": getattr(c, "bitrate", None), "user_limit": getattr(c, "user_limit", None), "overwrites": pack_ow(c),
        })
    emojis = []
    if include_emojis:
        for e in guild.emojis:
            try:
                raw = await e.read()
            except discord.HTTPException:
                continue
            emojis.append({"name": e.name, "animated": e.animated, "roles": [r.id for r in e.roles], "image": base64.b64encode(raw).decode()})
    webhooks = []
    try:
        for w in await guild.webhooks():
            if w.type == discord.WebhookType.incoming and w.channel:
                webhooks.append({"name": w.name, "channel": w.channel.id})
    except discord.HTTPException as exc:
        log.warning("guild.webhooks failed: %s", exc)
    members = {}
    if include_members:
        for m in guild.members:
            ids = [r.id for r in m.roles if not r.is_default() and not r.managed]
            if ids:
                members[str(m.id)] = ids
    return {
        "meta": {"generator": CREDIT, "format": 2, "guild": guild.name, "guild_id": guild.id, "created": discord.utils.utcnow().isoformat()},
        "roles": roles, "channels": channels, "emojis": emojis, "webhooks": webhooks, "members": members,
    }


class Backup(commands.Cog):
    """Creates, schedules and restores server backups."""
    grp = app_commands.Group(name="backup", description="Backup and restore roles, channels, emojis and webhooks", default_permissions=discord.Permissions(administrator=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot

    async def cog_load(self):
        """Start the background loop of this cog."""
        self.schedule_loop.start()

    async def cog_unload(self):
        """Stop the background loop of this cog."""
        self.schedule_loop.cancel()

    def folder(self, gid):
        """Return the backup folder of a server and create it if needed."""
        p = Path(self.bot.settings.get("data_dir", "data")) / "backups" / str(gid)
        p.mkdir(parents=True, exist_ok=True)
        return p

    async def create(self, guild, name):
        """Write a compressed backup file and return the snapshot."""
        b = self.bot.cfg(guild.id)["backup"]
        data = await snapshot(guild, b["include_members"], b["include_emojis"])
        raw = gzip.compress(json.dumps(data).encode("utf-8"))
        (self.folder(guild.id) / f"{name}{EXT}").write_bytes(raw)
        return data

    def files(self, gid):
        """List the backup files of a server in name order."""
        return sorted(self.folder(gid).glob(f"*{EXT}"))

    @tasks.loop(minutes=15)
    async def schedule_loop(self):
        """Create automatic backups when their interval has passed and delete old ones."""
        try:
            for guild in self.bot.guilds:
                b = self.bot.cfg(guild.id)["backup"]
                if not b["auto"] or not self.bot.module_on(guild.id, "backup"):
                    continue
                if time.time() - b["last"] < b["interval_hours"] * 3600:
                    continue
                await self.create(guild, "auto-" + discord.utils.utcnow().strftime("%Y-%m-%d_%H-%M"))
                b["last"] = int(time.time())
                autos = [f for f in self.files(guild.id) if f.name.startswith("auto-")]
                for old in autos[:-b["keep"]]:
                    old.unlink(missing_ok=True)
        except Exception:
            log.exception("scheduled backup failed")

    @schedule_loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected before the loop starts."""
        await self.bot.wait_until_ready()

    @grp.command(name="create", description="Save roles, channels, emojis and webhooks")
    @app_commands.describe(name="Name of the backup (default: date)")
    async def b_create(self, it: discord.Interaction, name: str = ""):
        """Save roles, channels, emojis and webhooks."""
        name = name or discord.utils.utcnow().strftime("%Y-%m-%d_%H-%M")
        if not NAME_RE.fullmatch(name):
            return await it.response.send_message("Use only letters, numbers, - and _ (max 40).", ephemeral=True)
        await it.response.defer(ephemeral=True)
        d = await self.create(it.guild, name)
        await it.followup.send(f"Backup '{name}' saved: {len(d['roles'])} roles, {len(d['channels'])} channels, {len(d['emojis'])} emojis, {len(d['webhooks'])} webhooks, {len(d['members'])} members with roles.")

    @grp.command(name="schedule", description="Automatic backups")
    @app_commands.describe(enabled="Turn on or off", interval_hours="Hours between backups", keep="Automatic backups to keep", include_members="Also store which member had which role", include_emojis="Also store emoji images")
    async def b_schedule(self, it: discord.Interaction, enabled: Optional[bool] = None, interval_hours: Optional[app_commands.Range[int, 1, 720]] = None, keep: Optional[app_commands.Range[int, 1, 60]] = None, include_members: Optional[bool] = None, include_emojis: Optional[bool] = None):
        """Automatic backups."""
        b = self.bot.cfg(it.guild_id)["backup"]
        for k, v in (("auto", enabled), ("interval_hours", interval_hours), ("keep", keep), ("include_members", include_members), ("include_emojis", include_emojis)):
            if v is not None:
                b[k] = v
        await it.response.send_message(f"Automatic backups: {'on' if b['auto'] else 'off'}, every {b['interval_hours']} h, keep {b['keep']}, members {b['include_members']}, emojis {b['include_emojis']}", ephemeral=True)

    @grp.command(name="list", description="List backups")
    async def b_list(self, it: discord.Interaction):
        """List backups."""
        lines = [f"{f.name[:-len(EXT)]} ({f.stat().st_size // 1024} KB)" for f in self.files(it.guild_id)]
        await it.response.send_message("\n".join(lines) or "No backups yet.", ephemeral=True)

    def path(self, gid, name):
        """Return the path of a backup by name, or None if the name is invalid or missing."""
        p = self.folder(gid) / f"{name}{EXT}"
        return p if NAME_RE.fullmatch(name) and p.exists() else None

    @grp.command(name="download", description="Download a backup file")
    async def b_download(self, it: discord.Interaction, name: str):
        """Download a backup file."""
        p = self.path(it.guild_id, name)
        if not p:
            return await it.response.send_message("Backup not found.", ephemeral=True)
        if p.stat().st_size > 24 * 1024 * 1024:
            return await it.response.send_message("The file is too large for Discord. Copy it from the data/backups folder.", ephemeral=True)
        await it.response.send_message(file=discord.File(io.BytesIO(p.read_bytes()), filename=p.name), ephemeral=True)

    @grp.command(name="delete", description="Delete a backup")
    async def b_delete(self, it: discord.Interaction, name: str):
        """Delete a backup."""
        p = self.path(it.guild_id, name)
        if not p:
            return await it.response.send_message("Backup not found.", ephemeral=True)
        p.unlink()
        await it.response.send_message("Deleted.", ephemeral=True)

    @grp.command(name="restore", description="Recreate missing roles, channels, emojis and webhooks (nothing is deleted)")
    @app_commands.describe(name="Backup name", member_roles="Give members their old roles back")
    async def b_restore(self, it: discord.Interaction, name: str, member_roles: bool = True):
        """Recreate missing roles, channels, emojis and webhooks (nothing is deleted)."""
        p = self.path(it.guild_id, name)
        if not p:
            return await it.response.send_message("Backup not found.", ephemeral=True)
        await it.response.defer(ephemeral=True)
        data = json.loads(gzip.decompress(p.read_bytes()))
        guild = it.guild
        rmap, cmap, report = {}, {}, {"roles": 0, "channels": 0, "emojis": 0, "webhooks": 0, "members": 0}
        for r in data["roles"]:
            role = discord.utils.get(guild.roles, name=r["name"])
            if role is None:
                try:
                    role = await guild.create_role(name=r["name"], colour=discord.Colour(r["color"]), hoist=r["hoist"], mentionable=r["mentionable"], permissions=discord.Permissions(r["permissions"]), reason="Backup restore")
                    report["roles"] += 1
                except discord.HTTPException:
                    continue
            rmap[r["id"]] = role
        ordered = [rmap[r["id"]] for r in data["roles"] if r["id"] in rmap and rmap[r["id"]].is_assignable()]
        if ordered:
            base = min(r.position for r in ordered)
            try:
                await guild.edit_role_positions({role: base + i for i, role in enumerate(ordered)}, reason="Backup restore")
            except discord.HTTPException as exc:
                log.warning("guild.edit_role_positions failed: %s", exc)

        def overwrites(items):
            """Build permission overwrites for the restored channel from the saved ones."""
            out = {}
            for o in items:
                target = (guild.default_role if o["id"] == data["meta"].get("guild_id") else rmap.get(o["id"])) if o["type"] == "role" else guild.get_member(o["id"])
                if target:
                    out[target] = discord.PermissionOverwrite.from_pair(discord.Permissions(o["allow"]), discord.Permissions(o["deny"]))
            return out

        for c in data["channels"]:
            if c["type"] != "category":
                continue
            cat = discord.utils.get(guild.categories, name=c["name"])
            if cat is None:
                try:
                    cat = await guild.create_category(c["name"], overwrites=overwrites(c["overwrites"]), reason="Backup restore")
                    report["channels"] += 1
                except discord.HTTPException:
                    continue
            cmap[c["id"]] = cat
        for c in data["channels"]:
            if c["type"] == "category":
                continue
            parent = cmap.get(c["category"])
            pool = parent.channels if parent else guild.channels
            found = next((x for x in pool if x.name == c["name"] and x.type.name == c["type"]), None)
            if found:
                cmap[c["id"]] = found
                continue
            kw = {"category": parent, "overwrites": overwrites(c["overwrites"]), "reason": "Backup restore"}
            try:
                if c["type"] in ("text", "news"):
                    ch = await guild.create_text_channel(c["name"], topic=c["topic"], nsfw=c["nsfw"], slowmode_delay=c["slowmode"], **kw)
                elif c["type"] == "voice":
                    ch = await guild.create_voice_channel(c["name"], user_limit=c["user_limit"] or 0, **kw)
                elif c["type"] == "stage_voice":
                    ch = await guild.create_stage_channel(c["name"], **kw)
                elif c["type"] == "forum":
                    ch = await guild.create_forum(c["name"], topic=c["topic"] or "", nsfw=c["nsfw"], **kw)
                else:
                    continue
                cmap[c["id"]] = ch
                report["channels"] += 1
            except discord.HTTPException as exc:
                log.warning("guild.create_text_channel failed: %s", exc)
        have = {e.name for e in guild.emojis}
        for e in data.get("emojis", []):
            if e["name"] in have:
                continue
            try:
                await guild.create_custom_emoji(name=e["name"], image=base64.b64decode(e["image"]), roles=[rmap[i] for i in e["roles"] if i in rmap], reason="Backup restore")
                report["emojis"] += 1
            except discord.HTTPException:
                break
        for w in data.get("webhooks", []):
            ch = cmap.get(w["channel"])
            if not isinstance(ch, discord.TextChannel):
                continue
            try:
                if not any(x.name == w["name"] for x in await ch.webhooks()):
                    await ch.create_webhook(name=w["name"], reason="Backup restore")
                    report["webhooks"] += 1
            except discord.HTTPException as exc:
                log.warning("any failed: %s", exc)
        if member_roles:
            def make(member, roles):
                """Create the job that gives one member their roles back."""

                async def job():
                    """Add the saved roles to one member and count it."""
                    await member.add_roles(*roles, reason="Backup restore")
                    report["members"] += 1
                return job

            jobs = []
            for uid, ids in data.get("members", {}).items():
                m = guild.get_member(int(uid))
                if not m:
                    continue
                roles = [rmap[i] for i in ids if i in rmap and rmap[i].is_assignable() and rmap[i] not in m.roles]
                if roles:
                    jobs.append(make(m, roles))
            _, role_failures = await bulk(jobs, limit=3)
            report["failed member updates"] = role_failures
        await it.followup.send("Restore finished. Created: " + ", ".join(f"{v} {k}" for k, v in report.items()) + ". Existing items were left untouched.")


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Backup(bot))
