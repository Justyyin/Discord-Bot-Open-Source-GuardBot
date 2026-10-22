"""Server administration: modules, command switches, prefix, aliases, permissions and raw settings."""

import io
import json
import re
from typing import Optional, Union

import discord
from discord import app_commands
from discord.ext import commands

from .. import __version__, configio, i18n
from ..defaults import COMMAND_MODULES, DEFAULTS, FALLBACK_PERMS, MODULES, PROTECTED_COMMANDS
from ..utils import emb, trim

KNOWN = sorted(set(COMMAND_MODULES) | set(FALLBACK_PERMS))
LOCKED_KEYS = ("case_counter",)


def parse_item(raw):
    """Turn a mention or a number string into an int, anything else stays text."""
    m = re.fullmatch(r"<[#@&!]*(\d+)>", raw.strip())
    if m:
        return int(m.group(1))
    return int(raw) if raw.strip().isdigit() else raw.strip()


def parse_value(raw, current):
    """Convert user input to the type of the setting it replaces (bool, int, float, list or text)."""
    raw = raw.strip()
    if raw.lower() in ("none", "null"):
        return None
    if isinstance(current, bool):
        return raw.lower() in ("1", "true", "yes", "on")
    if isinstance(current, int):
        return int(parse_item(raw))
    if isinstance(current, float):
        return float(raw)
    if isinstance(current, list):
        return [parse_item(x) for x in raw.split(",") if x.strip()]
    if current is None:
        return parse_item(raw)
    return raw


def walk(d, path):
    """Follow a dotted path like 'automod.caps.percent' and return the parent dict and the last key."""
    parts = path.split(".")
    for p in parts[:-1]:
        d = d[p]
    return d, parts[-1]


