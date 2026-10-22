"""Pure parts of economy, role menus, schedule, feeds, activity, bulk actions and case search."""

import unittest
from datetime import datetime
from types import SimpleNamespace as NS
from zoneinfo import ZoneInfo

from guardbot.cogs.activity import KEEP_DAYS, bar, day_key, last_days, prune, top_channels
from guardbot.cogs.bulk import MAX_USERS, parse_ids
from guardbot.cogs.economy import Economy, cooldown_left, fmt_amount, wait_text
from guardbot.cogs.feeds import SEEN_KEEP, new_entries, parse_feed, remember, valid_feed, youtube_id
from guardbot.cogs.moderation import filter_cases
from guardbot.cogs.rolemenu import role_problem
from guardbot.cogs.schedule import advance, parse_when, valid_item

BERLIN = ZoneInfo("Europe/Berlin")
ATOM = b"""<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>yt:2</id><title>Second</title><link rel="alternate" href="https://y/2"/></entry>
<entry><id>yt:1</id><title>First</title><link href="https://y/1"/></entry></feed>"""
RSS = b"<rss><channel><item><title>A</title><link>https://s/a</link><guid>g-a</guid></item><item><title>B</title><link>https://s/b</link></item></channel></rss>"


class ScheduleTest(unittest.TestCase):
    """Reading times and repeating them."""

    def test_relative_clock_and_date(self):
        """in 2h, HH:MM and a date all give the right moment in the server time zone."""
        now = datetime(2026, 1, 10, 12, 0, tzinfo=BERLIN).timestamp()
        self.assertEqual(parse_when("in 2h", BERLIN, now), now + 7200)
        self.assertEqual(parse_when("in 30", BERLIN, now), now + 1800)
        self.assertEqual(parse_when("18:30", BERLIN, now), datetime(2026, 1, 10, 18, 30, tzinfo=BERLIN).timestamp())
        self.assertEqual(parse_when("09:00", BERLIN, now), datetime(2026, 1, 11, 9, 0, tzinfo=BERLIN).timestamp())
        self.assertEqual(parse_when("2026-12-24 18:00", BERLIN, now), datetime(2026, 12, 24, 18, 0, tzinfo=BERLIN).timestamp())

    def test_bad_or_past_times(self):
        """Nonsense and times in the past are refused."""
        now = datetime(2026, 1, 10, 12, 0, tzinfo=BERLIN).timestamp()
        for text in ("", "tomorrow", "25:99", "2020-01-01 10:00", "in 0m", "in x"):
            self.assertIsNone(parse_when(text, BERLIN, now), text)

    def test_repeat_skips_missed_runs_and_keeps_local_time(self):
        """After downtime the next run is in the future, and daily runs keep the clock time across the change to summer time."""
        at = datetime(2026, 3, 27, 10, 0, tzinfo=BERLIN).timestamp()
        now = datetime(2026, 3, 30, 12, 0, tzinfo=BERLIN).timestamp()
        nxt = advance(at, "daily", BERLIN, now)
        self.assertGreater(nxt, now)
        self.assertEqual(datetime.fromtimestamp(nxt, BERLIN).hour, 10)
        self.assertGreater(advance(at, "hourly", BERLIN, now), now)
        self.assertLessEqual(advance(at, "hourly", BERLIN, now) - now, 3600)
        self.assertGreater(advance(at, "weekly", BERLIN, now), now)
        self.assertEqual(advance(now + 50, "daily", BERLIN, now), now + 50)


class ShapeTest(unittest.TestCase):
    """Imported or damaged data must be recognised before the loops use it."""

    def test_schedule_item_shape(self):
        """Only complete items with the right types pass."""
        ok = {"channel": 1, "at": 5.5, "text": "x", "repeat": "daily"}
        self.assertTrue(valid_item(ok))
        for bad in ({**ok, "at": "soon"}, {**ok, "at": True}, {**ok, "repeat": "yearly"}, {**ok, "channel": "1"}, {"channel": 1}, "text", None):
            self.assertFalse(valid_item(bad), bad)

    def test_feed_shape(self):
        """Only complete feeds with the right types pass."""
        ok = {"kind": "rss", "target": "https://x", "channel": 1, "ping": None, "seen": [], "seeded": False}
        self.assertTrue(valid_feed(ok))
        for bad in ({**ok, "kind": "ftp"}, {**ok, "seen": "a"}, {**ok, "ping": "1"}, {"kind": "rss"}, [], None):
            self.assertFalse(valid_feed(bad), bad)


