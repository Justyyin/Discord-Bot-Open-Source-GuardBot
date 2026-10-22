"""Guided setup with buttons, AutoMod presets, server templates and the health overview."""

import asyncio
import logging

import discord
from discord.ext import commands

from .. import i18n
from ..defaults import MODULES
from ..presets import AUTOMOD_PRESETS, AUTOMOD_RULES, BLUEPRINTS, TEMPLATES, apply_automod_preset, apply_template, blueprint_missing, blueprint_size
from ..utils import emb

log = logging.getLogger(__name__)


def overview(cfg, guild):
    """List what is set up on a server as (name, ok, detail) rows."""
    def channel(cid):
        """Name of a channel or None when it is not set or gone."""
        ch = guild.get_channel(cid) if cid else None
        return f"#{ch.name}" if ch else None

    def role(rid):
        """Name of a role or None when it is not set or gone."""
        r = guild.get_role(rid) if rid else None
        return f"@{r.name}" if r else None

    rows = []
    log_ch = channel(cfg["log"].get("main"))
    rows.append(("Log channel", bool(log_ch), log_ch or "not set, run /admin setup"))
    welcome = channel(cfg["welcome"]["channel"])
    on = cfg["modules"].get("welcome")
    rows.append(("Welcome", bool(on and welcome), f"{welcome}" if on and welcome else "off" if not on else "no channel"))
    staff = role(cfg["jail"]["staff_role"])
    rows.append(("Staff role", bool(staff), staff or "not set"))
    gulag_role, gulag_ch = role(cfg["jail"]["role"]), channel(cfg["jail"]["channel"])
    rows.append(("Gulag", bool(gulag_role and gulag_ch), f"{gulag_role}, {gulag_ch}" if gulag_role and gulag_ch else "not set up"))
    rules = [r for r in AUTOMOD_RULES if cfg["automod"][r]["enabled"]]
    rows.append(("AutoMod", bool(cfg["modules"].get("automod") and rules), f"{len(rules)} of {len(AUTOMOD_RULES)} rules on" if cfg["modules"].get("automod") else "module off"))
    on_count = sum(1 for m in MODULES if cfg["modules"].get(m))
    rows.append(("Modules", True, f"{on_count} of {len(MODULES)} on"))
    rows.append(("Language", True, i18n.LANGUAGES.get(cfg.get("language", "en"), "English")))
    return rows


def health_embed(bot, guild):
    """Build the health overview: what is set up plus the problems found by the self-test."""
    cfg = bot.cfg(guild.id)
    rows = overview(cfg, guild)
    e = emb("Health of this server", color=discord.Color.blurple())
    e.description = "\n".join(f"{'ok' if ok else 'todo'}  {name}: {detail}" for name, ok, detail in rows)
    debug = bot.get_cog("Debug")
    if debug is not None:
        problems, checks = debug.selftest(guild)
        value = f"{len(problems)} problem(s) in {checks} checks\n" + "\n".join(f"- {p}" for p in problems[:8]) if problems else f"All {checks} checks passed."
        e.add_field(name="Self-test", value=value[:1000], inline=False)
    todo = [name for name, ok, _ in rows if not ok]
    e.set_footer(text=("Open: " + ", ".join(todo) + ". Run /admin setup to fix it.") if todo else "Everything important is set up.")
    return e


class Picker(discord.ui.View):
    """A message with one channel or role menu that applies the choice."""

    def __init__(self, user_id, select, create=None):
        """Add the menu and an optional button that creates a new channel."""
        super().__init__(timeout=300)
        self.user_id = user_id
        self.add_item(select)
        if create:
            button = discord.ui.Button(label="Create a new channel", style=discord.ButtonStyle.secondary)
            button.callback = create
            self.add_item(button)

    async def interaction_check(self, interaction):
        """Only the person who opened the assistant may use it."""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This assistant belongs to someone else. Run /admin setup yourself."), ephemeral=True)
            return False
        return True


class BuildConfirm(discord.ui.View):
    """Shows what the setup assistant would create and builds it after a click."""

    def __init__(self, cog, user_id, name):
        """Remember the blueprint and the person who may confirm."""
        super().__init__(timeout=300)
        self.cog, self.user_id, self.name = cog, user_id, name

    async def interaction_check(self, interaction):
        """Only the person who opened the assistant may confirm, and only with Manage Server."""
        if interaction.user.id != self.user_id or not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This assistant belongs to someone else. Run /admin setup yourself."), ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Create", style=discord.ButtonStyle.danger)
    async def create(self, interaction, button):
        """Create the missing roles, categories and channels."""
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content="Creating, this takes a moment.", view=self)
        text = await self.cog.build(interaction.guild, self.name, interaction.user)
        await interaction.edit_original_response(content=text, view=None)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction, button):
        """Do nothing."""
        await interaction.response.edit_message(content="Cancelled. Nothing was created.", view=None)
        self.stop()


