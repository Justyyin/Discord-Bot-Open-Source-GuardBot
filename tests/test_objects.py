"""Tests against real discord.py objects (Guild, Role, Member, TextChannel) built from API payloads, without a connection."""

import asyncio
import tempfile
import unittest
from types import SimpleNamespace

import discord
from discord.state import ConnectionState

from guardbot.core import EXTENSIONS, Bot

EVERYONE, MOD, ADMIN = 1, 2, 3
OWNER_ID = 10


def role(rid, name, perms, position):
    return {"id": str(rid), "name": name, "permissions": str(perms), "position": position, "color": 0, "hoist": False, "managed": False, "mentionable": False, "flags": 0}


def member(uid, roles, bot=False):
    return {"user": {"id": str(uid), "username": f"user{uid}", "discriminator": "0", "avatar": None, "global_name": f"User {uid}", "bot": bot},
            "roles": [str(r) for r in roles], "joined_at": "2024-01-01T00:00:00+00:00", "deaf": False, "mute": False, "flags": 0}


def make_guild():
    state = ConnectionState(dispatch=lambda *a, **k: None, handlers={}, hooks={}, http=SimpleNamespace(), intents=discord.Intents.all())
    ban = discord.Permissions(ban_members=True, moderate_members=True).value
    data = {
        "id": "1", "name": "Test", "owner_id": str(OWNER_ID), "afk_timeout": 60, "verification_level": 0, "default_message_notifications": 0,
        "explicit_content_filter": 0, "mfa_level": 0, "premium_tier": 0, "preferred_locale": "en-US", "nsfw_level": 0, "system_channel_flags": 0,
        "features": [], "emojis": [], "stickers": [],
        "roles": [role(EVERYONE, "@everyone", 1024, 0), role(MOD, "Mod", ban, 1), role(ADMIN, "Admin", discord.Permissions(administrator=True).value, 2)],
        "channels": [{"id": "5", "type": 0, "name": "general", "position": 0, "permission_overwrites": [], "nsfw": False}],
        "members": [member(OWNER_ID, []), member(20, [MOD]), member(21, []), member(22, [ADMIN]), member(23, [MOD], bot=True)],
        "member_count": 5, "unavailable": False,
    }
    return discord.Guild(data=data, state=state)


class RealObjectTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = Bot({"data_dir": tempfile.mkdtemp()})

        async def never_ready():
            await asyncio.Event().wait()

        self.bot.wait_until_ready = never_ready
        for ext in EXTENSIONS:
            await self.bot.load_extension(f"guardbot.cogs.{ext}")
        self.bot.arrange_commands()
        self.bot.loop = asyncio.get_running_loop()
        self.guild = make_guild()

    async def asyncTearDown(self):
        for cog in list(self.bot.cogs):
            await self.bot.remove_cog(cog)
        await asyncio.sleep(0)
        self.bot.store.close()

    def test_real_permissions_decide_the_default_access(self):
        mod, plain, admin, owner = (self.guild.get_member(i) for i in (20, 21, 22, OWNER_ID))
        self.assertTrue(self.bot.can_use(mod, "ban"))
        self.assertFalse(self.bot.can_use(plain, "ban"))
        self.assertTrue(self.bot.can_use(admin, "ban"))
        self.assertTrue(self.bot.can_use(owner, "ban"))

    def test_configured_roles_and_denials_override_discord_permissions(self):
        mod, plain = self.guild.get_member(20), self.guild.get_member(21)
        self.bot.cfg(1)["perms"]["ban"] = {"roles": [ADMIN]}
        self.assertFalse(self.bot.can_use(mod, "ban"))
        self.bot.cfg(1)["perms"]["ban"] = {"users": [21]}
        self.assertTrue(self.bot.can_use(plain, "ban"))
        self.bot.cfg(1)["perms"]["ban"] = {"deny_roles": [MOD]}
        self.assertFalse(self.bot.can_use(mod, "ban"))

    def test_roster_uses_real_roles_and_skips_bots(self):
        team = self.bot.get_cog("Team")
        self.bot.cfg(1)["team"]["roster_roles"] = [MOD]
        self.assertEqual({m.id for m in team.roster(self.guild)}, {20})
        self.bot.cfg(1)["team"]["roster_roles"] = [ADMIN]
        team.roster_cache.clear()
        self.assertEqual({m.id for m in team.roster(self.guild)}, {22})

    def test_channel_permissions_follow_the_role_overwrites(self):
        channel = self.guild.get_channel(5)
        plain, mod = self.guild.get_member(21), self.guild.get_member(20)
        self.assertTrue(channel.permissions_for(plain).view_channel)
        self.assertFalse(channel.permissions_for(plain).send_messages)
        self.assertTrue(channel.permissions_for(self.guild.get_member(22)).send_messages)
        self.assertFalse(channel.permissions_for(mod).manage_channels)

    async def test_gated_listener_is_skipped_for_a_real_guild_when_the_module_is_off(self):
        calls = []

        class Probe:
            gate = {"on_message": "automod"}

            async def on_message(self, message):
                calls.append(message)

        probe = Probe()
        message = SimpleNamespace(guild=self.guild)
        self.bot.cfg(1)["modules"]["automod"] = False
        self.assertIsNone(self.bot._schedule_event(probe.on_message, "on_message", message))
        self.bot.cfg(1)["modules"]["automod"] = True
        task = self.bot._schedule_event(probe.on_message, "on_message", message)
        await task
        self.assertEqual(len(calls), 1)

    async def test_event_listeners_log_with_the_server_and_leave_no_context_behind(self):
        from guardbot import logsetup
        seen = []

        class Probe:
            async def on_message(self, message):
                seen.append(dict(logsetup.CONTEXT.get()))

        probe = Probe()
        await self.bot._schedule_event(probe.on_message, "on_message", SimpleNamespace(guild=self.guild))
        self.assertEqual(seen, [{"guild": 1, "command": "on_message"}])
        self.assertEqual(logsetup.CONTEXT.get(), {})


if __name__ == "__main__":
    unittest.main()
