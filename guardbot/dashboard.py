"""Web dashboard that runs inside the bot. Login with Discord, access only for members who manage a server the bot is connected to."""

import asyncio
import hmac
import ipaddress
import json
import logging
import math
import os
import secrets
import time
from datetime import datetime, timezone
from collections import deque
from pathlib import Path
from urllib.parse import urlencode, urlparse

import aiohttp
import discord
from aiohttp import web

from . import __version__, configio, i18n, layout
from .defaults import DEFAULTS, MODULES, PROTECTED_COMMANDS

log = logging.getLogger(__name__)

WEB = Path(__file__).resolve().parent / "web"
STATIC = {"/static/app.js": ("app.js", "text/javascript"), "/static/app.css": ("app.css", "text/css"), "/static/favicon.svg": ("favicon.svg", "image/svg+xml")}
DISCORD = "https://discord.com"
SESSION_SECONDS = 8 * 3600
STATE_SECONDS = 600
MAX_SESSIONS = 1000
MAX_BODY = 262_144
MAX_TEXT = 2000
MAX_LIST = 500
COOKIE = "gb_session"
STATE_COOKIE = "gb_state"
# Settings that are state of the bot, not choices of the administrator
HIDDEN_LEAVES = {"items", "next", "last", "hits", "saved", "active", "role_saved", "counter", "pending", "open", "hashes", "texts", "members"}
HIDDEN_TOP = {"aliases", "perms", "case_counter", "reaction_roles", "chanlocks", "notify", "tags", "polls", "giveaways", "reminders", "autoresponder", "sticky", "rolemenus", "schedule", "feeds", "activity", "stats", "disabled_commands", "prefix", "language", "modules", "history", "roletemplates", "temproles", "exceptions", "reasons", "dashboard_access"}
SECRET_WORDS = ("token", "secret", "webhook", "password")
# Access levels: viewers read, moderators change the settings of these sections, administrators change everything
LEVELS = {"none": 0, "viewer": 1, "mod": 2, "admin": 3}
MOD_SECTIONS = {"mod", "automod", "antiscam", "raid", "jail", "probation", "watchlist", "nicknames", "stickyroles", "exceptions", "welcome", "verify", "tickets", "reports", "suggestions", "modmail", "appeals"}
CSP = "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' https://cdn.discordapp.com data:; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"


def is_loopback(host):
    """True for localhost and loopback addresses."""
    if host in ("localhost", ""):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


TITLES = {
    "xp": "XP and levels", "antiscam": "Anti-scam", "automod": "AutoMod", "antinuke": "Anti-nuke", "mod": "Moderation", "jail": "Gulag", "raid": "Raid protection",
    "modwatch": "Moderator limits", "permaudit": "Permission audit", "tempvoice": "Temporary voice", "log": "Log channels", "log_options": "Log options", "debug": "Diagnostics",
    "welcome": "Welcome and goodbye", "boosters": "Boosters", "verify": "Verification", "modmail": "Mod-mail", "appeals": "Ban appeals", "reports": "Reports",
}


CATEGORIES = {
    "general": "Basics", "modules": "Basics", "log": "Basics", "log_options": "Basics", "debug": "Basics", "backup": "Basics", "privacy": "Basics", "invites": "Basics",
    "mod": "Moderation", "jail": "Moderation", "automod": "Moderation", "modmail": "Moderation", "appeals": "Moderation", "reports": "Moderation",
    "stickyroles": "Moderation", "nicknames": "Moderation", "watchlist": "Moderation", "approval": "Moderation",
    "antiscam": "Security", "antinuke": "Security", "raid": "Security", "lockdown": "Security", "verify": "Security", "probation": "Security", "modwatch": "Security", "permaudit": "Security",
    "welcome": "Community", "boosters": "Community", "birthday": "Community", "xp": "Community", "economy": "Community", "tickets": "Community", "starboard": "Community",
    "tempvoice": "Community", "suggestions": "Community", "counting": "Community", "music": "Community",
    "rules": "Structure and team", "archive": "Structure and team", "team": "Structure and team", "applications": "Structure and team",
}

