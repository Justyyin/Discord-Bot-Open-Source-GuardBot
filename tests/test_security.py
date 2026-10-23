"""Link safety, settings import, short link and new member checks, moderator limits and the self-test."""

import asyncio
import copy
import json
import tempfile
import unittest
from datetime import timedelta
from types import SimpleNamespace as NS

import discord

from guardbot import configio
from guardbot.cogs.moderation.reports import LINK_RE
from guardbot.core import EXTENSIONS, Bot
from guardbot.defaults import DEFAULTS
from guardbot.linkcheck import Resolver, host_of, is_public


class LinkTest(unittest.IsolatedAsyncioTestCase):
    """The link resolver must never contact private addresses."""

    def test_public_addresses(self):
        """Private, loopback, link-local and metadata addresses are rejected."""
        for bad in ("10.0.0.1", "192.168.1.5", "172.16.0.1", "127.0.0.1", "169.254.169.254", "::1", "0.0.0.0", "not an ip"):
            self.assertFalse(is_public(bad), bad)
        self.assertTrue(is_public("8.8.8.8"))

    def test_host_of(self):
        """The host is lower case and works without a scheme."""
        self.assertEqual(host_of("https://Bit.LY/abc"), "bit.ly")
        self.assertEqual(host_of("bit.ly/abc"), "bit.ly")
        self.assertIsNone(host_of(""))

    async def test_resolver_refuses_unsafe_targets(self):
        """Private literals, other schemes and odd ports are refused before any request is made."""
        r = Resolver(session=object())
        for url in ("http://127.0.0.1/x", "http://169.254.169.254/latest", "http://[::1]/", "ftp://example.com/", "http://example.com:8080/"):
            self.assertIsNone(await r.final_url(url), url)


class ConfigIoTest(unittest.TestCase):
    """Export, validation and import of settings."""

    def cfg(self):
        """A fresh settings dict with some runtime data."""
        c = copy.deepcopy(DEFAULTS)
        c["case_counter"] = 7
        c["polls"]["items"] = {"1": {"q": "x"}}
        c["automod"]["hits"] = {"words": 3}
        c["prefix"] = "?"
        return c

    def test_export_drops_runtime_data(self):
        """Counters, polls and hits are not exported, settings are."""
        out = configio.export_config(self.cfg())["settings"]
        self.assertNotIn("case_counter", out)
        self.assertNotIn("polls", out)
        self.assertNotIn("hits", out["automod"])
        self.assertEqual(out["prefix"], "?")

    def test_default_settings_are_valid(self):
        """The exported defaults pass validation."""
        self.assertEqual(configio.validate(configio.export_config(copy.deepcopy(DEFAULTS))["settings"]), [])

    def test_validation_finds_problems(self):
        """Unknown keys, wrong types and protected commands are reported."""
        bad = {"nonsense": 1, "automod": {"caps": {"percent": "high"}}, "disabled_commands": ["module"], "modules": {"automod": "yes"}}
        text = " | ".join(configio.validate(bad))
        for part in ("unknown setting nonsense", "automod.caps.percent must be a number", "protected commands", "modules.automod must be a bool"):
            self.assertIn(part, text)

    def test_import_keeps_runtime_data(self):
        """Importing replaces settings but keeps counters and running data of the target server."""
        source = self.cfg()
        source["prefix"] = "$"
        payload = configio.export_config(source)
        target = self.cfg()
        target["case_counter"] = 99
        new = configio.apply_import(target, payload)
        self.assertEqual(new["prefix"], "$")
        self.assertEqual(new["case_counter"], 99)
        self.assertEqual(new["polls"]["items"], {"1": {"q": "x"}})

    def test_parse_rejects_foreign_files(self):
        """Files that are too large, not JSON or not from GuardBot are refused."""
        self.assertIsNone(configio.parse(b"x" * (configio.MAX_BYTES + 1))[0])
        self.assertIsNone(configio.parse(b"not json")[0])
        self.assertIsNone(configio.parse(json.dumps({"a": 1}).encode())[0])
        good = json.dumps(configio.export_config(copy.deepcopy(DEFAULTS))).encode()
        payload, problems = configio.parse(good)
        self.assertIsNotNone(payload)
        self.assertEqual(problems, [])

    def test_report_link_pattern(self):
        """Message links are parsed into guild, channel and message."""
        m = LINK_RE.search("https://discord.com/channels/1/2/3")
        self.assertEqual(m.groups(), ("1", "2", "3"))