class FeedTest(unittest.TestCase):
    """Reading feeds safely."""

    def test_atom_and_rss(self):
        """Both formats give id, title and link."""
        a = parse_feed(ATOM)
        self.assertEqual([e["id"] for e in a], ["yt:2", "yt:1"])
        self.assertEqual(a[0]["link"], "https://y/2")
        r = parse_feed(RSS)
        self.assertEqual([e["id"] for e in r], ["g-a", "https://s/b"])

    def test_entity_bombs_are_refused(self):
        """Documents with a doctype or entities never reach the parser."""
        bomb = b'<?xml version="1.0"?><!DOCTYPE l [<!ENTITY a "aaaa"><!ENTITY b "&a;&a;&a;">]><rss><channel><item><title>&b;</title></item></channel></rss>'
        with self.assertRaises(ValueError):
            parse_feed(bomb)
        with self.assertRaises(ValueError):
            parse_feed(b'<!DocType x><rss/>')

    def test_new_entries_oldest_first_and_limited(self):
        """Only unseen entries are posted, oldest first, at most three at once."""
        entries = [{"id": str(i), "title": "", "link": ""} for i in range(10, 0, -1)]
        fresh = new_entries(entries, ["1", "2"])
        self.assertEqual(len(fresh), 3)
        self.assertEqual([e["id"] for e in fresh], ["8", "9", "10"])
        self.assertEqual(new_entries(entries, [e["id"] for e in entries]), [])

    def test_seen_list_stays_small(self):
        """The list of seen entries is capped."""
        seen = []
        remember(seen, [{"id": str(i)} for i in range(500)])
        self.assertEqual(len(seen), SEEN_KEEP)

    def test_youtube_id(self):
        """The channel ID is found in a link or alone."""
        cid = "UC" + "a" * 22
        self.assertEqual(youtube_id(f"https://www.youtube.com/channel/{cid}"), cid)
        self.assertEqual(youtube_id(cid), cid)
        self.assertIsNone(youtube_id("https://www.youtube.com/@name"))


class ActivityTest(unittest.TestCase):
    """Counting helpers."""

    def test_top_channels_and_days(self):
        """Sums over the chosen days only and sorts by count."""
        days = {"2026-01-09": {"channels": {"1": 5, "2": 1}}, "2026-01-10": {"channels": {"1": 1, "3": 9}}, "2025-12-01": {"channels": {"9": 99}}}
        keys = last_days(days, 3, "2026-01-10")
        self.assertEqual(keys, ["2026-01-08", "2026-01-09", "2026-01-10"])
        self.assertEqual(top_channels(days, keys), [("3", 9), ("1", 6), ("2", 1)])

    def test_prune_keeps_the_retention_time(self):
        """Old days are removed, recent ones stay."""
        days = {"2026-01-10": {}, "2025-01-01": {}}
        prune(days, "2026-01-10")
        self.assertEqual(list(days), ["2026-01-10"])
        self.assertGreater(KEEP_DAYS, 30)

    def test_bar(self):
        """Bars scale to the largest value and handle zero."""
        self.assertEqual(bar(10, 10), "#" * 20)
        self.assertEqual(bar(0, 0), "")
        self.assertEqual(len(day_key(0)), 10)


class BulkAndCasesTest(unittest.TestCase):
    """Bulk input and case search."""

    def test_parse_ids(self):
        """IDs and mentions are found once, in order."""
        self.assertEqual(parse_ids("<@123456789012345678> 223456789012345678 123456789012345678, x 12"), [123456789012345678, 223456789012345678])
        self.assertEqual(parse_ids(""), [])
        self.assertGreaterEqual(MAX_USERS, 10)

    def test_filter_cases(self):
        """Every filter narrows the result."""
        cases = [
            {"id": 1, "type": "ban", "user": 5, "user_name": "Spam Bot", "mod": 9, "reason": "Posted Scam links", "ts": 1000},
            {"id": 2, "type": "warn", "user": 5, "user_name": "Spam Bot", "mod": 8, "reason": "rude", "ts": 100000},
            {"id": 3, "type": "note", "user": 6, "user_name": "Nice", "mod": 9, "reason": "scam victim", "ts": 100000},
        ]
        ids = lambda **kw: [c["id"] for c in filter_cases(cases, now=100500, **kw)]  # noqa: E731
        self.assertEqual(ids(), [1, 2, 3])
        self.assertEqual(ids(uid=5), [1, 2])
        self.assertEqual(ids(kind="note"), [3])
        self.assertEqual(ids(search="spam"), [1, 2])
        self.assertEqual(ids(text="SCAM"), [1, 3])
        self.assertEqual(ids(mod=9), [1, 3])
        self.assertEqual(ids(days=1), [2, 3])
        self.assertEqual(ids(text="scam", mod=9, days=1), [3])


