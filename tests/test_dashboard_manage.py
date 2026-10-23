"""Dashboard pages for commands, skills, AI and the profile of the bot, with the real bot and its cogs."""

import asyncio
import base64
import io
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from aiohttp.test_utils import TestClient, TestServer
import discord
from PIL import Image

from guardbot import dashboard_manage as dm
from guardbot.core import EXTENSIONS, Bot
from guardbot.dashboard import Dashboard
from tests.test_dashboard import ADMIN, GUEST, VIEWER, FakeGuild

KEY = "sk-test-0123456789abcdefghij"
OWNER = 777


def png_url(size=(64, 64)):
    buf = io.BytesIO()
    Image.new("RGB", size, (200, 30, 30)).save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


class Role:
    """A role with what the skills check needs."""

    def __init__(self, rid, name, position, perms=0):
        self.id, self.name, self.position, self.managed = rid, name, position, False
        self.permissions = discord.Permissions(perms)

    def is_default(self):
        return self.id == 5

    def is_assignable(self):
        return self.position < 9

    def __ge__(self, other):
        return self.position >= other.position


class Guild(FakeGuild):
    """The fake server of the dashboard tests plus what these pages need."""

    def __init__(self):
        super().__init__(5)
        self.edits = []

        async def edit(**kw):
            self.edits.append(kw)

        self.roles = [Role(5, "@everyone", 0), Role(20, "Member", 1), Role(21, "Admin", 2, discord.Permissions(manage_roles=True).value), Role(30, "Bot", 9)]
        self.me = SimpleNamespace(top_role=self.roles[-1], nick="Guard", display_avatar=SimpleNamespace(url="https://cdn/a.png"), guild_banner=None, edit=lambda **kw: edit(**kw))
        self.text_channels = []

    def get_role(self, rid):
        return next((r for r in self.roles if r.id == rid), None)

    def get_channel(self, cid):
        return next((c for c in self.channels if c.id == cid), None)


class ImageTest(unittest.TestCase):
    def test_accepts_real_pictures_only(self):
        self.assertTrue(dm.parse_image(png_url()).startswith(b"\x89PNG"))
        for bad in (None, 5, "data:image/svg+xml;base64,AAAA", "data:image/png;base64,%%%", "data:image/png;base64," + base64.b64encode(b"x" * 500).decode(),
                    "data:image/jpeg;base64," + png_url().split(",")[1]):
            with self.assertRaises(ValueError):
                dm.parse_image(bad)

    def test_size_limit(self):
        big = "data:image/png;base64," + base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"0" * (dm.MAX_IMAGE + 10)).decode()
        with self.assertRaises(ValueError):
            dm.parse_image(big)


class ManageTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = Bot({"data_dir": tempfile.mkdtemp(), "dashboard": {"enabled": True, "port": 8080}, "owner_ids": [OWNER]})

        async def never_ready():
            await asyncio.Event().wait()

        self.bot.wait_until_ready = never_ready
        for ext in EXTENSIONS:
            await self.bot.load_extension(f"guardbot.cogs.{ext}")
        self.bot.arrange_commands()
        self.bot.loop = asyncio.get_running_loop()
        self.guild = Guild()
        patches = [mock.patch.object(Bot, "is_ready", lambda s: True), mock.patch.object(Bot, "get_guild", lambda s, gid: self.guild if gid == 5 else None),
                   mock.patch.object(Bot, "guilds", new_callable=mock.PropertyMock, return_value=[self.guild]),
                   mock.patch.object(Bot, "user", new_callable=mock.PropertyMock, return_value=SimpleNamespace(name="GuardBot", display_avatar=SimpleNamespace(url="https://cdn/b.png"), banner=None, edit=self.user_edit))]
        self.user_edits = []
        self.bot.application_info = mock.AsyncMock(return_value=SimpleNamespace(team=None, owner=SimpleNamespace(id=OWNER), description="about"))
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.dash = Dashboard(self.bot)
        self.server = TestServer(self.dash.make_app())
        await self.server.start_server()
        host = f"127.0.0.1:{self.server.port}"
        self.dash.hosts.add(host)
        self.dash.origins.add(f"http://{host}")
        self.client = TestClient(self.server)
        await self.client.start_server()
        self.origin = {"Origin": f"http://{host}"}

    async def user_edit(self, **kw):
        self.user_edits.append(kw)

    async def asyncTearDown(self):
        await self.client.close()
        for cog in list(self.bot.cogs):
            await self.bot.remove_cog(cog)
        await asyncio.sleep(0)
        self.bot.store.close()

    async def login(self, uid=ADMIN):
        await self.client.get("/login", allow_redirects=False)
        state = self.client.session.cookie_jar.filter_cookies(self.client.make_url("/"))["gb_state"].value

        async def fake(code):
            return {"id": str(uid), "username": "tester", "avatar": None}

        with mock.patch.object(self.dash, "exchange", fake):
            await self.client.get("/callback", params={"code": "abc", "state": state}, allow_redirects=False)
        csrf = (await (await self.client.get("/api/me")).json())["csrf"]
        self.h = {**self.origin, "X-CSRF-Token": csrf}

    async def post(self, path, body):
        return await self.client.post("/api/guild/5" + path, json=body, headers=self.h)

    # ---- commands

    async def test_command_list_and_switches(self):
        await self.login()
        data = await (await self.client.get("/api/guild/5/commands")).json()
        rows = {r["key"]: r for r in data["commands"]}
        self.assertIn("ban", rows)
        self.assertEqual(rows["ban"]["path"], "/moderation ban")
        self.assertEqual(rows["ban"]["permission"], "ban_members")
        self.assertTrue(rows["ban"]["enabled"])
        self.assertTrue(rows["module"]["protected"])
        self.assertEqual(data["prefix"], self.bot.prefix_for(5))
        self.assertEqual((await self.post("/commands/set", {"key": "ban", "enabled": False})).status, 200)
        self.assertIn("ban", self.bot.cfg(5)["disabled_commands"])
        self.assertEqual((await self.post("/commands/set", {"key": "ban", "enabled": True})).status, 200)
        self.assertNotIn("ban", self.bot.cfg(5)["disabled_commands"])
        self.assertEqual((await self.post("/commands/set", {"key": "module", "enabled": False})).status, 422)
        self.assertEqual((await self.post("/commands/set", {"key": "nonsense", "enabled": False})).status, 400)

    async def test_command_roles(self):
        await self.login()
        self.assertEqual((await self.post("/commands/set", {"key": "ban", "roles": ["20"]})).status, 200)
        self.assertEqual(self.bot.cfg(5)["perms"]["ban"]["roles"], [20])
        self.assertEqual((await self.post("/commands/set", {"key": "ban", "roles": [999]})).status, 422)
        self.assertEqual((await self.post("/commands/set", {"key": "ban", "roles": []})).status, 200)
        self.assertNotIn("ban", self.bot.cfg(5)["perms"])

    async def test_aliases(self):
        await self.login()
        self.assertEqual((await self.post("/commands/alias", {"alias": "Zap", "command": "ban"})).status, 200)
        self.assertEqual(self.bot.cfg(5)["aliases"]["zap"], "ban")
        self.assertEqual((await self.post("/commands/alias", {"alias": "kick", "command": "ban"})).status, 422)
        self.assertEqual((await self.post("/commands/alias", {"alias": "bad name", "command": "ban"})).status, 400)
        self.assertEqual((await self.post("/commands/alias", {"alias": "zap", "command": None})).status, 200)
        self.assertEqual(self.bot.cfg(5)["aliases"], {})

    async def test_changes_need_admin_and_csrf(self):
        await self.login(GUEST)
        self.assertEqual((await self.client.get("/api/guild/5/commands")).status, 403)
        await self.login(ADMIN)
        r = await self.client.post("/api/guild/5/commands/set", json={"key": "ban", "enabled": False}, headers=self.origin)
        self.assertEqual(r.status, 403)
        self.assertNotIn("ban", self.bot.cfg(5)["disabled_commands"])

    async def test_viewer_can_read_but_not_change(self):
        self.bot.cfg(5)["dashboard_access"] = {"viewer_roles": [20], "mod_roles": []}
        await self.login(VIEWER)
        self.assertEqual((await self.client.get("/api/guild/5/commands")).status, 200)
        self.assertEqual((await self.client.get("/api/guild/5/skills")).status, 200)
        for path, body in (("/commands/set", {"key": "ban", "enabled": False}), ("/skills/save", {"spec": {}}), ("/ai/key", {"provider": "kimi", "key": KEY}), ("/profile/server", {"nick": "x"})):
            self.assertEqual((await self.post(path, body)).status, 403, path)

    # ---- skills

    async def test_skills_roundtrip(self):
        await self.login()
        spec = {"name": "hello", "kind": "command", "actions": [{"do": "reply", "text": "Hi {user}"}]}
        r = await self.post("/skills/save", {"spec": spec})
        self.assertEqual(r.status, 200)
        listing = await (await self.client.get("/api/guild/5/skills")).json()
        self.assertEqual([s["spec"]["name"] for s in listing["skills"]], ["hello"])
        self.assertEqual((await self.post("/skills/toggle", {"name": "hello", "enabled": False})).status, 200)
        self.assertFalse(self.bot.cfg(5)["skills"]["items"]["hello"]["enabled"])
        self.assertEqual((await self.post("/skills/delete", {"name": "hello"})).status, 200)
        self.assertEqual(self.bot.cfg(5)["skills"]["items"], {})
        self.assertEqual((await self.post("/skills/delete", {"name": "hello"})).status, 404)

    async def test_skills_are_validated(self):
        await self.login()
        for spec in ({"name": "x", "kind": "command", "actions": [{"do": "eval", "text": "1"}]},
                     {"name": "x", "kind": "command", "actions": [{"do": "reply", "text": "a"}], "exec": "os.system"},
                     {"name": "ban", "kind": "command", "actions": [{"do": "reply", "text": "a"}]},
                     {"name": "x", "kind": "command", "actions": [{"do": "add_role", "role": 21}]}):
            r = await self.post("/skills/save", {"spec": spec})
            self.assertEqual(r.status, 422, spec)
        self.assertEqual(self.bot.cfg(5)["skills"]["items"], {})
        ok = {"name": "join", "kind": "command", "actions": [{"do": "add_role", "role": 20}]}
        self.assertEqual((await self.post("/skills/save", {"spec": ok})).status, 200)

    # ---- AI

    async def test_ai_key_is_write_only(self):
        await self.login()
        info = await (await self.client.get("/api/guild/5/ai")).json()
        self.assertFalse(info["has_key"])
        r = await self.post("/ai/key", {"provider": "kimi", "key": KEY})
        body = await r.text()
        self.assertEqual(r.status, 200)
        self.assertNotIn(KEY, body)
        info_raw = await (await self.client.get("/api/guild/5/ai")).text()
        self.assertNotIn(KEY, info_raw)
        self.assertNotIn(self.bot.cfg(5)["ai"]["key_enc"], info_raw)
        self.assertTrue((await (await self.client.get("/api/guild/5/ai")).json())["has_key"])
        self.assertNotIn(KEY, repr(self.bot.cfg(5)))
        full = await self.client.get("/api/guild/5")
        self.assertNotIn(self.bot.cfg(5)["ai"]["key_enc"], await full.text())
        export = await (await self.client.get("/api/guild/5/export")).text()
        self.assertNotIn(self.bot.cfg(5)["ai"]["key_enc"], export)

    async def test_provider_cannot_change_without_a_new_key(self):
        await self.login()
        await self.post("/ai/key", {"provider": "kimi", "key": KEY})
        r = await self.post("/ai/set", {"provider": "openai", "model": "gpt-5", "daily_limit": 10, "second_opinion": True})
        self.assertEqual(r.status, 200)
        c = self.bot.cfg(5)["ai"]
        self.assertEqual((c["provider"], c["model"], c["daily_limit"], c["second_opinion"]), ("kimi", "gpt-5", 10, True))
        # the generic settings path must not reach the AI section either
        r = await self.client.post("/api/guild/5/set", json={"changes": [{"path": "ai.provider", "value": "openai"}]}, headers=self.h)
        self.assertEqual(r.status, 422)
        self.assertEqual(self.bot.cfg(5)["ai"]["provider"], "kimi")

    async def test_ai_validation_and_removal(self):
        await self.login()
        self.assertEqual((await self.post("/ai/key", {"provider": "evil", "key": KEY})).status, 422)
        self.assertEqual((await self.post("/ai/key", {"provider": "kimi", "key": "short"})).status, 422)
        self.assertEqual((await self.post("/ai/set", {"daily_limit": 0})).status, 422)
        self.assertEqual((await self.post("/ai/set", {"model": "bad model!"})).status, 422)
        await self.post("/ai/key", {"provider": "anthropic", "key": KEY})
        self.assertEqual((await self.post("/ai/remove", {})).status, 200)
        self.assertEqual(self.bot.cfg(5)["ai"]["key_enc"], "")
        self.assertFalse(self.bot.cfg(5)["modules"]["ai"])

    # ---- profile

    async def test_server_profile(self):
        await self.login()
        r = await self.client.post("/api/guild/5/profile/server", json={"nick": "Warden", "avatar": png_url()}, headers=self.h)
        self.assertEqual(r.status, 200)
        edit = self.guild.edits[-1]
        self.assertEqual(edit["nick"], "Warden")
        self.assertTrue(edit["avatar"].startswith(b"\x89PNG"))

    async def test_profile_rejects_bad_input_and_throttles(self):
        await self.login()
        for body in ({"nick": "x" * 40}, {"avatar": "data:image/png;base64,AAAA"}, {"bio": "y" * 300}):
            r = await self.client.post("/api/guild/5/profile/server", json=body, headers=self.h)
            self.assertEqual(r.status, 422, body)
        self.assertEqual((await self.client.post("/api/guild/5/profile/server", json={}, headers=self.h)).status, 400)
        self.assertEqual(self.guild.edits, [])

    async def test_global_profile_is_for_the_owner_only(self):
        await self.login(ADMIN)
        r = await self.client.post("/api/bot/profile", json={"name": "NewName"}, headers=self.h)
        self.assertEqual(r.status, 403)
        self.assertEqual(self.user_edits, [])
        info = await (await self.client.get("/api/guild/5/profile")).json()
        self.assertFalse(info["owner"])
        self.assertIsNone(info["global"]["bio"])

    async def test_owner_changes_the_global_profile(self):
        self.guild.members[OWNER] = SimpleNamespace(guild_permissions=SimpleNamespace(administrator=True, manage_guild=True), roles=[])
        self.bot.http = SimpleNamespace(edit_application_info=mock.AsyncMock())
        await self.login(OWNER)
        info = await (await self.client.get("/api/guild/5/profile")).json()
        self.assertTrue(info["owner"])
        self.assertEqual(info["global"]["bio"], "about")
        r = await self.client.post("/api/bot/profile", json={"name": "NewName", "avatar": png_url(), "bio": "Hello"}, headers=self.h)
        self.assertEqual(r.status, 200, await r.text())
        self.assertEqual(self.user_edits[0]["username"], "NewName")
        self.bot.http.edit_application_info.assert_awaited_once()
        r = await self.client.post("/api/bot/profile", json={"name": "Again"}, headers=self.h)
        self.assertEqual(r.status, 429)
        self.assertEqual(len(self.user_edits), 1)

    async def test_panels(self):
        await self.login()
        r = await self.post("/panels/create", {"name": "welcome", "template": "welcome"})
        self.assertEqual(r.status, 200)
        pid = (await r.json())["id"]
        self.assertEqual((await self.post("/panels/create", {"name": "welcome", "template": "rules"})).status, 422)
        up = await self.client.post("/api/guild/5/panels/image", json={"image": png_url((300, 100)), "name": "banner.png"}, headers=self.h)
        self.assertEqual(up.status, 200)
        image = (await up.json())["id"]
        self.assertEqual((await self.client.post("/api/guild/5/panels/image", json={"image": "data:image/png;base64,AAAA"}, headers=self.h)).status, 422)
        listing = await (await self.client.get("/api/guild/5/panels")).json()
        panel = listing["panels"][0]["panel"]
        panel["sections"][0]["banner"] = image
        panel["buttons"] = [{"kind": "role", "label": "Member", "role": "20"}, {"kind": "link", "label": "Site", "url": "https://example.com"}]
        del panel["messages"]
        self.assertEqual((await self.post("/panels/save", {"id": pid, "panel": panel})).status, 200)
        stored = self.bot.cfg(5)["panels"]["items"][pid]
        self.assertEqual(stored["sections"][0]["banner"], image)
        pic = await self.client.get(f"/api/guild/5/panels/image/{image}")
        self.assertEqual((pic.status, pic.content_type), (200, "image/png"))
        bad = dict(panel, buttons=[{"kind": "role", "label": "Admin", "role": "21"}])
        self.assertEqual((await self.post("/panels/save", {"id": pid, "panel": bad})).status, 422)
        self.assertEqual((await self.post("/panels/save", {"id": pid, "panel": dict(panel, evil=1)})).status, 422)
        self.assertEqual((await self.post("/panels/post", {"id": pid, "channel": "999"})).status, 422)
        self.assertEqual((await self.post("/panels/update", {"id": pid})).status, 422)
        self.assertEqual((await self.post("/panels/delete", {"id": pid})).status, 200)
        self.assertEqual(self.bot.cfg(5)["panels"]["items"], {})
        self.assertEqual((await self.post("/panels/delete", {"id": pid})).status, 404)

    async def test_panels_need_admin_to_change(self):
        self.bot.cfg(5)["dashboard_access"] = {"viewer_roles": [20], "mod_roles": []}
        await self.login(VIEWER)
        self.assertEqual((await self.client.get("/api/guild/5/panels")).status, 200)
        self.assertEqual((await self.post("/panels/create", {"name": "x", "template": "empty"})).status, 403)

    async def test_plugin_catalog(self):
        from guardbot.defaults import MODULES
        await self.login()
        info = await (await self.client.get("/api/guild/5")).json()
        self.assertEqual({p["key"] for p in info["plugins"]}, set(MODULES))
        cats = {c["key"] for c in info["categories"]}
        self.assertTrue(all(p["category"] in cats for p in info["plugins"]))
        sections = {s["key"] for s in info["sections"]}
        self.assertTrue(all(set(p["sections"]) <= sections for p in info["plugins"]))
        jail = next(p for p in info["plugins"] if p["key"] == "jail")
        self.assertEqual(jail["sections"], ["jail"])
        self.assertTrue(jail["title_de"])

    async def test_texts_are_public(self):
        r = await self.client.get("/api/texts/de")
        self.assertEqual(r.status, 200)
        self.assertEqual((await r.json())["Plugins"], "Plugins")
        self.assertEqual((await r.json())["Sign in with Discord"], "Mit Discord anmelden")
        self.assertEqual(await (await self.client.get("/api/texts/xx")).json(), {})
        self.assertEqual((await self.client.get("/api/texts/../../etc")).status, 404)

    async def test_oversized_bodies_are_refused(self):
        await self.login()
        r = await self.client.post("/api/guild/5/commands/set", data=b'{"key": "ban", "x": "' + b"a" * 300000 + b'"}', headers={**self.h, "Content-Type": "application/json"})
        self.assertEqual(r.status, 413)


if __name__ == "__main__":
    unittest.main()
