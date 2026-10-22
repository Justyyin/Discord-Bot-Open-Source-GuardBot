"""Update from GitHub: find a newer release, download it, check it, install it with a backup and roll back when it does not start."""

import asyncio
import hashlib
import logging
import os
import re
import shutil
import stat
import subprocess
import sys
import time
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

import aiohttp
from yarl import URL

from . import __version__
from .linkcheck import make_session

log = logging.getLogger(__name__)

API = "https://api.github.com"
REPO_RE = re.compile(r"[A-Za-z0-9_.-]{1,100}/[A-Za-z0-9_.-]{1,100}")
VERSION_RE = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")
HOSTS = ("api.github.com", "github.com", "codeload.github.com", "objects.githubusercontent.com", "release-assets.githubusercontent.com")
MAX_DOWNLOAD = 60 * 1024 * 1024
MAX_UNPACKED = 250 * 1024 * 1024
MAX_FILES = 6000
# Never replaced by an update: the secrets, the settings and everything the bot stores
PROTECTED = (".env", "settings.json", "data", "music", ".venv", "venv", ".git", "__pycache__")


def parse_version(text):
    """Turn v1.4.0 or 1.4.0-beta into (1, 4, 0), or None when it is not a version."""
    m = VERSION_RE.match((text or "").strip())
    return tuple(int(x) for x in m.groups()) if m else None


def is_newer(tag, current=None):
    """True if a release tag is a higher version than the running one."""
    new, old = parse_version(tag), parse_version(current or __version__)
    return bool(new and old and new > old)


def valid_repo(text):
    """True for owner/name of a GitHub repository."""
    return bool(text) and bool(REPO_RE.fullmatch(text)) and ".." not in text


def in_docker():
    """True inside a container, where the code belongs to the image and cannot be updated in place."""
    return Path("/.dockerenv").exists()


def host_ok(url):
    """True if a download address is https and on a GitHub host."""
    p = urlparse(url)
    return p.scheme == "https" and (p.hostname or "").lower() in HOSTS and p.port in (None, 443)


async def fetch_latest(session, repo):
    """Read the newest release of a repository. Returns a dict or None when there is none."""
    if not valid_repo(repo):
        raise ValueError("update.repo must look like owner/name")
    async with session.get(f"{API}/repos/{repo}/releases/latest", headers={"Accept": "application/vnd.github+json"}, timeout=aiohttp.ClientTimeout(total=15)) as r:
        if r.status == 404:
            return None
        if r.status != 200:
            raise ValueError(f"GitHub answered {r.status}")
        data = await r.json()
    tag = str(data.get("tag_name", ""))
    if parse_version(tag) is None or data.get("draft") or data.get("prerelease"):
        return None
    zip_url, sha_url = data.get("zipball_url"), None
    for a in data.get("assets", []):
        name = str(a.get("name", ""))
        if name.lower().endswith(".zip"):
            zip_url = a.get("browser_download_url") or zip_url
        elif name.lower().endswith(".zip.sha256"):
            sha_url = a.get("browser_download_url")
    return {"tag": tag, "name": str(data.get("name") or tag)[:100], "notes": str(data.get("body") or "")[:3000], "page": str(data.get("html_url", "")), "zip": zip_url, "sha": sha_url}


async def download(session, url, dest, limit=MAX_DOWNLOAD):
    """Download a file from GitHub with a size limit. Redirects are followed by hand and must stay on GitHub. Returns the SHA-256."""
    for _ in range(5):
        if not host_ok(url):
            raise ValueError("download address is not on GitHub")
        async with session.get(url, allow_redirects=False, timeout=aiohttp.ClientTimeout(total=300)) as r:
            if r.status in (301, 302, 303, 307, 308) and r.headers.get("Location"):
                url = str(r.url.join(URL(r.headers["Location"])))
                continue
            if r.status != 200:
                raise ValueError(f"download failed with status {r.status}")
            digest, size = hashlib.sha256(), 0
            dest = Path(dest)
            dest.parent.mkdir(parents=True, exist_ok=True)
            tmp = dest.with_suffix(".part")
            with open(tmp, "wb") as f:
                async for chunk in r.content.iter_chunked(65536):
                    size += len(chunk)
                    if size > limit:
                        f.close()
                        tmp.unlink(missing_ok=True)
                        raise ValueError("download is too large")
                    digest.update(chunk)
                    f.write(chunk)
            os.replace(tmp, dest)
            return digest.hexdigest()
    raise ValueError("too many redirects")


