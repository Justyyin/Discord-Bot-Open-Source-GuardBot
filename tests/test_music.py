"""Music library, queue, link policy and the download pipeline."""

import functools
import http.server
import shutil
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path

import discord

from guardbot import musiclib as ml
from guardbot import musicdl
from guardbot.linkcheck import url_problem

HAVE_FFMPEG = shutil.which("ffmpeg") is not None


def make_flac(path, artist="", album="", title="", track=""):
    """Create a one second FLAC with tags using ffmpeg."""
    path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=440:duration=1"]
    for key, value in (("artist", artist), ("album", album), ("title", title), ("track", track)):
        if value:
            cmd += ["-metadata", f"{key}={value}"]
    subprocess.run(cmd + [str(path)], check=True)


class NamesTest(unittest.TestCase):
    """File names are safe on every system."""

    def test_clean(self):
        """Separators, dots, reserved names and long names are handled."""
        self.assertEqual(clean := ml.clean("AC/DC"), "AC DC")
        self.assertEqual(ml.clean(".."), "Unknown")
        self.assertEqual(ml.clean("../../etc/passwd"), "etc passwd")
        self.assertEqual(ml.clean("CON"), "_CON")
        self.assertEqual(ml.clean('a:b*c?"d'), "a b c d")
        self.assertEqual(ml.clean(None, "x"), "x")
        self.assertLessEqual(len(ml.clean("x" * 300)), 100)
        self.assertEqual(ml.clean("Beyoncé"), "Beyoncé")
        self.assertNotIn("/", clean)

    def test_target_path_structure_and_collisions(self):
        """Files land in Artist/Album/NN - Title and never overwrite each other."""
        root = Path(tempfile.mkdtemp())
        p = ml.target_path(root, "Daft Punk", "Discovery", "One More Time", 1, ".FLAC")
        self.assertEqual(p.relative_to(root).as_posix(), "Daft Punk/Discovery/01 - One More Time.flac")
        p.parent.mkdir(parents=True)
        p.write_bytes(b"x")
        self.assertTrue(ml.target_path(root, "Daft Punk", "Discovery", "One More Time", 1, ".flac").name.endswith("(2).flac"))
        single = ml.target_path(root, "", "", "Song", 0, ".mp3")
        self.assertEqual(single.relative_to(root).as_posix(), "Unknown Artist/Singles/Song.mp3")
        evil = ml.target_path(root, "../..", "..", "../x", 0, ".mp3")
        self.assertTrue(ml.inside(root, evil))
        self.assertEqual(ml.target_path(root, "a", "b", "c", 0, ".x/../y").suffix, ".bin")

    def test_resolve_rejects_escapes(self):
        """Paths outside the library and symbolic links are not playable."""
        root = Path(tempfile.mkdtemp()) / "music"
        root.mkdir()
        outside = root.parent / "secret.flac"
        outside.write_bytes(b"x")
        (root / "ok.flac").write_bytes(b"x")
        (root / "link.flac").symlink_to(outside)
        self.assertIsNotNone(ml.resolve(root, "ok.flac"))
        self.assertIsNone(ml.resolve(root, "../secret.flac"))
        self.assertIsNone(ml.resolve(root, "link.flac"))
        self.assertIsNone(ml.resolve(root, "missing.flac"))

    def test_time_helpers(self):
        """Time formatting and parsing."""
        self.assertEqual(ml.fmt_time(65), "1:05")
        self.assertEqual(ml.fmt_time(3725), "1:02:05")
        self.assertEqual(ml.parse_time("1:30"), 90)
        self.assertEqual(ml.parse_time("90"), 90)
        self.assertIsNone(ml.parse_time("abc"))
        self.assertEqual(len(ml.bar(30, 60)), 18)

    def test_guess_from_path(self):
        """Without tags the folder structure is used."""
        self.assertEqual(ml.guess_from_path("Artist/Album/03 - Title.flac"), ("Artist", "Album", "Title"))
        self.assertEqual(ml.guess_from_path("Artist/Song.mp3"), ("Artist", "", "Song"))


class QueueTest(unittest.TestCase):
    """Queue and loop modes."""

    def tracks(self, n):
        """Make n tracks."""
        return [ml.Track(f"t{i}", "a", "local", f"{i}.flac", 10, 1 + i % 2) for i in range(n)]

    def test_order_and_loops(self):
        """Tracks play in order, loop track repeats, loop queue goes round, skip ignores loop track."""
        q = ml.Queue()
        for t in self.tracks(3):
            q.add(t)
        self.assertEqual(q.advance().title, "t0")
        q.loop = "track"
        self.assertEqual(q.advance().title, "t0")
        self.assertEqual(q.advance(skipped=True).title, "t1")
        q.loop = "queue"
        self.assertEqual(q.advance().title, "t2")
        self.assertEqual(q.advance().title, "t1")
        q.loop = "off"
        q.clear()
        self.assertIsNone(q.advance())

    def test_remove_shuffle_count(self):
        """Removal is one-based, shuffle keeps all tracks, the per-user count works."""
        q = ml.Queue()
        for t in self.tracks(5):
            q.add(t)
        self.assertEqual(q.remove(2).title, "t1")
        self.assertIsNone(q.remove(9))
        before = sorted(t.title for t in q.items)
        q.shuffle()
        self.assertEqual(sorted(t.title for t in q.items), before)
        self.assertEqual(q.count_by(1), sum(1 for t in q.items if t.requester == 1))
        self.assertEqual(q.total_length(), 40)


