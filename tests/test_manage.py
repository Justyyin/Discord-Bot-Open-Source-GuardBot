"""Tests for the structure, moderation and administration features of version 1.5."""

import asyncio
import tempfile
import time
import unittest
from types import SimpleNamespace as NS

import discord

from guardbot import configio
from guardbot.cogs.moderation import approval, history, members
from guardbot.cogs.security import exceptions
from guardbot.cogs.server import applications, rules, structure, team
from guardbot.cogs.security.automod import RULE_KEYS, without_rule
from guardbot.core import EXTENSIONS, Bot
from guardbot.defaults import DEFAULTS


def role(rid, perms=0, managed=False, default=False, name="r"):
    """A fake role."""
    return NS(id=rid, permissions=discord.Permissions(perms), managed=managed, is_default=lambda: default, name=name)


class MembersLogic(unittest.TestCase):
    """Sticky roles and name moderation."""

    def test_keep_roles(self):
        roles = [role(1, default=True), role(2, managed=True), role(3), role(4, discord.Permissions(administrator=True).value), role(5), role(6)]
        self.assertEqual(members.keep_roles(roles, exclude=[5], skip=[6]), [3])
        self.assertEqual(members.keep_roles(roles, exclude=[5], skip=[6], dangerous=True), [3, 4])

    def test_dehoist(self):
        self.assertEqual(members.dehoist("!!! Max"), "Max")
        self.assertEqual(members.dehoist("​~ -Max"), "Max")
        self.assertEqual(members.dehoist("Max"), "Max")
        self.assertEqual(members.dehoist("!!!"), "")

    def test_banned_words_with_tricks(self):
        self.assertEqual(members.banned_word("xX_N 1 G h t_Xx", ["night"]), "night")
        self.assertIsNone(members.banned_word("Knightley", []))
        self.assertEqual(members.banned_word("Bаdword", ["badword"]), "badword")

    def test_check_name(self):
        conf = {"dehoist": True, "words": ["bad"], "rename_to": "Moderated name"}
        self.assertEqual(members.check_name("!Max", conf)[0], "Max")
        self.assertEqual(members.check_name("!!!", conf)[0], "Moderated name")
        self.assertEqual(members.check_name("a b a d", conf)[0], "Moderated name")
        self.assertEqual(members.check_name("Max", conf), (None, None))
        conf["dehoist"] = False
        self.assertEqual(members.check_name("!Max", conf), (None, None))


class StructureLogic(unittest.TestCase):
    """Channels, archive and roles."""

    def test_permissions_are_masked(self):
        admin = discord.Permissions(administrator=True, manage_roles=True).value
        mine = discord.Permissions(manage_roles=True, kick_members=True).value
        self.assertEqual(structure.masked_permissions(admin, mine, False), discord.Permissions(manage_roles=True).value)
        self.assertEqual(structure.masked_permissions(admin, mine, True), admin)

    def test_idle(self):
        now = time.time()
        old = discord.utils.time_snowflake(discord.utils.utcnow() - __import__("datetime").timedelta(days=100))
        new = discord.utils.time_snowflake(discord.utils.utcnow())
        self.assertTrue(structure.is_idle(NS(id=1, last_message_id=old), 60, now))
        self.assertFalse(structure.is_idle(NS(id=1, last_message_id=new), 60, now))
        self.assertTrue(structure.is_idle(NS(id=old, last_message_id=None), 60, now))

    def test_sort_key(self):
        names = ["zeta", "-alpha", "Beta"]
        out = sorted((NS(name=n, id=i) for i, n in enumerate(names)), key=structure.sort_key)
        self.assertEqual([c.name for c in out], ["-alpha", "Beta", "zeta"])

    def test_rules(self):
        self.assertEqual(rules.numbered(["a", "b"]), "**1.** a\n**2.** b")
        now = 1_000_000
        self.assertFalse(rules.needs_reminder({"rules": 2}, 2, now - 999999, 48, now))
        self.assertFalse(rules.needs_reminder({"rules_reminded": 2}, 2, now - 999999, 48, now))
        self.assertFalse(rules.needs_reminder(None, 1, now - 3600, 48, now))
        self.assertTrue(rules.needs_reminder(None, 1, now - 49 * 3600, 48, now))
        self.assertTrue(rules.needs_reminder({"rules": 1, "rules_reminded": 1}, 2, now - 49 * 3600, 48, now))


