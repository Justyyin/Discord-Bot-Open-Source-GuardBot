"""Downloads and metadata of the music cog: link extraction, tags and moving files into the library. No Discord objects."""

import logging
import shutil
from pathlib import Path

from . import musiclib as ml

try:
    import yt_dlp
except ImportError:  # link playback and downloads are reported as unavailable
    yt_dlp = None

log = logging.getLogger(__name__)

NET_INPUT = "-reconnect 1 -reconnect_streaming 1 -reconnect_delay_max 5 -protocol_whitelist http,https,tcp,tls,crypto"
LOSSLESS_CODECS = ("flac", "alac", "wav", "pcm", "ape", "wavpack")
INDEX_TTL = 120
RESUME_WITHIN = 900
PAGE = 10
FORMATS = ("best", "flac", "mp3", "opus", "m4a")


class YdlLogger:
    """Sends the output of yt-dlp to the normal log."""

    def debug(self, msg):
        """Debug output is dropped, yt-dlp prints progress here."""
        return None

    def info(self, msg):
        """Information is dropped."""
        return None

    def warning(self, msg):
        """Warnings go to the log at info level."""
        log.info("yt-dlp: %s", msg)

    def error(self, msg):
        """Errors go to the log as warnings."""
        log.warning("yt-dlp: %s", msg)


GENERIC = {"on": True}


def base_options(ffmpeg, **extra):
    """Common yt-dlp options: quiet, time-limited and without local file access. The generic extractor can be switched off with music_generic in settings.json."""
    opts = {"quiet": True, "no_warnings": True, "noprogress": True, "socket_timeout": 20, "retries": 3, "logger": YdlLogger(), "ffmpeg_location": ffmpeg if ffmpeg != "ffmpeg" else None, "ignoreerrors": False}
    if not GENERIC["on"]:
        opts["allowed_extractors"] = ["default", "-generic"]
    opts.update(extra)
    return opts


def extract(url, ffmpeg, playlist=False, limit=50, search=False):
    """Read the metadata of a link or search. Runs in a thread. Playlists are listed without resolving every entry."""
    opts = base_options(ffmpeg, format="bestaudio/best", noplaylist=not playlist, playlistend=limit, extract_flat="in_playlist" if playlist else False, skip_download=True, default_search="auto" if search else None)
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


def clean_artist(name):
    """Remove the ' - Topic' suffix that YouTube adds to automatically generated artist channels."""
    name = (name or "").strip()
    return name[:-8].strip() if name.endswith(" - Topic") else name


def write_tags(path, artist, album, title, track):
    """Write the tags that are missing in a file. Failures are logged and ignored, the folder structure still works."""
    if ml.mutagen is None:
        return
    try:
        f = ml.mutagen.File(path, easy=True)
        if f is None:
            return
        if f.tags is None:
            f.add_tags()
        for key, value in (("artist", artist), ("album", album), ("title", title), ("tracknumber", str(track) if track else "")):
            if value and not f.tags.get(key):
                f.tags[key] = value
        f.save()
    except (ml.mutagen.MutagenError, OSError, NotImplementedError, KeyError) as exc:
        log.info("could not write tags to %s: %s", Path(path).name, exc)


def download_job(url, folder, ffmpeg, fmt, playlist, limit, max_seconds, max_mb):
    """Download the audio of a link into a temporary folder. Runs in a thread. Returns [(file, info)]."""
    post = [{"key": "FFmpegExtractAudio", "preferredcodec": fmt, "preferredquality": "0" if fmt != "mp3" else "320"}] if fmt != "best" else []
    opts = base_options(
        ffmpeg, format="bestaudio/best", outtmpl=str(Path(folder) / "%(id)s.%(ext)s"), restrictfilenames=True, noplaylist=not playlist,
        playlistend=limit, max_filesize=max_mb * 1024 * 1024, postprocessors=post,
        match_filter=yt_dlp.utils.match_filter_func(f"!is_live & duration <=? {max_seconds}"),
    )
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    entries = [e for e in (info.get("entries") or [info]) if e]
    out = []
    for e in entries:
        done = e.get("requested_downloads") or []
        if done and Path(done[0]["filepath"]).is_file():
            out.append((Path(done[0]["filepath"]), e))
    return out


def file_into_library(root, source, info):
    """Move a downloaded file to music/<Artist>/<Album>/<NN - Title>.<ext> and fill missing tags. Returns (library entry, source codec).

    Tags that are stored in the file win, then the metadata of the website."""
    tags = ml.read_tags(source)
    artist = clean_artist(tags["artist"]) or clean_artist(info.get("artist") or info.get("album_artist") or info.get("creator") or info.get("uploader") or info.get("channel"))
    album = tags["album"] or info.get("album") or ""
    title = tags["title"] or info.get("track") or info.get("title") or source.stem
    track = tags["track"] or info.get("track_number") or 0
    dest = ml.target_path(root, artist, album, title, track, source.suffix)
    if not ml.inside(root, dest):
        raise ValueError("refusing to write outside the library")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(dest))
    write_tags(dest, artist, album, title, track)
    return ml.read_entry(root, dest.relative_to(Path(root)).as_posix()), info.get("acodec") or "unknown"