class FakeResolver:
    """Stands in for the link resolver and returns prepared answers."""

    def __init__(self, answers):
        """Store the prepared answers."""
        self.answers = answers

    async def final_url(self, url, **kwargs):
        """Return the prepared target of a URL, or None."""
        return self.answers.get(url)

    async def close(self):
        """Nothing to close."""


class FakeRole:
    """A role that can be compared by position."""

    def __init__(self, position, managed=False, name="role"):
        """Store the position."""
        self.position, self.managed, self.name = position, managed, name

    def __ge__(self, other):
        """Compare by position."""
        return self.position >= other.position


class BotCase(unittest.IsolatedAsyncioTestCase):
    """Loads the bot with all cogs, like the main tests do."""

    async def asyncSetUp(self):
        """Create the bot."""
        self.bot = Bot({"data_dir": tempfile.mkdtemp()})

        async def never_ready():
            await asyncio.Event().wait()

        self.bot.wait_until_ready = never_ready
        for ext in EXTENSIONS:
            await self.bot.load_extension(f"guardbot.cogs.{ext}")

    async def asyncTearDown(self):
        """Remove the cogs and close the storage."""
        for cog in list(self.bot.cogs):
            await self.bot.remove_cog(cog)
        await asyncio.sleep(0)
        self.bot.store.close()


class AutoModNewChecks(BotCase):
    """Short links, new member links and dry run."""

    async def test_shortlinks(self):
        """A short link is followed and judged by its target."""
        cog = self.bot.get_cog("AutoMod")
        a = self.bot.cfg(1)["automod"]
        a["shortlinks"]["enabled"] = True
        a["phishing"]["list"].append("evil.example")
        cog.resolver = FakeResolver({"https://bit.ly/x": "https://evil.example/login", "https://bit.ly/ok": "https://example.org/"})
        self.assertIn("phishing domain evil.example", await cog.check_shortlinks("look https://bit.ly/x", a))
        self.assertIsNone(await cog.check_shortlinks("look https://bit.ly/ok", a))
        self.assertIn("could not be verified", await cog.check_shortlinks("https://bit.ly/dead", a))
        a["shortlinks"]["block_unresolved"] = False
        self.assertIsNone(await cog.check_shortlinks("https://bit.ly/dead", a))
        a["shortlinks"]["resolve"] = False
        self.assertIn("short link", await cog.check_shortlinks("https://bit.ly/ok", a))
        a["shortlinks"]["enabled"] = False
        self.assertIsNone(await cog.check_shortlinks("https://bit.ly/ok", a))
        self.assertIsNone(await cog.check_shortlinks("https://example.org/", a))

    async def test_new_member_links(self):
        """Members who just joined may not post links, except allowed hosts."""
        cog = self.bot.get_cog("AutoMod")
        a = self.bot.cfg(1)["automod"]
        a["newlinks"].update(enabled=True, hours=24)
        now = discord.utils.utcnow()
        fresh, old = NS(author=NS(joined_at=now - timedelta(hours=1))), NS(author=NS(joined_at=now - timedelta(days=3)))
        self.assertIsNotNone(cog.check_newlinks(fresh, ["example.org"], a))
        self.assertIsNone(cog.check_newlinks(old, ["example.org"], a))
        self.assertIsNone(cog.check_newlinks(fresh, ["tenor.com"], a))
        self.assertIsNone(cog.check_newlinks(fresh, [], a))
        a["newlinks"]["enabled"] = False
        self.assertIsNone(cog.check_newlinks(fresh, ["example.org"], a))

    async def test_dry_run_flags(self):
        """Dry run works per rule and for all rules."""
        cog = self.bot.get_cog("AutoMod")
        self.assertTrue(cog.dry({"dry_run": ["all"]}, "words"))
        self.assertTrue(cog.dry({"dry_run": ["channel_rule"]}, "channel rule"))
        self.assertFalse(cog.dry({"dry_run": ["caps"]}, "words"))
        self.assertFalse(cog.dry({"dry_run": []}, "words"))