INFO = {
    "general": ("Prefix, language and turned off commands of this server.", "Prefix, Sprache und abgeschaltete Befehle dieses Servers."),
    "modules": ("Turn whole features on or off.", "Ganze Funktionen ein- oder ausschalten."),
    "log": ("Which channel receives which kind of log entry.", "Welcher Kanal welche Art von Protokolleintrag bekommt."),
    "log_options": ("What the logs contain and what they leave out.", "Was die Protokolle enthalten und was sie auslassen."),
    "debug": ("Error reports, usage statistics and diagnostics.", "Fehlerberichte, Nutzungsstatistik und Diagnose."),
    "backup": ("Automatic backups of roles, channels and emojis.", "Automatische Sicherungen von Rollen, Kanälen und Emojis."),
    "privacy": ("How long data of members who left is kept.", "Wie lange Daten ausgetretener Mitglieder aufbewahrt werden."),
    "invites": ("Invite tracking: who joined with which invite.", "Einladungs-Tracking: wer mit welcher Einladung beigetreten ist."),
    "mod": ("Warnings, escalation, expiry, reasons and appeals of punishments.", "Verwarnungen, Eskalation, Ablauf und Gründe von Strafen."),
    "jail": ("The gulag: a role and a room for members under watch.", "Der Gulag: Rolle und Raum für Mitglieder unter Beobachtung."),
    "automod": ("Automatic rules for spam, links, words, caps and mentions.", "Automatische Regeln gegen Spam, Links, Wörter, Großschreibung und Erwähnungen."),
    "modmail": ("Members write to the team through the bot.", "Mitglieder schreiben dem Team über den Bot."),
    "appeals": ("Ban appeals from the main server.", "Einsprüche gegen Banns vom Hauptserver."),
    "reports": ("Members report messages to the staff.", "Mitglieder melden Nachrichten an das Team."),
    "stickyroles": ("Restore roles, timeouts and mutes when a member returns.", "Rollen, Timeouts und Mutes wiederherstellen, wenn ein Mitglied zurückkehrt."),
    "nicknames": ("Name moderation: dehoist, banned words, automatic renaming.", "Namensmoderation: Sonderzeichen, verbotene Wörter, automatisches Umbenennen."),
    "watchlist": ("Silent watch list. The team is alerted at the first message.", "Stille Beobachtungsliste. Das Team wird bei der ersten Nachricht gewarnt."),
    "approval": ("Four-eyes approval: a second moderator must agree to serious actions.", "Vier-Augen-Freigabe: Ein zweiter Moderator muss schweren Aktionen zustimmen."),
    "antiscam": ("Detects fake giveaways and crypto scams in text and images.", "Erkennt Fake-Gewinnspiele und Krypto-Betrug in Text und Bildern."),
    "antinuke": ("Stops mass deletions, permission grants and new bots.", "Stoppt Massenlöschungen, Rechtevergabe und neue Bots."),
    "raid": ("Detects join swarms and reacts automatically.", "Erkennt Beitrittswellen und reagiert automatisch."),
    "lockdown": ("Close the server or channels in an emergency.", "Server oder Kanäle im Notfall schließen."),
    "verify": ("New members must verify before they get access.", "Neue Mitglieder müssen sich verifizieren, bevor sie Zugang bekommen."),
    "probation": ("New members may not post links or files at first.", "Neue Mitglieder dürfen zunächst keine Links oder Dateien posten."),
    "modwatch": ("Limits for moderators: too many bans or kicks trigger an alert.", "Grenzen für Moderatoren: zu viele Bans oder Kicks lösen Alarm aus."),
    "permaudit": ("Reports roles with dangerous permissions.", "Meldet Rollen mit gefährlichen Rechten."),
    "welcome": ("Welcome and goodbye messages, auto roles and direct messages.", "Begrüßung, Verabschiedung, Auto-Rollen und Direktnachrichten."),
    "boosters": ("Thank members who boost the server.", "Mitgliedern danken, die den Server boosten."),
    "birthday": ("Birthday role and message.", "Geburtstagsrolle und Nachricht."),
    "xp": ("Levels, XP rates, level roles and the level-up message.", "Level, XP-Raten, Level-Rollen und die Level-Up-Nachricht."),
    "economy": ("Currency, daily reward, work and shop.", "Währung, tägliche Belohnung, Arbeit und Shop."),
    "tickets": ("Support tickets with types, panel and transcripts.", "Support-Tickets mit Arten, Panel und Protokollen."),
    "starboard": ("Best messages are collected in a channel.", "Die besten Nachrichten werden in einem Kanal gesammelt."),
    "tempvoice": ("Members create their own temporary voice rooms.", "Mitglieder erstellen eigene temporäre Sprachräume."),
    "suggestions": ("Members suggest, others vote, the team decides.", "Mitglieder schlagen vor, andere stimmen ab, das Team entscheidet."),
    "counting": ("Counting game in one channel.", "Zählspiel in einem Kanal."),
    "music": ("Music player, library and downloads.", "Musikplayer, Bibliothek und Downloads."),
    "rules": ("Rules with accept button, version and reminders.", "Regeln mit Annehmen-Knopf, Version und Erinnerungen."),
    "archive": ("Report or move inactive channels.", "Inaktive Kanäle melden oder verschieben."),
    "team": ("Team statistics, weekly report and duty roster.", "Teamstatistik, Wochenbericht und Dienstplan."),
    "applications": ("Staff applications with a form and a team vote.", "Team-Bewerbungen mit Formular und Abstimmung."),
}