async def fetch_text(session, url, limit=4096):
    """Read a small text file from GitHub."""
    if not host_ok(url):
        raise ValueError("address is not on GitHub")
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as r:
        if r.status != 200:
            raise ValueError(f"status {r.status}")
        return (await r.content.read(limit)).decode("utf-8", "replace")


def expected_hash(text):
    """The SHA-256 from the first 64 hex characters of a checksum file."""
    m = re.search(r"\b([0-9a-fA-F]{64})\b", text or "")
    return m.group(1).lower() if m else None


def safe_name(name):
    """True if an archive entry stays inside the target folder."""
    if not name or name.startswith(("/", "\\")) or "\\" in name or re.match(r"[A-Za-z]:", name):
        return False
    return ".." not in PurePosixPath(name).parts


def inspect(zf):
    """Check an archive and return its root folder prefix. Raises ValueError for anything unsafe or not GuardBot."""
    infos = zf.infolist()
    if not infos or len(infos) > MAX_FILES:
        raise ValueError("the archive is empty or has too many files")
    if sum(i.file_size for i in infos) > MAX_UNPACKED:
        raise ValueError("the archive is too large when unpacked")
    for i in infos:
        if not safe_name(i.filename):
            raise ValueError(f"unsafe path in the archive: {i.filename[:80]}")
        mode = i.external_attr >> 16
        if mode and stat.S_ISLNK(mode):
            raise ValueError("the archive contains a link")
    roots = {i.filename.split("/", 1)[0] for i in infos}
    root = roots.pop() + "/" if len(roots) == 1 else ""
    names = {i.filename for i in infos}
    if f"{root}main.py" not in names or f"{root}guardbot/__init__.py" not in names:
        raise ValueError("this archive is not GuardBot")
    return root


def archive_version(zf, root):
    """The version written in guardbot/__init__.py inside an archive."""
    text = zf.read(f"{root}guardbot/__init__.py").decode("utf-8", "replace")
    m = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    return m.group(1) if m else None


def targets(zf, root):
    """The files of an archive that an update may write, as (archive name, relative path)."""
    out = []
    for i in zf.infolist():
        if i.is_dir() or not i.filename.startswith(root):
            continue
        rel = i.filename[len(root):]
        if rel and rel.split("/", 1)[0] not in PROTECTED:
            out.append((i.filename, rel))
    return out


def backup(app_dir, rel_paths, dest):
    """Save the current version of the files an update will replace. Returns the path of the backup archive."""
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in rel_paths:
            p = Path(app_dir) / rel
            if p.is_file():
                z.write(p, rel)
    return dest


def apply(zf, root, app_dir):
    """Write the files of an archive into the program folder, one by one and never outside it. Returns the relative paths written."""
    base = Path(app_dir).resolve()
    written = []
    for name, rel in targets(zf, root):
        target = (base / rel).resolve()
        if base not in target.parents:
            raise ValueError(f"path leaves the program folder: {rel}")
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(target.name + ".new")
        with zf.open(name) as src, open(tmp, "wb") as out:
            shutil.copyfileobj(src, out)
        if rel in ("start.sh",):
            os.chmod(tmp, 0o755)
        os.replace(tmp, target)
        written.append(rel)
    return written


