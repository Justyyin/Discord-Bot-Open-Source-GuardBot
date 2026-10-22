"""Dashboard: login, access rules, changes of settings and the headers."""

import copy
import os
import unittest
from types import SimpleNamespace
from unittest import mock

from aiohttp.test_utils import TestClient, TestServer

from guardbot import dashboard
from guardbot.dashboard import Dashboard, SPECS, apply_change, describe
from guardbot.defaults import DEFAULTS

ADMIN, GUEST = 111, 222


class Perms:
    """Permission set of a fake member."""

    def __init__(self, manage=False):
        """Store the flags."""
        self.administrator = False
        self.manage_guild = manage


class FakeGuild:
    """A server with two members: one manages it, one does not."""

    def __init__(self, gid=5):
        """Create channels and roles."""
        self.id, self.owner_id, self.unavailable, self.name, self.icon, self.member_count = gid, 999, False, "Test", None, 3
        self.channels = [SimpleNamespace(id=10, name="general", position=0), SimpleNamespace(id=11, name="logs", position=1)]
        self.roles = [SimpleNamespace(id=5, name="@everyone", position=0, is_default=lambda: True), SimpleNamespace(id=20, name="Mod", position=1, is_default=lambda: False)]
        self.members = {ADMIN: SimpleNamespace(guild_permissions=Perms(True)), GUEST: SimpleNamespace(guild_permissions=Perms(False))}

    def get_member(self, uid):
        """Look up a member."""
        return self.members.get(uid)


class FakeBot:
    """The few parts of the bot the dashboard uses."""

    def __init__(self, ready=True):
        """One server, default settings."""
        self.settings = {"dashboard": {"enabled": True, "port": 8080}}
        self.guild = FakeGuild()
        self.guilds = [self.guild]
        self.config = copy.deepcopy(DEFAULTS)
        self.ready = ready
        self.application_id = 1
        self.latency = 0.05
        self.logged = []
        self.store = SimpleNamespace(cases=lambda gid: [{"id": 1, "type": "warn", "user_name": "u", "mod_name": "m", "reason": "r", "ts": 1, "active": True}])
        self.tree = SimpleNamespace(get_commands=lambda: [SimpleNamespace(name="ban"), SimpleNamespace(name="warn"), SimpleNamespace(name="module")])

    def is_ready(self):
        """Connected or not."""
        return self.ready

    def is_closed(self):
        """Never closed."""
        return False

    def get_guild(self, gid):
        """Return the server if known."""
        return self.guild if gid == self.guild.id else None

    def cfg(self, gid):
        """Settings."""
        return self.config

    def log(self, guild, category, embed):
        """Remember log entries."""
        self.logged.append(embed.description)


class HelperTest(unittest.TestCase):
    """Checks of single settings."""

    def setUp(self):
        """Fresh settings and ID sets."""
        self.cfg = copy.deepcopy(DEFAULTS)
        self.args = ({10, 11}, {20}, {"ban", "warn", "module"})

    def test_specs_hide_internal_state(self):
        """Counters, runtime state and stored items are not editable."""
        for path in ("case_counter", "tickets.open", "lockdown.active", "automod.hits", "rolemenus.items", "antiscam.hashes", "probation.members"):
            self.assertNotIn(path, SPECS)
        self.assertIn("raid.joins", SPECS)
        self.assertIn("welcome.channel", SPECS)

    def test_valid_changes(self):
        """Booleans, numbers, texts, channels and roles are stored with the right type."""
        self.assertEqual(apply_change(self.cfg, "raid.enabled", True, *self.args), True)
        self.assertEqual(apply_change(self.cfg, "raid.joins", 7, *self.args), 7)
        self.assertEqual(apply_change(self.cfg, "welcome.channel", "10", *self.args), "10")
        self.assertEqual(self.cfg["welcome.channel".split(".")[0]]["channel"], 10)
        apply_change(self.cfg, "welcome.roles", ["20"], *self.args)
        self.assertEqual(self.cfg["welcome"]["roles"], [20])
        apply_change(self.cfg, "modules.economy", True, *self.args)
        self.assertTrue(self.cfg["modules"]["economy"])
        apply_change(self.cfg, "prefix", "?", *self.args)
        self.assertEqual(self.cfg["prefix"], "?")
        apply_change(self.cfg, "language", "de", *self.args)
        apply_change(self.cfg, "disabled_commands", ["ban"], *self.args)
        self.assertEqual(self.cfg["disabled_commands"], ["ban"])

    def test_rejected_changes(self):
        """Wrong types, unknown IDs, protected commands and internal settings are refused and nothing changes."""
        before = copy.deepcopy(self.cfg)
        for path, value in (
            ("raid.enabled", "yes"), ("raid.joins", "7"), ("raid.joins", True), ("raid.joins", float("inf")), ("raid.joins", 1.5), ("welcome.channel", "999"), ("welcome.channel", 10),
            ("welcome.roles", ["10"]), ("case_counter", 5), ("tickets.open", {}), ("automod.hits", 1), ("modules.nothing", True), ("language", "xx"), ("prefix", "a b"),
            ("prefix", "x" * 9), ("disabled_commands", ["module"]), ("disabled_commands", ["unknown"]), ("__class__", 1), ("raid", {}), ("antinuke.limits.role_delete", [1, 2]),
        ):
            with self.assertRaises(ValueError, msg=path):
                apply_change(self.cfg, path, value, *self.args)
        self.assertEqual(self.cfg, before)

    def test_describe_uses_strings_for_ids(self):
        """Discord IDs are sent as strings so that JavaScript does not round them."""
        self.cfg["welcome"]["channel"] = 1234567890123456789
        fields = {f["path"]: f for s in describe(self.cfg, ["ban"]) for f in s["fields"]}
        self.assertEqual(fields["welcome.channel"]["value"], "1234567890123456789")
        self.assertIn("modules.automod", fields)


