"""Command layout: gathers the many single slash commands under a few group commands, so the 100 command limit of Discord is no problem.

Text commands such as !ban keep their names. Permissions, module switches, aliases and the disable list keep using the original name of a command, which is stored on the command as extras["gb_root"].
"""

import logging

import discord
from discord import app_commands

log = logging.getLogger(__name__)

# group name: (description, original root commands that move into it)
GROUPS = {
    "moderation": ("Warnings, punishments, cases and cleanup", [
        "warn", "unwarn", "warnings", "clearwarns", "note", "mute", "unmute", "kick", "ban", "unban", "tempban", "jail", "unjail", "jailed",
        "role", "case", "cases", "bulk", "escalation", "purge", "slowmode",
    ]),
    "security": ("Protection against raids, scams and nukes", ["antinuke", "antiscam", "raid", "block", "unblock", "blocklist", "approval"]),
    "access": ("New members, verification and lockdown", ["verify", "probation", "lockdown", "lockdownconfig", "unlock", "lockchannel", "unlockchannel", "jailsetup"]),
    "server": ("Logs, backups, statistics and server information", ["log", "backup", "privacy", "invites", "stats", "serverinfo", "roleinfo", "health", "diagnose", "debug"]),
    "admin": ("Settings, modules, permissions and setup of the bot", ["settings", "config", "module", "command", "perms", "alias", "prefix", "language", "setup", "history", "exceptions", "dashaccess"]),
    "info": ("Information about you, members and the bot", ["about", "avatar", "botinfo", "ping", "userinfo", "mydata", "leaderboard", "rank", "find"]),
    "community": ("Welcome, boosters, reminders, statistics and voice rooms", ["welcome", "booster", "afk", "remind", "activity", "tempvoice", "voice"]),
    "engage": ("Economy, giveaways, polls, counting and starboard", ["economy", "giveaway", "poll", "counting", "starboard"]),
    "support": ("Tickets, suggestions, tags and automatic replies", ["ticket", "suggest", "tag", "autoresponder"]),
    "members": ("Returning members, names, watch list and reason templates", ["stickyroles", "nickname", "watch", "reason"]),
    "structure": ("Channels, categories, archive, timed roles, role templates and rules", ["channel", "category", "archive", "temprole", "roletemplate", "rules"]),
    "team": ("Statistics, weekly report, duty roster and applications", ["teamstats", "weekly", "duty", "apply", "modwatch", "permaudit"]),
    "post": ("Messages, scheduled posts, feeds and role menus", ["say", "embed", "message", "sticky", "schedule", "feed", "reactionrole", "rolemenu"]),
}


def command_key(cmd):
    """The original root name of a slash command, the key for permissions, module switches and the disable list."""
    node = cmd
    while node is not None:
        key = (getattr(node, "extras", None) or {}).get("gb_root")
        if key:
            return key
        node = getattr(node, "parent", None)
    root = getattr(cmd, "root_parent", None)
    return root.name if root is not None else cmd.name


def apply(bot):
    """Move the listed commands into their groups. Call it once, after all cogs are loaded and renames are applied."""
    renamed = {old: new for new, old in bot.canonical.items()}
    bot.layout = {}
    for group_name, (description, members) in GROUPS.items():
        group = app_commands.Group(name=group_name, description=description, guild_only=True)
        group.extras["gb_container"] = True
        for original in members:
            current = renamed.get(original, original)
            cmd = bot.tree.get_command(current, type=discord.AppCommandType.chat_input)
            if cmd is None:
                log.warning("command layout: /%s does not exist, skipped", current)
                continue
            bot.tree.remove_command(current, type=discord.AppCommandType.chat_input)
            cmd.extras["gb_root"] = original
            group.add_command(cmd)
            bot.layout[original] = f"{group_name} {cmd.name}"
        if group.commands:
            bot.tree.add_command(group)


def all_keys(tree):
    """Every original command name that is currently registered as a slash command."""
    keys = set()
    for root in tree.get_commands(type=discord.AppCommandType.chat_input):
        if (getattr(root, "extras", None) or {}).get("gb_container"):
            keys.update(command_key(c) for c in root.commands)
        else:
            keys.add(command_key(root))
    return keys


def slash_path(bot, original):
    """The words to type after the slash for a command, for example 'moderation ban'."""
    return getattr(bot, "layout", {}).get(original, original)
