"""Member management: sticky roles, name moderation, watch list and reason templates."""

import asyncio
import logging
import time
from datetime import timedelta
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ... import i18n, scamscan
from ...defaults import DANGEROUS
from ...utils import emb, fmt_duration, parse_duration, require, trim

log = logging.getLogger(__name__)

SCAN_SECONDS = 600

HIDDEN = dict.fromkeys(map(ord, "​‌‍‎‏⁠﻿­"))
ACTIONS = ("warn", "mute", "kick", "ban", "tempban", "jail")
ACTION_PERMISSION = {"warn": "moderate_members", "mute": "moderate_members", "kick": "kick_members", "ban": "ban_members", "tempban": "ban_members", "jail": "manage_roles"}


def keep_roles(roles, exclude=(), dangerous=False, skip=()):
    """IDs of the roles that are worth remembering: no @everyone, no bot roles, none excluded and by default none with dangerous permissions."""
    out = []
    for r in roles:
        if r.is_default() or r.managed or r.id in exclude or r.id in skip:
            continue
        if not dangerous and any(getattr(r.permissions, p, False) for p in DANGEROUS):
            continue
        out.append(r.id)
    return out


def dehoist(name):
    """Remove characters from the start of a name that push it to the top of the member list."""
    cleaned = (name or "").translate(HIDDEN).lstrip()
    while cleaned and ord(cleaned[0]) < 128 and not cleaned[0].isalnum():
        cleaned = cleaned[1:].lstrip()
    return cleaned


def banned_word(name, words):
    """The first banned word that is in a name, also with look-alike letters and spaces, or None."""
    compact = scamscan.normalize(name)[2]
    for w in words:
        key = scamscan.squash(w)
        if key and key in compact:
            return w
    return None


def check_name(name, conf):
    """Decide about a name. Returns (new name or None, reason or None). None means the name is fine."""
    if conf["dehoist"]:
        cleaned = dehoist(name)
        if cleaned != (name or ""):
            return (cleaned[:32] if cleaned else conf["rename_to"]), "starts with a special character"
    word = banned_word(name, conf["words"])
    if word:
        return conf["rename_to"], f"contains the banned word '{word}'"
    return None, None


class Via:
    """A small stand-in for a command context, so that interaction commands can use the approval check of text commands."""

    def __init__(self, it):
        """Copy what the approval check needs."""
        self.guild, self.author, self.channel, self.it = it.guild, it.user, it.channel, it

    async def send(self, text, ephemeral=False, **kwargs):
        """Answer through the interaction."""
        await self.it.followup.send(text, ephemeral=ephemeral)