class Blueprints(unittest.TestCase):
    """What the setup assistant creates."""

    def test_missing_items_only(self):
        from guardbot import presets
        bp = presets.BLUEPRINTS["community"]
        roles, cats, chans = presets.blueprint_missing(bp, set(), set(), set())
        self.assertEqual((len(roles), len(cats), len(chans)), (1, 4, sum(len(c["channels"]) for c in bp["categories"])))
        roles, cats, chans = presets.blueprint_missing(bp, {"moderator"}, {"general", "rules"}, {"info"})
        self.assertEqual(roles, [])
        self.assertNotIn("Info", [c["name"] for c in cats])
        self.assertNotIn("general", [c["name"] for _, c in chans])
        self.assertIn("media", [c["name"] for _, c in chans])

    def test_blueprints_stay_small_and_valid(self):
        from guardbot import presets
        for name, bp in presets.BLUEPRINTS.items():
            roles, cats, chans = presets.blueprint_size(bp)
            self.assertLessEqual(roles + cats + chans, 25, name)
            for r in bp["roles"]:
                self.assertFalse(discord.Permissions(**{p: True for p in r["permissions"]}).administrator)
            for cat in bp["categories"]:
                for ch in cat["channels"]:
                    self.assertLessEqual(len(ch["name"]), 100)
                    self.assertIn(ch["kind"], ("text", "voice"))


class ConfigLogic(unittest.TestCase):
    """History, rollback and copy."""

    def test_diff_and_entry(self):
        old, new = {"a": 1, "b": {"x": 1}, "c": 3}, {"a": 1, "b": {"x": 2}, "d": 4}
        self.assertEqual(history.diff(old, new), ["b", "c", "d"])
        entry = history.make_entry(7, old, new, [[1, "/x"]], 100)
        self.assertEqual(entry["before"], {"b": {"x": 1}, "c": 3})
        self.assertEqual(entry["sections"], ["b", "c", "d"])

    def test_large_sections_cannot_be_rolled_back(self):
        old = {"big": {"x": "y" * (history.MAX_ENTRY_BYTES + 10)}}
        entry = history.make_entry(1, old, {"big": {}}, [], 1)
        self.assertEqual(entry["sections"], ["big"])
        self.assertEqual(entry["before"], {})

    def test_recent_actors(self):
        got = history.recent_actors([(120, 1, "/a"), (190, 2, "/b"), (191, 2, "/b"), (10, 3, "/old")], 200)
        self.assertEqual(got, [[2, "/b"], [1, "/a"]])

    def test_restore_keeps_runtime_state(self):
        cfg = {"tickets": {"category": 5, "open": {"1": {"user": 2}}, "counter": 9}}
        configio.restore(cfg, "tickets", {"category": 7, "max_open": 1})
        self.assertEqual(cfg["tickets"]["category"], 7)
        self.assertEqual(cfg["tickets"]["open"], {"1": {"user": 2}})
        self.assertEqual(cfg["tickets"]["counter"], 9)
        self.assertIn("support_role", cfg["tickets"])

    def test_remap(self):
        big = 10 ** 17
        mapping = {big + 1: big + 101, big + 2: big + 102}
        value = {"channel": big + 1, "gone": big + 9, "roles": [big + 1, big + 9, big + 2], "by_channel": {str(big + 2): {"x": 1}, str(big + 8): {"x": 2}}, "count": 5, "text": "hi", "flag": True}
        new, ok, dropped = configio.remap(value, mapping)
        self.assertEqual(new["channel"], big + 101)
        self.assertIsNone(new["gone"])
        self.assertEqual(new["roles"], [big + 101, big + 102])
        self.assertEqual(list(new["by_channel"]), [str(big + 102)])
        self.assertEqual((new["count"], new["text"], new["flag"]), (5, "hi", True))
        self.assertEqual((ok, dropped), (4, 3))

    def test_id_map_matches_by_name(self):
        def guild(base, names):
            return NS(default_role=NS(id=base), roles=[NS(id=base + i, name=n, is_default=lambda: False) for i, n in enumerate(names, 1)], channels=[NS(id=base + 50 + i, name=n, type="text") for i, n in enumerate(names, 1)])
        a, b = guild(1000, ["Mod", "Admin"]), guild(2000, ["admin", "Other"])
        m = configio.id_map(a, b)
        self.assertEqual(m[1000], 2000)
        self.assertEqual(m[1002], 2001)
        self.assertNotIn(1001, m)
        self.assertEqual(m[1052], 2051)