class Wizard(discord.ui.View):
    """The main window of /admin setup."""

    def __init__(self, cog, user_id):
        """Keep the cog and the person who opened the window."""
        super().__init__(timeout=600)
        self.cog = cog
        self.bot = cog.bot
        self.user_id = user_id
        for key, text in TEMPLATES.items():
            self.template.add_option(label=key.capitalize(), value=key, description=text["text"][:100])
        for key in AUTOMOD_PRESETS:
            self.preset.add_option(label=key.capitalize(), value=key, description={"loose": "Only phishing and mass mentions", "normal": "Phishing, invites, caps, flood, mentions", "strict": "Everything including links, personal data and threats"}[key])
        for code, name in i18n.LANGUAGES.items():
            self.language.add_option(label=name, value=code)

    async def interaction_check(self, interaction):
        """Only the person who opened the assistant may use it, and only with Manage Server."""
        if interaction.user.id != self.user_id or not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This assistant belongs to someone else. Run /admin setup yourself."), ephemeral=True)
            return False
        return True

    def cfg(self, interaction):
        """Settings of the server of an interaction."""
        return self.bot.cfg(interaction.guild_id)

    @discord.ui.button(label="Log channel", style=discord.ButtonStyle.primary, row=0)
    async def logs(self, interaction, button):
        """Choose or create the channel that receives the logs."""
        async def chosen(it):
            """Use the selected channel."""
            ch = menu.values[0]
            self.cfg(it)["log"]["main"] = ch.id
            self.cfg(it)["modules"]["logging"] = True
            await it.response.send_message(f"Logs go to {ch.mention}. Categories can be split later with /server log.", ephemeral=True)

        async def create(it):
            """Create a private log channel."""
            guild = it.guild
            over = {guild.default_role: discord.PermissionOverwrite(view_channel=False), guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, embed_links=True, attach_files=True)}
            try:
                ch = await guild.create_text_channel("guardbot-logs", overwrites=over, reason="Setup assistant")
            except discord.HTTPException as exc:
                return await it.response.send_message(f"I could not create the channel: {exc}", ephemeral=True)
            self.cfg(it)["log"]["main"] = ch.id
            self.cfg(it)["modules"]["logging"] = True
            await it.response.send_message(f"Created {ch.mention}. Only you and I can see it. Give your staff access in the channel settings.", ephemeral=True)

        menu = discord.ui.ChannelSelect(channel_types=[discord.ChannelType.text], placeholder="Choose the log channel")
        menu.callback = chosen
        await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Where should logs go?"), view=Picker(self.user_id, menu, create), ephemeral=True)

    @discord.ui.button(label="Welcome", style=discord.ButtonStyle.primary, row=0)
    async def welcome(self, interaction, button):
        """Choose the welcome channel and switch welcome messages on."""
        async def chosen(it):
            """Use the selected channel."""
            ch = menu.values[0]
            self.cfg(it)["welcome"]["channel"] = ch.id
            self.cfg(it)["modules"]["welcome"] = True
            await it.response.send_message(f"Welcome messages go to {ch.mention}. Change the text with /community welcome set.", ephemeral=True)

        menu = discord.ui.ChannelSelect(channel_types=[discord.ChannelType.text], placeholder="Choose the welcome channel")
        menu.callback = chosen
        await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Where should new members be welcomed?"), view=Picker(self.user_id, menu), ephemeral=True)

    @discord.ui.button(label="Staff roles", style=discord.ButtonStyle.primary, row=0)
    async def staff(self, interaction, button):
        """Choose the roles of the moderators and use them as staff role of tickets, mod-mail, gulag and anti-nuke."""
        async def chosen(it):
            """Apply the selected roles."""
            ids = [r.id for r in menu.values]
            c = self.cfg(it)
            c["jail"]["staff_role"] = ids[0]
            c["tickets"]["support_role"] = ids[0]
            c["modmail"]["staff_role"] = ids[0]
            c["antinuke"]["staff_roles"] = ids
            await it.response.send_message(
                f"Staff roles set to {' '.join(f'<@&{i}>' for i in ids)}. The first one is used for the gulag, tickets and mod-mail. Command access still follows Discord permissions, change it with /admin perms.",
                ephemeral=True,
            )

        menu = discord.ui.RoleSelect(placeholder="Choose the moderator roles", min_values=1, max_values=5)
        menu.callback = chosen
        await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Which roles are your moderators?"), view=Picker(self.user_id, menu), ephemeral=True)

    @discord.ui.button(label="Gulag", style=discord.ButtonStyle.primary, row=0)
    async def gulag(self, interaction, button):
        """Create the gulag role and channel and lock the role out of all other channels."""
        jail = self.bot.get_cog("Jail")
        if jail is None:
            return await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "The gulag module is not loaded."), ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        self.cfg(interaction)["modules"]["jail"] = True
        await interaction.followup.send(await jail.build(interaction.guild), ephemeral=True)

    @discord.ui.button(label="Create channels", style=discord.ButtonStyle.primary, row=0)
    async def structure(self, interaction, button):
        """Offer to create the roles, categories and channels of a template."""
        async def chosen(it):
            """Show what would be created."""
            name = menu.values[0]
            roles, cats, chans = blueprint_missing(BLUEPRINTS[name], {r.name.casefold() for r in it.guild.roles}, {c.name.casefold() for c in it.guild.channels}, {c.name.casefold() for c in it.guild.categories})
            if not (roles or cats or chans):
                return await it.response.send_message(f"Everything of the {name} template exists already.", ephemeral=True)
            lines = [f"Roles: {', '.join(r['name'] for r in roles) or 'none'}", f"Categories: {', '.join(c['name'] for c in cats) or 'none'}", "Channels: " + (", ".join(f"{ch['name']}" for _, ch in chans) or "none")]
            room = 500 - len(it.guild.channels)
            if len(cats) + len(chans) > room:
                return await it.response.send_message("The server would exceed the limit of 500 channels.", ephemeral=True)
            await it.response.send_message(f"Template {name}. Nothing that exists is changed or deleted. This would be created:\n" + "\n".join(lines) + "\nStaff channels are only visible for the new staff role and me.", view=BuildConfirm(self.cog, self.user_id, name), ephemeral=True)

        menu = discord.ui.Select(placeholder="Choose a template", options=[discord.SelectOption(label=k.capitalize(), value=k, description="%d roles, %d categories, %d channels" % blueprint_size(v)) for k, v in BLUEPRINTS.items()])
        menu.callback = chosen
        await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "Which template should be created?"), view=Picker(self.user_id, menu), ephemeral=True)

    @discord.ui.button(label="Check", style=discord.ButtonStyle.success, row=4)
    async def check(self, interaction, button):
        """Show the health overview."""
        await interaction.response.send_message(embed=health_embed(self.bot, interaction.guild), ephemeral=True)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.secondary, row=4)
    async def close(self, interaction, button):
        """Disable the window."""
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.select(placeholder="AutoMod preset", row=1, min_values=1, max_values=1)
    async def preset(self, interaction, select):
        """Apply an AutoMod preset."""
        rules = apply_automod_preset(self.cfg(interaction), select.values[0])
        await interaction.response.send_message(f"AutoMod preset {select.values[0]} applied: {', '.join(rules)}. Fine-tune with /automod.", ephemeral=True)

    @discord.ui.select(placeholder="Server template", row=2, min_values=1, max_values=1)
    async def template(self, interaction, select):
        """Apply a server template."""
        mods = apply_template(self.cfg(interaction), select.values[0])
        await interaction.response.send_message(f"Template {select.values[0]} applied. Switched on: {', '.join(mods)}. Nothing was switched off. Use /admin module to change it.", ephemeral=True)

    @discord.ui.select(placeholder="Language of member messages", row=3, min_values=1, max_values=1)
    async def language(self, interaction, select):
        """Set the language of the member-facing texts."""
        code = select.values[0]
        self.cfg(interaction)["language"] = code
        await interaction.response.send_message(i18n.tr(code, "Language set to {language}.", language=i18n.LANGUAGES[code]), ephemeral=True)


