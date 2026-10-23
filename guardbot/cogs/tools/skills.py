"""Skills: commands, games and automations that a server builds from a fixed set of safe building blocks."""

import json
import logging
import random
import time
from typing import Any, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ... import i18n, skills as engine
from ...cog import BaseCog
from ...utils import emb, require

log = logging.getLogger(__name__)

RPS = ("rock", "paper", "scissors")
TEXTS = (
    "That name is already used by a bot command.",
    "That name is already used by an alias or a tag.",
    "A skill with that name exists already. Use /support skill edit.",
)


class Runner:
    """Does the Discord work of a skill for one person in one channel."""

    def __init__(self, cog: "Skills", guild: discord.Guild, member: discord.Member, channel: Any, respond: Any = None):
        """`respond(text, ephemeral, embed)` answers the person; without it the channel gets the message."""
        self.cog, self.guild, self.member, self.channel, self.respond = cog, guild, member, channel, respond

    def embed(self, text: str, title: Optional[str], color: Optional[str]) -> Optional[discord.Embed]:
        """An embed if a title or colour was asked for."""
        if not title and not color:
            return None
        e = discord.Embed(title=title, description=text, color=int(color[1:], 16) if color else discord.Color.blurple())
        return e

    async def reply(self, text: str, ephemeral: bool, title: Optional[str], color: Optional[str]) -> bool:
        """Answer the person who used the skill."""
        e = self.embed(text, title, color)
        try:
            if self.respond:
                await self.respond(None if e else text, ephemeral, e)
            else:
                await self.channel.send(None if e else text, embed=e, allowed_mentions=discord.AllowedMentions(users=[self.member]))
            return True
        except discord.HTTPException as exc:
            log.warning("skill reply failed in %s: %s", self.guild.id, exc)
            return False

    async def send(self, channel_id: int, text: str, title: Optional[str], color: Optional[str]) -> bool:
        """Post in another channel of the server."""
        ch = self.guild.get_channel(channel_id)
        if ch is None or not hasattr(ch, "send") or not ch.permissions_for(self.guild.me).send_messages:
            return False
        e = self.embed(text, title, color)
        try:
            await ch.send(None if e else text, embed=e, allowed_mentions=discord.AllowedMentions.none())
            return True
        except discord.HTTPException:
            return False

    async def dm(self, text: str) -> bool:
        """Send a private message to the person."""
        try:
            await self.member.send(text, allowed_mentions=discord.AllowedMentions.none())
            return True
        except discord.HTTPException:
            return False

    async def log(self, text: str) -> bool:
        """Write a line to the server log."""
        self.cog.bot.log(self.guild, "main", emb("Skill", text, user=self.member))
        return True

    def role(self, role_id: int) -> Optional[discord.Role]:
        """A role the bot is allowed to hand out: it must exist, be below the bot and not be dangerous."""
        role = self.guild.get_role(role_id)
        if role is None or role.managed or role >= self.guild.me.top_role or role.is_default():
            return None
        if any(getattr(role.permissions, p, False) for p in ("administrator", "manage_guild", "manage_roles", "manage_channels", "ban_members", "kick_members", "manage_webhooks")):
            return None
        return role

    async def add_role(self, role_id: int) -> bool:
        """Give the person a role."""
        role = self.role(role_id)
        if role is None:
            return False
        try:
            await self.member.add_roles(role, reason="Skill")
            return True
        except discord.HTTPException:
            return False

    async def remove_role(self, role_id: int) -> bool:
        """Take a role from the person."""
        role = self.role(role_id)
        if role is None:
            return False
        try:
            await self.member.remove_roles(role, reason="Skill")
            return True
        except discord.HTTPException:
            return False

    async def coins(self, amount: int) -> bool:
        """Give coins, only while the economy module is on."""
        eco = self.cog.bot.get_cog("Economy")
        if eco is None or not self.cog.bot.module_on(self.guild.id, "economy"):
            return False
        eco.add(self.guild.id, self.member.id, amount)
        return True


