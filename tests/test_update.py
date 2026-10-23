"""Update from GitHub: versions, archive checks, installation, rollback and the notice."""

import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from guardbot import updater
from guardbot.cogs.server.updates import Updates


def make_zip(path, version, extra=None, root="GuardBot-x/", names=None):
    """Write a small fake release archive."""
    files = {"main.py": "print('main')\n", "guardbot/__init__.py": f'__version__ = "{version}"\n', "guardbot/core.py": f"# core {version}\n", "requirements.txt": "aiohttp\n"}
    files.update(extra or {})
    with zipfile.ZipFile(path, "w") as z:
        for name, text in files.items():
            z.writestr(root + name, text)
        for name in names or ():
            z.writestr(name, "x")
    return path


class VersionTest(unittest.TestCase):
    """Reading and comparing versions."""

    def test_parse_and_compare(self):
        """Tags with v and suffixes are understood and compared as numbers."""
        self.assertEqual(updater.parse_version("v1.4.0"), (1, 4, 0))
        self.assertEqual(updater.parse_version("1.10.2-beta"), (1, 10, 2))
        self.assertIsNone(updater.parse_version("latest"))
        self.assertTrue(updater.is_newer("v1.10.0", "1.9.9"))
        self.assertFalse(updater.is_newer("v1.4.0", "1.4.0"))
        self.assertFalse(updater.is_newer("v1.3.9", "1.4.0"))
        self.assertFalse(updater.is_newer("nonsense", "1.4.0"))

    def test_repo_and_hosts(self):
        """Only owner/name and GitHub hosts over https are accepted."""
        self.assertTrue(updater.valid_repo("octo/guardbot"))
        for bad in ("", "octo", "a/b/c", "../x", "octo/..", "o o/x", "https://github.com/a/b"):
            self.assertFalse(updater.valid_repo(bad), bad)
        self.assertTrue(updater.host_ok("https://codeload.github.com/a/b/zip/refs/tags/v1"))
        for bad in ("http://github.com/x", "https://evil.example/x", "https://github.com.evil.example/x", "https://127.0.0.1/x", "https://github.com:8443/x", "file:///etc/passwd"):
            self.assertFalse(updater.host_ok(bad), bad)

    def test_checksum_file(self):
        """The hash is found in a checksum file."""
        h = "a" * 64
        self.assertEqual(updater.expected_hash(f"{h}  GuardBot.zip\n"), h)
        self.assertIsNone(updater.expected_hash("nothing"))


class StartTest(unittest.TestCase):
    """The import check used before an update is kept."""

    def test_real_code_starts_and_broken_code_does_not(self):
        """The code of this repository imports, an empty folder does not."""
        root = Path(__file__).resolve().parent.parent
        self.assertTrue(updater.starts(root))
        with tempfile.TemporaryDirectory() as empty:
            self.assertFalse(updater.starts(empty, timeout=30))


