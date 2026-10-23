"""Music sources: which service a link belongs to and reading songs from saved page data. No network is used."""

import json
import unittest

from guardbot import musicbot, musicsources as ms


class ServiceTest(unittest.TestCase):
    def test_hosts(self):
        cases = {
            "https://www.youtube.com/watch?v=abc": "youtube", "https://youtu.be/abc": "youtube", "https://music.youtube.com/watch?v=x": "youtube",
            "https://soundcloud.com/a/b": "soundcloud", "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC": "spotify",
            "https://music.apple.com/de/album/x/123?i=456": "apple_music", "https://tidal.com/browse/track/123": "tidal",
            "https://listen.tidal.com/album/99": "tidal", "https://example.org/song.mp3": None, "https://notyoutube.com/x": None,
            "https://youtube.com.evil.example/x": None, "not a link": None,
        }
        for url, want in cases.items():
            self.assertEqual(ms.service(url), want, url)

    def test_ids(self):
        self.assertEqual(ms.spotify_id("https://open.spotify.com/intl-de/track/4uLU6hMCjMI75M1A2tKUQC?si=x"), ("track", "4uLU6hMCjMI75M1A2tKUQC"))
        self.assertEqual(ms.spotify_id("https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"), ("playlist", "37i9dQZF1DXcBWIGoYBM5M"))
        self.assertIsNone(ms.spotify_id("https://open.spotify.com/artist/x"))
        self.assertEqual(ms.tidal_id("https://tidal.com/browse/album/123456"), ("album", "123456"))
        self.assertIsNone(ms.tidal_id("https://tidal.com/browse/artist/1"))

    def test_iso_duration(self):
        self.assertEqual(ms.iso_seconds("PT3M25S"), 205)
        self.assertEqual(ms.iso_seconds("PT1H2M"), 3720)
        self.assertEqual(ms.iso_seconds("P0D"), 0)
        self.assertEqual(ms.iso_seconds("garbage"), 0)
        self.assertEqual(ms.iso_seconds(None), 0)

    def test_search_text(self):
        self.assertEqual(ms.Song("Title", "Artist").query(), "Artist - Title")
        self.assertEqual(ms.Song("Only title").query(), "Only title")


class ParserTest(unittest.TestCase):
    def test_spotify_track_list(self):
        data = {"props": {"pageProps": {"state": {"data": {"entity": {"trackList": [
            {"title": "One", "subtitle": "Band A", "duration": 200000}, {"title": "Two", "subtitle": "Band B, Band C", "duration": 1000}]}}}}}}
        page = f'<html><script id="__NEXT_DATA__" type="application/json">{json.dumps(data)}</script></html>'
        songs = ms.parse_spotify_embed(page)
        self.assertEqual([(s.title, s.artist, s.length) for s in songs], [("One", "Band A", 200.0), ("Two", "Band B, Band C", 1.0)])

    def test_spotify_single_track(self):
        data = {"entity": {"type": "track", "name": "Song", "artists": [{"name": "X"}, {"name": "Y"}], "duration": 61000}}
        page = f'<script id="__NEXT_DATA__" type="application/json">{json.dumps(data)}</script>'
        self.assertEqual([(s.title, s.artist) for s in ms.parse_spotify_embed(page)], [("Song", "X, Y")])

    def test_apple_album_and_single_song(self):
        album = {"@type": "MusicAlbum", "name": "Album", "byArtist": {"name": "The Band"}, "tracks": [
            {"@type": "MusicRecording", "name": "First", "duration": "PT2M", "url": "https://music.apple.com/x?i=111"},
            {"@type": "MusicRecording", "name": "Second", "duration": "PT3M", "url": "https://music.apple.com/x?i=222", "byArtist": [{"name": "Guest"}]}]}
        page = f'<script type="application/ld+json">{json.dumps(album)}</script>'
        self.assertEqual([(s.title, s.artist, s.length) for s in ms.parse_apple(page)], [("First", "The Band", 120.0), ("Second", "Guest", 180.0)])
        self.assertEqual([s.title for s in ms.parse_apple(page, "222")], ["Second"])
        song = {"@type": "MusicRecording", "name": "Solo", "byArtist": {"name": "Singer"}}
        self.assertEqual([(s.title, s.artist) for s in ms.parse_apple(f'<script type="application/ld+json">{json.dumps(song)}</script>')], [("Solo", "Singer")])

    def test_meta_fallback(self):
        page = '<meta property="og:title" content="Night Drive by Some Artist on TIDAL">'
        self.assertEqual([(s.title, s.artist) for s in ms.parse_apple(page)], [("Night Drive", "Some Artist")])
        self.assertEqual([(s.title, s.artist) for s in ms.parse_spotify_embed("<title>Song - Artist | Site</title>")], [("Song", "Artist")])
        self.assertEqual(ms.parse_apple("<html></html>"), [])

    def test_broken_json_is_ignored(self):
        page = '<script type="application/ld+json">{not json</script><meta property="og:title" content="Fallback">'
        self.assertEqual([s.title for s in ms.parse_apple(page)], ["Fallback"])

    def test_tidal_api(self):
        track = {"data": {"id": "1", "type": "tracks", "attributes": {"title": "T", "duration": "PT4M"}, "relationships": {"artists": {"data": [{"id": "a", "type": "artists"}]}}},
                 "included": [{"id": "a", "type": "artists", "attributes": {"name": "Art"}}]}
        self.assertEqual([(s.title, s.artist, s.length) for s in ms.parse_tidal_api(track)], [("T", "Art", 240.0)])
        album = {"data": [{"id": "2", "type": "tracks"}, {"id": "1", "type": "tracks"}], "included": [
            {"id": "1", "type": "tracks", "attributes": {"title": "B"}}, {"id": "2", "type": "tracks", "attributes": {"title": "A"}}]}
        self.assertEqual([s.title for s in ms.parse_tidal_api(album)], ["A", "B"])
        self.assertEqual(ms.parse_tidal_api("nonsense"), [])


class ResolverTest(unittest.IsolatedAsyncioTestCase):
    async def test_rejects_other_links(self):
        r = ms.Resolver(lambda: None, {})
        with self.assertRaises(ValueError):
            await r.songs("https://example.org/x", 5)
        with self.assertRaises(ValueError):
            await r.songs("https://open.spotify.com/artist/x", 5)

    async def test_tidal_album_needs_keys(self):
        r = ms.Resolver(lambda: None, {}, env={})
        with self.assertRaises(ValueError) as ctx:
            await r.songs("https://tidal.com/browse/album/12345678", 5)
        self.assertIn("TIDAL_CLIENT_ID", str(ctx.exception))


class MusicBotSettingsTest(unittest.TestCase):
    def test_defaults_and_override(self):
        conf = musicbot.settings_of({})
        self.assertFalse(conf["enabled"])
        self.assertEqual(conf["token_env"], "MUSIC_TOKEN")
        self.assertTrue(musicbot.settings_of({"music_bot": {"enabled": True}})["enabled"])

    def test_invite_permissions_are_small(self):
        import discord
        perms = discord.Permissions(musicbot.INVITE_PERMISSIONS)
        self.assertTrue(perms.connect and perms.speak and perms.send_messages)
        self.assertFalse(perms.administrator or perms.manage_guild or perms.ban_members or perms.manage_roles)


if __name__ == "__main__":
    unittest.main()