def context_for(guild: discord.Guild, member: discord.Member, channel: Any, args: list[str]) -> dict:
    """The words a skill text can use."""
    ctx: dict[str, Any] = {
        "user": member.mention, "user_name": member.display_name, "user_id": member.id, "server": guild.name,
        "channel": getattr(channel, "mention", ""), "count": guild.member_count,
        "role_ids": {r.id for r in getattr(member, "roles", [])},
    }
    for i, a in enumerate(args[:2], 1):
        ctx[f"arg{i}"] = discord.utils.escape_mentions(a)[:200]
    return ctx


class Answer(discord.ui.View):
    """The buttons of a quiz question. Only the person who started it can answer."""

    def __init__(self, cog: "Skills", runner: Runner, spec: dict, ctx: dict, question: dict):
        """Create one button per answer."""
        super().__init__(timeout=spec.get("seconds", 30))
        self.cog, self.runner, self.spec, self.ctx, self.question = cog, runner, spec, ctx, question
        self.done = False
        for i, text in enumerate(question["options"]):
            btn = discord.ui.Button(label=text[:80], style=discord.ButtonStyle.secondary)
            btn.callback = self.make(i)
            self.add_item(btn)

    def make(self, index: int) -> Any:
        """The callback of the button with this index."""
        async def callback(it: discord.Interaction) -> None:
            if it.user.id != self.runner.member.id:
                return await it.response.send_message("This question is not for you.", ephemeral=True)
            self.done = True
            self.stop()
            right = index == self.question["answer"]
            ctx = dict(self.ctx, answer=self.question["options"][index])
            text = engine.render(self.spec.get("correct_text" if right else "wrong_text", "Right!" if right else "Wrong."), ctx)
            await it.response.edit_message(content=text, view=None)
            await self.cog.finish(self.runner, self.spec["name"], self.spec.get("on_win" if right else "on_lose", []), ctx)
        return callback

    async def on_timeout(self) -> None:
        """Nothing to do: unanswered questions just end."""
        self.stop()