class ModWatchTest(BotCase):
    """The moderator limit."""

    async def test_limit_triggers_once_per_window(self):
        """The third ban within the span triggers, excluded and bot users do not."""
        cog = self.bot.get_cog("ModWatch")
        guild = NS(id=5, owner_id=1)
        self.bot.cfg(5)["modules"]["modwatch"] = True
        self.bot.cfg(5)["modwatch"]["limits"]["ban"] = [3, 3600]
        fired = []

        async def fake_trigger(*args):
            """Record the call."""
            fired.append(args[2])

        cog.trigger = fake_trigger
        mod = NS(id=50, bot=False)
        for _ in range(2):
            await cog.count(guild, mod, "ban")
        self.assertEqual(fired, [])
        await cog.count(guild, mod, "ban")
        self.assertEqual(fired, ["ban"])
        self.bot.cfg(5)["modwatch"]["whitelist"].append(51)
        for _ in range(5):
            await cog.count(guild, NS(id=51, bot=False), "ban")
            await cog.count(guild, NS(id=1, bot=False), "ban")
            await cog.count(guild, NS(id=52, bot=True), "ban")
        self.assertEqual(fired, ["ban"])

    async def test_module_off_counts_nothing(self):
        """With the module off nothing is counted."""
        cog = self.bot.get_cog("ModWatch")
        self.bot.cfg(6)["modules"]["modwatch"] = False
        await cog.count(NS(id=6, owner_id=1), NS(id=9, bot=False), "ban")
        self.assertEqual(cog.hits, {})


class DiagnoseTest(BotCase):
    """The checks of the self-test."""

    async def test_role_checks(self):
        """A role above the bot, a managed role and a missing role are reported."""
        cog = self.bot.get_cog("Debug")
        top = FakeRole(5)
        guild = NS(me=NS(top_role=top), get_role=lambda i: {1: FakeRole(9, name="high"), 2: FakeRole(1, True, "bot"), 3: FakeRole(1, name="ok")}.get(i))
        self.assertIn("above my highest role", cog.check_target(guild, "x", 1, "role"))
        self.assertIn("managed", cog.check_target(guild, "x", 2, "role"))
        self.assertIn("no longer exists", cog.check_target(guild, "x", 4, "role"))
        self.assertIsNone(cog.check_target(guild, "x", 3, "role"))
        self.assertIsNone(cog.check_target(guild, "x", 1, "exists"))

    async def test_channel_checks(self):
        """A missing channel and missing permissions are reported."""
        cog = self.bot.get_cog("Debug")
        perms = NS(view_channel=True, send_messages=True, embed_links=False, attach_files=True)
        channel = NS(name="logs", permissions_for=lambda me: perms)
        guild = NS(me=NS(), get_channel=lambda i: channel if i == 1 else None)
        self.assertIn("embed links", cog.check_target(guild, "log", 1, "send"))
        self.assertIn("no longer exists", cog.check_target(guild, "log", 2, "send"))
        perms.embed_links = True
        self.assertIsNone(cog.check_target(guild, "log", 1, "logsend"))

    async def test_new_modules_are_registered(self):
        """Every new feature has a module switch and a permission or an open default."""
        for module in ("modwatch", "permaudit", "reports", "invites", "debug"):
            self.assertIn(module, DEFAULTS["modules"])
        self.assertIsNotNone(self.bot.tree.get_command("Report message", type=discord.AppCommandType.message))

    async def test_database_tools(self):
        """The integrity check passes and vacuum keeps the data."""
        store = self.bot.store
        store.cfg(77)["prefix"] = "?"
        store.flush()
        self.assertEqual(store.integrity(), ["ok"])
        store.vacuum()
        self.assertGreater(store.file_size(), 0)

    async def test_error_report_is_queued_and_limited(self):
        """The first error reaches the error channel, a second one within five seconds is only counted."""
        guild = NS(id=8)
        self.bot.cfg(8)["debug"]["error_channel"] = 123
        self.bot.queue = asyncio.Queue()
        self.bot.report_error(guild, "/test", ValueError("boom"))
        self.bot.report_error(guild, "/test", ValueError("boom again"))
        self.assertEqual(self.bot.queue.qsize(), 1)
        self.assertEqual(self.bot.cfg(8)["debug"]["errors"], 2)
        self.bot.report_error(None, "/test", ValueError("no guild"))
        self.assertEqual(self.bot.queue.qsize(), 1)


