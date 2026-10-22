"""Load tests for the scan path and the OCR queue, plus the new probation, swarm, timeline and learning helpers."""

import asyncio
import copy
import time
import unittest
from types import SimpleNamespace
from unittest import mock

from guardbot import scamscan, swarm
from guardbot.cogs import antiscam
from guardbot.cogs.moderation import build_timeline
from guardbot.cogs.probation import due, has_link, is_harmless
from guardbot.defaults import DEFAULTS
from guardbot.scamscan import text_key


class FakeBot:
    """Just enough of the bot for the anti-scam cog."""

    def __init__(self):
        """One server configuration, no AutoMod cog."""
        self.config = copy.deepcopy(DEFAULTS)
        self.settings = {}
        self.bot_deleted = set()
        self.tree = SimpleNamespace()
        self.acted = []

    def cfg(self, gid):
        """Settings of the server."""
        return self.config

    def module_on(self, gid, name):
        """All modules are on."""
        return True

    def get_cog(self, name):
        """No other cogs."""
        return None


class Attachment:
    """A fake image attachment with fixed bytes."""

    def __init__(self, data, name="a.png"):
        """Store the bytes."""
        self.data, self.filename, self.content_type, self.size = data, name, "image/png", len(data)

    async def read(self):
        """Return the bytes."""
        return self.data


class Message:
    """A fake message that counts deletions."""

    def __init__(self, text, attachments=(), n=0):
        """Build a message from a plain member."""
        self.content, self.attachments, self.embeds, self.id = text, list(attachments), [], n
        self.author = SimpleNamespace(bot=False, id=n, mention="x")
        self.guild = SimpleNamespace(id=1)
        self.deleted = False

    async def delete(self):
        """Mark as deleted."""
        self.deleted = True


def make_cog():
    """An AntiScam cog on a fake bot."""
    cog = antiscam.AntiScam(FakeBot())
    return cog