def build_stats(cfg, cases, count=30, today=None):
    """Numbers for the charts: messages, joins, leaves and cases per day over the last days, plus case totals per type."""
    from .cogs.community.activity import last_days
    keys = last_days({}, count, today)
    days = cfg["activity"]["days"]
    first = keys[0]
    per_day = {k: 0 for k in keys}
    totals = {}
    for c in cases:
        day = datetime.fromtimestamp(c["ts"], timezone.utc).strftime("%Y-%m-%d")
        if day >= first:
            totals[c["type"]] = totals.get(c["type"], 0) + 1
            if day in per_day:
                per_day[day] += 1
    return {
        "days": keys,
        "messages": [days.get(k, {}).get("msgs", 0) for k in keys],
        "joins": [days.get(k, {}).get("joins", 0) for k in keys],
        "leaves": [days.get(k, {}).get("leaves", 0) for k in keys],
        "cases": [per_day[k] for k in keys],
        "case_types": totals,
    }


def label(key):
    """Readable name of a setting key."""
    return key.replace("_", " ").capitalize()


def id_kind(leaf, default):
    """Which kind of Discord object a setting holds, from its name: channel, role or None. Lists give 'channels' or 'roles'."""
    if isinstance(default, list):
        if leaf.endswith("channels"):
            return "channels"
        if leaf.endswith("roles"):
            return "roles"
        return None
    if default is None or isinstance(default, int):
        if leaf in ("channel", "category", "hub") or leaf.endswith(("_channel", "_category")):
            return "channel"
        if leaf == "role" or leaf.endswith("_role"):
            return "role"
    return None


def field_spec(path, default):
    """Describe one setting that the dashboard may edit, or None when it is internal or not a simple value."""
    leaf = path.rsplit(".", 1)[-1]
    if leaf in HIDDEN_LEAVES or any(w in leaf for w in SECRET_WORDS) or path in configio.RUNTIME or ".limits" in path:
        return None
    kind = id_kind(leaf, default)
    if kind:
        return {"path": path, "label": label(leaf), "type": kind}
    if isinstance(default, bool):
        return {"path": path, "label": label(leaf), "type": "bool"}
    if isinstance(default, int):
        return {"path": path, "label": label(leaf), "type": "int"}
    if isinstance(default, float):
        return {"path": path, "label": label(leaf), "type": "float"}
    if isinstance(default, str) or default is None:
        return {"path": path, "label": label(leaf), "type": "text", "long": isinstance(default, str) and len(default) > 40}
    if isinstance(default, list) and not (default and isinstance(default[0], (list, dict))):
        numbers = bool(default) and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in default)
        return {"path": path, "label": label(leaf), "type": "numbers" if numbers else "list"}
    return None


def walk(default, prefix=""):
    """Yield (path, default value) for every leaf of the default settings, in order."""
    for key, value in default.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict) and value:
            yield from walk(value, path)
        elif not isinstance(value, dict):
            yield path, value


def specs():
    """All editable settings as {path: spec}."""
    out = {}
    for path, default in walk(DEFAULTS):
        if path.split(".")[0] in HIDDEN_TOP:
            continue
        spec = field_spec(path, default)
        if spec:
            out[path] = spec
    return out


SPECS = specs()


def get_path(cfg, path):
    """Read a dotted path of a settings dict."""
    for part in path.split("."):
        cfg = cfg[part]
    return cfg


def set_path(cfg, path, value):
    """Write a dotted path of a settings dict."""
    parts = path.split(".")
    for part in parts[:-1]:
        cfg = cfg[part]
    cfg[parts[-1]] = value


def show(spec, value):
    """Convert a stored value into JSON for the page. IDs become strings because JavaScript cannot hold 64-bit numbers."""
    if spec["type"] in ("channel", "role"):
        return str(value) if value else None
    if spec["type"] in ("channels", "roles"):
        return [str(v) for v in value]
    return value