if __name__ == "__main__":
    unittest.main()


class FeedFetchTest(unittest.IsolatedAsyncioTestCase):
    """The feed download refuses internal targets, also after a redirect, and big documents."""

    class Resp:
        """A fake response."""

        def __init__(self, status, headers=None, body=b""):
            """Keep the answer."""
            self.status, self.headers, self.body = status, headers or {}, body
            self.content = self

        async def __aenter__(self):
            """Enter the response."""
            return self

        async def __aexit__(self, *exc):
            """Leave the response."""
            return False

        async def iter_chunked(self, size):
            """Yield the body in pieces."""
            for i in range(0, len(self.body), size):
                yield self.body[i:i + size]

    class Session:
        """A fake session that returns prepared answers and records the requested URLs."""

        def __init__(self, answers):
            """Keep the answers."""
            self.answers, self.urls = list(answers), []

        def get(self, url, **kw):
            """Return the next answer."""
            self.urls.append(url)
            return self.answers.pop(0)

    async def test_internal_targets_are_never_requested(self):
        """Private, loopback, metadata and odd-port addresses stop before any request."""
        from guardbot.cogs.community.feeds import fetch

        for url in ("http://127.0.0.1/feed", "http://localhost/feed", "http://169.254.169.254/latest/meta-data", "http://[::1]/x", "http://10.0.0.5/x", "https://example.com:22/x", "file:///etc/passwd", "ftp://example.com/x"):
            session = self.Session([])
            with self.assertRaises(ValueError, msg=url):
                await fetch(session, url)
            self.assertEqual(session.urls, [], url)

    async def test_redirect_to_internal_address_is_refused(self):
        """A public address that redirects to an internal one is stopped at the second step."""
        from guardbot.cogs.community.feeds import fetch

        session = self.Session([self.Resp(302, {"Location": "http://169.254.169.254/latest"})])
        with self.assertRaises(ValueError):
            await fetch(session, "https://example.com/feed")
        self.assertEqual(session.urls, ["https://example.com/feed"])

    async def test_redirect_loop_and_size_limit(self):
        """Endless redirects and huge documents are cut off."""
        from guardbot.cogs.community.feeds import MAX_BYTES, fetch

        loop = self.Session([self.Resp(301, {"Location": "https://example.com/b"}) for _ in range(10)])
        with self.assertRaises(ValueError):
            await fetch(loop, "https://example.com/a")
        big = self.Session([self.Resp(200, body=b"x" * (MAX_BYTES + 10))])
        with self.assertRaises(ValueError):
            await fetch(big, "https://example.com/a")
        ok = self.Session([self.Resp(200, body=b"<rss/>")])
        self.assertEqual(await fetch(ok, "https://example.com/a"), b"<rss/>")
