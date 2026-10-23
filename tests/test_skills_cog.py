"""Tests for the skills cog with real discord.py objects and a fake channel."""

import asyncio
import tempfile
import unittest
from types import SimpleNamespace

from guardbot.core import EXTENSIONS, Bot
from tests.test_objects import ADMIN, EVERYONE, MOD, make_guild


class Chan:
    def __init__(self):
        self.sent = []
        self.id = 5
        self.mention = "#general"

    async def send(self, content=None, **kw):
        self.sent.append(content)


class SkillsCogTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = Bot({"data_dir": tempfile.mkdtemp()})

        async def never_ready():
            await asyncio.Event().wait()

        self.bot.wait_until_ready = never_ready
        for ext in EXTENSIONS:
            await self.bot.load_extension(f"guardbot.cogs.{ext}")
        self.bot.arrange_commands()
        self.bot.loop = asyncio.get_running_loop()
        self.cog = self.bot.get_cog("Skills")
        self.guild = make_guild()
        # a guild whose bot sits above Mod but below Admin
        self.fake = SimpleNamespace(id=1, me=SimpleNamespace(top_role=self.guild.get_role(ADMIN)), get_role=self.guild.get_role, get_channel=self.guild.get_channel, name="Test", member_count=5)

    async def asyncTearDown(self):
        for cog in list(self.bot.cogs):
            await self.bot.remove_cog(cog)
        await asyncio.sleep(0)
        self.bot.store.close()

    def test_dangerous_roles_are_refused(self):
        runner = __import__("guardbot.cogs.tools.skills", fromlist=["Runner"]).Runner(self.cog, self.fake, None, None)
        self.assertIsNone(runner.role(ADMIN))
        self.assertIsNone(runner.role(MOD))
        self.assertIsNone(runner.role(EVERYONE))
        self.assertIsNone(runner.role(999))

    def test_name_clash_with_commands(self):
        self.assertIsNotNone(self.cog.name_error(1, "help"))
        self.assertIsNotNone(self.cog.name_error(1, "ban"))
        self.assertIsNone(self.cog.name_error(1, "hello"))

    async def test_prefix_command_runs(self):
        from guardbot import skills as S
        spec = S.clean({"name": "hi", "kind": "command", "actions": [{"do": "reply", "text": "Hello {arg1}!"}], "cooldown": 0})
        self.cog.items(1)["hi"] = spec
        chan = Chan()
        author = self.guild.get_member(21)
        msg = SimpleNamespace(author=author, guild=self.guild, content=self.bot.prefix_for(1) + "hi there", channel=chan)
        await self.cog.on_message(msg)
        self.assertEqual(chan.sent, ["Hello there!"])
        self.assertEqual(self.cog.conf(1)["meta"]["hi"]["uses"], 1)

    async def test_disabled_module_and_skill(self):
        from guardbot import skills as S
        self.cog.items(1)["hi"] = S.clean({"name": "hi", "kind": "command", "actions": [{"do": "reply", "text": "x"}], "cooldown": 0})
        chan = Chan()
        author = self.guild.get_member(21)
        msg = SimpleNamespace(author=author, guild=self.guild, content=self.bot.prefix_for(1) + "hi", channel=chan)
        self.bot.cfg(1)["modules"]["skills"] = False
        await self.cog.on_message(msg)
        self.bot.cfg(1)["modules"]["skills"] = True
        self.cog.items(1)["hi"]["enabled"] = False
        await self.cog.on_message(msg)
        self.assertEqual(chan.sent, [])

    async def test_message_trigger_and_cooldown(self):
        from guardbot import skills as S
        self.cog.items(1)["greet"] = S.clean({"name": "greet", "kind": "automation", "cooldown": 30, "trigger": {"event": "message_contains", "words": ["hello"]}, "actions": [{"do": "reply", "text": "hi {user_name}"}]})
        chan = Chan()
        author = self.guild.get_member(21)
        msg = SimpleNamespace(author=author, guild=self.guild, content="well hello all", channel=chan)
        await self.cog.on_message(msg)
        await self.cog.on_message(msg)
        self.assertEqual(len(chan.sent), 1)

    async def test_personal_counters_follow_the_privacy_tools(self):
        from guardbot import skills as S
        S.Vars(self.cog.conf(1)["vars"]).put("points", "user", 21, 5)
        privacy = self.bot.get_cog("Privacy")
        self.assertEqual(privacy.export(1, 21)["skill_counters"], {"points": 5})
        privacy.forget(1, 21)
        self.assertNotIn("21", self.cog.conf(1)["vars"]["users"])
        self.assertEqual(privacy.export(1, 21)["skill_counters"], {})


if __name__ == "__main__":
    unittest.main()