class TeamLogic(unittest.TestCase):
    """Statistics, duty and applications."""

    def test_cases_by_mod_skips_automatic(self):
        cases = [
            {"ts": 100, "mod": 1, "type": "warn", "extra": {}}, {"ts": 150, "mod": 1, "type": "ban", "extra": {}},
            {"ts": 150, "mod": 9, "type": "mute", "extra": {"auto": True}}, {"ts": 10, "mod": 2, "type": "warn", "extra": {}},
        ]
        self.assertEqual(team.cases_by_mod(cases, 50), {1: {"warn": 1, "ban": 1}})

    def test_inactive(self):
        stats = {"1": {"last": 1000}, "2": {"last": 5}}
        self.assertEqual(team.inactive_members([1, 2, 3], stats, 1, 90000), [(3, 0), (2, 5), (1, 1000)])
        self.assertEqual(team.inactive_members([1], stats, 1, 1200), [])

    def test_pick_available(self):
        away = {"2": {"until": 0}, "3": {"until": 50}, "4": {"until": 500}}
        assigned = {"1": 300, "5": 100}
        self.assertEqual(team.pick_available([1, 2, 3, 4, 5], away, assigned, 100), 3)
        self.assertEqual(team.pick_available([1, 2, 4, 5], away, assigned, 100), 5)
        self.assertIsNone(team.pick_available([2, 4], away, assigned, 100))
        self.assertEqual(team.pick_available([3], away, assigned, 100), 3)

    def test_report_is_due_once(self):
        from datetime import datetime, timezone
        monday = datetime(2026, 10, 19, 10, tzinfo=timezone.utc)
        self.assertTrue(team.due(monday, 0, 9, 0, monday.timestamp()))
        self.assertFalse(team.due(monday, 0, 11, 0, monday.timestamp()))
        self.assertFalse(team.due(monday, 1, 9, 0, monday.timestamp()))
        self.assertFalse(team.due(monday, 0, 9, monday.timestamp() - 3600, monday.timestamp()))

    def test_votes(self):
        self.assertEqual(applications.tally({"1": "yes", "2": "no", "3": "yes"}), (2, 1))
        self.assertEqual(applications.outcome({"1": "yes", "2": "yes"}, 2), "accepted")
        self.assertEqual(applications.outcome({"1": "no", "2": "no"}, 2), "denied")
        self.assertIsNone(applications.outcome({"1": "yes", "2": "no"}, 2))

    def test_approver_rules(self):
        guild = NS(owner_id=1)
        req = {"mod": 10, "kind": "ban", "bulk_kind": None}

        def member(uid, ban=False, admin=False, roles=()):
            return NS(id=uid, guild=guild, guild_permissions=NS(ban_members=ban, administrator=admin, kick_members=False, moderate_members=False), roles=[NS(id=r) for r in roles])
        self.assertFalse(approval.may_decide(member(10, ban=True), req, None))
        self.assertTrue(approval.may_decide(member(11, ban=True), req, None))
        self.assertFalse(approval.may_decide(member(12), req, None))
        self.assertFalse(approval.may_decide(member(11, ban=True), req, 99))
        self.assertTrue(approval.may_decide(member(11, roles=[99]), req, 99))
        self.assertTrue(approval.may_decide(member(13, admin=True), req, 99))

    def test_exceptions(self):
        items = {"antiscam": {"channels": [5], "roles": []}, "automod": {"channels": [], "roles": [7]}, "caps": {"channels": [8], "roles": []}}
        self.assertTrue(exceptions.excepted(items, "antiscam", {5}, set()))
        self.assertFalse(exceptions.excepted(items, "antiscam", {8}, {7}))
        self.assertTrue(exceptions.excepted(items, "caps", set(), {7}))
        self.assertTrue(exceptions.excepted(items, "caps", {8}, set()))
        self.assertFalse(exceptions.excepted(items, "words", {8}, set()))

    def test_automod_rule_switch(self):
        a = DEFAULTS["automod"]
        b = without_rule({**a, "caps": {**a["caps"], "enabled": True}}, "caps")
        self.assertFalse(b["caps"]["enabled"])
        self.assertEqual(without_rule(a, "blocklist")["blocklist"], {"link": [], "message": [], "image": []})
        self.assertEqual(without_rule({**a, "channels": {"all": {}}}, "channel rule")["channels"], {})
        for key in RULE_KEYS:
            without_rule(a, key)


