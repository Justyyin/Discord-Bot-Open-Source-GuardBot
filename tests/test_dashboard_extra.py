"""Dashboard pages for the look of the dashboard and the music player, plus the checks of dashlook."""

import unittest

from guardbot import dashhelp, dashlook, dashtexts, plugins
from tests.test_dashboard import ADMIN, VIEWER
from tests.test_dashboard_manage import ManageTest, png_url

PLUGS = set(plugins.PLUGINS)
CATS = {c[0] for c in plugins.CATEGORIES}


class LookCleanTest(unittest.TestCase):
    def good(self):
        return {"accent": "#AA00ff", "background": "", "dim": 30, "blur": 4, "compact": True, "hide_categories": ["fun"],
                "menus": [{"id": "m1", "title": "  Team   tools ", "open": False}],
                "tabs": [{"id": "t1", "title": "Mod", "icon": "hammer", "menu": "m1", "kind": "plugins", "plugins": ["moderation", "automod", "automod"]},
                         {"id": "t2", "title": "Home", "icon": "nope", "menu": "", "kind": "page", "page": "overview"},
                         {"id": "t3", "title": "Site", "icon": "link", "kind": "link", "url": "https://example.org/a?b=c"},
                         {"id": "t4", "title": "Rules", "icon": "note", "kind": "note", "text": "line 1\nline 2"}]}

    def test_good_look(self):
        out = dashlook.clean(self.good(), PLUGS, CATS, {"wallpaper": "0123456789abcdef.png"})
        self.assertEqual(out["accent"], "#aa00ff")
        self.assertIsNone(out["background"])
        self.assertEqual(out["wallpaper"], "0123456789abcdef.png")
        self.assertEqual(out["menus"], [{"id": "m1", "title": "Team tools", "open": False}])
        self.assertEqual(out["tabs"][0]["plugins"], ["moderation", "automod"])
        self.assertEqual(out["tabs"][1]["icon"], "star")
        self.assertEqual(out["tabs"][3]["text"], "line 1\nline 2")

    def test_bad_values(self):
        bad = [
            {"accent": "red"}, {"accent": "#12345"}, {"dim": 95}, {"blur": True}, {"hide_categories": ["nope"]},
            {"menus": [{"title": ""}]}, {"menus": [{"title": "x" * 41}]}, {"menus": [{"title": "m"}] * 13},
            {"tabs": [{"title": "a", "kind": "script"}]}, {"tabs": [{"title": "a", "kind": "link", "url": "http://plain.example"}]},
            {"tabs": [{"title": "a", "kind": "link", "url": "javascript:alert(1)"}]}, {"tabs": [{"title": "a", "kind": "link", "url": "https://a b"}]},
            {"tabs": [{"title": "a", "kind": "plugins", "plugins": []}]}, {"tabs": [{"title": "a", "kind": "plugins", "plugins": ["unknown"]}]},
            {"tabs": [{"title": "a", "kind": "page", "page": "../../etc"}]}, {"tabs": [{"title": "a", "kind": "note", "text": ""}]},
            {"tabs": [{"title": "a", "kind": "note", "text": "x", "menu": "m9"}]}, "not a dict",
        ]
        for data in bad:
            with self.assertRaises(dashlook.LookError, msg=str(data)[:80]):
                dashlook.clean(data, PLUGS, CATS)

    def test_duplicate_ids_are_renamed(self):
        out = dashlook.clean({"menus": [{"id": "m1", "title": "A"}, {"id": "m1", "title": "B"}]}, PLUGS, CATS)
        self.assertEqual(len({m["id"] for m in out["menus"]}), 2)

    def test_icons_exist_in_page(self):
        js = (dashtexts.WEB).read_text(encoding="utf-8")
        for name in dashlook.ICONS:
            self.assertRegex(js, rf"\b{name}: \"", name)

    def test_help_texts_cover_plugins(self):
        self.assertEqual(set(dashhelp.ABOUT), PLUGS)