class ArchiveTest(unittest.TestCase):
    """Checks of the downloaded archive."""

    def setUp(self):
        """A temporary folder."""
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        """Remove the folder."""
        self.tmp.cleanup()

    def test_good_archive(self):
        """A proper release is accepted and its version is read."""
        with zipfile.ZipFile(make_zip(self.dir / "a.zip", "1.5.0")) as z:
            root = updater.inspect(z)
            self.assertEqual(root, "GuardBot-x/")
            self.assertEqual(updater.archive_version(z, root), "1.5.0")

    def test_unsafe_archives(self):
        """Paths that leave the folder, links, empty and foreign archives are refused."""
        for names in (["GuardBot-x/../evil.py"], ["/etc/passwd"], ["GuardBot-x/a\\b.py"], ["C:/x.py"]):
            with zipfile.ZipFile(make_zip(self.dir / "b.zip", "1.5.0", names=names)) as z:
                with self.assertRaises(ValueError, msg=names):
                    updater.inspect(z)
        link = self.dir / "link.zip"
        with zipfile.ZipFile(make_zip(link, "1.5.0"), "a") as z:
            info = zipfile.ZipInfo("GuardBot-x/link")
            info.external_attr = 0o120777 << 16
            z.writestr(info, "/etc/passwd")
        with zipfile.ZipFile(link) as z:
            with self.assertRaises(ValueError):
                updater.inspect(z)
        other = self.dir / "other.zip"
        with zipfile.ZipFile(other, "w") as z:
            z.writestr("x/readme.txt", "hi")
        with zipfile.ZipFile(other) as z:
            with self.assertRaises(ValueError):
                updater.inspect(z)

    def test_protected_files_are_never_written(self):
        """The token, the settings and the data are not part of an update."""
        extra = {".env": "DISCORD_TOKEN=evil", "settings.json": "{}", "data/guardbot.db": "x", "music/a.mp3": "x", ".venv/bin/python": "x", "docs/new.md": "ok"}
        with zipfile.ZipFile(make_zip(self.dir / "c.zip", "1.5.0", extra)) as z:
            rels = {rel for _, rel in updater.targets(z, "GuardBot-x/")}
        self.assertIn("docs/new.md", rels)
        self.assertIn("guardbot/core.py", rels)
        for name in (".env", "settings.json", "data/guardbot.db", "music/a.mp3", ".venv/bin/python"):
            self.assertNotIn(name, rels)


class InstallTest(unittest.TestCase):
    """Installation with backup and rollback."""

    def setUp(self):
        """A fake installation with a secret and data."""
        self.tmp = tempfile.TemporaryDirectory()
        self.app = Path(self.tmp.name) / "app"
        (self.app / "guardbot").mkdir(parents=True)
        (self.app / "data").mkdir()
        (self.app / "main.py").write_text("old main\n")
        (self.app / "guardbot" / "__init__.py").write_text('__version__ = "1.4.0"\n')
        (self.app / "guardbot" / "core.py").write_text("old core\n")
        (self.app / "requirements.txt").write_text("aiohttp\n")
        (self.app / ".env").write_text("DISCORD_TOKEN=secret\n")
        (self.app / "data" / "guardbot.db").write_text("my data")
        self.data = self.app / "data"
        self.zip = make_zip(Path(self.tmp.name) / "r.zip", "1.5.0", {".env": "DISCORD_TOKEN=evil", "data/guardbot.db": "evil", "guardbot/new.py": "# new\n"})

    def tearDown(self):
        """Remove everything."""
        self.tmp.cleanup()

    def test_success(self):
        """New files are written, secrets and data stay, the old files are saved."""
        with mock.patch.object(updater, "starts", return_value=True), mock.patch.object(updater, "install_requirements", return_value=True):
            ok, message = updater.install(self.zip, self.app, self.data, current="1.4.0")
        self.assertTrue(ok, message)
        self.assertIn("1.5.0", (self.app / "guardbot" / "__init__.py").read_text())
        self.assertTrue((self.app / "guardbot" / "new.py").exists())
        self.assertEqual((self.app / ".env").read_text(), "DISCORD_TOKEN=secret\n")
        self.assertEqual((self.app / "data" / "guardbot.db").read_text(), "my data")
        backups = list((self.data / "update").glob("backup-*.zip"))
        self.assertEqual(len(backups), 1)
        with zipfile.ZipFile(backups[0]) as z:
            self.assertEqual(z.read("guardbot/core.py"), b"old core\n")

    def test_rollback_when_it_does_not_start(self):
        """When the new code cannot start the old files come back and new files are removed."""
        with mock.patch.object(updater, "starts", return_value=False), mock.patch.object(updater, "install_requirements", return_value=True):
            ok, message = updater.install(self.zip, self.app, self.data, current="1.4.0")
        self.assertFalse(ok)
        self.assertIn("rolled back", message)
        self.assertEqual((self.app / "guardbot" / "core.py").read_text(), "old core\n")
        self.assertIn("1.4.0", (self.app / "guardbot" / "__init__.py").read_text())
        self.assertFalse((self.app / "guardbot" / "new.py").exists())

    def test_same_version_is_refused(self):
        """An archive that is not newer is not installed."""
        ok, message = updater.install(self.zip, self.app, self.data, current="1.5.0")
        self.assertFalse(ok)
        self.assertEqual((self.app / "guardbot" / "core.py").read_text(), "old core\n")

    def test_failed_packages_roll_back(self):
        """A failed package installation is rolled back too."""
        (self.app / "requirements.txt").write_text("old\n")
        with mock.patch.object(updater, "starts", return_value=True), mock.patch.object(updater, "install_requirements", return_value=False):
            ok, _ = updater.install(self.zip, self.app, self.data, current="1.4.0")
        self.assertFalse(ok)
        self.assertEqual((self.app / "requirements.txt").read_text(), "old\n")