class Admin(commands.Cog):
    """Commands to manage modules, commands, prefix, aliases, permissions and raw settings."""
    module = app_commands.Group(name="module", description="Turn features on or off", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    command = app_commands.Group(name="command", description="Turn single commands on or off", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    alias = app_commands.Group(name="alias", description="Prefix command aliases", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    perms = app_commands.Group(name="perms", description="Who may use which command", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    config = app_commands.Group(name="config", description="Read and change any setting", default_permissions=discord.Permissions(administrator=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot

    @module.command(name="list", description="Show all modules")
    async def m_list(self, it: discord.Interaction):
        """Show all modules."""
        mods = self.bot.cfg(it.guild_id)["modules"]
        await it.response.send_message("\n".join(f"{k}: {'on' if v else 'off'}" for k, v in mods.items()), ephemeral=True)

    async def module_names(self, it: discord.Interaction, current: str):
        """Suggest module names while the user types."""
        return [app_commands.Choice(name=m, value=m) for m in MODULES if current.lower() in m][:25]

    @module.command(name="enable", description="Turn a module on")
    @app_commands.autocomplete(name=module_names)
    async def m_enable(self, it: discord.Interaction, name: str):
        """Turn a module on."""
        if name not in MODULES:
            return await it.response.send_message(f"Unknown module. Use /module list. Modules: {', '.join(MODULES)}", ephemeral=True)
        self.bot.cfg(it.guild_id)["modules"][name] = True
        await it.response.send_message(f"{name}: on", ephemeral=True)

    @module.command(name="disable", description="Turn a module off")
    @app_commands.autocomplete(name=module_names)
    async def m_disable(self, it: discord.Interaction, name: str):
        """Turn a module off."""
        if name not in MODULES:
            return await it.response.send_message(f"Unknown module. Use /module list. Modules: {', '.join(MODULES)}", ephemeral=True)
        self.bot.cfg(it.guild_id)["modules"][name] = False
        await it.response.send_message(f"{name}: off", ephemeral=True)

    @command.command(name="disable", description="Turn one command off")
    async def c_disable(self, it: discord.Interaction, name: str):
        """Turn one command off."""
        name = self.bot.canonical.get(name.lower(), name.lower())
        if name in PROTECTED_COMMANDS:
            return await it.response.send_message(i18n.say(it.client, it.guild, "That command cannot be disabled."), ephemeral=True)
        lst = self.bot.cfg(it.guild_id)["disabled_commands"]
        if name not in lst:
            lst.append(name)
        await it.response.send_message(f"{name} is disabled.", ephemeral=True)

    @command.command(name="enable", description="Turn one command on again")
    async def c_enable(self, it: discord.Interaction, name: str):
        """Turn one command on again."""
        name = self.bot.canonical.get(name.lower(), name.lower())
        lst = self.bot.cfg(it.guild_id)["disabled_commands"]
        if name in lst:
            lst.remove(name)
        await it.response.send_message(f"{name} is enabled.", ephemeral=True)

    @command.command(name="list", description="Show disabled commands")
    async def c_list(self, it: discord.Interaction):
        """Show disabled commands."""
        lst = self.bot.cfg(it.guild_id)["disabled_commands"]
        await it.response.send_message(", ".join(lst) or "No commands are disabled.", ephemeral=True)

    @app_commands.command(name="prefix", description="Change the prefix for text commands")
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def prefix_cmd(self, it: discord.Interaction, new_prefix: app_commands.Range[str, 1, 5]):
        """Change the prefix for text commands."""
        self.bot.cfg(it.guild_id)["prefix"] = new_prefix
        await it.response.send_message(f"The prefix is now {new_prefix}", ephemeral=True)

    @app_commands.command(name="language", description="Set the language of the messages that members see")
    @app_commands.describe(code="Language of welcome texts, notices and error messages")
    @app_commands.choices(code=[app_commands.Choice(name=f"{name} ({key})", value=key) for key, name in i18n.LANGUAGES.items()])
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def language_cmd(self, it: discord.Interaction, code: app_commands.Choice[str]):
        """Set the language of member-facing texts. Settings replies of the bot stay English."""
        self.bot.cfg(it.guild_id)["language"] = code.value
        await it.response.send_message(i18n.tr(code.value, "Language set to {language}.", language=i18n.LANGUAGES[code.value]), ephemeral=True)

    @alias.command(name="add", description="Create a short name for a prefix command")
    async def a_add(self, it: discord.Interaction, alias: str, command: str):
        """Create a short name for a prefix command."""
        command = self.bot.canonical.get(command.lower(), command.lower())
        if self.bot.get_command(command) is None and command not in self.bot.canonical.values():
            return await it.response.send_message(i18n.say(it.client, it.guild, "Unknown command."), ephemeral=True)
        self.bot.cfg(it.guild_id)["aliases"][alias.lower()] = command
        await it.response.send_message(f"{self.bot.prefix_for(it.guild_id)}{alias.lower()} now runs {command}.", ephemeral=True)

    @alias.command(name="remove", description="Delete an alias")
    async def a_remove(self, it: discord.Interaction, alias: str):
        """Delete an alias."""
        if self.bot.cfg(it.guild_id)["aliases"].pop(alias.lower(), None) is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "No such alias."), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Removed."), ephemeral=True)

    @alias.command(name="list", description="Show aliases")
    async def a_list(self, it: discord.Interaction):
        """Show aliases."""
        al = self.bot.cfg(it.guild_id)["aliases"]
        await it.response.send_message("\n".join(f"{k} -> {v}" for k, v in al.items()) or "No aliases.", ephemeral=True)

    def rule(self, gid, command):
        """Return the permission rule of a command and create an empty one if none exists."""
        return self.bot.cfg(gid)["perms"].setdefault(command, {"roles": [], "users": [], "deny_roles": [], "deny_users": []})

    @perms.command(name="allow", description="Only these roles or users may use a command")
    async def p_allow(self, it: discord.Interaction, command: str, target: Union[discord.Member, discord.Role]):
        """Only these roles or users may use a command."""
        command = self.bot.canonical.get(command.lower(), command.lower())
        r = self.rule(it.guild_id, command)
        key = "roles" if isinstance(target, discord.Role) else "users"
        if target.id not in r[key]:
            r[key].append(target.id)
        await it.response.send_message(f"{target.mention} may use {command}.", ephemeral=True)

    @perms.command(name="deny", description="Block a role or user from a command")
    async def p_deny(self, it: discord.Interaction, command: str, target: Union[discord.Member, discord.Role]):
        """Block a role or user from a command."""
        command = self.bot.canonical.get(command.lower(), command.lower())
        r = self.rule(it.guild_id, command)
        key = "deny_roles" if isinstance(target, discord.Role) else "deny_users"
        if target.id not in r[key]:
            r[key].append(target.id)
        await it.response.send_message(f"{target.mention} cannot use {command}.", ephemeral=True)

    @perms.command(name="reset", description="Back to the default permission of a command")
    async def p_reset(self, it: discord.Interaction, command: str):
        """Back to the default permission of a command."""
        self.bot.cfg(it.guild_id)["perms"].pop(self.bot.canonical.get(command.lower(), command.lower()), None)
        await it.response.send_message(i18n.say(it.client, it.guild, "Reset."), ephemeral=True)

    @perms.command(name="show", description="Show permission rules")
    async def p_show(self, it: discord.Interaction, command: Optional[str] = None):
        """Show permission rules."""
        rules = self.bot.cfg(it.guild_id)["perms"]
        lines = []
        for name, r in rules.items():
            if command and name != command.lower():
                continue
            lines.append(f"{name}: allow {' '.join('<@&' + str(i) + '>' for i in r['roles']) + ' ' + ' '.join('<@' + str(i) + '>' for i in r['users']) or '-'} | deny {' '.join('<@&' + str(i) + '>' for i in r['deny_roles']) + ' ' + ' '.join('<@' + str(i) + '>' for i in r['deny_users']) or '-'}")
        defaults = ", ".join(f"{k}={v}" for k, v in FALLBACK_PERMS.items())
        await it.response.send_message(trim("\n".join(lines) or f"No custom rules. Defaults: {defaults}", 1900), ephemeral=True)

    @config.command(name="get", description="Read a setting, for example automod.caps.percent")
    async def cfg_get(self, it: discord.Interaction, path: str):
        """Read a setting, for example automod.caps.percent."""
        try:
            d, key = walk(self.bot.cfg(it.guild_id), path)
            value = d[key]
        except (KeyError, TypeError):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Unknown setting."), ephemeral=True)
        await it.response.send_message(f"```json\n{trim(json.dumps(value, indent=1, ensure_ascii=False), 1800)}\n```", ephemeral=True)

    @config.command(name="set", description="Change a setting. Lists use commas, IDs or mentions are accepted")
    async def cfg_set(self, it: discord.Interaction, path: str, value: str):
        """Change a setting. Lists use commas, IDs or mentions are accepted."""
        if path.split(".")[0] in LOCKED_KEYS:
            return await it.response.send_message(i18n.say(it.client, it.guild, "That setting cannot be changed."), ephemeral=True)
        try:
            d, key = walk(self.bot.cfg(it.guild_id), path)
            current = d[key]
            if isinstance(current, dict):
                return await it.response.send_message(i18n.say(it.client, it.guild, "That is a group of settings. Pick one inside it."), ephemeral=True)
            d[key] = parse_value(value, current)
        except (KeyError, TypeError, ValueError):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Unknown setting or invalid value."), ephemeral=True)
        await it.response.send_message(f"{path} = {d[key]}", ephemeral=True)

    @config.command(name="reset", description="Reset a setting group to its default, for example welcome")
    async def cfg_reset(self, it: discord.Interaction, section: str):
        """Reset a setting group to its default, for example welcome."""
        if section not in DEFAULTS or section in LOCKED_KEYS:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Unknown section."), ephemeral=True)
        import copy
        self.bot.cfg(it.guild_id)[section] = copy.deepcopy(DEFAULTS[section])
        await it.response.send_message(f"{section} reset.", ephemeral=True)

    @config.command(name="export", description="Download the settings of this server as a file")
    async def cfg_export(self, it: discord.Interaction):
        """Download the settings of this server as a file."""
        raw = json.dumps(configio.export_config(self.bot.cfg(it.guild_id)), indent=2, ensure_ascii=False).encode("utf-8")
        await it.response.send_message(i18n.say(it.client, it.guild, "Settings without running data such as open tickets, polls or counters. Keep the file private."), file=discord.File(io.BytesIO(raw), filename="guardbot-settings.json"), ephemeral=True)

    @config.command(name="import", description="Load settings from an exported file (first without confirm to only check it)")
    @app_commands.describe(file="File from /config export", confirm="Set to true to really apply it")
    async def cfg_import(self, it: discord.Interaction, file: discord.Attachment, confirm: bool = False):
        """Load settings from an exported file (first without confirm to only check it)."""
        if file.size > configio.MAX_BYTES:
            return await it.response.send_message(i18n.say(it.client, it.guild, "The file is larger than 1 MB."), ephemeral=True)
        payload, problems = configio.parse(await file.read())
        if problems:
            return await it.response.send_message(trim("The file was not imported:\n" + "\n".join(f"- {p}" for p in problems[:15]), 1900), ephemeral=True)
        if not confirm:
            return await it.response.send_message(f"The file is valid (made with GuardBot {payload.get('version', '?')}). This replaces all settings of this server except running data. Channel and role IDs belong to the server where the file was made, so run /diagnose afterwards. Repeat the command with confirm set to true to apply it.", ephemeral=True)
        cfg = self.bot.cfg(it.guild_id)
        new = configio.apply_import(cfg, payload)
        cfg.clear()
        cfg.update(new)
        await it.response.send_message(i18n.say(it.client, it.guild, "Settings imported. Run /diagnose to check that the channels and roles exist."), ephemeral=True)

    @app_commands.command(name="settings", description="Overview of the current configuration")
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def settings_cmd(self, it: discord.Interaction):
        """Overview of the current configuration."""
        g = self.bot.cfg(it.guild_id)
        e = emb("Settings")
        e.add_field(name="Prefix", value=self.bot.prefix_for(it.guild_id))
        e.add_field(name="Modules on", value=", ".join(k for k, v in g["modules"].items() if v) or "none", inline=False)
        e.add_field(name="Modules off", value=", ".join(k for k, v in g["modules"].items() if not v) or "none", inline=False)
        e.add_field(name="Log channels", value=" ".join(f"{k}: <#{v}>" for k, v in g["log"].items() if v) or "not set", inline=False)
        e.add_field(name="Jail", value=f"role {('<@&' + str(g['jail']['role']) + '>') if g['jail']['role'] else 'none'}, channel {('<#' + str(g['jail']['channel']) + '>') if g['jail']['channel'] else 'none'}")
        e.add_field(name="Disabled commands", value=", ".join(g["disabled_commands"]) or "none")
        await it.response.send_message(embed=e, ephemeral=True)

    @app_commands.command(name="about", description="About this bot")
    async def about_cmd(self, it: discord.Interaction):
        """About this bot."""
        e = emb("GuardBot", f"Open source Discord moderation and community bot.\nVersion {__version__}\nMade in Germany\n\nBugs, ideas and suggestions: Discord @justyyin")
        await it.response.send_message(embed=e, ephemeral=True)

    def find_command(self, words):
        """Find a slash command or subcommand by the words the user typed, honouring renamed commands."""
        renamed = {old: new for new, old in self.bot.canonical.items()}
        cmd = self.bot.tree.get_command(renamed.get(words[0], words[0]))
        if cmd is not None and hasattr(cmd, "get_command") and len(words) > 1:
            return cmd.get_command(words[1]) or cmd
        return cmd

    @commands.hybrid_command(name="help", description="List the commands, or explain one command")
    @app_commands.describe(command="Command name, for example ban or automod toggle")
    async def help_cmd(self, ctx, *, command: Optional[str] = None):
        """List the commands, or explain one command."""
        prefix = self.bot.prefix_for(ctx.guild.id)
        if command:
            words = command.lower().lstrip("/" + prefix).split()
            cmd = self.find_command(words) if words else None
            if cmd is None:
                return await ctx.send(i18n.say(ctx.bot, ctx.guild, "I do not know that command. Use /help for the list."), ephemeral=True)
            root = cmd.root_parent.name if getattr(cmd, "root_parent", None) else cmd.name
            root = self.bot.canonical.get(root, root)
            e = emb(f"/{cmd.qualified_name}", cmd.description)
            if hasattr(cmd, "commands"):
                e.add_field(name="Subcommands", value="\n".join(f"`/{c.qualified_name}` {c.description}" for c in cmd.commands)[:1000], inline=False)
            else:
                usage = " ".join((f"{p.name}:..." if p.required else f"[{p.name}:...]") for p in cmd.parameters)
                e.add_field(name="Usage", value=f"`/{cmd.qualified_name} {usage}`".strip(), inline=False)
                if cmd.parameters:
                    e.add_field(name="Options", value="\n".join(f"`{p.name}` {'' if p.required else '(optional) '}{p.description if p.description != '...' else ''}" for p in cmd.parameters)[:1000], inline=False)
            if self.bot.get_command(root):
                e.add_field(name="Text command", value=f"`{prefix}{root}` works too", inline=False)
            mod, perm = COMMAND_MODULES.get(root), FALLBACK_PERMS.get(root)
            e.add_field(name="Module", value=mod or "always on")
            e.add_field(name="Default permission", value=perm.replace("_", " ") if perm else "everyone, or Manage Server for setup commands")
            return await ctx.send(embed=e, ephemeral=True)
        by_module = {}
        for cmd, mod in COMMAND_MODULES.items():
            by_module.setdefault(mod, []).append(cmd)
        lines = [f"**{mod}**{'' if self.bot.module_on(ctx.guild.id, mod) else ' (off)'}: " + " ".join(f"`{c}`" for c in cmds) for mod, cmds in by_module.items()]
        lines.append("**admin**: " + " ".join(f"`{c}`" for c in PROTECTED_COMMANDS))
        e = emb("Commands", f"Slash commands and text commands ({prefix}) are available. Use /help command:ban to explain one command.\n\n" + "\n".join(lines))
        await ctx.send(embed=e, ephemeral=True)

async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Admin(bot))