class ExtraRoutesTest(ManageTest):
    """Reuses the bot, server and login of the manage tests; only the tests below run here."""

    async def test_look_roundtrip(self):
        await self.login()
        look = {"accent": "#ff8800", "tabs": [{"title": "Team", "kind": "plugins", "plugins": ["moderation"], "icon": "star"}]}
        r = await self.post("/look", {"look": look})
        self.assertEqual(r.status, 200)
        self.assertEqual(self.bot.cfg(5)["look"]["accent"], "#ff8800")
        info = await (await self.client.get("/api/guild/5")).json()
        self.assertEqual(info["look"]["tabs"][0]["title"], "Team")
        self.assertEqual((await self.post("/look", {"look": {"accent": "orange"}})).status, 422)
        self.assertEqual(self.bot.cfg(5)["look"]["accent"], "#ff8800")

    async def test_wallpaper(self):
        await self.login()
        r = await self.post("/look/wallpaper", {"image": png_url((300, 200))})
        self.assertEqual(r.status, 200)
        name = (await r.json())["wallpaper"]
        f = await self.client.get(f"/api/guild/5/look/wallpaper/{name}")
        self.assertEqual(f.status, 200)
        self.assertEqual(f.content_type, "image/png")
        self.assertEqual((await self.client.get("/api/guild/5/look/wallpaper/0000000000000000.png")).status, 404)
        self.assertEqual((await self.post("/look/wallpaper", {"image": "data:image/svg+xml;base64,AAAA"})).status, 422)
        self.assertEqual((await self.post("/look/wallpaper", {"remove": True})).status, 200)
        self.assertIsNone(self.bot.cfg(5)["look"]["wallpaper"])
        self.assertEqual((await self.client.get(f"/api/guild/5/look/wallpaper/{name}")).status, 404)

    async def test_wallpaper_needs_login(self):
        self.assertEqual((await self.client.get("/api/guild/5/look/wallpaper/0123456789abcdef.png")).status, 401)

    async def test_look_is_for_admins(self):
        self.bot.cfg(5)["dashboard_access"] = {"viewer_roles": [20], "mod_roles": []}
        await self.login(VIEWER)
        self.assertEqual((await self.post("/look", {"look": {}})).status, 403)
        self.assertEqual((await self.post("/look/wallpaper", {"remove": True})).status, 403)

    async def test_music_page(self):
        await self.login()
        data = await (await self.client.get("/api/guild/5/music")).json()
        self.assertFalse(data["second_bot"])
        self.assertIn("module_on", data)
        self.bot.cfg(5)["modules"]["music"] = False
        r = await self.post("/music/control", {"action": "skip"})
        self.assertEqual(r.status, 409)
        self.assertEqual((await self.post("/music/control", {"action": "rm -rf"})).status, 400)

    async def test_music_playlists(self):
        await self.login(ADMIN)
        tracks = [{"title": "Song", "artist": "Band", "kind": "search", "ref": "ytsearch1:Band - Song", "length": 100},
                  {"title": "Bad", "kind": "search", "ref": "file:///etc/passwd"}, {"title": "Outside", "kind": "local", "ref": "../../etc/passwd"}]
        r = await self.post("/music/playlist", {"name": "Evening", "tracks": tracks})
        self.assertEqual(r.status, 200, await r.text())
        data = await (await self.client.get("/api/guild/5/music?playlist=evening")).json()
        self.assertEqual(data["playlist"]["name"], "Evening")
        self.assertEqual([t["title"] for t in data["playlist"]["tracks"]], ["Song"])
        self.assertEqual((await self.post("/music/playlist", {"name": "Evening", "rename": "Night", "tracks": tracks})).status, 200)
        self.assertIn("Night", self.bot.cfg(5)["music"]["playlists"])
        self.assertEqual((await self.post("/music/playlist", {"name": "", "tracks": []})).status, 422)
        self.assertEqual((await self.post("/music/playlist", {"name": "Night", "delete": True})).status, 200)
        self.assertEqual(self.bot.cfg(5)["music"]["playlists"], {})

    async def test_brand_icons_are_optional(self):
        self.assertEqual((await self.client.get("/static/brand/discord.svg")).status, 404)
        self.assertEqual((await self.client.get("/static/brand/other.svg")).status, 404)


# Only the tests defined in ExtraRoutesTest should run here, not the inherited ones
for _name in [n for n in dir(ManageTest) if n.startswith("test_")]:
    if _name not in ExtraRoutesTest.__dict__:
        setattr(ExtraRoutesTest, _name, None)

del ManageTest


if __name__ == "__main__":
    unittest.main()
