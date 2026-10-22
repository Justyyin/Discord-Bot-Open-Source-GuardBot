"""Guided setup with buttons, AutoMod presets, server templates and the health overview."""

import logging

import discord
from discord.ext import commands

from .. import i18n
from ..defaults import MODULES
from ..presets import AUTOMOD_PRESETS, AUTOMOD_RULES, TEMPLATES, apply_automod_preset, apply_template
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
    rows.append(("Log channel", bool(log_ch), log_ch or "not set, run /setup"))
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
    e.set_footer(text=("Open: " + ", ".join(todo) + ". Run /setup to fix it.") if todo else "Everything important is set up.")
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
            await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This assistant belongs to someone else. Run /setup yourself."), ephemeral=True)
            return False
        return True


class Wizard(discord.ui.View):
    """The main window of /setup."""

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
            await interaction.response.send_message(i18n.say(interaction.client, interaction.guild, "This assistant belongs to someone else. Run /setup yourself."), ephemeral=True)
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
            await it.response.send_message(f"Logs go to {ch.mention}. Categories can be split later with /log.", ephemeral=True)

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
            await it.response.send_message(f"Welcome messages go to {ch.mention}. Change the text with /welcome set.", ephemeral=True)

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
                f"Staff roles set to {' '.join(f'<@&{i}>' for i in ids)}. The first one is used for the gulag, tickets and mod-mail. Command access still follows Discord permissions, change it with /perms.",
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
        await interaction.response.send_message(f"Template {select.values[0]} applied. Switched on: {', '.join(mods)}. Nothing was switched off. Use /module to change it.", ephemeral=True)

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

    @commands.hybrid_command(name="setup", description="Guided setup with buttons, AutoMod presets and templates")
    @commands.guild_only()
    async def setup_cmd(self, ctx):
        """Open the setup assistant."""
        e = emb("Setup assistant", color=discord.Color.blurple())
        e.description = (
            "Set up the most important things with a few clicks.\n\n"
            "Buttons: log channel, welcome channel, staff roles and the gulag.\n"
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
