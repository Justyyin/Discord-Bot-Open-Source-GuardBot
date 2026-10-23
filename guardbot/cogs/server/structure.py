"""Server structure: channels and categories by command, archiving of idle channels, timed roles and role templates."""

import asyncio
import logging
import time
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ... import i18n
from ...utils import emb, fmt_duration, parse_duration, require, trim

log = logging.getLogger(__name__)

MAX_MOVES = 10
MAX_SORT = 50
KINDS = ("text", "voice", "forum", "stage")


def last_activity(channel, now=None):
    """Unix time of the last message of a channel, or of its creation when it has none."""
    ident = getattr(channel, "last_message_id", None)
    return discord.utils.snowflake_time(ident or channel.id).timestamp()


def is_idle(channel, days, now=None):
    """True if nothing was written in a channel for this many days."""
    return (now if now is not None else time.time()) - last_activity(channel) > days * 86400


def masked_permissions(value, holder_value, holder_is_admin):
    """The permissions a template may give: only those the person who applies it has too, unless that person is an administrator."""
    return value if holder_is_admin else value & holder_value


def sort_key(channel):
    """Sort channels and categories by name, ignoring case and leading symbols."""
    name = channel.name.casefold().lstrip("-_ ")
    return (name, channel.id)


def role_template(role):
    """The part of a role that a template remembers."""
    return {"permissions": role.permissions.value, "color": role.colour.value, "hoist": role.hoist, "mentionable": role.mentionable}