class LoadTest(unittest.IsolatedAsyncioTestCase):
    """A thousand messages in a minute must be cheap and the OCR queue must stay bounded."""

    async def test_thousand_text_messages(self):
        """1000 mixed messages are scanned far faster than they arrive and only the scams are removed."""
        cog = make_cog()
        msgs = [Message("free btc giveaway claim now" if i % 10 == 0 else f"hello everyone number {i}", n=i) for i in range(1000)]
        start = time.perf_counter()
        for m in msgs:
            await cog.check(m)
        took = time.perf_counter() - start
        self.assertEqual(sum(m.deleted for m in msgs), 100)
        self.assertEqual(cog.conf(1)["hits"], 100)
        self.assertLess(took, 10, "1000 messages must be scanned in far less than the minute they arrive in")

    async def test_ocr_queue_is_bounded(self):
        """A flood of different images never keeps more than MAX_PENDING waiting, the rest is skipped."""
        cog = make_cog()
        c = cog.conf(1)
        peak = 0
        lock = asyncio.Event()

        def slow(data, lang, program):
            """Pretend to be a slow tesseract."""
            time.sleep(0.01)
            return "hello"

        async def watch():
            """Record the highest number of waiting images."""
            nonlocal peak
            while not lock.is_set():
                peak = max(peak, cog.pending)
                await asyncio.sleep(0)

        with mock.patch.object(scamscan, "read_text", slow):
            task = asyncio.create_task(watch())
            results = await asyncio.gather(*[cog.image_bad(Attachment(bytes([i % 256, i // 256]) + b"x" * 20), c) for i in range(300)])
            lock.set()
            await task
        self.assertLessEqual(peak, antiscam.MAX_PENDING)
        self.assertEqual(cog.pending, 0)
        self.assertTrue(all(not bad for bad, _ in results))
        self.assertLessEqual(len(cog.verdicts), 2000)

    async def test_known_image_skips_the_queue(self):
        """An image learned once is removed without reading it, even when the queue is full."""
        cog = make_cog()
        c = cog.conf(1)
        data = b"\x89PNG-scam-image"
        cog.remember(c, scamscan.digest(data), True)
        cog.pending = antiscam.MAX_PENDING
        bad, why = await cog.image_bad(Attachment(data), c)
        self.assertTrue(bad)
        self.assertIn("known", why)

    async def test_learning(self):
        """A marked message teaches the image and the words, and the same text is caught later."""
        cog = make_cog()
        c = cog.conf(1)
        cog.bot.log = lambda *a, **k: None
        mod = SimpleNamespace(mention="m")
        m = Message("some totally new wording about prizes", [Attachment(b"img-bytes-1")], n=5)
        images, text = await cog.learn(m, mod)
        self.assertEqual((images, text), (1, True))
        self.assertTrue(m.deleted)
        self.assertIn(scamscan.digest(b"img-bytes-1"), c["hashes"])
        self.assertIn(text_key(m.content), c["texts"])
        again = Message("Some totally  new wording, about PRIZES", n=6)
        await cog.check(again)
        self.assertEqual(c["hits"], 1)


class ProbationTest(unittest.TestCase):
    """Rules for new members."""

    def test_links(self):
        """Links and invites are found."""
        self.assertTrue(has_link("see https://example.com"))
        self.assertTrue(has_link("join discord.gg/abc"))
        self.assertFalse(has_link("hello there"))

    def test_harmless(self):
        """A first message is harmless when it is text without links or scam words."""
        self.assertTrue(is_harmless("hi, nice to meet you"))
        self.assertFalse(is_harmless("hi"))
        self.assertFalse(is_harmless("look https://example.com"))
        self.assertFalse(is_harmless("free btc giveaway claim now"))

    def test_due(self):
        """The time route ends after the minutes and can be switched off with zero."""
        self.assertTrue(due({"ts": 0}, 10, 601))
        self.assertFalse(due({"ts": 0}, 10, 599))
        self.assertFalse(due({"ts": 0}, 0, 10**9))


class SwarmTest(unittest.TestCase):
    """Raid detection by account patterns."""

    def test_stem(self):
        """Digits, marks and separators do not change the name pattern."""
        self.assertEqual(swarm.stem("Bot_Käse123"), swarm.stem("bot-kase7"))
        self.assertIsNone(swarm.stem("a1"))

    def test_name_group(self):
        """Accounts with the same name pattern are one group."""
        entries = [(i, f"spammer{i}", None, 1000 + i * 100000) for i in range(1, 5)]
        kinds = {k for k, _, _ in swarm.find_groups(entries, 3)}
        self.assertIn("name", kinds)

    def test_avatar_and_batch(self):
        """The same picture and accounts created together are found, unrelated accounts are not."""
        entries = [(1, "alpha", "h1", 100), (2, "bravo", "h1", 200), (3, "charlie", "h1", 300), (4, "delta", None, 10**7)]
        kinds = {k: ids for k, _, ids in swarm.find_groups(entries, 3)}
        self.assertEqual(kinds["avatar"], [1, 2, 3])
        self.assertEqual(kinds["created"], [1, 2, 3])
        self.assertEqual(swarm.find_groups([(1, "alpha", "x", 0), (2, "bravo", "y", 10**6)], 3), [])


class TimelineTest(unittest.TestCase):
    """The merged history of a user."""

    def test_order_and_content(self):
        """Joining, probation, cases and appeals are merged oldest first."""
        cases = [{"id": 3, "type": "warn", "user": 7, "mod": 9, "reason": "spam", "ts": 300, "active": True, "extra": {}}, {"id": 4, "type": "ban", "user": 8, "mod": 9, "reason": "x", "ts": 310, "active": True, "extra": {}}]
        appeals = {"1": {"user": 7, "ts": 400, "status": "open", "text": "please"}}
        events = build_timeline(7, cases, appeals, {"invite": "abc", "invited_by": 5}, joined=200, created=100, probation={"ts": 210, "ok": 1})
        self.assertEqual([e[0] for e in events], [100, 200, 210, 300, 400])
        self.assertIn("abc", events[1][1])
        self.assertTrue(all("Case #4" not in e[1] for e in events))


class MissingTextsTest(unittest.TestCase):
    """Admin replies fall back to English, and the test reports what is missing."""

    CORE = (
        "I cannot assign that role. Move my role above it.", "I cannot post in that channel.", "Case not found.", "Panel posted.",
        "Use this inside a ticket.", "Backup not found.", "You need the Manage Server permission.",
        "{user} Links and files are not allowed yet. Write a normal message first or wait a few minutes.",
    )

    def test_core_texts_are_translated(self):
        """The most common replies exist in all languages."""
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
        import missing_texts

        for lang in ("de", "fr", "es", "pt", "ru", "uk", "sv", "da", "zh", "ja", "ko"):
            gone = missing_texts.missing(lang)
            for text in self.CORE:
                self.assertNotIn(text, gone, f"{lang}: {text}")

    def test_fallback_is_english(self):
        """A text without translation is shown as written."""
        from guardbot import i18n

        self.assertEqual(i18n.tr("de", "A text nobody translated {x}", x=1), "A text nobody translated 1")


if __name__ == "__main__":
    unittest.main()