class SkillButton(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:sk:(?P<name>[a-z0-9_-]+)"):
    """A persistent button that runs a skill for whoever clicks it."""

    def __init__(self, name: str, label: str = "Run", style: str = "primary"):
        """Create the button for a skill."""
        super().__init__(discord.ui.Button(label=label[:80], style=getattr(discord.ButtonStyle, style, discord.ButtonStyle.primary), custom_id=f"gb:sk:{name}"))
        self.name = name

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button after a restart."""
        return cls(match["name"], item.label or "Run")

    async def callback(self, interaction: discord.Interaction) -> None:
        """Run the skill for the person who clicked."""
        cog = interaction.client.get_cog("Skills")
        if cog is not None:
            await cog.run_interaction(interaction, self.name, [], via_button=True)


class SkillModal(discord.ui.Modal):
    """Paste or edit a skill as JSON."""

    def __init__(self, cog: "Skills", title: str, text: str = ""):
        """Create the text box."""
        super().__init__(title=title[:45])
        self.cog = cog
        self.box = discord.ui.TextInput(label="Skill (JSON)", style=discord.TextStyle.paragraph, default=text[:4000], max_length=4000)
        self.add_item(self.box)

    async def on_submit(self, it: discord.Interaction) -> None:
        """Validate and save."""
        await it.response.send_message(await self.cog.save_text(it, self.box.value), ephemeral=True)


class Skills(BaseCog):
    """Custom commands, games and automations without code."""

    section = "skills"
    gate = {"on_message": "skills", "on_member_join": "skills", "on_member_remove": "skills"}

    skill = app_commands.Group(name="skill", description="Custom commands, games and automations", guild_only=True)

    def __init__(self, bot: Any):
        """Keep the bot and the cooldown table."""
        super().__init__(bot)
        self.cd: dict[tuple, float] = {}
        bot.add_dynamic_items(SkillButton)

    # ---- storage

    def items(self, gid: int) -> dict:
        """The skills of a server."""
        return self.conf(gid)["items"]

    def vars(self, gid: int) -> engine.Vars:
        """The counters of a server."""
        return engine.Vars(self.conf(gid)["vars"])

    def name_error(self, guild_id: int, name: str) -> Optional[str]:
        """Why a skill name cannot be used, or None."""
        if self.bot.get_command(name) or self.bot.tree.get_command(name):
            return "That name is already used by a bot command."
        if name in self.bot.cfg(guild_id)["aliases"] or name in self.bot.cfg(guild_id)["tags"]["items"]:
            return "That name is already used by an alias or a tag."
        return None

    def check_references(self, guild: discord.Guild, spec: dict) -> Optional[str]:
        """Roles and channels of a skill must exist on this server and roles must be safe to hand out."""
        refs = engine.references(spec)
        probe = Runner(self, guild, guild.me, None)
        for rid in refs["roles"]:
            if guild.get_role(rid) is None:
                return f"The role {rid} does not exist on this server."
        for action in engine.all_actions(spec):
            if action["do"] in ("add_role", "remove_role") and probe.role(action["role"]) is None:
                return f"The role {action['role']} cannot be handed out by the bot (too high, managed or has dangerous permissions)."
        for cid in refs["channels"]:
            if guild.get_channel(cid) is None:
                return f"The channel {cid} does not exist on this server."
        return None

    def store(self, guild: discord.Guild, spec: dict, author: int, replace: bool = False) -> Optional[str]:
        """Save a validated skill. Returns an error text or None."""
        items = self.items(guild.id)
        name = spec["name"]
        if name in items and not replace:
            return "A skill with that name exists already. Use /support skill edit."
        if name not in items:
            if len(items) >= engine.MAX_SKILLS:
                return f"A server can have {engine.MAX_SKILLS} skills at most."
            err = self.name_error(guild.id, name)
            if err:
                return err
        err = self.check_references(guild, spec)
        if err:
            return err
        items[name] = spec
        meta = self.conf(guild.id)["meta"].setdefault(name, {"author": author, "created": int(time.time()), "uses": 0})
        meta["author"] = meta.get("author", author)
        return None

    async def save_text(self, it: discord.Interaction, text: str) -> str:
        """Parse, validate and save a skill that was typed or pasted. Returns the message for the person."""
        if not it.user.guild_permissions.manage_guild:
            return i18n.say(it.client, it.guild, "You need the Manage Server permission for this.")
        try:
            spec = engine.clean(engine.parse_json(text))
        except engine.SpecError as exc:
            return i18n.say(it.client, it.guild, "The skill is not valid: {error}", error=str(exc))
        replace = spec["name"] in self.items(it.guild_id)
        err = self.store(it.guild, spec, it.user.id, replace=True)
        if err:
            return i18n.say(it.client, it.guild, err)
        return i18n.say(it.client, it.guild, "Skill `{name}` saved ({what}).", name=spec["name"], what=engine.describe(spec)) + (" " + i18n.say(it.client, it.guild, "It replaced the old one.") if replace else "")

    # ---- running

    def cooling(self, gid: int, name: str, uid: int, seconds: int) -> bool:
        """True while the person must wait."""
        key = (gid, name, uid)
        now = time.time()
        if now - self.cd.get(key, 0) < seconds:
            return True
        self.cd[key] = now
        if len(self.cd) > 5000:
            self.cd = {k: t for k, t in self.cd.items() if now - t < 3600}
        return False

    def allowed(self, spec: dict, member: discord.Member) -> bool:
        """True if the member holds one of the roles a skill is limited to, or if it has no limit."""
        return not spec["roles"] or any(r.id in spec["roles"] for r in member.roles) or member.guild_permissions.manage_guild

    async def finish(self, runner: Runner, name: str, actions: list, ctx: dict) -> None:
        """Run the actions that follow a game and report the ones that failed."""
        if not actions:
            return
        notes = await engine.run_actions(actions, ctx, runner, self.vars(runner.guild.id))
        if notes:
            log.info("skill %s: actions not done in %s: %s", name, runner.guild.id, ", ".join(notes))

    async def play(self, runner: Runner, spec: dict, ctx: dict) -> None:
        """Play a game once."""
        game, rng = spec["game"], random.Random()
        win_actions, lose_actions = spec.get("on_win", []), spec.get("on_lose", [])
        if game == "dice":
            rolls, total = engine.roll_dice(spec["sides"], spec["count"], rng)
            ctx.update(roll=total, rolls=", ".join(map(str, rolls)))
            won = "win_at" in spec and total >= spec["win_at"]
            text = spec.get("text", "{user} rolled {roll}.")
        elif game == "choice":
            ctx["choice"] = rng.choice(spec["options"])
            won, text = None, spec.get("text", "{user}: {choice}")
        elif game == "slots":
            reels, won = engine.spin_slots(spec["symbols"], rng)
            ctx["reels"] = " ".join(reels)
            text = spec.get("win_text" if won else "lose_text", "{reels}")
        elif game == "rps":
            ctx["pick"] = rng.choice(RPS)
            ctx["choice"] = ctx["pick"]
            await runner.reply(engine.render(spec.get("draw_text", "I pick {pick}. Pick yours with /support skill run."), ctx), False, None, None)
            return
        else:
            return
        await runner.reply(engine.render(text, ctx, self.vars(runner.guild.id), rng), False, None, None)
        if won is not None:
            await self.finish(runner, spec["name"], win_actions if won else lose_actions, ctx)

    async def quiz(self, runner: Runner, spec: dict, ctx: dict, it: discord.Interaction) -> None:
        """Ask one random question with buttons."""
        q = random.choice(spec["questions"])
        view = Answer(self, runner, spec, ctx, q)
        await it.response.send_message(f"**{q['q']}**", view=view)

    async def run_spec(self, runner: Runner, spec: dict, args: list[str], it: Optional[discord.Interaction] = None) -> None:
        """Run a skill for the person behind the runner."""
        ctx = context_for(runner.guild, runner.member, runner.channel, args)
        meta = self.conf(runner.guild.id)["meta"].setdefault(spec["name"], {"author": 0, "created": 0, "uses": 0})
        meta["uses"] = meta.get("uses", 0) + 1
        if spec["kind"] == "game":
            if spec["game"] == "quiz" and it is not None:
                return await self.quiz(runner, spec, ctx, it)
            return await self.play(runner, spec, ctx)
        notes = await engine.run_actions(spec["actions"], ctx, runner, self.vars(runner.guild.id))
        if notes:
            log.info("skill %s: actions not done in %s: %s", spec["name"], runner.guild.id, ", ".join(notes))

    async def run_interaction(self, it: discord.Interaction, name: str, args: list[str], via_button: bool = False) -> None:
        """Run a skill that was started with a slash command or a button."""
        spec = self.items(it.guild_id).get(name)
        if spec is None or not spec["enabled"] or not self.bot.module_on(it.guild_id, "skills"):
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no active skill with that name."), ephemeral=True)
        if not self.allowed(spec, it.user):
            return await it.response.send_message(i18n.say(it.client, it.guild, "You may not use this skill."), ephemeral=True)
        if self.cooling(it.guild_id, name, it.user.id, spec["cooldown"]):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Please wait a moment before using this skill again."), ephemeral=True)

        async def respond(text: Optional[str], ephemeral: bool, embed: Optional[discord.Embed]) -> None:
            if it.response.is_done():
                await it.followup.send(text, embed=embed, ephemeral=ephemeral, allowed_mentions=discord.AllowedMentions(users=[it.user]))
            else:
                await it.response.send_message(text, embed=embed, ephemeral=ephemeral, allowed_mentions=discord.AllowedMentions(users=[it.user]))

        runner = Runner(self, it.guild, it.user, it.channel, respond)
        await self.run_spec(runner, spec, args, it)
        if not it.response.is_done():
            await it.response.send_message(i18n.say(it.client, it.guild, "Done."), ephemeral=True)

    # ---- triggers

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        """Prefix commands and message triggers."""
        if msg.author.bot or not msg.guild or not msg.content or not isinstance(msg.author, discord.Member):
            return
        gid = msg.guild.id
        if not self.bot.module_on(gid, "skills"):
            return
        items = self.items(gid)
        if not items:
            return
        prefix = self.bot.prefix_for(gid)
        runner = Runner(self, msg.guild, msg.author, msg.channel)
        if msg.content.startswith(prefix):
            words = msg.content[len(prefix):].split()
            name = words[0].lower() if words else ""
            spec = items.get(name)
            if spec and spec["enabled"] and spec["kind"] in ("command", "game") and not self.bot.get_command(name):
                if spec["kind"] == "game" and spec["game"] == "quiz":
                    return
                if self.allowed(spec, msg.author) and not self.cooling(gid, name, msg.author.id, spec["cooldown"]):
                    await self.run_spec(runner, spec, words[1:3])
            return
        for spec in list(items.values()):
            trig = spec.get("trigger")
            if not spec["enabled"] or spec["kind"] != "automation" or not trig or trig["event"] != "message_contains":
                continue
            if trig.get("channel") and trig["channel"] != msg.channel.id:
                continue
            if engine.matches(trig, msg.content) and self.allowed(spec, msg.author) and not self.cooling(gid, spec["name"], msg.author.id, spec["cooldown"]):
                await self.run_spec(runner, spec, [])
                return

    async def fire(self, member: discord.Member, event: str) -> None:
        """Run the automations of an event such as a member joining."""
        gid = member.guild.id
        if not self.bot.module_on(gid, "skills") or member.bot:
            return
        for spec in list(self.items(gid).values()):
            if spec["enabled"] and spec["kind"] == "automation" and spec["trigger"]["event"] == event:
                channel = member.guild.system_channel
                await self.run_spec(Runner(self, member.guild, member, channel), spec, [])

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """Automations for new members."""
        await self.fire(member, "member_join")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """Automations for members who left. Role and DM actions fail quietly for them."""
        await self.fire(member, "member_leave")

    # ---- commands

    @skill.command(name="run", description="Use a skill")
    @app_commands.describe(name="Name of the skill", arg1="First word for the skill", arg2="Second word for the skill")
    async def skill_run(self, it: discord.Interaction, name: str, arg1: str = "", arg2: str = ""):
        """Use a skill."""
        await self.run_interaction(it, name.lower(), [a for a in (arg1, arg2) if a])

    @skill_run.autocomplete("name")
    async def skill_names(self, it: discord.Interaction, current: str):
        """Offer the names of the skills that can be used."""
        names = [n for n, s in self.items(it.guild_id).items() if s["enabled"] and s["kind"] != "automation" and current.lower() in n]
        return [app_commands.Choice(name=n, value=n) for n in sorted(names)[:25]]

    @skill.command(name="list", description="List the skills of this server")
    async def skill_list(self, it: discord.Interaction):
        """List the skills."""
        prefix = self.bot.prefix_for(it.guild_id)
        lines = [f"`{n}` {'(off) ' if not s['enabled'] else ''}{s['description'] or engine.describe(s)}" for n, s in sorted(self.items(it.guild_id).items())]
        await it.response.send_message(embed=emb("Skills", "\n".join(lines) or i18n.say(it.client, it.guild, "No skills yet."), footer=f"/support skill run or {prefix}name"), ephemeral=True)

    @skill.command(name="show", description="Show a skill as JSON")
    async def skill_show(self, it: discord.Interaction, name: str):
        """Show a skill so it can be copied."""
        if not await require(it):
            return
        spec = self.items(it.guild_id).get(name.lower())
        if spec is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no skill with that name."), ephemeral=True)
        meta = self.conf(it.guild_id)["meta"].get(spec["name"], {})
        body = json.dumps(spec, indent=1, ensure_ascii=False)
        await it.response.send_message(f"```json\n{body[:1800]}\n```" + i18n.say(it.client, it.guild, "Used {uses} times, made by <@{author}>.", uses=meta.get("uses", 0), author=meta.get("author", 0)), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @skill.command(name="create", description="Create a skill from an example you can change")
    @app_commands.describe(kind="command, game or automation", name="Name of the skill")
    async def skill_create(self, it: discord.Interaction, kind: engine.KINDS_LITERAL, name: str):
        """Open a box with a small example skill."""
        if not await require(it):
            return
        await it.response.send_modal(SkillModal(self, "New skill", json.dumps(engine.starter(kind, name.lower()), indent=1, ensure_ascii=False)))

    @skill.command(name="edit", description="Change a skill")
    async def skill_edit(self, it: discord.Interaction, name: str):
        """Open the JSON of a skill in a box."""
        if not await require(it):
            return
        spec = self.items(it.guild_id).get(name.lower())
        if spec is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no skill with that name."), ephemeral=True)
        await it.response.send_modal(SkillModal(self, "Edit skill", json.dumps(spec, indent=1, ensure_ascii=False)))

    @skill.command(name="import", description="Add a skill from JSON text")
    async def skill_import(self, it: discord.Interaction):
        """Open an empty box for a skill."""
        if not await require(it):
            return
        await it.response.send_modal(SkillModal(self, "Import skill"))

    def toggle_text(self, it: discord.Interaction, name: str, on: bool) -> str:
        """Turn a skill on or off and return the message."""
        spec = self.items(it.guild_id).get(name.lower())
        if spec is None:
            return i18n.say(it.client, it.guild, "There is no skill with that name.")
        spec["enabled"] = on
        return i18n.say(it.client, it.guild, "Skill `{name}` is now on.", name=spec["name"]) if on else i18n.say(it.client, it.guild, "Skill `{name}` is now off.", name=spec["name"])

    @skill.command(name="enable", description="Turn a skill on")
    async def skill_enable(self, it: discord.Interaction, name: str):
        """Turn a skill on."""
        if await require(it):
            await it.response.send_message(self.toggle_text(it, name, True), ephemeral=True)

    @skill.command(name="disable", description="Turn a skill off")
    async def skill_disable(self, it: discord.Interaction, name: str):
        """Turn a skill off."""
        if await require(it):
            await it.response.send_message(self.toggle_text(it, name, False), ephemeral=True)

    @skill.command(name="delete", description="Delete a skill")
    async def skill_delete(self, it: discord.Interaction, name: str):
        """Delete a skill."""
        if not await require(it):
            return
        if self.items(it.guild_id).pop(name.lower(), None) is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no skill with that name."), ephemeral=True)
        self.conf(it.guild_id)["meta"].pop(name.lower(), None)
        await it.response.send_message(i18n.say(it.client, it.guild, "Skill deleted."), ephemeral=True)

    @skill.command(name="panel", description="Post a message with buttons for skills")
    @app_commands.describe(names="Skill names separated by spaces", text="Text above the buttons")
    async def skill_panel(self, it: discord.Interaction, names: str, text: app_commands.Range[str, 1, 500] = "Choose:"):
        """Post buttons that run skills."""
        if not await require(it):
            return
        view = discord.ui.View(timeout=None)
        for n in names.lower().split()[:5]:
            spec = self.items(it.guild_id).get(n)
            if spec is None or spec["kind"] == "game" and spec["game"] == "quiz":
                return await it.response.send_message(i18n.say(it.client, it.guild, "`{name}` is not a skill that can have a button.", name=n), ephemeral=True)
            button = spec.get("button") or {"label": n, "style": "primary"}
            view.add_item(SkillButton(n, button["label"], button["style"]))
        await it.response.send_message(text, view=view)

    @skill.command(name="stats", description="Show how often skills were used")
    async def skill_stats(self, it: discord.Interaction):
        """Usage numbers."""
        meta = self.conf(it.guild_id)["meta"]
        rows = sorted(((m.get("uses", 0), n) for n, m in meta.items() if n in self.items(it.guild_id)), reverse=True)[:15]
        await it.response.send_message("\n".join(f"`{n}` {u}" for u, n in rows) or i18n.say(it.client, it.guild, "No skills yet."), ephemeral=True)


async def setup(bot: Any) -> None:
    """Register the cog with the bot."""
    await bot.add_cog(Skills(bot))