class WebTest(unittest.IsolatedAsyncioTestCase):
    """The web server with a fake bot."""

    async def asyncSetUp(self):
        """Start the server and prepare the allowed host names."""
        self.bot = FakeBot()
        self.dash = Dashboard(self.bot)
        self.server = TestServer(self.dash.make_app())
        await self.server.start_server()
        host = f"127.0.0.1:{self.server.port}"
        self.dash.hosts.add(host)
        self.dash.origins.add(f"http://{host}")
        self.client = TestClient(self.server)
        await self.client.start_server()
        self.origin = {"Origin": f"http://{host}"}

    async def asyncTearDown(self):
        """Stop everything."""
        await self.client.close()

    async def login(self, uid=ADMIN):
        """Run the login with a patched Discord call and return the CSRF token."""
        r = await self.client.get("/login", allow_redirects=False)
        self.assertEqual(r.status, 302)
        self.assertTrue(r.headers["Location"].startswith("https://discord.com/oauth2/authorize"))
        state = self.client.session.cookie_jar.filter_cookies(self.client.make_url("/"))["gb_state"].value
        async def fake(code):
            return {"id": str(uid), "username": "tester", "avatar": None}
        with mock.patch.object(self.dash, "exchange", fake):
            r = await self.client.get("/callback", params={"code": "abc", "state": state}, allow_redirects=False)
        self.assertEqual(r.status, 302)
        me = await (await self.client.get("/api/me")).json()
        return me["csrf"]

    async def test_everything_needs_a_login(self):
        """Without a session the API answers 401."""
        for path in ("/api/me", "/api/guild/5", "/api/guild/5/cases", "/api/guild/5/export"):
            self.assertEqual((await self.client.get(path)).status, 401, path)
        for path in ("/api/guild/5/set", "/api/guild/5/import", "/api/logout"):
            self.assertEqual((await self.client.post(path, json={}, headers=self.origin)).status, 401, path)

    async def test_headers_and_host(self):
        """Security headers are set, other host names and cross-site posts are refused."""
        r = await self.client.get("/")
        self.assertEqual(r.status, 200)
        self.assertIn("default-src 'none'", r.headers["Content-Security-Policy"])
        self.assertEqual(r.headers["X-Frame-Options"], "DENY")
        self.assertEqual((await self.client.get("/", headers={"Host": "evil.example"})).status, 400)
        self.assertEqual((await self.client.post("/api/logout", json={}, headers={"Origin": "https://evil.example"})).status, 403)
        self.assertEqual((await self.client.post("/api/logout", json={})).status, 403)

    async def test_forged_login_is_refused(self):
        """A callback without the matching state cookie does not give a session."""
        r = await self.client.get("/callback", params={"code": "abc", "state": "forged"}, allow_redirects=False)
        self.assertEqual(r.status, 400)
        self.assertEqual((await self.client.get("/api/me")).status, 401)

    async def test_admin_can_read_and_change(self):
        """A manager sees the server and changes a setting, and the change is logged."""
        csrf = await self.login()
        me = await (await self.client.get("/api/me")).json()
        self.assertEqual([g["id"] for g in me["guilds"]], ["5"])
        info = await (await self.client.get("/api/guild/5")).json()
        self.assertTrue(any(s["key"] == "modules" for s in info["sections"]))
        r = await self.client.post("/api/guild/5/set", json={"changes": [{"path": "raid.joins", "value": 9}]}, headers={**self.origin, "X-CSRF-Token": csrf})
        self.assertEqual(r.status, 200)
        self.assertEqual(self.bot.config["raid"]["joins"], 9)
        self.assertTrue(any("raid.joins" in x for x in self.bot.logged))
        r = await self.client.post("/api/guild/5/set", json={"changes": [{"path": "case_counter", "value": 1}]}, headers={**self.origin, "X-CSRF-Token": csrf})
        self.assertEqual(r.status, 422)
        self.assertEqual(self.bot.config["case_counter"], 0)

    async def test_csrf_token_is_needed(self):
        """A change without or with a wrong token is refused."""
        await self.login()
        for headers in (self.origin, {**self.origin, "X-CSRF-Token": "wrong"}):
            r = await self.client.post("/api/guild/5/set", json={"changes": [{"path": "raid.joins", "value": 9}]}, headers=headers)
            self.assertEqual(r.status, 403)
        self.assertEqual(self.bot.config["raid"]["joins"], DEFAULTS["raid"]["joins"])

    async def test_member_without_permission(self):
        """A user who does not manage the server sees no server and gets 403 on it."""
        csrf = await self.login(GUEST)
        me = await (await self.client.get("/api/me")).json()
        self.assertEqual(me["guilds"], [])
        self.assertEqual((await self.client.get("/api/guild/5")).status, 403)
        r = await self.client.post("/api/guild/5/set", json={"changes": [{"path": "raid.joins", "value": 9}]}, headers={**self.origin, "X-CSRF-Token": csrf})
        self.assertEqual(r.status, 403)

    async def test_unknown_user_and_unknown_server(self):
        """Someone who is not in the server and a server without the bot are refused."""
        await self.login(333)
        self.assertEqual((await self.client.get("/api/guild/5")).status, 403)
        self.assertEqual((await self.client.get("/api/guild/6")).status, 404)

    async def test_nothing_works_while_the_bot_is_offline(self):
        """When the bot is not connected the dashboard refuses to work."""
        await self.login()
        self.bot.ready = False
        self.assertEqual((await self.client.get("/api/me")).status, 503)
        self.assertEqual((await self.client.get("/api/guild/5")).status, 503)
        self.assertEqual((await self.client.get("/login", allow_redirects=False)).status, 503)

    async def test_permission_is_checked_live(self):
        """A manager who loses the permission loses access without a new login."""
        await self.login()
        self.assertEqual((await self.client.get("/api/guild/5")).status, 200)
        self.bot.guild.members[ADMIN].guild_permissions.manage_guild = False
        self.assertEqual((await self.client.get("/api/guild/5")).status, 403)

    async def test_logout_ends_the_session(self):
        """After logout the old cookie is useless."""
        csrf = await self.login()
        r = await self.client.post("/api/logout", json={}, headers={**self.origin, "X-CSRF-Token": csrf})
        self.assertEqual(r.status, 200)
        self.assertEqual((await self.client.get("/api/me")).status, 401)

    async def test_export_and_import(self):
        """Exported settings can be imported again, a broken file is refused."""
        csrf = await self.login()
        raw = await (await self.client.get("/api/guild/5/export")).text()
        headers = {**self.origin, "X-CSRF-Token": csrf}
        self.assertEqual((await self.client.post("/api/guild/5/import", data=raw, headers=headers)).status, 200)
        self.assertEqual((await self.client.post("/api/guild/5/import", data="{}", headers=headers)).status, 422)

    async def test_rate_limit(self):
        """Too many requests in a minute are answered with 429."""
        codes = [(await self.client.get("/login", allow_redirects=False)).status for _ in range(25)]
        self.assertIn(429, codes)