class PolicyTest(unittest.TestCase):
    """Which links the bot may open."""

    def test_url_problem(self):
        """Private targets, other schemes, odd ports and host lists."""
        self.assertIsNone(url_problem("https://example.org/a"))
        for bad in ("http://127.0.0.1/x", "http://192.168.0.1/", "http://localhost/", "http://x.internal/", "file:///etc/passwd", "ftp://example.org/", "https://example.org:8443/", "http://169.254.169.254/"):
            self.assertIsNotNone(url_problem(bad), bad)
        self.assertIsNotNone(url_problem("https://bad.example.org/", blocked=["example.org"]))
        self.assertIsNone(url_problem("https://good.org/", allowed=["good.org"]))
        self.assertIsNotNone(url_problem("https://other.org/", allowed=["good.org"]))

    def test_artist_cleanup(self):
        """The Topic suffix of generated YouTube channels is removed."""
        self.assertEqual(musicdl.clean_artist("Daft Punk - Topic"), "Daft Punk")
        self.assertEqual(musicdl.clean_artist(None), "")


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg is not installed")
class LibraryFilesTest(unittest.TestCase):
    """Scanning, tags, search and the audio source with real files."""

    def setUp(self):
        """Create a small library."""
        self.root = Path(tempfile.mkdtemp()) / "music"
        make_flac(self.root / "Daft Punk" / "Discovery" / "01 - One More Time.flac", "Daft Punk", "Discovery", "One More Time", "1")
        make_flac(self.root / "Unknown Band" / "03 - Untagged.flac")
        (self.root / ".incoming").mkdir()
        make_flac(self.root / ".incoming" / "hidden.flac")
        (self.root / "notes.txt").write_text("x")

    def test_scan_reads_tags_and_falls_back_to_folders(self):
        """Tagged files use their tags, untagged ones the folders, hidden folders and other files are skipped."""
        entries = ml.scan(self.root)
        self.assertEqual(len(entries), 2)
        tagged = next(e for e in entries if e["title"] == "One More Time")
        self.assertEqual((tagged["artist"], tagged["album"], tagged["track"]), ("Daft Punk", "Discovery", 1))
        self.assertTrue(tagged["lossless"])
        self.assertIn("lossless", ml.quality(tagged))
        plain = next(e for e in entries if e["artist"] == "Unknown Band")
        self.assertEqual(plain["title"], "Untagged")

    def test_cache_and_rescan(self):
        """A new file is found on the next scan and an unchanged file is not read again."""
        cache = {}
        self.assertEqual(len(ml.scan(self.root, cache)), 2)
        make_flac(self.root / "New" / "Song.flac")
        self.assertEqual(len(ml.scan(self.root, cache)), 3)
        (self.root / "New" / "Song.flac").unlink()
        self.assertEqual(len(ml.scan(self.root, cache)), 2)

    def test_search(self):
        """All words must match, title hits rank first."""
        entries = ml.scan(self.root)
        self.assertEqual(ml.search(entries, "daft one")[0]["title"], "One More Time")
        self.assertEqual(ml.search(entries, "nothing here"), [])
        self.assertEqual(ml.search(entries, ""), [])

    def test_ffmpeg_source_decodes_the_file(self):
        """The audio source produces PCM frames from a library file."""
        path = ml.resolve(self.root, "Daft Punk/Discovery/01 - One More Time.flac")
        source = discord.FFmpegPCMAudio(str(path), before_options="-protocol_whitelist file", options="-vn")
        try:
            self.assertEqual(len(source.read()), 3840)
        finally:
            source.cleanup()


@unittest.skipUnless(HAVE_FFMPEG and musicdl.yt_dlp is not None, "ffmpeg or yt-dlp is missing")
class DownloadTest(unittest.TestCase):
    """The download pipeline with a local web server that offers a FLAC file."""

    def test_download_sorts_into_library(self):
        """A linked file is downloaded and filed as Artist/Album/Track with its tags."""
        web = Path(tempfile.mkdtemp())
        make_flac(web / "song.flac", "Test Artist", "Test Album", "Test Song", "2")
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(web))
        handler.log_message = lambda *a, **k: None
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        root = Path(tempfile.mkdtemp()) / "music"
        folder = root / ml.TEMP_DIR / "job"
        folder.mkdir(parents=True)
        try:
            files = musicdl.download_job(f"http://127.0.0.1:{server.server_port}/song.flac", folder, "ffmpeg", "best", False, 5, 600, 50)
            self.assertEqual(len(files), 1)
            entry, codec = musicdl.file_into_library(root, *files[0])
        finally:
            server.shutdown()
        self.assertEqual(entry["path"], "Test Artist/Test Album/02 - Test Song.flac")
        self.assertTrue(entry["lossless"])
        self.assertEqual(codec, "flac")
        self.assertFalse(any(folder.glob("*")), "the temporary file must have been moved")


if __name__ == "__main__":
    unittest.main()


class GenericSwitchTest(unittest.TestCase):
    """The generic extractor can be switched off."""

    def test_option_only_set_when_switched_off(self):
        """allowed_extractors excludes the generic extractor only when the switch is off."""
        try:
            musicdl.GENERIC["on"] = True
            self.assertNotIn("allowed_extractors", musicdl.base_options("ffmpeg"))
            musicdl.GENERIC["on"] = False
            self.assertEqual(musicdl.base_options("ffmpeg")["allowed_extractors"], ["default", "-generic"])
        finally:
            musicdl.GENERIC["on"] = True
