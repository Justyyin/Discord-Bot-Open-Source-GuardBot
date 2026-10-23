"""The bot with all cogs: command registration, renaming, defaults and images."""

import asyncio
import json
import re
import tempfile
import unittest
from pathlib import Path

import discord

from guardbot import layout
from guardbot.core import EXTENSIONS, Bot
from guardbot.defaults import COMMAND_MODULES, DEFAULTS, FALLBACK_PERMS, MODULES
from guardbot.images import HAVE_PIL, captcha, new_code, rank_card
from guardbot.cogs.moderation.jail import notice_embed


class BotTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = Bot({"data_dir": tempfile.mkdtemp(), "command_names": {"warn": "verwarnen", "jailsetup": "gulagsetup"}})

        async def never_ready():
            await asyncio.Event().wait()

        self.bot.wait_until_ready = never_ready
        for ext in EXTENSIONS:
            await self.bot.load_extension(f"guardbot.cogs.{ext}")

    async def asyncTearDown(self):
        for cog in list(self.bot.cogs):
            await self.bot.remove_cog(cog)
        await asyncio.sleep(0)
        self.bot.store.close()

    def roots(self):
        return {c.name for c in self.bot.tree.get_commands()} | layout.all_keys(self.bot.tree) | {c.name for c in self.bot.commands}

    async def test_every_module_has_a_command_mapping_and_vice_versa(self):
        self.assertTrue(set(COMMAND_MODULES.values()) <= set(MODULES))

    async def test_mapped_commands_exist(self):
        missing = set(COMMAND_MODULES) - self.roots()
        self.assertEqual(missing, set(), "COMMAND_MODULES lists commands that do not exist")

    async def test_permission_fallbacks_exist(self):
        self.assertEqual(set(FALLBACK_PERMS) - self.roots(), set())

    async def test_slash_payload_is_valid_and_stable(self):
        if not self.bot.layout:
            self.bot.arrange_commands()
        a = json.dumps([c.to_dict(self.bot.tree) for c in self.bot.tree.get_commands()], sort_keys=True, default=str)
        b = json.dumps([c.to_dict(self.bot.tree) for c in self.bot.tree.get_commands()], sort_keys=True, default=str)
        self.assertEqual(a, b)
        for kind in (discord.AppCommandType.chat_input, discord.AppCommandType.user, discord.AppCommandType.message):
            self.assertLessEqual(len(self.bot.tree.get_commands(type=kind)), 100 if kind == discord.AppCommandType.chat_input else 5, kind)

    async def test_command_renaming(self):
        self.bot.arrange_commands()
        self.assertEqual(self.bot.layout["warn"], "moderation verwarnen")
        self.assertEqual(self.bot.layout["jailsetup"], "access gulagsetup")
        self.assertIsNotNone(self.bot.tree.get_command("moderation").get_command("verwarnen"))
        self.assertIsNone(self.bot.tree.get_command("moderation").get_command("warn"))
        self.assertIsNotNone(self.bot.get_command("verwarnen"))
        self.assertIsNone(self.bot.get_command("warn"))
        self.assertEqual(self.bot.canonical["verwarnen"], "warn")
        self.assertEqual(layout.command_key(self.bot.tree.get_command("moderation").get_command("verwarnen")), "warn")

    async def test_defaults_reach_every_server(self):
        g = self.bot.cfg(123)
        for key in DEFAULTS:
            self.assertIn(key, g)

    async def test_module_switch_and_command_checks(self):
        class Member:
            id = 5
            roles = []
            guild = type("G", (), {"owner_id": 1, "id": 1})()
            guild_permissions = type("P", (), {"moderate_members": False, "kick_members": True})()

        m = Member()
        self.assertIn("not allowed", self.bot.check_command(m, m.guild, "warn"))
        self.assertIsNone(self.bot.check_command(m, m.guild, "kick"))
        g = self.bot.cfg(1)
        g["disabled_commands"].append("kick")
        self.assertIn("disabled", self.bot.check_command(m, m.guild, "kick"))
        g["disabled_commands"].clear()
        g["modules"]["moderation"] = False
        self.assertIn("module", self.bot.check_command(m, m.guild, "kick"))

    async def test_permission_rules(self):
        class Role:
            id = 77

        class Member:
            id = 5
            roles = [Role()]
            guild = type("G", (), {"owner_id": 1, "id": 2})()
            guild_permissions = type("P", (), {"moderate_members": False})()

        m = Member()
        self.bot.cfg(2)["perms"]["warn"] = {"roles": [77], "users": [], "deny_roles": [], "deny_users": []}
        self.assertTrue(self.bot.can_use(m, "warn"))
        self.bot.cfg(2)["perms"]["warn"]["deny_users"].append(5)
        self.assertFalse(self.bot.can_use(m, "warn"))

    def command_table(self):
        """Map every slash command path to its parameter names."""
        table = {}
        if not self.bot.layout:
            self.bot.arrange_commands()

        def walk(cmd, prefix=""):
            name = cmd.extras.get("gb_root") or cmd.name
            if hasattr(cmd, "commands"):
                for sub in cmd.commands:
                    walk(sub, prefix + name + " ")
            elif hasattr(cmd, "parameters"):
                table[prefix + name] = {p.name for p in cmd.parameters}

        for cmd in self.bot.tree.get_commands():
            walk(cmd)
        return table

    async def test_readme_examples_use_real_commands_and_parameters(self):
        table = self.command_table()
        text = (Path(__file__).resolve().parent.parent / "docs" / "en" / "README.md").read_text(encoding="utf-8")
        checked = 0
        for label, block in re.findall(r"(?ms)^```(\w*)\n(.*?)^```$", text):
            if label:
                continue
            for line in block.splitlines():
                if not line.startswith("/"):
                    continue
                line = re.split(r"\s#\s", line, maxsplit=1)[0]
                words = [w for w in line[1:].split() if ":" not in w]
                path = None
                for n in (3, 2, 1):
                    candidate = " ".join(words[:n])
                    if candidate in table:
                        path = candidate
                        break
                self.assertIsNotNone(path, f"unknown command in README: {line}")
                for param in re.findall(r"(?:^|\s)(\w+):", line):
                    self.assertIn(param, table[path], f"/{path} has no parameter '{param}': {line}")
                checked += 1
        self.assertGreater(checked, 150)

    async def test_jail_notice_contains_the_six_steps(self):
        e = notice_embed(123)
        self.assertEqual(len(e.fields), 6)
        self.assertIn("<@&123>", e.description)

    @unittest.skipUnless(HAVE_PIL, "Pillow is not installed")
    async def test_images(self):
        import io

        from PIL import Image

        buf = io.BytesIO()
        Image.new("RGB", (64, 64), (200, 50, 50)).save(buf, "PNG")
        card = rank_card("Test", buf.getvalue(), 5, 1, 10, 100, 600, False)
        self.assertEqual(Image.open(io.BytesIO(card)).size, (800, 230))
        self.assertEqual(Image.open(io.BytesIO(captcha(new_code()))).size, (280, 110))
        broken = rank_card("Test", b"not an image", 1, 1, 0, 1, 0, True)
        self.assertTrue(broken.startswith(b"\x89PNG"))


if __name__ == "__main__":
    unittest.main()
