# Copyright (c) Justyn
import json
import re
from typing import Literal, Optional, Union

import discord
from discord import app_commands
from discord.ext import commands

from .. import __version__
from ..defaults import COMMAND_MODULES, DEFAULTS, FALLBACK_PERMS, MODULES, PROTECTED_COMMANDS
from ..utils import CREDIT, emb, trim

KNOWN = sorted(set(COMMAND_MODULES) | set(FALLBACK_PERMS))
LOCKED_KEYS = ("case_counter",)


def parse_item(raw):
    m = re.fullmatch(r"<[#@&!]*(\d+)>", raw.strip())
    if m:
        return int(m.group(1))
    return int(raw) if raw.strip().isdigit() else raw.strip()


def parse_value(raw, current):
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
    parts = path.split(".")
    for p in parts[:-1]:
        d = d[p]
    return d, parts[-1]


class Admin(commands.Cog):
    module = app_commands.Group(name="module", description="Turn features on or off", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    command = app_commands.Group(name="command", description="Turn single commands on or off", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    alias = app_commands.Group(name="alias", description="Prefix command aliases", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    perms = app_commands.Group(name="perms", description="Who may use which command", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)
    config = app_commands.Group(name="config", description="Read and change any setting", default_permissions=discord.Permissions(administrator=True), guild_only=True)

    def __init__(self, bot):
        self.bot = bot

    @module.command(name="list", description="Show all modules")
    async def m_list(self, it: discord.Interaction):
        mods = self.bot.cfg(it.guild_id)["modules"]
        await it.response.send_message("\n".join(f"{k}: {'on' if v else 'off'}" for k, v in mods.items()), ephemeral=True)

    @module.command(name="enable", description="Turn a module on")
    async def m_enable(self, it: discord.Interaction, name: Literal[tuple(MODULES)]):
        self.bot.cfg(it.guild_id)["modules"][name] = True
        self.bot.store.mark("config")
        await it.response.send_message(f"{name}: on", ephemeral=True)

    @module.command(name="disable", description="Turn a module off")
    async def m_disable(self, it: discord.Interaction, name: Literal[tuple(MODULES)]):
        self.bot.cfg(it.guild_id)["modules"][name] = False
        self.bot.store.mark("config")
        await it.response.send_message(f"{name}: off", ephemeral=True)

    @command.command(name="disable", description="Turn one command off")
    async def c_disable(self, it: discord.Interaction, name: str):
        name = self.bot.canonical.get(name.lower(), name.lower())
        if name in PROTECTED_COMMANDS:
            return await it.response.send_message("That command cannot be disabled.", ephemeral=True)
        lst = self.bot.cfg(it.guild_id)["disabled_commands"]
        if name not in lst:
            lst.append(name)
        self.bot.store.mark("config")
        await it.response.send_message(f"{name} is disabled.", ephemeral=True)

    @command.command(name="enable", description="Turn one command on again")
    async def c_enable(self, it: discord.Interaction, name: str):
        name = self.bot.canonical.get(name.lower(), name.lower())
        lst = self.bot.cfg(it.guild_id)["disabled_commands"]
        if name in lst:
            lst.remove(name)
        self.bot.store.mark("config")
        await it.response.send_message(f"{name} is enabled.", ephemeral=True)

    @command.command(name="list", description="Show disabled commands")
    async def c_list(self, it: discord.Interaction):
        lst = self.bot.cfg(it.guild_id)["disabled_commands"]
        await it.response.send_message(", ".join(lst) or "No commands are disabled.", ephemeral=True)

    @app_commands.command(name="prefix", description="Change the prefix for text commands")
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def prefix_cmd(self, it: discord.Interaction, new_prefix: app_commands.Range[str, 1, 5]):
        self.bot.cfg(it.guild_id)["prefix"] = new_prefix
        self.bot.store.mark("config")
        await it.response.send_message(f"The prefix is now {new_prefix}", ephemeral=True)

    @alias.command(name="add", description="Create a short name for a prefix command")
    async def a_add(self, it: discord.Interaction, alias: str, command: str):
        command = self.bot.canonical.get(command.lower(), command.lower())
        if self.bot.get_command(command) is None and command not in self.bot.canonical.values():
            return await it.response.send_message("Unknown command.", ephemeral=True)
        self.bot.cfg(it.guild_id)["aliases"][alias.lower()] = command
        self.bot.store.mark("config")
        await it.response.send_message(f"{self.bot.prefix_for(it.guild_id)}{alias.lower()} now runs {command}.", ephemeral=True)

    @alias.command(name="remove", description="Delete an alias")
    async def a_remove(self, it: discord.Interaction, alias: str):
        if self.bot.cfg(it.guild_id)["aliases"].pop(alias.lower(), None) is None:
            return await it.response.send_message("No such alias.", ephemeral=True)
        self.bot.store.mark("config")
        await it.response.send_message("Removed.", ephemeral=True)

    @alias.command(name="list", description="Show aliases")
    async def a_list(self, it: discord.Interaction):
        al = self.bot.cfg(it.guild_id)["aliases"]
        await it.response.send_message("\n".join(f"{k} -> {v}" for k, v in al.items()) or "No aliases.", ephemeral=True)

    def rule(self, gid, command):
        return self.bot.cfg(gid)["perms"].setdefault(command, {"roles": [], "users": [], "deny_roles": [], "deny_users": []})

    @perms.command(name="allow", description="Only these roles or users may use a command")
    async def p_allow(self, it: discord.Interaction, command: str, target: Union[discord.Member, discord.Role]):
        command = self.bot.canonical.get(command.lower(), command.lower())
        r = self.rule(it.guild_id, command)
        key = "roles" if isinstance(target, discord.Role) else "users"
        if target.id not in r[key]:
            r[key].append(target.id)
        self.bot.store.mark("config")
        await it.response.send_message(f"{target.mention} may use {command}.", ephemeral=True)

    @perms.command(name="deny", description="Block a role or user from a command")
    async def p_deny(self, it: discord.Interaction, command: str, target: Union[discord.Member, discord.Role]):
        command = self.bot.canonical.get(command.lower(), command.lower())
        r = self.rule(it.guild_id, command)
        key = "deny_roles" if isinstance(target, discord.Role) else "deny_users"
        if target.id not in r[key]:
            r[key].append(target.id)
        self.bot.store.mark("config")
        await it.response.send_message(f"{target.mention} cannot use {command}.", ephemeral=True)

    @perms.command(name="reset", description="Back to the default permission of a command")
    async def p_reset(self, it: discord.Interaction, command: str):
        self.bot.cfg(it.guild_id)["perms"].pop(self.bot.canonical.get(command.lower(), command.lower()), None)
        self.bot.store.mark("config")
        await it.response.send_message("Reset.", ephemeral=True)

    @perms.command(name="show", description="Show permission rules")
    async def p_show(self, it: discord.Interaction, command: Optional[str] = None):
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
        try:
            d, key = walk(self.bot.cfg(it.guild_id), path)
            value = d[key]
        except (KeyError, TypeError):
            return await it.response.send_message("Unknown setting.", ephemeral=True)
        await it.response.send_message(f"```json\n{trim(json.dumps(value, indent=1, ensure_ascii=False), 1800)}\n```", ephemeral=True)

    @config.command(name="set", description="Change a setting. Lists use commas, IDs or mentions are accepted")
    async def cfg_set(self, it: discord.Interaction, path: str, value: str):
        if path.split(".")[0] in LOCKED_KEYS:
            return await it.response.send_message("That setting cannot be changed.", ephemeral=True)
        try:
            d, key = walk(self.bot.cfg(it.guild_id), path)
            current = d[key]
            if isinstance(current, dict):
                return await it.response.send_message("That is a group of settings. Pick one inside it.", ephemeral=True)
            d[key] = parse_value(value, current)
        except (KeyError, TypeError, ValueError):
            return await it.response.send_message("Unknown setting or invalid value.", ephemeral=True)
        self.bot.store.mark("config")
        await it.response.send_message(f"{path} = {d[key]}", ephemeral=True)

    @config.command(name="reset", description="Reset a setting group to its default, for example welcome")
    async def cfg_reset(self, it: discord.Interaction, section: str):
        if section not in DEFAULTS or section in LOCKED_KEYS:
            return await it.response.send_message("Unknown section.", ephemeral=True)
        import copy
        self.bot.cfg(it.guild_id)[section] = copy.deepcopy(DEFAULTS[section])
        self.bot.store.mark("config")
        await it.response.send_message(f"{section} reset.", ephemeral=True)

    @app_commands.command(name="settings", description="Overview of the current configuration")
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def settings_cmd(self, it: discord.Interaction):
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
        e = emb("GuardBot", f"Open source Discord moderation and community bot.\nVersion {__version__}\nMade in Germany\n\nBugs, ideas and suggestions: Discord @justyyin")
        await it.response.send_message(embed=e, ephemeral=True)

    @commands.hybrid_command(name="help", description="List the available commands")
    async def help_cmd(self, ctx):
        prefix = self.bot.prefix_for(ctx.guild.id)
        by_module = {}
        for cmd, mod in COMMAND_MODULES.items():
            by_module.setdefault(mod, []).append(cmd)
        e = emb("Commands", f"Slash commands and prefix commands ({prefix}) are available. Use / to browse all options.")
        for mod, cmds in by_module.items():
            state = "" if self.bot.module_on(ctx.guild.id, mod) else " (off)"
            e.add_field(name=f"{mod}{state}", value=" ".join(f"`{c}`" for c in cmds), inline=False)
        e.add_field(name="Admin", value=" ".join(f"`{c}`" for c in PROTECTED_COMMANDS), inline=False)
        await ctx.send(embed=e, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Admin(bot))