class Runtime(unittest.IsolatedAsyncioTestCase):
    """The cogs together with a real bot object."""

    async def asyncSetUp(self):
        """Load every cog."""
        self.bot = Bot({"data_dir": tempfile.mkdtemp()})

        async def never_ready():
            await asyncio.Event().wait()

        self.bot.wait_until_ready = never_ready
        for ext in EXTENSIONS:
            await self.bot.load_extension(f"guardbot.cogs.{ext}")
        self.bot.arrange_commands()
        self.guild = NS(id=77, member_count=3, members=[], get_role=lambda i: None, get_channel=lambda i: None)

    async def asyncTearDown(self):
        """Unload everything."""
        for cog in list(self.bot.cogs):
            await self.bot.remove_cog(cog)
        await asyncio.sleep(0)
        self.bot.store.close()

    async def test_gated_listener_is_skipped_when_module_is_off(self):
        self.bot.loop = asyncio.get_running_loop()
        calls = []

        class Listener:
            gate = {"on_message": "automod"}

            async def on_message(self, msg):
                calls.append(msg)

        msg = NS(guild=NS(id=5))
        self.bot.cfg(5)["modules"]["automod"] = False
        self.assertIsNone(self.bot._schedule_event(Listener().on_message, "on_message", msg))
        self.bot.cfg(5)["modules"]["automod"] = True
        task = self.bot._schedule_event(Listener().on_message, "on_message", msg)
        await task
        self.assertEqual(len(calls), 1)

    async def test_command_search_finds_nested_commands(self):
        from guardbot.cogs.server.admin import search_commands
        names = [c.qualified_name for c in search_commands(self.bot.tree, "timeout")]
        self.assertTrue(any(n.startswith("moderation ") for n in names), names)
        self.assertEqual(search_commands(self.bot.tree, "zzzznothing"), [])

    async def test_help_overview_fits_into_one_embed(self):
        sent = []

        class Ctx:
            guild = self.guild
            bot = self.bot

            async def send(self, *a, **k):
                sent.append(k.get("embed") or a)

        ctx = Ctx()
        await self.bot.get_command("help").callback(self.bot.get_cog("Admin"), ctx, command=None)
        self.assertLess(len(sent[0].description), 4096)
        self.assertIn("/moderation", sent[0].description)

    async def test_history_records_and_rolls_back(self):
        cog = self.bot.get_cog("History")
        cfg = self.bot.cfg(77)
        self.assertIsNone(cog.record(self.guild, 100))
        self.bot.note_actor(77, 5, "/welcome set")
        cfg["welcome"]["message"] = "Hello"
        cfg["tickets"]["counter"] = 40
        entry = cog.record(self.guild, 105)
        self.assertEqual(entry["sections"], ["welcome"])
        self.assertEqual(entry["who"], [[5, "/welcome set"]])
        self.assertEqual(entry["before"]["welcome"]["message"], DEFAULTS["welcome"]["message"])
        self.assertIsNone(cog.record(self.guild, 110))
        configio.restore(cfg, "welcome", entry["before"]["welcome"])
        self.assertEqual(cfg["welcome"]["message"], DEFAULTS["welcome"]["message"])
        self.assertEqual(cog.record(self.guild, 120)["sections"], ["welcome"])
        self.assertEqual(len(cfg["history"]["items"]), 2)

    async def test_history_is_not_part_of_exports(self):
        cfg = self.bot.cfg(78)
        cfg["history"]["items"].append({"id": 1})
        cfg["team"]["stats"]["5"] = {"cases": 3}
        self.assertNotIn("history", configio.export_config(cfg)["settings"])
        self.assertNotIn("stats", configio.export_config(cfg)["settings"]["team"])
        self.assertEqual(configio.validate(configio.export_config(cfg)["settings"]), [])

    async def test_ping_routes_to_available_staff(self):
        team_cog = self.bot.get_cog("Team")
        cfg = self.bot.cfg(77)
        members_ = [NS(id=1, bot=False), NS(id=2, bot=False), NS(id=3, bot=False)]
        r = NS(id=900, members=members_, mention="<@&900>")
        guild = NS(id=77, get_role=lambda i: r if i == 900 else None)
        self.assertEqual(team_cog.ping(guild, "tickets", 900), ("<@&900>", [], [900]))
        cfg["team"]["route"].append("tickets")
        cfg["team"]["away"]["1"] = {"until": 0, "reason": "", "ts": 1}
        first = team_cog.ping(guild, "tickets", 900)
        second = team_cog.ping(guild, "tickets", 900)
        self.assertNotEqual(first, second)
        self.assertIn(first[1][0], (2, 3))
        self.assertEqual(self.bot.staff_ping(guild, "reports", 900)[2], [900])
        cfg["team"]["away"]["2"] = {"until": 0, "reason": "", "ts": 1}
        cfg["team"]["away"]["3"] = {"until": 0, "reason": "", "ts": 1}
        self.assertEqual(team_cog.ping(guild, "tickets", 900)[2], [900])

    async def test_counting(self):
        guild = NS(id=77)
        self.bot.team_count(guild, 5, "tickets", 120)
        self.bot.team_count(guild, 5, "tickets", 60)
        self.bot.team_count(guild, 5, "cases")
        s = self.bot.cfg(77)["team"]["stats"]["5"]
        self.assertEqual((s["tickets"], s["cases"], s["secs"], s["handled"]), (2, 1, 180, 2))
        self.bot.cfg(77)["modules"]["team"] = False
        self.bot.team_count(guild, 6, "cases")
        self.assertNotIn("6", self.bot.cfg(77)["team"]["stats"])

    async def test_approval_flow(self):
        cog = self.bot.get_cog("Approval")
        posted = []

        class Channel:
            id = 55
            mention = "#c"

            async def send(self, text=None, **kw):
                posted.append(kw)
                return NS(id=1234)

        replies = []

        async def send(text, **kw):
            replies.append(text)

        guild = NS(id=77, owner_id=1, get_channel=lambda i: None, get_role=lambda i: None)
        ctx = NS(guild=guild, author=NS(id=10), channel=Channel(), send=send, bot=self.bot)
        target = NS(id=20, __str__=lambda s: "target")
        self.assertFalse(await cog.gate(ctx, "ban", target, "x"))
        self.bot.cfg(77)["modules"]["approval"] = True
        self.assertFalse(await cog.gate(ctx, "mute", target, "x"))
        self.assertTrue(await cog.gate(ctx, "ban", target, "spam", None))
        item = self.bot.cfg(77)["approval"]["items"]["1"]
        self.assertEqual((item["status"], item["mod"], item["target"], item["message"], item["channel"]), ("open", 10, 20, 1234, 55))
        self.assertEqual(len(posted), 1)
        ctx.author = NS(id=1)
        self.assertFalse(await cog.gate(ctx, "ban", target, "owner"))

    async def test_undo_set_follows_escalation_and_batches(self):
        mod = self.bot.get_cog("Moderation")
        cases = self.bot.store.cases(77)
        cases += [
            {"id": 1, "type": "warn", "user": 5, "active": True, "extra": {}}, {"id": 2, "type": "mute", "user": 5, "active": True, "extra": {"from_case": 1, "auto": True}},
            {"id": 3, "type": "ban", "user": 6, "active": True, "extra": {"batch": "ab"}}, {"id": 4, "type": "ban", "user": 7, "active": True, "extra": {"batch": "ab"}},
            {"id": 5, "type": "ban", "user": 8, "active": True, "extra": {"batch": "cd"}},
        ]
        ids = lambda items: sorted(c["id"] for c in items)  # noqa: E731
        self.assertEqual(ids(mod.undo_set(77, cases[0])), [1, 2])
        self.assertEqual(ids(mod.undo_set(77, cases[0], follow=False)), [1])
        self.assertEqual(ids(mod.undo_set(77, cases[2])), [3])
        self.assertEqual(ids(mod.undo_set(77, cases[2], batch=True)), [3, 4])

    async def test_new_defaults_exist_for_every_server(self):
        cfg = self.bot.cfg(99)
        for key in ("approval", "stickyroles", "nicknames", "watchlist", "reasons", "archive", "temproles", "roletemplates", "rules", "history", "team", "exceptions", "applications", "dashboard_access"):
            self.assertIn(key, cfg)


