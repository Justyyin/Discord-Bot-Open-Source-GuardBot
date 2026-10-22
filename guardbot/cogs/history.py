"""History of settings changes with rollback, and copying settings from one server to another."""

import hashlib
import json
import logging
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from .. import configio, i18n
from ..utils import emb, require, trim

log = logging.getLogger(__name__)

MAX_ENTRY_BYTES = 120_000
ACTOR_WINDOW = 90


def diff(old, new):
    """Names of the sections whose value differs."""
    return sorted(k for k in set(old) | set(new) if old.get(k) != new.get(k))


def make_entry(number, old, new, who, now):
    """Build a history entry for a change: which sections, the values before and who probably did it. Sections too large to store cannot be rolled back."""
    changed = diff(old, new)
    before = {}
    for key in changed:
        value = old.get(key)
        if value is not None and len(json.dumps(value)) <= MAX_ENTRY_BYTES:
            before[key] = value
    return {"id": number, "ts": int(now), "sections": changed, "before": before, "who": who}


def recent_actors(actors, now, window=ACTOR_WINDOW):
    """The users and commands seen shortly before a change, newest first, without repeats."""
    seen, out = set(), []
    for ts, uid, what in sorted(actors, reverse=True):
        if now - ts <= window and (uid, what) not in seen:
            seen.add((uid, what))
            out.append([uid, what])
    return out[:4]


class Confirm(discord.ui.View):
    """Confirm or cancel an action that changes settings."""

    def __init__(self, user_id):
        """Remember who may answer."""
        super().__init__(timeout=90)
        self.user_id = user_id
        self.answer = None

    async def interaction_check(self, interaction):
        """Only the person who started the action may answer."""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This is not your confirmation."), ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Apply", style=discord.ButtonStyle.danger)
    async def yes(self, interaction, button):
        """Go on."""
        self.answer = True
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def no(self, interaction, button):
        """Stop."""
        self.answer = False
        await interaction.response.defer()
        self.stop()