def restore(backup_zip, app_dir, written):
    """Put the saved files back. Files that did not exist before are removed again."""
    base = Path(app_dir).resolve()
    with zipfile.ZipFile(backup_zip) as z:
        saved = set(z.namelist())
        for rel in written:
            target = (base / rel).resolve()
            if base not in target.parents:
                continue
            if rel in saved:
                with z.open(rel) as src, open(target, "wb") as out:
                    shutil.copyfileobj(src, out)
            else:
                target.unlink(missing_ok=True)


def starts(app_dir, timeout=90):
    """True if the installed code can be imported by a fresh Python process."""
    code = "import guardbot.core, guardbot.dashboard, guardbot.updater"
    try:
        r = subprocess.run([sys.executable, "-c", code], cwd=str(app_dir), capture_output=True, timeout=timeout, env={**os.environ, "PYTHONPATH": str(app_dir)})
    except (OSError, subprocess.TimeoutExpired):
        return False
    return r.returncode == 0


def install_requirements(app_dir, timeout=900):
    """Install the packages of requirements.txt. Returns True on success."""
    try:
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "-r", str(Path(app_dir) / "requirements.txt")], capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return r.returncode == 0


async def stage(session, release, data_dir, require_checksum=False):
    """Download a release into data/update and check it. Returns the path of the verified archive."""
    if not release.get("zip"):
        raise ValueError("the release has no archive")
    dest = Path(data_dir) / "update" / f"{re.sub(r'[^0-9A-Za-z.-]', '_', release['tag'])}.zip"
    got = await download(session, release["zip"], dest)
    if release.get("sha"):
        want = expected_hash(await fetch_text(session, release["sha"]))
        if want != got:
            dest.unlink(missing_ok=True)
            raise ValueError("the checksum of the download does not match")
    elif require_checksum:
        dest.unlink(missing_ok=True)
        raise ValueError("the release has no checksum file and update.require_checksum is on")
    with zipfile.ZipFile(dest) as z:
        root = inspect(z)
        version = archive_version(z, root)
    if parse_version(version) != parse_version(release["tag"]):
        dest.unlink(missing_ok=True)
        raise ValueError("the version inside the archive does not match the release tag")
    return dest


def install(archive, app_dir, data_dir, current=None):
    """Install a staged archive. Backs up the replaced files, installs new packages, checks that the code starts and rolls back if not.
    Returns (ok, message). Blocking, run it in a thread."""
    app_dir = Path(app_dir).resolve()
    with zipfile.ZipFile(archive) as z:
        root = inspect(z)
        version = archive_version(z, root)
        if not is_newer(version, current):
            return False, f"version {version} is not newer than the installed one"
        files = targets(z, root)
        old_req = (app_dir / "requirements.txt").read_text(encoding="utf-8") if (app_dir / "requirements.txt").exists() else ""
        saved = backup(app_dir, [rel for _, rel in files], Path(data_dir) / "update" / f"backup-{current or __version__}-{int(time.time())}.zip")
        written = []
        try:
            written = apply(z, root, app_dir)
            new_req = (app_dir / "requirements.txt").read_text(encoding="utf-8") if (app_dir / "requirements.txt").exists() else ""
            if new_req != old_req and not install_requirements(app_dir):
                raise ValueError("the new packages could not be installed")
            if not starts(app_dir):
                raise ValueError("the new version does not start")
        except (ValueError, OSError, zipfile.BadZipFile) as exc:
            log.error("update failed, rolling back: %s", exc)
            restore(saved, app_dir, written)
            return False, f"update failed and was rolled back: {exc}"
    return True, f"version {version} installed, the old files are saved in data/update/{saved.name}"


def new_session():
    """HTTP session that only reaches public addresses."""
    return make_session()


async def run_install(archive, app_dir, data_dir):
    """Install without blocking the bot."""
    return await asyncio.to_thread(install, archive, app_dir, data_dir)