class Structure(commands.Cog):
    """Channels, categories, archive, timed roles and role templates."""

    channel = app_commands.Group(name="channel", description="Create, copy, rename and sort channels", guild_only=True)
    category = app_commands.Group(name="category", description="Create, copy and sort categories", guild_only=True)
    archive = app_commands.Group(name="archive", description="Find and archive channels nobody uses", guild_only=True)
    temprole = app_commands.Group(name="temprole", description="Roles that end by themselves", guild_only=True)
    roletemplate = app_commands.Group(name="roletemplate", description="Save a role as a template and create roles from it", guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    async def cog_load(self):
        """Start the loops."""
        self.role_loop.start()
        self.archive_loop.start()

    async def cog_unload(self):
        """Stop the loops."""
        self.role_loop.cancel()
        self.archive_loop.cancel()

    # channels --------------------------------------------------------------

    def private_overwrites(self, guild):
        """Overwrites that hide a new channel from everyone except the staff role and the bot."""
        over = {guild.default_role: discord.PermissionOverwrite(view_channel=False), guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)}
        staff = guild.get_role(self.bot.cfg(guild.id)["jail"]["staff_role"] or 0)
        if staff:
            over[staff] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
        return over

    @channel.command(name="create", description="Create a channel")
    @app_commands.describe(name="Name", kind="Type", category="Category", private="Visible only for the staff role", topic="Topic of a text channel")
    async def channel_create(self, it: discord.Interaction, name: app_commands.Range[str, 1, 100], kind: Literal["text", "voice", "forum", "stage"] = "text", category: Optional[discord.CategoryChannel] = None, private: bool = False, topic: Optional[app_commands.Range[str, 1, 1024]] = None):
        """Create a channel."""
        guild = it.guild
        extra = {"overwrites": self.private_overwrites(guild)} if private else {}
        try:
            if kind == "text":
                ch = await guild.create_text_channel(name, category=category, topic=topic, reason=f"{it.user}", **extra)
            elif kind == "voice":
                ch = await guild.create_voice_channel(name, category=category, reason=f"{it.user}", **extra)
            elif kind == "forum":
                ch = await guild.create_forum(name, category=category, topic=topic, reason=f"{it.user}", **extra)
            else:
                ch = await guild.create_stage_channel(name, category=category, reason=f"{it.user}", **extra)
        except discord.HTTPException as exc:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Discord refused: {exc}", exc=exc), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Created {mention}.", mention=ch.mention), ephemeral=True)

    @channel.command(name="clone", description="Copy a channel with its permissions")
    async def channel_clone(self, it: discord.Interaction, channel: discord.abc.GuildChannel, name: Optional[app_commands.Range[str, 1, 100]] = None):
        """Copy a channel with its permissions. Messages are not copied."""
        if isinstance(channel, discord.CategoryChannel):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Use /structure category clone for categories."), ephemeral=True)
        try:
            new = await channel.clone(name=name, reason=f"{it.user}")
        except discord.HTTPException as exc:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Discord refused: {exc}", exc=exc), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Created {mention} as a copy of {mention2}.", mention=new.mention, mention2=channel.mention), ephemeral=True)

    @channel.command(name="rename", description="Rename a channel")
    async def channel_rename(self, it: discord.Interaction, channel: discord.abc.GuildChannel, name: app_commands.Range[str, 1, 100]):
        """Rename a channel."""
        old = channel.name
        try:
            await channel.edit(name=name, reason=f"{it.user}")
        except discord.HTTPException as exc:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Discord refused: {exc}", exc=exc), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Renamed '{old}' to '{name}'.", old=old, name=name), ephemeral=True)

    @channel.command(name="move", description="Move a channel to another category or position")
    @app_commands.describe(category="Target category", position="Position, 0 = top")
    async def channel_move(self, it: discord.Interaction, channel: discord.abc.GuildChannel, category: Optional[discord.CategoryChannel] = None, position: Optional[app_commands.Range[int, 0, 500]] = None):
        """Move a channel to another category or position."""
        if isinstance(channel, discord.CategoryChannel):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Categories are sorted with /structure category sort."), ephemeral=True)
        try:
            await channel.edit(category=category or channel.category, position=position if position is not None else discord.utils.MISSING, reason=f"{it.user}")
        except discord.HTTPException as exc:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Discord refused: {exc}", exc=exc), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Moved."), ephemeral=True)

    @channel.command(name="sort", description="Sort the channels of a category by name")
    async def channel_sort(self, it: discord.Interaction, category: Optional[discord.CategoryChannel] = None):
        """Sort the channels of a category by name, text channels before voice channels."""
        guild = it.guild
        pool = list(category.channels) if category else [c for c in guild.channels if c.category is None and not isinstance(c, discord.CategoryChannel)]
        if len(pool) > MAX_SORT:
            return await it.response.send_message(i18n.say(it.client, it.guild, "That are {count} channels, at most {MAX_SORT} are sorted at once.", count=len(pool), MAX_SORT=MAX_SORT), ephemeral=True)
        await it.response.defer(ephemeral=True)
        text = sorted([c for c in pool if not isinstance(c, (discord.VoiceChannel, discord.StageChannel))], key=sort_key)
        voice = sorted([c for c in pool if isinstance(c, (discord.VoiceChannel, discord.StageChannel))], key=sort_key)
        for index, ch in enumerate(text + voice):
            if ch.position != index:
                try:
                    await ch.edit(position=index, reason="Sorted by name")
                except discord.HTTPException as exc:
                    return await it.followup.send(i18n.say(it.client, it.guild, "Stopped at {name}: {exc}", name=ch.name, exc=exc))
                await asyncio.sleep(0.4)
        await it.followup.send(i18n.say(it.client, it.guild, "Sorted {count} channels.", count=len(pool)))

    @channel.command(name="copyperms", description="Copy the permissions of one channel to others")
    @app_commands.describe(source="Channel whose permissions are copied", target="Channel that receives them", whole_category="Apply to every channel of the target category instead")
    async def channel_copyperms(self, it: discord.Interaction, source: discord.abc.GuildChannel, target: discord.abc.GuildChannel, whole_category: bool = False):
        """Replace the permission overwrites of the target with those of the source."""
        targets = [target]
        if whole_category:
            cat = target if isinstance(target, discord.CategoryChannel) else target.category
            if cat is None:
                return await it.response.send_message(i18n.say(it.client, it.guild, "That channel has no category."), ephemeral=True)
            targets = list(cat.channels)
        targets = [t for t in targets if t.id != source.id]
        if len(targets) > MAX_SORT:
            return await it.response.send_message(i18n.say(it.client, it.guild, "At most {MAX_SORT} channels at once.", MAX_SORT=MAX_SORT), ephemeral=True)
        await it.response.defer(ephemeral=True)
        done = 0
        for t in targets:
            try:
                await t.edit(overwrites=dict(source.overwrites), reason=f"Permissions copied from {source.name} by {it.user}")
                done += 1
            except discord.HTTPException as exc:
                log.warning("copy of permissions to %s failed: %s", t.id, exc)
            await asyncio.sleep(0.4)
        await it.followup.send(i18n.say(it.client, it.guild, "Permissions of {name} copied to {done} of {count} channels.", name=source.name, done=done, count=len(targets)))

    # categories ------------------------------------------------------------

    @category.command(name="create", description="Create a category")
    async def category_create(self, it: discord.Interaction, name: app_commands.Range[str, 1, 100], private: bool = False):
        """Create a category."""
        extra = {"overwrites": self.private_overwrites(it.guild)} if private else {}
        try:
            cat = await it.guild.create_category(name, reason=f"{it.user}", **extra)
        except discord.HTTPException as exc:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Discord refused: {exc}", exc=exc), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Created the category {name}.", name=cat.name), ephemeral=True)

    @category.command(name="clone", description="Copy a category with all its channels and permissions")
    async def category_clone(self, it: discord.Interaction, category: discord.CategoryChannel, name: Optional[app_commands.Range[str, 1, 100]] = None):
        """Copy a category with all its channels and permissions."""
        if len(category.channels) > 40:
            return await it.response.send_message(i18n.say(it.client, it.guild, "That category has more than 40 channels."), ephemeral=True)
        await it.response.defer(ephemeral=True)
        try:
            new = await category.clone(name=name or f"{category.name} copy", reason=f"{it.user}")
            for ch in category.channels:
                copy = await ch.clone(reason=f"{it.user}")
                await copy.edit(category=new, sync_permissions=False)
                await asyncio.sleep(0.4)
        except discord.HTTPException as exc:
            return await it.followup.send(i18n.say(it.client, it.guild, "Discord refused: {exc}", exc=exc))
        await it.followup.send(i18n.say(it.client, it.guild, "Created {name} with {count} channels.", name=new.name, count=len(category.channels)))

    @category.command(name="rename", description="Rename a category")
    async def category_rename(self, it: discord.Interaction, category: discord.CategoryChannel, name: app_commands.Range[str, 1, 100]):
        """Rename a category."""
        try:
            await category.edit(name=name, reason=f"{it.user}")
        except discord.HTTPException as exc:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Discord refused: {exc}", exc=exc), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Renamed."), ephemeral=True)

    @category.command(name="sort", description="Sort all categories by name")
    async def category_sort(self, it: discord.Interaction):
        """Sort all categories by name."""
        cats = sorted(it.guild.categories, key=sort_key)
        if len(cats) > MAX_SORT:
            return await it.response.send_message(i18n.say(it.client, it.guild, "At most {MAX_SORT} categories are sorted at once.", MAX_SORT=MAX_SORT), ephemeral=True)
        await it.response.defer(ephemeral=True)
        for index, cat in enumerate(cats):
            if cat.position != index:
                try:
                    await cat.edit(position=index, reason="Sorted by name")
                except discord.HTTPException as exc:
                    return await it.followup.send(i18n.say(it.client, it.guild, "Stopped at {name}: {exc}", name=cat.name, exc=exc))
                await asyncio.sleep(0.4)
        await it.followup.send(i18n.say(it.client, it.guild, "Sorted {count} categories.", count=len(cats)))

    @category.command(name="sync", description="Give every channel of a category the permissions of the category")
    async def category_sync(self, it: discord.Interaction, category: discord.CategoryChannel):
        """Give every channel of a category the permissions of the category."""
        await it.response.defer(ephemeral=True)
        done = 0
        for ch in category.channels[:MAX_SORT]:
            try:
                await ch.edit(sync_permissions=True, reason=f"Synced with the category by {it.user}")
                done += 1
            except discord.HTTPException as exc:
                log.warning("sync of %s failed: %s", ch.id, exc)
            await asyncio.sleep(0.4)
        await it.followup.send(i18n.say(it.client, it.guild, "{done} channels now follow the category.", done=done))

    # archive ---------------------------------------------------------------

    def idle_channels(self, guild):
        """Text channels without a message for the configured time."""
        c = self.bot.cfg(guild.id)["archive"]
        skip = set(c["ignore_channels"]) | {x for x in (c["report_channel"],) if x}
        skip |= {v for k, v in self.bot.cfg(guild.id)["log"].items() if v}
        out = []
        for ch in guild.text_channels:
            if ch.id in skip or (ch.category_id and (ch.category_id in c["ignore_categories"] or ch.category_id == c["category"])):
                continue
            if ch.id in (guild.rules_channel.id if guild.rules_channel else 0, guild.system_channel.id if guild.system_channel else 0):
                continue
            if is_idle(ch, c["days"]):
                out.append(ch)
        return sorted(out, key=last_activity)

    async def run_archive(self, guild, action=None):
        """Apply the archive action to idle channels. Returns a short text."""
        c = self.bot.cfg(guild.id)["archive"]
        action = action or c["action"]
        idle = self.idle_channels(guild)
        c["last_scan"] = int(time.time())
        if not idle:
            return "No idle channels."
        target = guild.get_channel(c["category"] or 0)
        moved = []
        if action in ("move", "lock"):
            for ch in idle[:MAX_MOVES]:
                try:
                    if action == "move" and isinstance(target, discord.CategoryChannel):
                        await ch.edit(category=target, sync_permissions=True, reason="Archived: no messages")
                    else:
                        await ch.set_permissions(guild.default_role, send_messages=False, add_reactions=False, create_public_threads=False, reason="Archived: no messages")
                    moved.append(ch)
                except discord.HTTPException as exc:
                    log.warning("archive of %s failed: %s", ch.id, exc)
                await asyncio.sleep(0.5)
        lines = [f"{ch.mention} last message <t:{int(last_activity(ch))}:R>" for ch in idle[:25]]
        verb = {"report": "found", "move": "archived" if target else "found (no archive category set)", "lock": "locked"}[action]
        e = emb(f"Idle channels {verb}", "\n".join(lines) + (f"\nand {len(idle) - 25} more" if len(idle) > 25 else ""), discord.Color.light_grey())
        e.set_footer(text=f"No message for {c['days']} days. {len(moved)} changed.")
        channel = guild.get_channel(c["report_channel"] or 0)
        if channel is not None:
            try:
                await channel.send(embed=e)
            except discord.HTTPException as exc:
                log.warning("archive report failed: %s", exc)
        else:
            self.bot.log(guild, "server", e)
        for ch in idle:
            c["reported"][str(ch.id)] = int(time.time())
        return f"{len(idle)} idle channels {verb}, {len(moved)} changed."

    @tasks.loop(minutes=30)
    async def archive_loop(self):
        """Scan for idle channels at the set interval."""
        now = time.time()
        for guild in list(self.bot.guilds):
            c = self.bot.cfg(guild.id)["archive"]
            if not self.bot.module_on(guild.id, "archive") or now - c["last_scan"] < c["interval_hours"] * 3600:
                continue
            try:
                await self.run_archive(guild)
            except Exception:  # one server must not stop the others
                log.exception("archive scan of %s failed", guild.id)
                c["last_scan"] = int(now)

    @archive_loop.before_loop
    async def _wait_archive(self):
        """Wait until the bot is connected."""
        await self.bot.wait_until_ready()

    @archive.command(name="setup", description="Choose when and how idle channels are handled")
    @app_commands.describe(days="Idle after this many days without a message", action="report = only tell the team, move = into the archive category, lock = nobody can write", category="Archive category for move", report_channel="Channel for reports", interval_hours="How often to look")
    async def archive_setup(
        self, it: discord.Interaction, days: Optional[app_commands.Range[int, 7, 3650]] = None, action: Optional[Literal["report", "move", "lock"]] = None, category: Optional[discord.CategoryChannel] = None,
        report_channel: Optional[discord.TextChannel] = None, interval_hours: Optional[app_commands.Range[int, 1, 720]] = None,
    ):
        """Choose when and how idle channels are handled."""
        if not await require(it):
            return
        c = self.bot.cfg(it.guild_id)["archive"]
        for key, value in (("days", days), ("action", action), ("interval_hours", interval_hours)):
            if value is not None:
                c[key] = value
        if category is not None:
            c["category"] = category.id
        if report_channel is not None:
            c["report_channel"] = report_channel.id
        self.bot.cfg(it.guild_id)["modules"]["archive"] = True
        await it.response.send_message(i18n.say(it.client, it.guild, "Archive is on: after {days} days without a message the action is '{action}'. Every {interval_hours} hours. Start with 'report' and look at the result before you use move or lock.", days=c['days'], action=c['action'], interval_hours=c['interval_hours']), ephemeral=True)

    @archive.command(name="ignore", description="Never touch a channel or category")
    async def archive_ignore(self, it: discord.Interaction, channel: discord.abc.GuildChannel, remove: bool = False):
        """Never touch a channel or category."""
        if not await require(it):
            return
        c = self.bot.cfg(it.guild_id)["archive"]
        lst = c["ignore_categories"] if isinstance(channel, discord.CategoryChannel) else c["ignore_channels"]
        if remove and channel.id in lst:
            lst.remove(channel.id)
        elif not remove and channel.id not in lst:
            lst.append(channel.id)
        await it.response.send_message(i18n.say(it.client, it.guild, "Saved."), ephemeral=True)

    @archive.command(name="scan", description="Look for idle channels now")
    @app_commands.describe(action="Override the set action once")
    async def archive_scan(self, it: discord.Interaction, action: Optional[Literal["report", "move", "lock"]] = None):
        """Look for idle channels now."""
        if not await require(it):
            return
        await it.response.defer(ephemeral=True)
        await it.followup.send(await self.run_archive(it.guild, action))

    @archive.command(name="status", description="Show the settings")
    async def archive_status(self, it: discord.Interaction):
        """Show the settings and the idle channels."""
        c = self.bot.cfg(it.guild_id)["archive"]
        idle = self.idle_channels(it.guild)
        await it.response.send_message(
            f"Module: {'on' if self.bot.module_on(it.guild_id, 'archive') else 'off'}. Idle after {c['days']} days, action {c['action']}, every {c['interval_hours']} hours, last scan {'<t:' + str(c['last_scan']) + ':R>' if c['last_scan'] else 'never'}.\n"
            f"Idle now: {len(idle)} " + " ".join(ch.mention for ch in idle[:15]), ephemeral=True)

    # timed roles -----------------------------------------------------------

    def may_manage(self, it, role):
        """Why the person may not hand out a role, or None."""
        if role.is_default() or role.managed or not role.is_assignable():
            return "I cannot give that role. Move my role above it or choose another one."
        if it.user.id != it.guild.owner_id and role >= it.user.top_role:
            return "That role is equal to or higher than your highest role."
        return None

    @temprole.command(name="give", description="Give a role for a limited time")
    @app_commands.describe(member="Member", role="Role", duration="For example 7d, 12h, 2w", reason="Reason")
    async def temprole_give(self, it: discord.Interaction, member: discord.Member, role: discord.Role, duration: str, reason: Optional[str] = None):
        """Give a role for a limited time."""
        secs = parse_duration(duration)
        if not secs:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Invalid duration. Examples: 12h, 7d, 2w"), ephemeral=True)
        problem = self.may_manage(it, role)
        if problem:
            return await it.response.send_message(problem, ephemeral=True)
        if role in member.roles and str(member.id) + ":" + str(role.id) not in self.bot.cfg(it.guild_id)["temproles"]["items"]:
            return await it.response.send_message(i18n.say(it.client, it.guild, "That member already has the role without a time limit."), ephemeral=True)
        try:
            await member.add_roles(role, reason=f"Timed role by {it.user}: {reason or 'no reason'}")
        except discord.HTTPException as exc:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Discord refused: {exc}", exc=exc), ephemeral=True)
        until = int(time.time()) + secs
        self.bot.cfg(it.guild_id)["temproles"]["items"][f"{member.id}:{role.id}"] = until
        e = emb("Timed role given", f"{member.mention} got {role.mention} for {fmt_duration(secs)}, until <t:{until}:f>.", discord.Color.blurple(), it.user)
        self.bot.log(it.guild, "server", e)
        await it.response.send_message(i18n.say(it.client, it.guild, "{mention} has {mention2} until <t:{until}:f>.", mention=member.mention, mention2=role.mention, until=until), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @temprole.command(name="remove", description="End a timed role now")
    async def temprole_remove(self, it: discord.Interaction, member: discord.Member, role: discord.Role):
        """End a timed role now."""
        items = self.bot.cfg(it.guild_id)["temproles"]["items"]
        if items.pop(f"{member.id}:{role.id}", None) is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "That is not a timed role."), ephemeral=True)
        try:
            await member.remove_roles(role, reason=f"Timed role ended by {it.user}")
        except discord.HTTPException as exc:
            log.warning("timed role removal failed: %s", exc)
        await it.response.send_message(i18n.say(it.client, it.guild, "Ended."), ephemeral=True)

    @temprole.command(name="list", description="Show all timed roles")
    async def temprole_list(self, it: discord.Interaction):
        """Show all timed roles."""
        items = self.bot.cfg(it.guild_id)["temproles"]["items"]
        lines = [f"<@{k.split(':')[0]}> has <@&{k.split(':')[1]}> until <t:{v}:R>" for k, v in sorted(items.items(), key=lambda kv: kv[1])[:30]]
        await it.response.send_message("\n".join(lines) or "No timed roles.", ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @tasks.loop(seconds=30)
    async def role_loop(self):
        """Take timed roles away when their time is over."""
        now = time.time()
        for guild in list(self.bot.guilds):
            if not self.bot.module_on(guild.id, "temproles"):
                continue
            items = self.bot.cfg(guild.id)["temproles"]["items"]
            for key, until in list(items.items()):
                if until > now:
                    continue
                try:
                    uid, rid = (int(x) for x in key.split(":"))
                    member, role = guild.get_member(uid), guild.get_role(rid)
                    if member is not None and role is not None and role in member.roles:
                        await member.remove_roles(role, reason="Timed role ended")
                except discord.HTTPException as exc:
                    log.warning("timed role %s could not be removed: %s", key, exc)
                    continue
                except ValueError:
                    log.warning("damaged timed role entry %s was dropped", key)
                items.pop(key, None)

    @role_loop.before_loop
    async def _wait_roles(self):
        """Wait until the bot is connected."""
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Forget timed roles of a member who left."""
        items = self.bot.cfg(member.guild.id)["temproles"]["items"]
        for key in [k for k in items if k.startswith(f"{member.id}:")]:
            items.pop(key, None)

    # role templates --------------------------------------------------------

    @roletemplate.command(name="save", description="Save the settings of a role as a template")
    async def template_save(self, it: discord.Interaction, name: app_commands.Range[str, 1, 30], role: discord.Role):
        """Save the permissions, colour and options of a role as a template."""
        items = self.bot.cfg(it.guild_id)["roletemplates"]["items"]
        if name.lower() not in items and len(items) >= 30:
            return await it.response.send_message(i18n.say(it.client, it.guild, "At most 30 templates."), ephemeral=True)
        items[name.lower()] = role_template(role)
        await it.response.send_message(i18n.say(it.client, it.guild, "Template '{lower}' saved from {mention}.", lower=name.lower(), mention=role.mention), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @roletemplate.command(name="apply", description="Create a new role from a template")
    @app_commands.describe(name="Template name", role_name="Name of the new role")
    async def template_apply(self, it: discord.Interaction, name: str, role_name: app_commands.Range[str, 1, 100]):
        """Create a new role from a template. You can only give permissions that you have yourself."""
        t = self.bot.cfg(it.guild_id)["roletemplates"]["items"].get(name.lower())
        if not t:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no template with that name."), ephemeral=True)
        perms = masked_permissions(t["permissions"], it.user.guild_permissions.value, it.user.guild_permissions.administrator or it.user.id == it.guild.owner_id)
        try:
            role = await it.guild.create_role(name=role_name, permissions=discord.Permissions(perms), colour=discord.Colour(t["color"]), hoist=t["hoist"], mentionable=t["mentionable"], reason=f"Template {name} by {it.user}")
        except discord.HTTPException as exc:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Discord refused: {exc}", exc=exc), ephemeral=True)
        cut = " Some permissions were left out because you do not have them yourself." if perms != t["permissions"] else ""
        await it.response.send_message(i18n.say(it.client, it.guild, "Created {mention}.{cut}", mention=role.mention, cut=cut), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @roletemplate.command(name="list", description="Show all templates")
    async def template_list(self, it: discord.Interaction):
        """Show all templates."""
        items = self.bot.cfg(it.guild_id)["roletemplates"]["items"]
        lines = [f"**{n}**: {bin(t['permissions']).count('1')} permissions, colour #{t['color']:06x}" for n, t in items.items()]
        await it.response.send_message(trim("\n".join(lines), 1900) or "No templates yet.", ephemeral=True)

    @roletemplate.command(name="delete", description="Delete a template")
    async def template_delete(self, it: discord.Interaction, name: str):
        """Delete a template."""
        items = self.bot.cfg(it.guild_id)["roletemplates"]["items"]
        await it.response.send_message("Deleted." if items.pop(name.lower(), None) else i18n.say(it.client, it.guild, "There is no template with that name."), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Structure(bot))
