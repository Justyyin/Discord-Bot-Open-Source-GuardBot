"""Command layout: few group commands, original names kept for permissions, and the limits of Discord."""

import asyncio
import json
import tempfile
import unittest
from types import SimpleNamespace

import discord
from discord import app_commands

from guardbot import layout
from guardbot.core import EXTENSIONS, Bot
from guardbot.defaults import COMMAND_MODULES, FALLBACK_PERMS


def payload_size(node):
    """Characters of names, descriptions and values in a command payload, the way Discord counts them."""
    total = 0
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("name", "description", "value") and isinstance(value, (str, int)) and not isinstance(value, bool):
                total += len(str(value))
            elif isinstance(value, (dict, list)):
                total += payload_size(value)
    elif isinstance(node, list):
        total += sum(payload_size(x) for x in node)
    return total


class LayoutTest(unittest.IsolatedAsyncioTestCase):
    """The bot with all cogs, arranged into groups."""

    async def asyncSetUp(self):
        """Load every cog and arrange the commands."""
        self.bot = Bot({"data_dir": tempfile.mkdtemp()})

        async def never_ready():
            await asyncio.Event().wait()

        self.bot.wait_until_ready = never_ready
        for ext in EXTENSIONS:
            await self.bot.load_extension(f"guardbot.cogs.{ext}")
        self.before = layout.all_keys(self.bot.tree)
        self.bot.arrange_commands()
        self.roots = self.bot.tree.get_commands(type=discord.AppCommandType.chat_input)

    async def asyncTearDown(self):
        """Unload everything."""
        for cog in list(self.bot.cogs):
            await self.bot.remove_cog(cog)
        await asyncio.sleep(0)
        self.bot.store.close()

    async def test_few_roots(self):
        """The number of top-level slash commands is small and far below the limit."""
        self.assertLessEqual(len(self.roots), 25, sorted(c.name for c in self.roots))

    async def test_nothing_was_lost(self):
        """Every command that existed before is still there under its original key."""
        self.assertEqual(layout.all_keys(self.bot.tree), self.before)
        for original in (n for _, (_, members) in layout.GROUPS.items() for n in members):
            self.assertIn(original, self.bot.layout, original)

    async def test_limits_of_discord(self):
        """Every root has at most 25 children, is nested at most three levels and stays far below the size limit."""
        for root in self.roots:
            data = root.to_dict(self.bot.tree)
            self.assertLessEqual(payload_size(data), 3700, f"/{root.name} is too large")
            if isinstance(root, app_commands.Group):
                self.assertLessEqual(len(root.commands), 25, root.name)
                for child in root.commands:
                    if isinstance(child, app_commands.Group):
                        self.assertFalse(any(isinstance(x, app_commands.Group) for x in child.commands), f"{root.name} {child.name} is nested too deep")
        json.dumps([c.to_dict(self.bot.tree) for c in self.bot.tree.get_commands()], default=str)

    async def test_keys_keep_permissions_working(self):
        """A moved command still maps to its original name, so module switches, permissions and the disable list keep working."""
        group = self.bot.tree.get_command("moderation")
        self.assertEqual(layout.command_key(group.get_command("ban")), "ban")
        self.assertEqual(layout.command_key(group.get_command("case").get_command("link")), "case")
        self.assertEqual(layout.command_key(self.bot.tree.get_command("security").get_command("raid").get_command("setup")), "raid")
        self.assertEqual(layout.command_key(self.bot.tree.get_command("music")), "music")
        for key in layout.all_keys(self.bot.tree):
            if key in COMMAND_MODULES or key in FALLBACK_PERMS:
                continue
            self.assertNotIn(key, ("ban", "kick", "warn"), key)

    async def test_interaction_check_uses_the_original_name(self):
        """The slash command check applies the rules of /ban to /moderation ban."""
        messages = []

        async def send_message(text, ephemeral=False):
            """Remember what the user is told."""
            messages.append(text)

        member = SimpleNamespace(id=5, roles=[], guild=SimpleNamespace(owner_id=1, id=1), guild_permissions=SimpleNamespace(ban_members=False))
        guild = SimpleNamespace(id=1, owner_id=1)
        cmd = self.bot.tree.get_command("moderation").get_command("ban")
        interaction = SimpleNamespace(command=cmd, guild=guild, user=member, client=self.bot, response=SimpleNamespace(send_message=send_message))
        self.assertFalse(await self.bot.tree.interaction_check(interaction))
        self.assertEqual(len(messages), 1)
        member.guild_permissions.ban_members = True
        self.assertTrue(await self.bot.tree.interaction_check(interaction))
        self.bot.cfg(1)["disabled_commands"].append("ban")
        self.assertFalse(await self.bot.tree.interaction_check(interaction))

    async def test_help_finds_old_and_new_names(self):
        """/help understands the original name and the grouped path."""
        admin = self.bot.get_cog("Admin")
        for words in (["ban"], ["moderation", "ban"]):
            self.assertEqual(admin.find_command(words).qualified_name, "moderation ban")
        self.assertEqual(admin.find_command(["raid", "setup"]).qualified_name, "security raid setup")
        self.assertEqual(layout.slash_path(self.bot, "ban"), "moderation ban")
        self.assertEqual(layout.slash_path(self.bot, "music"), "music")


if __name__ == "__main__":
    unittest.main()