class CogTest(unittest.IsolatedAsyncioTestCase):
    """The background round: notice once, download, install only when automatic."""

    def make(self, **conf):
        """The cog on a fake bot."""
        meta = {}
        store = SimpleNamespace(get_meta=meta.get, set_meta=meta.__setitem__)
        bot = SimpleNamespace(settings={"update": dict({"repo": "octo/guardbot"}, **conf), "data_dir": tempfile.mkdtemp()}, store=store)
        cog = Updates(bot)
        cog.told = []

        async def tell(text, release):
            """Remember notices."""
            cog.told.append(text)
        cog.tell = tell
        return cog

    async def test_notice_once_and_manual_install(self):
        """A new version is announced one time and not installed without auto_install."""
        cog = self.make()
        release = {"tag": "v9.0.0", "name": "x", "notes": "", "page": "", "zip": "https://api.github.com/z", "sha": None}
        installs = []

        async def check():
            """A newer release."""
            cog.latest = release
            return release

        async def stage(rel):
            """Pretend to download."""
            cog.staged = Path(tempfile.mkdtemp()) / "x.zip"
            return cog.staged

        async def install():
            """Count installs."""
            installs.append(1)
            return True, "ok"
        cog.check, cog.stage, cog.install = check, stage, install
        await cog.cycle()
        await cog.cycle()
        self.assertEqual(len(cog.told), 1)
        self.assertEqual(installs, [])

    async def test_automatic_install(self):
        """With auto_install the downloaded version is installed."""
        cog = self.make(auto_install=True)
        release = {"tag": "v9.0.0", "name": "x", "notes": "", "page": "", "zip": "https://api.github.com/z", "sha": None}
        installs = []

        async def check():
            """A newer release."""
            cog.latest = release
            return release

        async def stage(rel):
            """Pretend to download."""
            return None

        async def install():
            """Count installs."""
            installs.append(1)
            return True, "ok"
        cog.check, cog.stage, cog.install = check, stage, install
        with mock.patch.object(updater, "in_docker", return_value=False):
            await cog.cycle()
        self.assertEqual(installs, [1])

    async def test_no_install_in_a_container(self):
        """In a container nothing is installed, even with auto_install."""
        cog = self.make(auto_install=True)
        cog.latest = {"tag": "v9.0.0"}
        with mock.patch.object(updater, "in_docker", return_value=True):
            ok, message = await cog.install()
        self.assertFalse(ok)
        self.assertIn("container", message)

    async def test_off_without_repository(self):
        """Without a repository no check is scheduled."""
        cog = self.make(repo="")
        with mock.patch("guardbot.cogs.server.updates.__repository__", ""):
            cog.repo = ""
            await cog.cog_load()
        self.assertIsNone(cog.task)

    async def test_status_text(self):
        """The status names the repository and the mode."""
        text = self.make().status()
        self.assertIn("octo/guardbot", text)
        self.assertIn("Automatic installation: off", text)


if __name__ == "__main__":
    unittest.main()