class Setup(commands.Cog):
    """Setup assistant and health overview."""

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    async def build(self, guild, name, user):
        """Create the roles, categories and channels of a blueprint that do not exist yet and connect them to the settings. Returns a short result text."""
        blueprint = BLUEPRINTS[name]
        cfg = self.bot.cfg(guild.id)
        made_roles, made_channels, failed = [], [], []
        roles = {r.name.casefold(): r for r in guild.roles}
        staff_role = None
        for spec in blueprint["roles"]:
            role = roles.get(spec["name"].casefold())
            if role is None:
                try:
                    role = await guild.create_role(name=spec["name"], colour=discord.Colour(spec["color"]), permissions=discord.Permissions(**{p: True for p in spec["permissions"]}), hoist=True, reason=f"Setup assistant ({user})")
                    made_roles.append(role.name)
                except discord.HTTPException as exc:
                    failed.append(f"role {spec['name']}: {exc}")
                    continue
                await asyncio.sleep(0.4)
            if spec.get("staff"):
                staff_role = role
        everyone = guild.default_role
        for cat in blueprint["categories"]:
            category = discord.utils.find(lambda c: c.name.casefold() == cat["name"].casefold(), guild.categories)
            over = {}
            if cat.get("private"):
                over = {everyone: discord.PermissionOverwrite(view_channel=False), guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True, embed_links=True, attach_files=True)}
                if staff_role is not None:
                    over[staff_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
            try:
                if category is None:
                    category = await guild.create_category(cat["name"], overwrites=over, reason=f"Setup assistant ({user})")
                    made_channels.append(f"category {cat['name']}")
                    await asyncio.sleep(0.4)
            except discord.HTTPException as exc:
                failed.append(f"category {cat['name']}: {exc}")
                continue
            existing = {c.name.casefold() for c in guild.channels}
            for ch in cat["channels"]:
                if ch["name"].casefold() in existing:
                    continue
                perms = {everyone: discord.PermissionOverwrite(send_messages=False)} if ch.get("readonly") else {}
                try:
                    if ch["kind"] == "voice":
                        made = await guild.create_voice_channel(ch["name"], category=category, reason=f"Setup assistant ({user})")
                    else:
                        made = await guild.create_text_channel(ch["name"], category=category, overwrites=perms, reason=f"Setup assistant ({user})")
                except discord.HTTPException as exc:
                    failed.append(f"channel {ch['name']}: {exc}")
                    continue
                made_channels.append(made.name)
                key = ch.get("key")
                if key == "log" and not cfg["log"]["main"]:
                    cfg["log"]["main"], cfg["modules"]["logging"] = made.id, True
                elif key == "rules" and not cfg["rules"]["channel"]:
                    cfg["rules"]["channel"] = made.id
                elif key == "welcome" and not cfg["welcome"]["channel"]:
                    cfg["welcome"]["channel"] = made.id
                await asyncio.sleep(0.4)
        if staff_role is not None:
            for section, key in (("jail", "staff_role"), ("tickets", "support_role"), ("modmail", "staff_role")):
                if not cfg[section][key]:
                    cfg[section][key] = staff_role.id
        parts = [f"Created roles: {', '.join(made_roles) or 'none'}.", f"Created channels: {', '.join(made_channels) or 'none'}."]
        if failed:
            parts.append("Problems: " + "; ".join(failed[:5]))
        parts.append("The log, rules and welcome channels and the staff role were set where they were empty. Give people the new staff role yourself.")
        return " ".join(parts)[:1900]

    @commands.hybrid_command(name="setup", description="Guided setup with buttons, AutoMod presets and templates")
    @commands.guild_only()
    async def setup_cmd(self, ctx):
        """Open the setup assistant."""
        e = emb("Setup assistant", color=discord.Color.blurple())
        e.description = (
            "Set up the most important things with a few clicks.\n\n"
            "Buttons: log channel, welcome channel, staff roles, the gulag and creating the channels and roles of a template.\n"
            "Menus: AutoMod preset (loose, normal, strict), server template (community, gaming, support) and the language of member messages.\n\n"
            "Nothing is switched off by a template. Press Check to see what is still open."
        )
        await ctx.send(embed=e, view=Wizard(self, ctx.author.id), ephemeral=True)

    @commands.hybrid_command(name="health", description="Show what is set up on this server and what is still open")
    @commands.guild_only()
    async def health(self, ctx):
        """Show the overview of what is set up plus the result of the self-test."""
        await ctx.send(embed=health_embed(self.bot, ctx.guild), ephemeral=True)


async def setup(bot):
    """Add the cog to the bot."""
    await bot.add_cog(Setup(bot))