class History(commands.Cog):
    """Settings history, rollback and copy."""

    hist = app_commands.Group(name="history", description="Who changed which settings, and take changes back", guild_only=True)

    da = app_commands.Group(name="dashaccess", description="Who may use the web dashboard besides the administrators", guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot
        self.last = {}
        self.digest = {}

    async def cog_load(self):
        """Start the watcher."""
        self.watch.start()

    async def cog_unload(self):
        """Stop the watcher."""
        self.watch.cancel()

    def conf(self, gid):
        """Return the history store of a server."""
        return self.bot.cfg(gid)["history"]

    def record(self, guild, now=None):
        """Compare the settings with the last known state and store an entry if they differ. Returns the entry or None."""
        now = now or time.time()
        current = configio.sections(self.bot.cfg(guild.id))
        text = json.dumps(current, sort_keys=True, default=str)
        digest = hashlib.sha1(text.encode()).hexdigest()
        if guild.id not in self.last:
            self.last[guild.id], self.digest[guild.id] = current, digest
            return None
        if digest == self.digest[guild.id]:
            return None
        h = self.conf(guild.id)
        entry = make_entry(h["next"], self.last[guild.id], current, recent_actors(self.bot.actors.get(guild.id, []), now), now)
        self.last[guild.id], self.digest[guild.id] = current, digest
        if not entry["sections"]:
            return None
        h["next"] += 1
        h["items"].append(entry)
        del h["items"][:-max(5, h["keep"])]
        return entry

    @tasks.loop(seconds=20)
    async def watch(self):
        """Look for changed settings on every server."""
        for guild in list(self.bot.guilds):
            if not self.bot.module_on(guild.id, "history"):
                self.last.pop(guild.id, None)
                continue
            try:
                self.record(guild)
            except Exception:  # one broken server must not stop the others
                log.exception("settings history of %s failed", guild.id)

    @watch.before_loop
    async def _wait(self):
        """Wait until the bot is connected."""
        await self.bot.wait_until_ready()

    def who_text(self, entry):
        """Readable text for the probable authors of a change."""
        return ", ".join(f"<@{uid}> ({what})" for uid, what in entry["who"]) or "unknown (no command seen)"

    @hist.command(name="list", description="Show the latest changes of the settings")
    async def hist_list(self, it: discord.Interaction, page: app_commands.Range[int, 1, 50] = 1):
        """Show the latest changes of the settings."""
        self.record(it.guild)
        items = self.conf(it.guild_id)["items"][::-1]
        chunk = items[(page - 1) * 8: page * 8]
        lines = [f"**#{x['id']}** <t:{x['ts']}:R> {', '.join(x['sections'])}\n{self.who_text(x)}" + ("" if x["before"] else " (cannot be rolled back)") for x in chunk]
        e = emb("Settings history", "\n".join(lines) or "No changes recorded yet. Changes are noticed every 20 seconds.", discord.Color.blurple())
        e.set_footer(text="Who is a guess: the users who used commands or buttons shortly before the change.")
        await it.response.send_message(embed=e, ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @hist.command(name="show", description="Show one change in detail")
    async def hist_show(self, it: discord.Interaction, number: int):
        """Show one change in detail."""
        entry = next((x for x in self.conf(it.guild_id)["items"] if x["id"] == number), None)
        if entry is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no change with that number."), ephemeral=True)
        now = configio.sections(self.bot.cfg(it.guild_id))
        lines = []
        for key in entry["sections"]:
            if key not in entry["before"]:
                lines.append(f"**{key}**: too large to keep")
                continue
            before, after = entry["before"][key], now.get(key)
            lines.append(f"**{key}**: " + (f"{len(json.dumps(before))} characters before" if isinstance(before, (dict, list)) else f"before: {trim(str(before), 80)}") + ("" if after != before else ", same as now"))
        await it.response.send_message(embed=emb(f"Change #{number}", f"<t:{entry['ts']}:F>\n{self.who_text(entry)}\n\n" + "\n".join(lines), discord.Color.blurple()), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @hist.command(name="rollback", description="Put the settings back to how they were before a change")
    @app_commands.describe(number="Number of the change", section="Only this section, empty = everything the change touched")
    async def hist_rollback(self, it: discord.Interaction, number: int, section: Optional[str] = None):
        """Put the settings back to how they were before a change. Later changes to the same sections are replaced too."""
        if not await require(it, "administrator"):
            return
        entry = next((x for x in self.conf(it.guild_id)["items"] if x["id"] == number), None)
        if entry is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no change with that number."), ephemeral=True)
        keys = [k for k in entry["sections"] if k in entry["before"] and (section is None or k == section)]
        if not keys:
            return await it.response.send_message("Nothing can be rolled back for this change.", ephemeral=True)
        view = Confirm(it.user.id)
        await it.response.send_message(f"Put {', '.join(keys)} back to the state before change #{number}? Settings changed since then in these sections are lost.", view=view, ephemeral=True)
        await view.wait()
        if not view.answer:
            return await it.edit_original_response(content="Cancelled.", view=None)
        cfg = self.bot.cfg(it.guild_id)
        for key in keys:
            configio.restore(cfg, key, entry["before"][key])
        self.bot.note_actor(it.guild_id, it.user.id, f"/admin history rollback {number}")
        self.record(it.guild)
        e = emb("Settings rolled back", f"Change #{number}: {', '.join(keys)}", discord.Color.orange(), it.user)
        self.bot.log(it.guild, "server", e)
        await it.edit_original_response(content=f"Done: {', '.join(keys)}. Commands and menus use the old values at once.", view=None)

    @hist.command(name="keep", description="How many changes are kept")
    async def hist_keep(self, it: discord.Interaction, count: app_commands.Range[int, 5, 200]):
        """How many changes are kept."""
        if not await require(it, "administrator"):
            return
        self.conf(it.guild_id)["keep"] = count
        await it.response.send_message(f"The last {count} changes are kept.", ephemeral=True)

    # copy -----------------------------------------------------------------

    def source_guilds(self, user, current):
        """Servers the bot is on where the user may manage settings, except the current one."""
        out = []
        for g in self.bot.guilds:
            m = g.get_member(user.id)
            if g.id != current and m is not None and m.guild_permissions.manage_guild:
                out.append(g)
        return out

    async def source_autocomplete(self, it: discord.Interaction, current: str):
        """Offer the servers the user manages."""
        return [app_commands.Choice(name=g.name[:90], value=str(g.id)) for g in self.source_guilds(it.user, it.guild_id) if current.lower() in g.name.lower()][:25]

    async def section_autocomplete(self, it: discord.Interaction, current: str):
        """Offer the copyable sections."""
        names = ["all"] + sorted(configio.sections(self.bot.cfg(it.guild_id)))
        last = current.split(",")[-1].strip().lower()
        base = ",".join(x.strip() for x in current.split(",")[:-1])
        return [app_commands.Choice(name=(base + "," if base else "") + n, value=(base + "," if base else "") + n) for n in names if last in n][:25]

    @hist.command(name="copy", description="Copy settings from another server where you are a manager")
    @app_commands.describe(source="Server to copy from", sections="Sections separated by commas, or all", dry_run="Only show what would happen")
    @app_commands.autocomplete(source=source_autocomplete, sections=section_autocomplete)
    async def hist_copy(self, it: discord.Interaction, source: str, sections: str = "all", dry_run: bool = True):
        """Copy settings from another server. Channels and roles are matched by name, anything without a counterpart is left out. You must manage both servers."""
        if not await require(it, "administrator"):
            return
        src = self.bot.get_guild(int(source)) if source.isdigit() else None
        member = src.get_member(it.user.id) if src else None
        if src is None or src.id == it.guild_id or member is None or not member.guild_permissions.manage_guild:
            return await it.response.send_message("Choose a server from the list where you have the Manage Server permission and where I am too.", ephemeral=True)
        have = configio.sections(self.bot.cfg(src.id))
        wanted = list(have) if sections.strip().lower() == "all" else [s.strip() for s in sections.split(",") if s.strip()]
        unknown = [s for s in wanted if s not in have]
        if unknown:
            return await it.response.send_message(f"Unknown sections: {', '.join(unknown)}", ephemeral=True)
        mapping = configio.id_map(src, it.guild)
        plan, lines = {}, []
        for key in wanted:
            new, ok, dropped = configio.remap(have[key], mapping)
            plan[key] = new
            lines.append(f"{key}: {ok} channel/role ids matched, {dropped} without counterpart left out")
        text = trim("\n".join(lines), 1500)
        if dry_run:
            return await it.response.send_message(f"Nothing was changed. This would be copied from {src.name}:\n{text}\nRun it again with dry_run set to false to apply.", ephemeral=True)
        view = Confirm(it.user.id)
        await it.response.send_message(f"Copy {len(plan)} sections from {src.name} and replace the settings here?\n{text}", view=view, ephemeral=True)
        await view.wait()
        if not view.answer:
            return await it.edit_original_response(content="Cancelled.", view=None)
        cfg = self.bot.cfg(it.guild_id)
        for key, value in plan.items():
            configio.restore(cfg, key, value)
        self.bot.note_actor(it.guild_id, it.user.id, f"/admin history copy from {src.name}")
        self.record(it.guild)
        self.bot.log(it.guild, "server", emb("Settings copied", f"From {src.name}: {', '.join(plan)}", discord.Color.orange(), it.user))
        await it.edit_original_response(content=f"Copied {len(plan)} sections. Undo it with /admin history rollback.", view=None)

    @da.command(name="add", description="Give a role access to the dashboard")
    @app_commands.describe(level="viewer = read only, mod = may change moderation settings", role="Role")
    async def da_add(self, it: discord.Interaction, level: Literal["viewer", "mod"], role: discord.Role):
        """Give a role access to the dashboard. Moderators can change the moderation settings, viewers can only read."""
        if not await require(it, "administrator"):
            return
        access = self.bot.cfg(it.guild_id)["dashboard_access"]
        key = f"{level}_roles"
        other = "mod_roles" if level == "viewer" else "viewer_roles"
        if role.id in access[other]:
            access[other].remove(role.id)
        if role.id not in access[key]:
            access[key].append(role.id)
        await it.response.send_message(f"{role.mention} is now '{level}' in the dashboard. Members with it can sign in at once.", ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @da.command(name="remove", description="Take dashboard access away from a role")
    async def da_remove(self, it: discord.Interaction, role: discord.Role):
        """Take dashboard access away from a role."""
        if not await require(it, "administrator"):
            return
        access = self.bot.cfg(it.guild_id)["dashboard_access"]
        for key in ("viewer_roles", "mod_roles"):
            if role.id in access[key]:
                access[key].remove(role.id)
        await it.response.send_message("Removed.", ephemeral=True)

    @da.command(name="list", description="Show who has dashboard access")
    async def da_list(self, it: discord.Interaction):
        """Show who has dashboard access."""
        access = self.bot.cfg(it.guild_id)["dashboard_access"]
        text = f"Moderators: {' '.join('<@&' + str(i) + '>' for i in access['mod_roles']) or 'none'}\nViewers: {' '.join('<@&' + str(i) + '>' for i in access['viewer_roles']) or 'none'}\nAdministrators (Manage Server) always have full access."
        await it.response.send_message(text, ephemeral=True, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(History(bot))