class EconomyTest(unittest.TestCase):
    """Balances and waiting times."""

    def cog(self):
        """A cog on a fake bot with an in-memory store."""
        users = {}

        class Store:
            """Minimal store."""

            user_data = {"1": users}

            def user(self, gid, uid):
                """Return the record of a user."""
                return users.setdefault(str(uid), {})

        conf = {"name": "coins", "max_balance": 1000}
        return Economy(NS(store=Store(), cfg=lambda gid: {"economy": conf}))

    def test_balance_never_negative_and_capped(self):
        """Taking more than owned gives zero, adding beyond the cap stops at the cap."""
        cog = self.cog()
        self.assertEqual(cog.add(1, 7, 300), 300)
        self.assertEqual(cog.add(1, 7, -999), 0)
        self.assertEqual(cog.add(1, 7, 5000), 1000)
        self.assertEqual(cog.balance_of(1, 7), 1000)
        self.assertEqual(cog.balance_of(1, 8), 0)

    def test_cooldown_and_text(self):
        """Waiting times are computed and written in hours and minutes."""
        self.assertEqual(cooldown_left(100, 60, now=130), 30)
        self.assertEqual(cooldown_left(100, 60, now=500), 0)
        self.assertEqual(wait_text(3661), "1h 2m")
        self.assertEqual(wait_text(30), "1m")
        self.assertEqual(fmt_amount({"name": "gold"}, 1234), "1,234 gold")


class RoleProblemTest(unittest.TestCase):
    """Which roles may be offered."""

    def role(self, **kw):
        """A fake role."""
        perms = NS(**{p: False for p in ("administrator", "manage_guild", "manage_roles", "manage_channels", "ban_members", "kick_members", "manage_webhooks")})
        for k in [k for k in kw if k.startswith("p_")]:
            setattr(perms, k[2:], kw[k])
        guild = NS(owner_id=1)
        r = NS(guild=guild, permissions=perms, managed=kw.get("managed", False), is_default=lambda: kw.get("default", False), is_assignable=lambda: kw.get("assignable", True), position=kw.get("pos", 1))
        return r

    def test_rules(self):
        """Default, managed, unassignable and dangerous roles are refused, a plain role is fine."""
        self.assertIsNone(role_problem(self.role()))
        self.assertIsNotNone(role_problem(self.role(default=True)))
        self.assertIsNotNone(role_problem(self.role(managed=True)))
        self.assertIsNotNone(role_problem(self.role(assignable=False)))
        self.assertIn("ban_members", role_problem(self.role(p_ban_members=True)))


if __name__ == "__main__":
    unittest.main()


class ShopFlowTest(unittest.IsolatedAsyncioTestCase):
    """Buying charges once, refunds when the role cannot be given, and speaks the server language."""

    def setup_cog(self, fail_role=False, language="en"):
        """A cog with a shop that has a plain item and a role item."""
        users = {"5": {"coins": 100}}

        class Store:
            """Minimal store."""

            user_data = {"1": users}

            def user(self, gid, uid):
                """Return the record of a user."""
                return users.setdefault(str(uid), {})

        conf = {"name": "coins", "max_balance": 1000, "shop": {"1": {"name": "Sticker", "price": 30, "role": None, "stock": 1}, "2": {"name": "VIP", "price": 60, "role": 9, "stock": None}}}
        bot = NS(store=Store(), cfg=lambda gid: {"economy": conf, "language": language})
        sent = []

        class Ctx:
            """Fake context."""

            guild = NS(id=1, get_role=lambda rid: NS(is_assignable=lambda: True))

            class author:
                """Fake author."""

                id = 5
                roles = []

                @staticmethod
                async def add_roles(*roles, reason=None):
                    """Give roles or fail."""
                    if fail_role:
                        import discord

                        raise discord.HTTPException(NS(status=403, reason="no"), "no")

            async def send(self, text=None, **kw):
                """Record the answer."""
                sent.append(text)

        return Economy(bot), Ctx(), users, conf, sent

    async def test_plain_item_charged_once_and_stock_used(self):
        """The balance drops once and a sold out item cannot be bought again."""
        cog, ctx, users, conf, sent = self.setup_cog()
        await cog.buy.callback(cog, ctx, 1)
        self.assertEqual(users["5"]["coins"], 70)
        self.assertEqual(users["5"]["items"], {"Sticker": 1})
        await cog.buy.callback(cog, ctx, 1)
        self.assertEqual(users["5"]["coins"], 70)
        self.assertIn("sold out", sent[-1])

    async def test_failed_role_is_refunded(self):
        """If the role cannot be given nothing stays charged."""
        cog, ctx, users, conf, sent = self.setup_cog(fail_role=True)
        await cog.buy.callback(cog, ctx, 2)
        self.assertEqual(users["5"]["coins"], 100)
        self.assertIn("Nothing was charged", sent[-1])

    async def test_answers_follow_the_server_language(self):
        """A German server gets German answers."""
        cog, ctx, users, conf, sent = self.setup_cog(language="de")
        await cog.buy.callback(cog, ctx, 1)
        self.assertIn("gekauft", sent[-1])