if __name__ == "__main__":
    unittest.main()


class ModuleStatus(unittest.TestCase):
    def test_setup_state_follows_changed_settings(self):
        from guardbot import configio
        from guardbot.store import fill
        cfg = {}
        fill(cfg, DEFAULTS)
        status = configio.module_status(cfg)
        self.assertEqual(status["welcome"], (False, "open"))
        self.assertEqual(status["utility"][1], "none")
        cfg["welcome"]["channel"] = 5
        cfg["modules"]["welcome"] = True
        self.assertEqual(configio.module_status(cfg)["welcome"], (True, "done"))
        cfg["rules"]["remind_hours"] = 5
        self.assertEqual(configio.module_status(cfg)["rules"][1], "done")

    def test_every_module_is_classified(self):
        from guardbot import configio
        from guardbot.store import fill
        cfg = {}
        fill(cfg, DEFAULTS)
        self.assertEqual(set(configio.module_status(cfg)), set(cfg["modules"]))


class Performance(unittest.TestCase):
    def test_queue_gives_only_due_members_once(self):
        from guardbot.cogs.server.rules import ReminderQueue, due_time
        q = ReminderQueue()
        q.add(1, 100)
        q.add(2, 50)
        q.add(2, 10)
        q.add(3, 500)
        self.assertEqual(q.pop_due(200, 10), [2, 1])
        self.assertEqual(q.pop_due(200, 10), [])
        self.assertEqual(len(q), 1)
        self.assertEqual(due_time(100, 1000, 1), 1000 + 3600)
        self.assertEqual(due_time(5000, 1000, 2), 5000 + 7200)

    def test_queue_limit_and_speed_for_large_servers(self):
        import time as _t
        from guardbot.cogs.server.rules import ReminderQueue
        q = ReminderQueue()
        start = _t.perf_counter()
        for i in range(200000):
            q.add(i, i)
        self.assertEqual(len(q.pop_due(10 ** 9, 20)), 20)
        self.assertLess(_t.perf_counter() - start, 3.0)