def number(value, whole):
    """Validate a number from the page."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or abs(value) > 10**12:
        raise ValueError("not a valid number")
    if whole:
        if value != int(value):
            raise ValueError("a whole number is needed")
        return int(value)
    return float(value)


def to_id(value, valid):
    """Turn an ID string from the page into an int and check that it exists on the server."""
    if not isinstance(value, str) or not value.isdigit() or int(value) not in valid:
        raise ValueError("unknown channel or role")
    return int(value)


def coerce(spec, value, channels, roles, default):
    """Check a value from the page against the type of the setting and return what is stored."""
    t = spec["type"]
    if t == "bool":
        if not isinstance(value, bool):
            raise ValueError("true or false is needed")
        return value
    if t in ("int", "float"):
        return number(value, t == "int")
    if t == "text":
        if value is None or value == "":
            if default is None:
                return None
            return ""
        if not isinstance(value, str) or len(value) > MAX_TEXT:
            raise ValueError("text is too long")
        return value
    if t == "channel" or t == "role":
        if value in (None, ""):
            return None
        return to_id(value, channels if t == "channel" else roles)
    if t in ("channels", "roles"):
        if not isinstance(value, list) or len(value) > MAX_LIST:
            raise ValueError("a list is needed")
        return sorted({to_id(v, channels if t == "channels" else roles) for v in value})
    if t == "numbers":
        if not isinstance(value, list) or len(value) != len(default):
            raise ValueError(f"{len(default)} numbers are needed")
        return [number(v, isinstance(d, int)) for v, d in zip(value, default)]
    if t == "list":
        if not isinstance(value, list) or len(value) > MAX_LIST or not all(isinstance(v, str) and len(v) <= 200 for v in value):
            raise ValueError("a list of short texts is needed")
        return [v for v in value if v.strip()]
    raise ValueError("this setting cannot be changed here")


def describe(cfg, commands):
    """Build the settings page of a server: list of sections with fields and current values."""
    sections = []
    general = [
        {"path": "prefix", "label": "Command prefix", "type": "text", "value": cfg["prefix"]},
        {"path": "language", "label": "Language of replies", "type": "choice", "value": cfg["language"], "choices": [[k, v] for k, v in i18n.LANGUAGES.items()]},
        {"path": "disabled_commands", "label": "Turned off commands", "type": "commands", "value": list(cfg["disabled_commands"]), "choices": [c for c in commands if c not in PROTECTED_COMMANDS]},
    ]
    sections.append({"key": "general", "title": "General", "fields": general})
    sections.append({"key": "modules", "title": "Modules", "fields": [{"path": f"modules.{k}", "label": label(k), "type": "bool", "value": bool(cfg["modules"].get(k, v))} for k, v in MODULES.items()]})
    tops = {}
    for path, spec in SPECS.items():
        tops.setdefault(path.split(".")[0], []).append(spec)
    for top, items in tops.items():
        fields = []
        for spec in items:
            try:
                value = show(spec, get_path(cfg, spec["path"]))
            except KeyError:
                continue
            fields.append(dict(spec, value=value, group=" / ".join(label(p) for p in spec["path"].split(".")[1:-1])))
        if fields:
            sections.append({"key": top, "title": TITLES.get(top, label(top)), "fields": fields})
    for s in sections:
        s["category"] = CATEGORIES.get(s["key"], "More")
        info = INFO.get(s["key"])
        if info:
            s["info"], s["info_de"] = info
    return sections


def apply_change(cfg, path, value, channels, roles, commands):
    """Validate one change and write it. Returns the value as shown on the page. Raises ValueError with a reason."""
    if path == "prefix":
        if value in (None, ""):
            cfg["prefix"] = None
        elif isinstance(value, str) and 1 <= len(value) <= 5 and not any(c.isspace() or c in "`@#" for c in value):
            cfg["prefix"] = value
        else:
            raise ValueError("prefix must be 1 to 5 characters without spaces")
        return cfg["prefix"]
    if path == "language":
        if value not in i18n.LANGUAGES:
            raise ValueError("unknown language")
        cfg["language"] = value
        return value
    if path == "disabled_commands":
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            raise ValueError("a list is needed")
        bad = [v for v in value if v in PROTECTED_COMMANDS or v not in commands]
        if bad:
            raise ValueError("these commands cannot be turned off: " + ", ".join(bad[:5]))
        cfg["disabled_commands"] = sorted(set(value))
        return cfg["disabled_commands"]
    if path.startswith("modules."):
        name = path.split(".", 1)[1]
        if name not in MODULES or not isinstance(value, bool):
            raise ValueError("unknown module or value")
        cfg["modules"][name] = value
        return value
    spec = SPECS.get(path)
    if spec is None:
        raise ValueError("this setting cannot be changed here")
    default = get_path(DEFAULTS, path)
    new = coerce(spec, value, channels, roles, default)
    set_path(cfg, path, new)
    top = path.split(".")[0]
    problems = configio.validate({top: cfg[top]})
    if problems:
        raise ValueError(problems[0])
    return show(spec, new)


class Dashboard:
    """The web server of the dashboard."""

    def __init__(self, bot):
        """Read the settings. The dashboard is off unless dashboard.enabled is true in settings.json."""
        self.bot = bot
        c = bot.settings.get("dashboard", {}) or {}
        self.enabled = bool(c.get("enabled", False))
        self.host = str(c.get("host", "127.0.0.1"))
        self.port = int(c.get("port", 8080) or 8080)
        self.public = str(c.get("public_url") or f"http://localhost:{self.port}").rstrip("/")
        self.insecure_ok = bool(c.get("allow_insecure_http", False))
        self.trust_proxy = bool(c.get("trust_proxy", False))
        parsed = urlparse(self.public)
        self.secure = parsed.scheme == "https"
        self.hosts = {parsed.netloc.lower()}
        if is_loopback(self.host):
            self.hosts |= {f"localhost:{self.port}", f"127.0.0.1:{self.port}"}
        self.origins = {f"{parsed.scheme}://{parsed.netloc}".lower()} | ({f"http://localhost:{self.port}", f"http://127.0.0.1:{self.port}"} if is_loopback(self.host) else set())
        self.sessions = {}
        self.hits = {}
        self.runner = None
        self.http = None

    # ---- start and stop

    def problem(self):
        """Why the dashboard cannot start, or None."""
        if not os.getenv("DISCORD_CLIENT_SECRET"):
            return "DISCORD_CLIENT_SECRET is missing in .env (OAuth2 page of your application in the Developer Portal)"
        if not is_loopback(self.host) and not self.secure and not self.insecure_ok:
            return "the dashboard may only listen on a public address behind HTTPS: set dashboard.public_url to an https address (reverse proxy) or use host 127.0.0.1 with an SSH tunnel"
        if urlparse(self.public).scheme not in ("http", "https") or not urlparse(self.public).netloc:
            return "dashboard.public_url is not a valid address"
        return None

    async def start(self):
        """Start listening if the dashboard is enabled. Never raises, a broken dashboard must not stop the bot."""
        if not self.enabled:
            return
        why = self.problem()
        if why:
            log.error("dashboard not started: %s", why)
            return
        try:
            app = self.make_app()
            self.runner = web.AppRunner(app, access_log=None)
            await self.runner.setup()
            await web.TCPSite(self.runner, self.host, self.port).start()
        except OSError as exc:
            log.error("dashboard not started: %s", exc)
            self.runner = None
            return
        log.info("dashboard on %s (listening on %s:%d). Add %s/callback as redirect in the Developer Portal", self.public, self.host, self.port, self.public)

    async def stop(self):
        """Stop listening."""
        if self.runner:
            await self.runner.cleanup()
            self.runner = None

    def make_app(self):
        """Create the web application with its routes and the security middleware."""
        app = web.Application(middlewares=[self.guard], client_max_size=MAX_BODY)
        app.router.add_get("/", self.page)
        for path in STATIC:
            app.router.add_get(path, self.static)
        app.router.add_get("/login", self.login)
        app.router.add_get("/callback", self.callback)
        app.router.add_post("/api/logout", self.logout)
        app.router.add_get("/api/me", self.me)
        app.router.add_get("/api/guild/{gid:\\d+}", self.guild_info)
        app.router.add_post("/api/guild/{gid:\\d+}/set", self.guild_set)
        app.router.add_get("/api/guild/{gid:\\d+}/cases", self.guild_cases)
        app.router.add_get("/api/guild/{gid:\\d+}/stats", self.guild_stats)
        app.router.add_get("/api/guild/{gid:\\d+}/export", self.guild_export)
        app.router.add_post("/api/guild/{gid:\\d+}/import", self.guild_import)
        return app

    # ---- security

    def client_ip(self, request):
        """Address of the visitor. Behind a reverse proxy (trust_proxy) the last entry of X-Forwarded-For."""
        if self.trust_proxy:
            fwd = request.headers.get("X-Forwarded-For", "")
            if fwd:
                return fwd.split(",")[-1].strip()
        return request.remote or "?"

    def limited(self, ip, bucket, limit):
        """True if a visitor made more than `limit` requests in the last minute for a kind of request."""
        now = time.time()
        q = self.hits.setdefault((ip, bucket), deque())
        while q and now - q[0] > 60:
            q.popleft()
        if len(q) >= limit:
            return True
        q.append(now)
        if len(self.hits) > 5000:
            for key in [k for k, v in self.hits.items() if not v or now - v[-1] > 60]:
                del self.hits[key]
        return False

    @web.middleware
    async def guard(self, request, handler):
        """Every request: allowed host name (stops DNS rebinding), rate limit, origin check for changes and security headers."""
        try:
            if request.host.lower() not in self.hosts:
                raise web.HTTPBadRequest(text="unknown host")
            ip = self.client_ip(request)
            login = request.path in ("/login", "/callback")
            if self.limited(ip, "login" if login else "api", 20 if login else 300):
                raise web.HTTPTooManyRequests(text="too many requests")
            if request.method == "POST":
                origin = (request.headers.get("Origin") or "").lower()
                if origin not in self.origins:
                    raise web.HTTPForbidden(text="origin not allowed")
            resp = await handler(request)
        except web.HTTPException as exc:
            self.harden(exc)
            raise
        self.harden(resp)
        return resp

    def harden(self, resp):
        """Add the security headers to a response."""
        resp.headers["Content-Security-Policy"] = CSP
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["X-Frame-Options"] = "DENY"
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        resp.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        resp.headers["Cache-Control"] = "no-store"
        if self.secure:
            resp.headers["Strict-Transport-Security"] = "max-age=31536000"

    def cookie_name(self, name):
        """With HTTPS the cookies use the __Host- prefix, so no other site or subdomain can set them."""
        return f"__Host-{name}" if self.secure else name

    def set_cookie(self, resp, name, value, seconds):
        """Set a cookie that scripts cannot read and that is only sent to this site."""
        resp.set_cookie(self.cookie_name(name), value, max_age=seconds, httponly=True, secure=self.secure, samesite="Lax", path="/")

    def session_of(self, request):
        """The valid session of a request, or None."""
        token = request.cookies.get(self.cookie_name(COOKIE), "")
        s = self.sessions.get(token)
        if s is None:
            return None
        if s["exp"] < time.time():
            self.sessions.pop(token, None)
            return None
        return s

    def require(self, request, change=False):
        """Return the session or raise 401. Changes also need the CSRF token of the session."""
        s = self.session_of(request)
        if s is None:
            raise web.HTTPUnauthorized(text="login required")
        if change and not hmac.compare_digest(request.headers.get("X-CSRF-Token", ""), s["csrf"]):
            raise web.HTTPForbidden(text="bad token")
        return s

    def ready(self):
        """True while the bot is connected to Discord."""
        return self.bot.is_ready() and not self.bot.is_closed()

    def guild_for(self, request, session, change=False, need="admin"):
        """The server of a request if the bot is connected to it and the user has at least the needed level. Raises 503, 404 or 403."""
        if not self.ready():
            raise web.HTTPServiceUnavailable(text="the bot is not connected")
        guild = self.bot.get_guild(int(request.match_info["gid"]))
        if guild is None or guild.unavailable:
            raise web.HTTPNotFound(text="the bot is not on this server")
        if self.level(guild, session["uid"]) < LEVELS[need]:
            raise web.HTTPForbidden(text="you need the Manage Server permission" if need == "admin" else "you have no access to this server")
        return guild

    def level(self, guild, uid):
        """Access level of a user on a server right now: 3 administrator, 2 moderator, 1 viewer, 0 none. The levels below administrator come from roles set with /admin dashaccess."""
        if self.manages(guild, uid):
            return LEVELS["admin"]
        member = guild.get_member(uid)
        if member is None:
            return LEVELS["none"]
        access = self.bot.cfg(guild.id)["dashboard_access"]
        roles = {r.id for r in member.roles}
        if roles & set(access["mod_roles"]):
            return LEVELS["mod"]
        if roles & set(access["viewer_roles"]):
            return LEVELS["viewer"]
        return LEVELS["none"]

    @staticmethod
    def manages(guild, uid):
        """True if the user is the owner or has Administrator or Manage Server on the server right now."""
        if guild.owner_id == uid:
            return True
        member = guild.get_member(uid)
        if member is None:
            return False
        p = member.guild_permissions
        return p.administrator or p.manage_guild

    def new_session(self, user):
        """Create a session for a Discord user and return its token."""
        now = time.time()
        for token in [t for t, s in self.sessions.items() if s["exp"] < now]:
            del self.sessions[token]
        while len(self.sessions) >= MAX_SESSIONS:
            self.sessions.pop(next(iter(self.sessions)))
        token = secrets.token_urlsafe(32)
        self.sessions[token] = {"uid": int(user["id"]), "name": str(user.get("global_name") or user.get("username") or "user")[:80], "avatar": user.get("avatar"), "csrf": secrets.token_urlsafe(24), "exp": now + SESSION_SECONDS}
        return token

    # ---- pages and login

    async def page(self, request):
        """The single page of the dashboard."""
        return web.Response(body=(WEB / "index.html").read_bytes(), content_type="text/html", charset="utf-8")

    async def static(self, request):
        """Fixed files, only the ones listed in STATIC."""
        name, kind = STATIC[request.path]
        return web.Response(body=(WEB / name).read_bytes(), content_type=kind)

    async def login(self, request):
        """Send the visitor to Discord. The state value is also kept in a cookie to stop forged logins."""
        if not self.ready():
            raise web.HTTPServiceUnavailable(text="the bot is not connected")
        state = secrets.token_urlsafe(24)
        query = urlencode({"client_id": self.bot.application_id, "redirect_uri": self.public + "/callback", "response_type": "code", "scope": "identify", "state": state, "prompt": "none"})
        resp = web.HTTPFound(f"{DISCORD}/oauth2/authorize?{query}")
        self.set_cookie(resp, STATE_COOKIE, state, STATE_SECONDS)
        raise resp

    async def exchange(self, code):
        """Trade the code for the Discord user. The access token is revoked at once, it is never stored."""
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout, trust_env=False) as http:
            data = {"client_id": str(self.bot.application_id), "client_secret": os.getenv("DISCORD_CLIENT_SECRET", ""), "grant_type": "authorization_code", "code": code, "redirect_uri": self.public + "/callback"}
            async with http.post(f"{DISCORD}/api/v10/oauth2/token", data=data) as r:
                if r.status != 200:
                    raise ValueError("token request refused")
                token = (await r.json())["access_token"]
            try:
                async with http.get(f"{DISCORD}/api/v10/users/@me", headers={"Authorization": f"Bearer {token}"}) as r:
                    if r.status != 200:
                        raise ValueError("user request refused")
                    user = await r.json()
            finally:
                try:
                    await http.post(f"{DISCORD}/api/v10/oauth2/token/revoke", data={"client_id": data["client_id"], "client_secret": data["client_secret"], "token": token})
                except (aiohttp.ClientError, asyncio.TimeoutError):
                    pass
        return user

    async def callback(self, request):
        """Finish the login: check the state, get the user and start a session."""
        cookie = request.cookies.get(self.cookie_name(STATE_COOKIE), "")
        state = request.query.get("state", "")
        code = request.query.get("code", "")
        if not cookie or not hmac.compare_digest(cookie, state) or not code or len(code) > 200:
            raise web.HTTPBadRequest(text="login failed, start again at the dashboard")
        try:
            user = await self.exchange(code)
            int(user["id"])
        except (ValueError, KeyError, aiohttp.ClientError, asyncio.TimeoutError) as exc:
            log.info("dashboard login failed: %s", exc)
            raise web.HTTPBadRequest(text="login failed, start again at the dashboard")
        resp = web.HTTPFound("/")
        self.set_cookie(resp, COOKIE, self.new_session(user), SESSION_SECONDS)
        resp.del_cookie(self.cookie_name(STATE_COOKIE), path="/")
        raise resp

    async def logout(self, request):
        """End the session."""
        s = self.require(request, change=True)
        for token in [t for t, v in self.sessions.items() if v is s]:
            del self.sessions[token]
        resp = web.json_response({"ok": True})
        resp.del_cookie(self.cookie_name(COOKIE), path="/")
        return resp

    # ---- api

    def commands(self):
        """Names of the top-level commands the bot has."""
        return sorted(layout.all_keys(self.bot.tree))

    async def me(self, request):
        """The user and the servers they may manage. Only servers where the bot is connected are listed."""
        s = self.require(request)
        if not self.ready():
            raise web.HTTPServiceUnavailable(text="the bot is not connected")
        guilds = [
            {"id": str(g.id), "name": g.name, "icon": g.icon.with_size(64).url if g.icon else None}
            for g in self.bot.guilds
            if not g.unavailable and self.level(g, s["uid"]) >= LEVELS["viewer"]
        ]
        guilds.sort(key=lambda g: g["name"].lower())
        avatar = f"https://cdn.discordapp.com/avatars/{s['uid']}/{s['avatar']}.png?size=64" if s["avatar"] else None
        return web.json_response({"user": {"name": s["name"], "avatar": avatar}, "csrf": s["csrf"], "guilds": guilds, "version": __version__})

    async def guild_info(self, request):
        """Overview, channels, roles and all settings of one server."""
        s = self.require(request)
        guild = self.guild_for(request, s, need="viewer")
        level = self.level(guild, s["uid"])
        cfg = self.bot.cfg(guild.id)
        channels = [{"id": str(c.id), "name": c.name, "kind": "category" if isinstance(c, discord.CategoryChannel) else "voice" if isinstance(c, (discord.VoiceChannel, discord.StageChannel)) else "text"} for c in sorted(guild.channels, key=lambda c: (c.position, c.id))]
        roles = [{"id": str(r.id), "name": r.name} for r in sorted(guild.roles, key=lambda r: -r.position) if not r.is_default()]
        modules = cfg["modules"]
        return web.json_response({
            "id": str(guild.id), "name": guild.name, "icon": guild.icon.with_size(128).url if guild.icon else None,
            "members": guild.member_count, "cases": len(self.bot.store.cases(guild.id)), "modules_on": sum(1 for k in MODULES if modules.get(k, MODULES[k])), "modules_total": len(MODULES),
            "latency_ms": round(self.bot.latency * 1000) if math.isfinite(self.bot.latency) else None,
            "channels": channels, "roles": roles, "sections": self.mark_editable(describe(cfg, self.commands()), level),
            "level": next(k for k, v in LEVELS.items() if v == level),
            "module_status": [{"name": k, "on": on, "setup": setup} for k, (on, setup) in sorted(configio.module_status(cfg).items())],
        })

    @staticmethod
    def mark_editable(sections, level):
        """Tell the page which sections the user may change."""
        for s in sections:
            s["editable"] = level >= LEVELS["admin"] or (level >= LEVELS["mod"] and s["key"] in MOD_SECTIONS)
        return sections

    async def read_json(self, request):
        """Read a JSON object from the body."""
        if request.content_type != "application/json":
            raise web.HTTPUnsupportedMediaType(text="JSON is needed")
        try:
            data = await request.json()
        except ValueError:
            raise web.HTTPBadRequest(text="invalid JSON")
        if not isinstance(data, dict):
            raise web.HTTPBadRequest(text="an object is needed")
        return data

    def audit(self, guild, session, text):
        """Write a change to the log channel of the server and to the bot log."""
        log.info("dashboard: %s (%d) in %s: %s", session["name"], session["uid"], guild.id, text)
        e = discord.Embed(title="Dashboard change", description=f"{session['name']} (`{session['uid']}`): {text}"[:1000], color=discord.Color.blurple())
        try:
            self.bot.log(guild, "security", e)
        except Exception as exc:  # the log must never break a change
            log.warning("dashboard audit log failed: %s", exc)

    async def guild_set(self, request):
        """Change one or more settings. Each change is checked, the first problem stops and is reported."""
        s = self.require(request, change=True)
        guild = self.guild_for(request, s, change=True, need="mod")
        level = self.level(guild, s["uid"])
        data = await self.read_json(request)
        changes = data.get("changes")
        if not isinstance(changes, list) or not 1 <= len(changes) <= 50:
            raise web.HTTPBadRequest(text="changes must be a list of 1 to 50 entries")
        cfg = self.bot.cfg(guild.id)
        channels = {c.id for c in guild.channels}
        roles = {r.id for r in guild.roles if not r.is_default()}
        commands = set(self.commands())
        done, errors = {}, {}
        for ch in changes:
            if not isinstance(ch, dict) or not isinstance(ch.get("path"), str):
                raise web.HTTPBadRequest(text="invalid change")
            path = ch["path"]
            if level < LEVELS["admin"] and path.split(".")[0] not in MOD_SECTIONS:
                errors[path] = "this setting needs the Manage Server permission"
                continue
            self.bot.note_actor(guild.id, s["uid"], "dashboard")
            try:
                done[path] = apply_change(cfg, path, ch.get("value"), channels, roles, commands)
            except ValueError as exc:
                errors[path] = str(exc)
                continue
            self.audit(guild, s, f"`{path}` is now `{json.dumps(done[path], ensure_ascii=False)[:200]}`")
        return web.json_response({"saved": done, "errors": errors}, status=200 if not errors else 422)

    async def guild_cases(self, request):
        """The latest moderation cases, read only."""
        s = self.require(request)
        guild = self.guild_for(request, s, need="viewer")
        cases = self.bot.store.cases(guild.id)[-100:][::-1]
        out = [{"id": c["id"], "type": c["type"], "user": c["user_name"], "mod": c.get("mod_name", ""), "reason": str(c["reason"])[:300], "ts": c["ts"], "active": c.get("active", True)} for c in cases]
        return web.json_response({"cases": out})

    async def guild_stats(self, request):
        """Numbers for the charts of the overview, read only."""
        s = self.require(request)
        guild = self.guild_for(request, s, need="viewer")
        try:
            count = min(90, max(7, int(request.query.get("days", "30"))))
        except ValueError:
            count = 30
        return web.json_response(build_stats(self.bot.cfg(guild.id), self.bot.store.cases(guild.id), count))

    async def guild_export(self, request):
        """Download the portable settings as a file."""
        s = self.require(request)
        guild = self.guild_for(request, s)
        body = json.dumps(configio.export_config(self.bot.cfg(guild.id)), indent=2, ensure_ascii=False)
        return web.Response(text=body, content_type="application/json", headers={"Content-Disposition": f'attachment; filename="guardbot-{guild.id}.json"'})

    async def guild_import(self, request):
        """Replace the settings with an exported file after validation. Runtime state of the server is kept."""
        s = self.require(request, change=True)
        guild = self.guild_for(request, s, change=True)
        raw = await request.read()
        payload, problems = configio.parse(raw)
        if problems:
            return web.json_response({"errors": problems[:10]}, status=422)
        cfg = self.bot.cfg(guild.id)
        new = configio.apply_import(cfg, payload)
        cfg.clear()
        cfg.update(new)
        self.bot.note_actor(guild.id, s["uid"], "dashboard import")
        self.audit(guild, s, "imported a settings file")
        return web.json_response({"ok": True})
