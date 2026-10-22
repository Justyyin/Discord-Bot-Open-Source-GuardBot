"""Music library and queue: file naming, tag reading, scanning, searching and the play queue. No Discord code."""

import os
import random
import re
import unicodedata
from collections import deque
from dataclasses import dataclass
from pathlib import Path

try:
    import mutagen
except ImportError:  # the library still works without tags, using the folder names
    mutagen = None

AUDIO_EXT = {".flac", ".wav", ".aiff", ".aif", ".wv", ".ape", ".mp3", ".m4a", ".aac", ".ogg", ".opus", ".oga"}
LOSSLESS_EXT = {".flac", ".wav", ".aiff", ".aif", ".wv", ".ape"}
RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
TEMP_DIR = ".incoming"


def clean(text, fallback="Unknown"):
    """Make text safe as a single file or folder name on every system. Never returns a path separator or '..'."""
    text = unicodedata.normalize("NFC", str(text or ""))
    text = re.sub(r'[\x00-\x1f<>:"/\\|?*]', " ", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    if text.split(".")[0].upper() in RESERVED:
        text = "_" + text
    return text[:100].strip(" .") or fallback


def inside(root, path):
    """True if a path, after resolving links, lies inside the library folder."""
    try:
        return Path(path).resolve().is_relative_to(Path(root).resolve())
    except (OSError, ValueError):
        return False


def target_path(root, artist, album, title, track, ext):
    """Build music/<Artist>/<Album>/<NN - Title>.<ext> and add (2), (3)... if the file already exists."""
    folder = Path(root) / clean(artist, "Unknown Artist") / clean(album, "Singles")
    name = (f"{int(track):02d} - " if track else "") + clean(title, "Untitled")
    ext = ext if re.fullmatch(r"\.[a-z0-9]{2,5}", ext.lower()) else ".bin"
    path, n = folder / f"{name}{ext.lower()}", 2
    while path.exists():
        path = folder / f"{name} ({n}){ext.lower()}"
        n += 1
    return path


def resolve(root, rel):
    """Return the absolute path of a library file, or None if it is missing or outside the library."""
    path = (Path(root) / rel)
    if not path.is_file() or path.is_symlink() or not inside(root, path):
        return None
    return path.resolve()


def guess_from_path(rel):
    """Read artist, album and title from the folder structure Artist/Album/NN - Title.ext."""
    p = Path(rel)
    parts = p.parts
    title = re.sub(r"^\d{1,3}\s*[-._]\s*", "", p.stem)
    artist = parts[-3] if len(parts) >= 3 else (parts[0] if len(parts) == 2 else "")
    album = parts[-2] if len(parts) >= 3 else ""
    return artist, album, title


def _first(tags, key):
    """First value of a tag as text."""
    value = tags.get(key) if tags else None
    return str(value[0]).strip() if value else ""


def read_tags(path):
    """Read only what is really stored in a file: artist, album, title, track and technical data. Missing values stay empty."""
    out = {"artist": "", "album": "", "title": "", "track": 0, "length": 0.0, "rate": 0, "bits": 0, "bitrate": 0, "alac": False}
    if mutagen is None:
        return out
    try:
        f = mutagen.File(path, easy=True)
    except (mutagen.MutagenError, OSError):
        return out
    if f is None:
        return out
    tags = f.tags
    out["artist"] = _first(tags, "albumartist") or _first(tags, "artist")
    out["album"], out["title"] = _first(tags, "album"), _first(tags, "title")
    m = re.match(r"\d+", _first(tags, "tracknumber"))
    out["track"] = int(m.group()) if m else 0
    info = f.info
    out["length"] = float(getattr(info, "length", 0) or 0)
    out["rate"] = int(getattr(info, "sample_rate", 0) or 0)
    out["bits"] = int(getattr(info, "bits_per_sample", 0) or 0)
    out["bitrate"] = int(getattr(info, "bitrate", 0) or 0)
    out["alac"] = getattr(info, "codec", "") == "alac"
    return out


def read_entry(root, rel):
    """Build a library entry: tags first, then the folder structure Artist/Album/NN - Title."""
    path = Path(root) / rel
    artist, album, title = guess_from_path(rel)
    t = read_tags(path)
    ext = path.suffix.lower()
    return {
        "path": Path(rel).as_posix(), "artist": t["artist"] or artist, "album": t["album"] or album, "title": t["title"] or title,
        "track": t["track"], "length": t["length"], "ext": ext, "lossless": ext in LOSSLESS_EXT or t["alac"],
        "rate": t["rate"], "bits": t["bits"], "bitrate": t["bitrate"],
    }


def scan(root, cache=None):
    """Walk the library and return all audio files as entries. Unchanged files are taken from the cache."""
    root, cache, found = Path(root), cache if cache is not None else {}, []
    if not root.is_dir():
        return found
    seen = set()
    for folder, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            if Path(name).suffix.lower() not in AUDIO_EXT or name.startswith("."):
                continue
            full = Path(folder) / name
            rel = full.relative_to(root).as_posix()
            try:
                st = full.stat()
            except OSError:
                continue
            stamp = (st.st_mtime_ns, st.st_size)
            if rel not in cache or cache[rel][0] != stamp:
                cache[rel] = (stamp, read_entry(root, rel))
            seen.add(rel)
            found.append(cache[rel][1])
    for gone in set(cache) - seen:
        del cache[gone]
    return sorted(found, key=lambda e: (e["artist"].lower(), e["album"].lower(), e["track"], e["title"].lower()))


def search(entries, query, limit=25):
    """Find entries that contain every word of the query in artist, album, title or path. Title matches rank first."""
    words = [w for w in re.split(r"\s+", query.lower().strip()) if w]
    if not words:
        return []
    scored = []
    for e in entries:
        hay = f"{e['artist']} {e['album']} {e['title']} {e['path']}".lower()
        if all(w in hay for w in words):
            title = e["title"].lower()
            scored.append((-sum(w in title for w in words), -(query.lower().strip() == title), e["artist"].lower(), e["title"].lower(), e))
    scored.sort(key=lambda s: s[:4])
    return [s[4] for s in scored[:limit]]


def total_bytes(root):
    """Total size of all files in the library in bytes."""
    total = 0
    for folder, _, files in os.walk(root):
        for name in files:
            try:
                total += (Path(folder) / name).stat().st_size
            except OSError:
                continue
    return total


def quality(entry):
    """Describe the audio quality of a library entry for display."""
    ext = entry["ext"][1:].upper()
    if entry["lossless"]:
        rate = f" {entry['rate'] / 1000:g} kHz" if entry["rate"] else ""
        bits = f" / {entry['bits']} bit" if entry["bits"] else ""
        return f"{ext}{rate}{bits} (lossless)"
    kbps = f" {entry['bitrate'] // 1000} kbps" if entry["bitrate"] else ""
    return f"{ext}{kbps} (lossy)"


def fmt_time(seconds):
    """Format seconds as m:ss or h:mm:ss."""
    seconds = int(max(seconds or 0, 0))
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def parse_time(text):
    """Turn 90, 1:30 or 1:02:03 into seconds, or None."""
    parts = text.strip().split(":")
    if not 1 <= len(parts) <= 3 or not all(p.isdigit() for p in parts):
        return None
    total = 0
    for p in parts:
        total = total * 60 + int(p)
    return total


def bar(position, length, width=18):
    """A text progress bar."""
    if not length:
        return "-" * width
    filled = min(width - 1, int(width * position / length))
    return "=" * filled + "o" + "-" * (width - filled - 1)


@dataclass
class Track:
    """One entry of the queue."""

    title: str
    artist: str
    kind: str          # "local" (path inside the library) or "web" (page URL)
    ref: str
    length: float
    requester: int
    lossless: bool = False
    detail: str = ""


class Queue:
    """The play queue of one server with loop modes."""

    def __init__(self):
        """Start empty."""
        self.items = deque()
        self.current = None
        self.loop = "off"

    def __len__(self):
        """Number of waiting tracks."""
        return len(self.items)

    def add(self, track, front=False):
        """Append a track, or put it first."""
        (self.items.appendleft if front else self.items.append)(track)

    def count_by(self, user_id):
        """How many waiting tracks a user added."""
        return sum(1 for t in self.items if t.requester == user_id)

    def advance(self, skipped=False):
        """Pick the next track according to the loop mode and make it current. Returns it or None."""
        if self.loop == "track" and self.current and not skipped:
            return self.current
        if self.loop == "queue" and self.current:
            self.items.append(self.current)
        self.current = self.items.popleft() if self.items else None
        return self.current

    def shuffle(self):
        """Mix the waiting tracks."""
        mixed = list(self.items)
        random.shuffle(mixed)
        self.items = deque(mixed)

    def remove(self, number):
        """Remove the waiting track with this number (1 is next). Returns it or None."""
        if not 1 <= number <= len(self.items):
            return None
        track = self.items[number - 1]
        del self.items[number - 1]
        return track

    def clear(self):
        """Remove all waiting tracks and return how many there were."""
        n = len(self.items)
        self.items.clear()
        return n

    def total_length(self):
        """Total length of the waiting tracks in seconds."""
        return sum(t.length or 0 for t in self.items)
