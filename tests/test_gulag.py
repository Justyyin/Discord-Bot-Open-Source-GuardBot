"""The gulag notice, the reminder, release requests and roles given by hand."""

import asyncio
import tempfile
import unittest
from types import SimpleNamespace

import discord

from guardbot.cogs.moderation import jail as J
from guardbot.core import EXTENSIONS, Bot


class Chan:
    """A gulag channel that records what is sent and deleted."""

    def __init__(self, cid=50):
        self.id, self.sent, self.deleted, self.edited, self.last_message_id, self.next_id = cid, [], [], [], None, 1000

    async def send(self, content=None, **kw):
        self.next_id += 1
        self.last_message_id = self.next_id
        self.sent.append((content, kw))
        return SimpleNamespace(id=self.next_id)

    def get_partial_message(self, mid):
        chan = self

        class Partial:
            async def delete(self):
                chan.deleted.append(mid)

            async def edit(self, **kw):
                chan.edited.append(mid)

        return Partial()


class Role:
    def __init__(self, rid, members=()):
        self.id, self.members, self.mention = rid, list(members), f"<@&{rid}>"

    def __eq__(self, other):
        return getattr(other, "id", None) == self.id

    def __hash__(self):
        return self.id


class GulagTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = Bot({"data_dir": tempfile.mkdtemp()})

        async def never_ready():
            await asyncio.Event().wait()

        self.bot.wait_until_ready = never_ready
        for ext in EXTENSIONS:
            await self.bot.load_extension(f"guardbot.cogs.{ext}")
        self.bot.loop = asyncio.get_running_loop()
        self.cog = self.bot.get_cog("Jail")
        self.chan = Chan()
        self.role, self.staff = Role(60), Role(70)
        self.guild = SimpleNamespace(id=1, icon=None, get_role=lambda rid: {60: self.role, 70: self.staff}.get(rid), get_channel=lambda cid: self.chan if cid == 50 else None)
        j = self.bot.cfg(1)["jail"]
        j.update(role=60, channel=50, staff_role=70)

    async def asyncTearDown(self):
        for cog in list(self.bot.cogs):
            await self.bot.remove_cog(cog)
        await asyncio.sleep(0)
        self.bot.store.close()

    def member(self, uid=5, roles=()):
        return SimpleNamespace(id=uid, bot=False, guild=self.guild, roles=list(roles), mention=f"<@{uid}>",
                               guild_permissions=discord.Permissions.none())

    def test_notice_looks_like_the_template(self):
        e = J.notice_embed(70)
        self.assertEqual(e.title, "\U0001F510 Account Security Required")
        self.assertTrue(e.description.startswith("To get out of this channel, you need to secure your Discord account first.\n\n"))
        self.assertIn("ping a member who has the <@&70> role so a staff member can remove you from the gulag.", e.description)
        self.assertEqual([f.name for f in e.fields], ["1\ufe0f\u20e3 Reset Your Password", "2\ufe0f\u20e3 Enable 2FA", "3\ufe0f\u20e3 Check Suspicious Devices",
                                                     "4\ufe0f\u20e3 Remove Suspicious Authorized Apps", "5\ufe0f\u20e3 Clear Browser Data", "6\ufe0f\u20e3 Ping Staff"])
        self.assertIn("**Two-Factor Authentication**", e.fields[1].value)
        self.assertIn("**User Settings** → **Authorized Apps**", e.fields[3].value)
        self.assertIn('**"join servers for you"**', e.fields[3].value)
        self.assertIn("<@&70> role in this channel.", e.fields[5].value)
        self.assertEqual(e.footer.text, "Account Safety Check")
        self.assertEqual(e.colour, discord.Color.red())
        self.assertIsNotNone(e.timestamp)

    def test_reminder_looks_like_the_template(self):
        e = J.reminder_embed("$unban", 10)
        self.assertEqual(e.title, "\U0001F510 Account Recovery Reminder")
        self.assertEqual(e.description, "If you've been hacked previously and want to get out of here, please run:\n```\n$unban\n```")
        self.assertEqual(e.footer.text, "This reminder refreshes every 10 minutes.")

    def test_notice_is_translated(self):
        self.bot.cfg(1)["language"] = "de"
        e = J.notice_embed(70, tr=self.cog.tr(self.guild))
        self.assertNotIn("Account Security Required", e.title)
        self.assertIn("<@&70>", e.description)

    async def test_notice_with_mention_for_everyone_who_gets_the_role(self):
        before, after = self.member(), self.member(roles=[self.role])
        await self.cog.on_member_update(before, after)
        content, kw = self.chan.sent[-1]
        self.assertEqual(content, "<@5>")
        self.assertEqual(kw["embed"].title, "\U0001F510 Account Security Required")
        self.assertTrue(self.bot.store.users(1)["5"]["jailed"])
        await self.cog.on_member_update(after, before)
        self.assertFalse(self.bot.store.users(1)["5"]["jailed"])
        self.assertEqual(len(self.chan.sent), 1)

    async def test_own_role_changes_do_not_post_twice(self):
        before, after = self.member(), self.member(roles=[self.role])
        self.cog.mark_own(after)
        await self.cog.on_member_update(before, after)
        self.assertEqual(self.chan.sent, [])

    async def test_notice_can_be_switched_off(self):
        self.bot.cfg(1)["jail"]["security_notice"] = False
        await self.cog.on_member_update(self.member(), self.member(roles=[self.role]))
        self.assertEqual(self.chan.sent, [])

    def message(self, text, member):
        return SimpleNamespace(author=member, guild=self.guild, channel=self.chan, content=text, reply=self.noop, _state=self.bot._connection)

    async def noop(self, *a, **k):
        self.replied = a

    async def test_release_word_makes_a_request_once(self):
        m = self.member(roles=[self.role])
        prefix = self.bot.prefix_for(1)
        msg = self.message(prefix + "unban", m)
        self.assertTrue(self.cog.claims(msg))
        self.assertFalse(self.cog.claims(self.message(prefix + "unban", self.member(6))))
        self.assertFalse(self.cog.claims(self.message(prefix + "unban someone", m)))
        await self.cog.on_message(msg)
        content, kw = self.chan.sent[-1]
        self.assertEqual(content, "<@&70>")
        self.assertIn("<@5>", kw["embed"].description)
        self.assertEqual(len(kw["view"].children), 2)
        await self.cog.on_message(msg)
        self.assertEqual(len(self.chan.sent), 1)

    async def test_request_is_hidden_from_the_command_handler(self):
        m = self.member(roles=[self.role])
        msg = self.message(self.bot.prefix_for(1) + "unban", m)
        other = self.message(self.bot.prefix_for(1) + "unban 123", m)
        seen = []

        async def fake(bot, message, *, cls=None):
            seen.append(message.content)

        from unittest import mock
        from discord.ext import commands
        with mock.patch.object(commands.bot.BotBase, "get_context", fake):
            await self.bot.get_context(msg)
            await self.bot.get_context(other)
        self.assertEqual(seen, ["", other.content])
        self.assertEqual(msg.content, self.bot.prefix_for(1) + "unban")

    async def test_reminder_follows_the_gulag(self):
        await self.cog.refresh_reminder(self.guild, 0)
        self.assertEqual(self.chan.sent, [])
        self.role.members = [self.member(roles=[self.role])]
        await self.cog.refresh_reminder(self.guild, 1000)
        self.assertEqual(len(self.chan.sent), 1)
        first = self.bot.cfg(1)["jail"]["reminder_message"]
        await self.cog.refresh_reminder(self.guild, 1100)
        self.assertEqual(len(self.chan.sent), 1)
        await self.cog.refresh_reminder(self.guild, 1700)
        self.assertEqual(self.chan.edited, [first])
        await self.chan.send("someone wrote")
        await self.cog.refresh_reminder(self.guild, 2400)
        self.assertEqual(self.chan.deleted, [first])
        self.assertEqual(len(self.chan.sent), 3)
        self.role.members = []
        await self.cog.refresh_reminder(self.guild, 2500)
        self.assertIsNone(self.bot.cfg(1)["jail"]["reminder_message"])


if __name__ == "__main__":
    unittest.main()
