"""Panels: validation, pictures, posting, role buttons and the dashboard routes."""

import asyncio
import io
import tempfile
import unittest
from types import SimpleNamespace

import discord
from PIL import Image

from guardbot import panels as P
from guardbot.core import EXTENSIONS, Bot


def png(color=(10, 120, 200), size=(300, 100)):
    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, "PNG")
    return buf.getvalue()


class EngineTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.conf = {"items": {}, "next": 1, "images": {}}

    def test_templates_are_valid(self):
        for kind in P.TEMPLATES:
            panel = P.clean(P.template(kind, "x"), {})
            self.assertGreaterEqual(len(panel["sections"]), 1)
        self.assertTrue(P.template("roles", "x")["single"])
        self.assertEqual(P.template("verify", "x")["buttons"][0]["kind"], "verify")

    def test_strict_validation(self):
        base = P.template("welcome", "w")
        for bad in (dict(base, script="x"), dict(base, sections=[]), dict(base, name="Bad Name"),
                    dict(base, buttons=[{"kind": "role"}]), dict(base, buttons=[{"kind": "link", "label": "a", "url": "http://x.example"}]),
                    dict(base, buttons=[{"kind": "eval", "label": "a"}]), dict(base, sections=[dict(base["sections"][0], color="red")]),
                    dict(base, sections=[dict(base["sections"][0], banner="0123456789abcdef")]),
                    dict(base, buttons=[{"kind": "verify", "label": "a"}, {"kind": "verify", "label": "b"}])):
            with self.assertRaises(P.PanelError):
                P.clean(bad, {})
        ok = P.clean(dict(base, buttons=[{"kind": "link", "label": "Site", "url": "https://example.com"}, {"kind": "role", "emoji": "\u26bd", "role": "123"}]), {})
        self.assertEqual(ok["buttons"][1]["role"], 123)

    def test_emoji_check(self):
        self.assertEqual(P.clean_emoji("<:kl:123456>"), "<:kl:123456>")
        self.assertEqual(P.clean_emoji("1\ufe0f\u20e3"), "1\ufe0f\u20e3")
        with self.assertRaises(P.PanelError):
            P.clean_emoji("hello")

    def test_pictures_are_checked_stored_once_and_cleaned(self):
        a = P.store_image(self.conf, self.dir, 1, png(), "banner.png")
        self.assertEqual(P.store_image(self.conf, self.dir, 1, png(), "again.png"), a)
        self.assertTrue(P.image_path(self.conf, self.dir, 1, a).is_file())
        for bad in (b"x" * 500, b"<svg></svg>" * 20):
            with self.assertRaises(P.PanelError):
                P.store_image(self.conf, self.dir, 1, bad)
        self.assertEqual(P.clean_images(self.conf, self.dir, 1), 0)  # new pictures stay for an hour
        self.assertEqual(P.clean_images(self.conf, self.dir, 1, keep_new=False), 1)
        self.assertIsNone(P.image_path(self.conf, self.dir, 1, a))

    def test_build(self):
        pid = P.store_image(self.conf, self.dir, 1, png(), "b.png")
        section = P.clean_section({"title": "Hi {server}", "text": "x", "banner": pid, "image": pid, "color": "#ff0000"}, self.conf["images"])
        guild = SimpleNamespace(id=1, name="Lautre", member_count=5)
        embed, files = P.build_section(section, self.conf, self.dir, guild, 0)
        self.assertEqual(embed.title, "Hi Lautre")
        self.assertEqual(embed.image.url, "attachment://image0.png")
        self.assertEqual([f.filename for f in files], ["banner0.png", "image0.png"])
        banner_only = P.clean_section({"banner": pid}, self.conf["images"])
        embed, files = P.build_section(banner_only, self.conf, self.dir, guild, 1)
        self.assertIsNone(embed)
        self.assertEqual(len(files), 1)

    def test_view(self):
        panel = P.clean(dict(P.template("roles", "r"), buttons=[{"kind": "role", "label": str(i), "role": 5} for i in range(7)] + [{"kind": "verify", "label": "Go"}]), {})
        view = P.build_view(3, panel)
        ids = [c.custom_id for c in view.children]
        self.assertEqual(ids[0], "gb:pn:3:0")
        self.assertEqual(ids[-1], "gb:verify")
        self.assertEqual(view.children[-1].item.label, "Go")
        self.assertEqual(max(c.row for c in view.children), 1)


class Chan:
    def __init__(self):
        self.id, self.mention, self.sent, self.edits, self.deleted = 77, "#welcome", [], [], []

    def permissions_for(self, member):
        return SimpleNamespace(send_messages=True)

    async def send(self, **kw):
        self.sent.append(kw)
        return SimpleNamespace(id=1000 + len(self.sent))

    def get_partial_message(self, mid):
        chan = self

        class M:
            async def edit(self, **kw):
                chan.edits.append((mid, kw))

            async def delete(self):
                chan.deleted.append(mid)

        return M()