class StartTest(unittest.TestCase):
    """Rules for starting the server."""

    def make(self, **conf):
        """A dashboard with the given settings."""
        bot = FakeBot()
        bot.settings = {"dashboard": dict({"enabled": True}, **conf)}
        return Dashboard(bot)

    def test_secret_is_needed(self):
        """Without the client secret the dashboard does not start."""
        with mock.patch.dict(os.environ, {"DISCORD_CLIENT_SECRET": ""}):
            self.assertIn("DISCORD_CLIENT_SECRET", self.make().problem())

    def test_public_address_needs_https(self):
        """A public address without HTTPS is refused, localhost and HTTPS are fine."""
        with mock.patch.dict(os.environ, {"DISCORD_CLIENT_SECRET": "x"}):
            self.assertIn("HTTPS", self.make(host="0.0.0.0", public_url="http://example.com").problem())
            self.assertIsNone(self.make(host="0.0.0.0", public_url="https://example.com").problem())
            self.assertIsNone(self.make().problem())

    def test_loopback(self):
        """Loopback detection."""
        self.assertTrue(dashboard.is_loopback("127.0.0.1"))
        self.assertTrue(dashboard.is_loopback("::1"))
        self.assertFalse(dashboard.is_loopback("0.0.0.0"))
        self.assertFalse(dashboard.is_loopback("192.168.1.2"))


if __name__ == "__main__":
    unittest.main()