class Members(commands.Cog):
    """Sticky roles, name moderation, watch list and reason templates."""

    sticky = app_commands.Group(name="stickyroles", description="Give roles and timeouts back to members who return", guild_only=True)
    nickname = app_commands.Group(name="nickname", description="Remove special characters and banned words from names", guild_only=True)
    watch = app_commands.Group(name="watch", description="Quietly watch members and tell the team at their first message", guild_only=True)
    reason = app_commands.Group(name="reason", description="Reason templates with a fixed punishment", guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    # sticky roles ---------------------------------------------------------

    def special_roles(self, gid):
        """Roles that are handled by other modules and must not be given back here."""
        c = self.bot.cfg(gid)
        return {r for r in (c["probation"]["role"], c["jail"]["role"], c["verify"]["unverified_role"]) if r}

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Remember the roles and a running timeout of a member who leaves."""
        gid = member.guild.id
        if member.bot or not self.bot.module_on(gid, "stickyroles"):
            return
        c = self.bot.cfg(gid)["stickyroles"]
        rec = self.bot.store.user(gid, member.id)
        if rec.get("jailed"):
            return
        data = {"ts": int(time.time())}
        if c["roles"]:
            data["roles"] = keep_roles(member.roles, c["exclude"], c["dangerous"], self.special_roles(gid))
        until = member.timed_out_until
        if c["punishments"] and until and until.timestamp() > time.time():
            data["timeout"] = int(until.timestamp())
        if data.get("roles") or data.get("timeout"):
            rec["sticky"] = data

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Give roles and a timeout back to a member who returns, and check the name."""
        gid = member.guild.id
        if member.bot:
            return
        if self.bot.module_on(gid, "stickyroles"):
            await self.restore(member)
        if self.bot.module_on(gid, "watchlist"):
            item = self.bot.cfg(gid)["watchlist"]["items"].get(str(member.id))
            if item:
                await self.alert(member.guild, member, item, "joined the server")
        await self.fix_name(member)

    async def restore(self, member):
        """Apply the remembered roles and timeout."""
        gid = member.guild.id
        rec = self.bot.store.users(gid).get(str(member.id))
        data = rec.pop("sticky", None) if rec else None
        if not data:
            return
        self.bot.store.user(gid, member.id)
        c = self.bot.cfg(gid)["stickyroles"]
        if c["days"] and time.time() - data["ts"] > c["days"] * 86400:
            return
        if not rec.get("jailed"):
            skip = self.special_roles(gid)
            roles = [r for r in (member.guild.get_role(i) for i in data.get("roles", [])) if r and r.is_assignable() and r.id not in skip and r.id not in c["exclude"]]
            if not c["dangerous"]:
                roles = [r for r in roles if not any(getattr(r.permissions, p, False) for p in DANGEROUS)]
            if roles:
                try:
                    await member.add_roles(*roles, reason="Sticky roles")
                except discord.HTTPException as exc:
                    log.warning("sticky roles for %s failed: %s", member.id, exc)
        left = data.get("timeout", 0) - time.time()
        if left > 5:
            try:
                await member.timeout(discord.utils.utcnow() + timedelta(seconds=min(left, 28 * 86400)), reason="Timeout continues after rejoining")
            except discord.HTTPException as exc:
                log.warning("timeout after rejoin for %s failed: %s", member.id, exc)
            else:
                e = emb("Timeout applied again", f"{member.mention} left during a timeout and came back. The rest of the timeout ({fmt_duration(int(left))}) applies again.", discord.Color.orange(), member)
                self.bot.log(member.guild, "moderation", e)

    @sticky.command(name="setup", description="Choose what is given back to members who return")
    @app_commands.describe(roles="Give roles back", punishments="Apply a running timeout again", days="Forget after this many days (0 = never)", dangerous="Also give back roles with dangerous permissions")
    async def sticky_setup(self, it: discord.Interaction, roles: Optional[bool] = None, punishments: Optional[bool] = None, days: Optional[app_commands.Range[int, 0, 3650]] = None, dangerous: Optional[bool] = None):
        """Choose what is given back to members who return."""
        if not await require(it):
            return
        c = self.bot.cfg(it.guild_id)["stickyroles"]
        for key, value in (("roles", roles), ("punishments", punishments), ("days", days), ("dangerous", dangerous)):
            if value is not None:
                c[key] = value
        self.bot.cfg(it.guild_id)["modules"]["stickyroles"] = True
        await it.response.send_message(i18n.say(it.client, it.guild, "Sticky roles are on. Roles: {roles}, running timeouts: {punishments}, forgotten after {value} days, dangerous roles: {dangerous}.", roles=c['roles'], punishments=c['punishments'], value=c['days'] or 'never', dangerous=c['dangerous']), ephemeral=True)

    @sticky.command(name="exclude", description="Never give a role back, or allow it again")
    async def sticky_exclude(self, it: discord.Interaction, role: discord.Role, remove: bool = False):
        """Never give a role back, or allow it again."""
        if not await require(it):
            return
        lst = self.bot.cfg(it.guild_id)["stickyroles"]["exclude"]
        if remove and role.id in lst:
            lst.remove(role.id)
        elif not remove and role.id not in lst:
            lst.append(role.id)
        await it.response.send_message(f"{role.mention} is {'allowed again' if remove else 'never given back'}.", ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @sticky.command(name="status", description="Show the settings and how many members are remembered")
    async def sticky_status(self, it: discord.Interaction):
        """Show the settings and how many members are remembered."""
        c = self.bot.cfg(it.guild_id)["stickyroles"]
        n = sum(1 for r in self.bot.store.users(it.guild_id).values() if r.get("sticky"))
        await it.response.send_message(
            i18n.say(it.client, it.guild, "Module: {value}. Roles: {roles}, timeouts: {punishments}, days: {value2}, dangerous: {dangerous}. Excluded roles: {value3}. Remembered members: {n}.", value='on' if self.bot.module_on(it.guild_id, 'stickyroles') else 'off', roles=c['roles'], punishments=c['punishments'], value2=c['days'] or 'never', dangerous=c['dangerous'], value3=' '.join(('<@&' + str(i) + '>' for i in c['exclude'])) or 'none', n=n), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @sticky.command(name="forget", description="Delete what is remembered about a member")
    async def sticky_forget(self, it: discord.Interaction, user: discord.User):
        """Delete what is remembered about a member."""
        if not await require(it):
            return
        rec = self.bot.store.users(it.guild_id).get(str(user.id))
        if rec and rec.pop("sticky", None):
            self.bot.store.user(it.guild_id, user.id)
            return await it.response.send_message(i18n.say(it.client, it.guild, "Forgotten."), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Nothing is stored about that member."), ephemeral=True)

    # name moderation -------------------------------------------------------

    async def fix_name(self, member):
        """Check the display name of a member and rename if a rule applies. Returns True if it was changed."""
        gid = member.guild.id
        if member.bot or not self.bot.module_on(gid, "nicknames"):
            return False
        c = self.bot.cfg(gid)["nicknames"]
        if member.id == member.guild.owner_id or any(r.id in c["exempt_roles"] for r in member.roles):
            return False
        name = member.display_name if c["usernames"] else (member.nick or "")
        if not name or member.nick == c["rename_to"]:
            return False
        new, why = check_name(name, c)
        if new is None:
            return False
        try:
            await member.edit(nick=new, reason=f"Name moderation: {why}")
        except discord.HTTPException as exc:
            log.info("name of %s could not be changed: %s", member.id, exc)
            return False
        if c["notify"]:
            e = emb("Name changed", f"{member.mention}: '{trim(name, 60)}' {why}. New nickname: '{new}'.", discord.Color.light_grey(), member)
            self.bot.log(member.guild, "moderation", e)
        return True

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Check a new nickname."""
        if before.nick != after.nick or before.display_name != after.display_name:
            await self.fix_name(after)

    @nickname.command(name="setup", description="Set the rules for names")
    @app_commands.describe(dehoist="Remove special characters at the start", usernames="Also check the global name, not only the nickname", rename_to="Nickname for banned names", notify="Write a log entry")
    async def nick_setup(self, it: discord.Interaction, dehoist: Optional[bool] = None, usernames: Optional[bool] = None, rename_to: Optional[app_commands.Range[str, 1, 32]] = None, notify: Optional[bool] = None):
        """Set the rules for names."""
        if not await require(it):
            return
        c = self.bot.cfg(it.guild_id)["nicknames"]
        for key, value in (("dehoist", dehoist), ("usernames", usernames), ("rename_to", rename_to), ("notify", notify)):
            if value is not None:
                c[key] = value
        self.bot.cfg(it.guild_id)["modules"]["nicknames"] = True
        await it.response.send_message(i18n.say(it.client, it.guild, "Name moderation is on. Dehoist: {dehoist}, check global names: {usernames}, replacement: '{rename_to}', banned words: {count}.", dehoist=c['dehoist'], usernames=c['usernames'], rename_to=c['rename_to'], count=len(c['words'])), ephemeral=True)

    @nickname.command(name="word", description="Add a banned word, or remove it again")
    async def nick_word(self, it: discord.Interaction, word: app_commands.Range[str, 2, 40], remove: bool = False):
        """Add a banned word, or remove it again."""
        if not await require(it):
            return
        words = self.bot.cfg(it.guild_id)["nicknames"]["words"]
        if remove:
            if word in words:
                words.remove(word)
        elif word not in words and len(words) < 200:
            words.append(word)
        await it.response.send_message(i18n.say(it.client, it.guild, "{count} banned words.", count=len(words)), ephemeral=True)

    @nickname.command(name="exempt", description="Roles that are never renamed")
    async def nick_exempt(self, it: discord.Interaction, role: discord.Role, remove: bool = False):
        """Roles that are never renamed."""
        if not await require(it):
            return
        lst = self.bot.cfg(it.guild_id)["nicknames"]["exempt_roles"]
        if remove and role.id in lst:
            lst.remove(role.id)
        elif not remove and role.id not in lst:
            lst.append(role.id)
        await it.response.send_message(i18n.say(it.client, it.guild, "Saved."), ephemeral=True)

    @nickname.command(name="list", description="Show the rules and the banned words")
    async def nick_list(self, it: discord.Interaction):
        """Show the rules and the banned words."""
        c = self.bot.cfg(it.guild_id)["nicknames"]
        await it.response.send_message(i18n.say(it.client, it.guild, "Dehoist: {dehoist}, global names: {usernames}, replacement: '{rename_to}'\nBanned words: {value}", dehoist=c['dehoist'], usernames=c['usernames'], rename_to=c['rename_to'], value=', '.join(c['words']) or 'none'), ephemeral=True)

    @nickname.command(name="check", description="Test a name without changing anything")
    async def nick_check(self, it: discord.Interaction, name: str):
        """Test a name without changing anything."""
        new, why = check_name(name, self.bot.cfg(it.guild_id)["nicknames"])
        await it.response.send_message("This name is fine." if new is None else f"This name {why}. It would become '{new}'.", ephemeral=True)

    @nickname.command(name="scan", description="Check all members now and rename those who break a rule")
    async def nick_scan(self, it: discord.Interaction):
        """Check all members now and rename those who break a rule."""
        if not await require(it):
            return
        await it.response.defer(ephemeral=True)
        changed, checked, started = 0, 0, time.monotonic()
        for member in list(it.guild.members):
            checked += 1
            if checked % 200 == 0:
                await asyncio.sleep(0)
            if time.monotonic() - started > SCAN_SECONDS:
                break
            if await self.fix_name(member):
                changed += 1
                await asyncio.sleep(0.5)
        if checked < len(it.guild.members):
            return await it.followup.send(i18n.say(it.client, it.guild, "{changed} names changed. Stopped after {checked} members because of the time limit. Run the scan again to continue with the rest.", changed=changed, checked=checked))
        await it.followup.send(i18n.say(it.client, it.guild, "{changed} names changed.", changed=changed))

    # watch list ------------------------------------------------------------

    async def alert(self, guild, member, item, what, message=None):
        """Tell the team that a watched member did something."""
        c = self.bot.cfg(guild.id)["watchlist"]
        e = emb("Watched member", f"{member.mention} {what}.", discord.Color.orange(), member)
        e.add_field(name="Reason for watching", value=trim(item["reason"], 500), inline=False)
        e.add_field(name="Added", value=f"<t:{item['ts']}:R> by <@{item['by']}>")
        if message is not None:
            e.add_field(name="Message", value=f"[Jump]({message.jump_url})\n{trim(message.content, 200)}" if message.content else f"[Jump]({message.jump_url})", inline=False)
        channel = guild.get_channel(c["channel"] or 0)
        ping = f"<@&{c['ping_role']}>" if c["ping_role"] else None
        if channel is not None:
            try:
                return await channel.send(ping, embed=e, allowed_mentions=discord.AllowedMentions(roles=[discord.Object(c["ping_role"])] if c["ping_role"] else []))
            except discord.HTTPException as exc:
                log.warning("watch list alert failed: %s", exc)
        self.bot.log(guild, "moderation", e)

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Tell the team when a watched member writes."""
        if msg.guild is None or msg.author.bot or not self.bot.module_on(msg.guild.id, "watchlist"):
            return
        c = self.bot.cfg(msg.guild.id)["watchlist"]
        item = c["items"].get(str(msg.author.id))
        if not item or (item.get("seen") and not c["repeat"]):
            return
        item["seen"] = int(time.time())
        await self.alert(msg.guild, msg.author, item, "wrote a message", msg)

    @watch.command(name="add", description="Put a member on the watch list")
    @app_commands.describe(user="Member or user ID", reason="Why this person is watched")
    async def watch_add(self, it: discord.Interaction, user: discord.User, reason: app_commands.Range[str, 3, 500]):
        """Put a member on the watch list."""
        c = self.bot.cfg(it.guild_id)["watchlist"]
        if len(c["items"]) >= 200:
            return await it.response.send_message(i18n.say(it.client, it.guild, "The watch list is full (200)."), ephemeral=True)
        c["items"][str(user.id)] = {"reason": reason, "by": it.user.id, "ts": int(time.time()), "seen": 0, "name": str(user)}
        self.bot.cfg(it.guild_id)["modules"]["watchlist"] = True
        await it.response.send_message(i18n.say(it.client, it.guild, "{user} is on the watch list. The person is not told. The team gets a message at the first message{value}.", user=user, value=' and at every one' if c['repeat'] else ''), ephemeral=True)

    @watch.command(name="remove", description="Take a member off the watch list")
    async def watch_remove(self, it: discord.Interaction, user: discord.User):
        """Take a member off the watch list."""
        items = self.bot.cfg(it.guild_id)["watchlist"]["items"]
        await it.response.send_message("Removed." if items.pop(str(user.id), None) else i18n.say(it.client, it.guild, "That user is not on the watch list."), ephemeral=True)

    @watch.command(name="list", description="Show the watch list")
    async def watch_list(self, it: discord.Interaction):
        """Show the watch list."""
        items = self.bot.cfg(it.guild_id)["watchlist"]["items"]
        lines = [f"<@{uid}> ({uid}) by <@{i['by']}> <t:{i['ts']}:R>{' (seen)' if i.get('seen') else ''}: {trim(i['reason'], 80)}" for uid, i in list(items.items())[:25]]
        await it.response.send_message("\n".join(lines) or "The watch list is empty.", ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @watch.command(name="setup", description="Where alerts go and whether every message counts")
    @app_commands.describe(channel="Channel for alerts, empty = moderation log", ping_role="Role to ping", repeat="Alert at every message, not only the first")
    async def watch_setup(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None, ping_role: Optional[discord.Role] = None, repeat: Optional[bool] = None):
        """Where alerts go and whether every message counts."""
        if not await require(it):
            return
        c = self.bot.cfg(it.guild_id)["watchlist"]
        if channel is not None:
            c["channel"] = channel.id
        if ping_role is not None:
            c["ping_role"] = ping_role.id
        if repeat is not None:
            c["repeat"] = repeat
        self.bot.cfg(it.guild_id)["modules"]["watchlist"] = True
        await it.response.send_message(i18n.say(it.client, it.guild, "Saved."), ephemeral=True)

    # reason templates ------------------------------------------------------

    @reason.command(name="add", description="Create or change a reason template")
    @app_commands.describe(name="Short name, for example spam", action="Punishment", text="Reason text that is stored in the case", duration="For mute, tempban and jail, for example 1h or 7d")
    async def reason_add(self, it: discord.Interaction, name: app_commands.Range[str, 1, 30], action: Literal["warn", "mute", "kick", "ban", "tempban", "jail"], text: app_commands.Range[str, 3, 500], duration: Optional[str] = None):
        """Create or change a reason template."""
        if not await require(it):
            return
        secs = parse_duration(duration) if duration else None
        if duration and not secs:
            return await it.response.send_message(i18n.say(it.client, it.guild, "I did not understand the duration. Use 30m, 2h or 1d."), ephemeral=True)
        if action == "tempban" and not secs:
            return await it.response.send_message(i18n.say(it.client, it.guild, "A temporary ban needs a duration."), ephemeral=True)
        items = self.bot.cfg(it.guild_id)["reasons"]["items"]
        if name.lower() not in items and len(items) >= 50:
            return await it.response.send_message(i18n.say(it.client, it.guild, "At most 50 templates."), ephemeral=True)
        items[name.lower()] = {"action": action, "seconds": secs, "text": text}
        await it.response.send_message(i18n.say(it.client, it.guild, "Template '{lower}' saved: {action}{value}.", lower=name.lower(), action=action, value=' for ' + fmt_duration(secs) if secs else ''), ephemeral=True)

    @reason.command(name="remove", description="Delete a reason template")
    async def reason_remove(self, it: discord.Interaction, name: str):
        """Delete a reason template."""
        if not await require(it):
            return
        items = self.bot.cfg(it.guild_id)["reasons"]["items"]
        await it.response.send_message("Deleted." if items.pop(name.lower(), None) else i18n.say(it.client, it.guild, "There is no template with that name."), ephemeral=True)

    @reason.command(name="list", description="Show all reason templates")
    async def reason_list(self, it: discord.Interaction):
        """Show all reason templates."""
        items = self.bot.cfg(it.guild_id)["reasons"]["items"]
        lines = [f"**{n}**: {i['action']}{' ' + fmt_duration(i['seconds']) if i.get('seconds') else ''}, {trim(i['text'], 80)}" for n, i in items.items()]
        await it.response.send_message("\n".join(lines) or "No templates yet. Create one with /members reason add.", ephemeral=True)

    @reason.command(name="use", description="Punish a user with a template")
    @app_commands.describe(user="Member or user ID", name="Template name")
    async def reason_use(self, it: discord.Interaction, user: discord.User, name: str):
        """Punish a user with a template, so that everyone on the team handles the same case the same way."""
        item = self.bot.cfg(it.guild_id)["reasons"]["items"].get(name.lower())
        if not item:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no template with that name."), ephemeral=True)
        need = ACTION_PERMISSION[item["action"]]
        if not getattr(it.user.guild_permissions, need):
            return await it.response.send_message(i18n.say(it.client, it.guild, "You need the {title} permission for this.", title=need.replace('_', ' ').title()), ephemeral=True)
        mod = self.bot.get_cog("Moderation")
        target = it.guild.get_member(user.id) or user
        err = mod.target_error(it.guild, it.user, target)
        if err:
            return await it.response.send_message(err, ephemeral=True)
        await it.response.defer(ephemeral=True)
        ctx = Via(it)
        if item["action"] in ("ban", "tempban", "kick") and await mod.gated(ctx, item["action"], target, item["text"], item.get("seconds")):
            return
        ok, text, _ = await mod.punish(it.guild, it.user, target, item["action"], item["text"], item.get("seconds"), {"template": name.lower()})
        await it.followup.send(text, ephemeral=not ok)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Members(bot))