class Role:
    def __init__(self, rid, position=1, perms=0):
        self.id, self.name, self.position, self.managed = rid, f"role{rid}", position, False
        self.permissions = discord.Permissions(perms)
        self.guild = None

    def is_default(self):
        return False

    def is_assignable(self):
        return True

    def __ge__(self, other):
        return self.position >= other.position

    def __eq__(self, other):
        return getattr(other, "id", None) == self.id

    def __hash__(self):
        return self.id


class CogTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = Bot({"data_dir": tempfile.mkdtemp()})

        async def never_ready():
            await asyncio.Event().wait()

        self.bot.wait_until_ready = never_ready
        for ext in EXTENSIONS:
            await self.bot.load_extension(f"guardbot.cogs.{ext}")
        self.bot.loop = asyncio.get_running_loop()
        self.cog = self.bot.get_cog("Panels")
        self.chan = Chan()
        self.roles = {11: Role(11), 12: Role(12), 13: Role(13, perms=discord.Permissions(administrator=True).value)}
        self.guild = SimpleNamespace(id=1, name="Lautre", member_count=5, me=None, owner_id=0, get_role=self.roles.get, get_channel=lambda cid: self.chan if cid == 77 else None)
        for r in self.roles.values():
            r.guild = self.guild

    async def asyncTearDown(self):
        for cog in list(self.bot.cogs):
            await self.bot.remove_cog(cog)
        await asyncio.sleep(0)
        self.bot.store.close()

    async def test_save_post_update_delete(self):
        conf = self.cog.conf(1)
        pic = P.store_image(conf, self.bot.store.dir, 1, png(), "w.png")
        data = P.template("roles", "origin")
        data["sections"].insert(0, {"banner": pic, "title": "", "text": "", "footer": "", "color": None, "image": None, "thumbnail": None})
        data["buttons"] = [{"kind": "role", "label": "KL", "emoji": "1\ufe0f\u20e3", "role": 11}, {"kind": "role", "label": "Kreis KL", "emoji": "2\ufe0f\u20e3", "role": 12}]
        pid = self.cog.save(self.guild, None, data)
        with self.assertRaises(P.PanelError):
            self.cog.save(self.guild, None, dict(data, buttons=[{"kind": "role", "label": "x", "role": 13}]))
        with self.assertRaises(P.PanelError):
            self.cog.save(self.guild, None, data)  # same name
        await self.cog.post(self.guild, pid, self.chan)
        self.assertEqual(len(self.chan.sent), 2)
        self.assertEqual(self.chan.sent[0]["files"][0].filename, "banner0.png")
        self.assertNotIn("embed", self.chan.sent[0])
        self.assertIn("view", self.chan.sent[1])
        self.assertEqual(conf["items"][pid]["messages"], [1001, 1002])
        await self.cog.update(self.guild, pid)
        self.assertEqual([m for m, _ in self.chan.edits], [1001, 1002])
        await self.cog.post(self.guild, pid, self.chan)
        self.assertEqual(self.chan.deleted, [1001, 1002])
        await self.cog.delete(self.guild, pid, messages=True)
        self.assertEqual(conf["items"], {})

    async def test_role_buttons_with_single_choice(self):
        data = P.template("roles", "origin")
        data["buttons"] = [{"kind": "role", "label": "KL", "role": 11}, {"kind": "role", "label": "Kreis", "role": 12}]
        pid = self.cog.save(self.guild, None, data)
        log = []

        class Member:
            roles = [self.roles[12]]

            async def add_roles(self, *r, reason=None):
                log.append(("add", [x.id for x in r]))
                self.roles = self.roles + list(r)

            async def remove_roles(self, *r, reason=None):
                log.append(("remove", [x.id for x in r]))
                self.roles = [x for x in self.roles if x not in r]

        answers = []

        async def send(text, ephemeral=False):
            answers.append(text)

        async def defer(ephemeral=False):
            pass

        it = SimpleNamespace(guild_id=1, guild=self.guild, user=Member(), response=SimpleNamespace(defer=defer, send_message=send), followup=SimpleNamespace(send=send))
        await self.cog.press(it, int(pid), 0)
        self.assertEqual(log, [("remove", [12]), ("add", [11])])
        await self.cog.press(it, int(pid), 0)
        self.assertEqual(log[-1], ("remove", [11]))
        self.assertIn("role11", answers[-1])
        await self.cog.press(it, 999, 0)
        self.assertEqual(len(log), 3)


if __name__ == "__main__":
    unittest.main()
