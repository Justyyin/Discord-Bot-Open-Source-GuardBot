"""Dashboard pages for the music player and the look of the dashboard, and the optional brand icons of the footer."""

import logging
import re
from pathlib import Path
from typing import Any

import discord
from aiohttp import web

from . import dashlook, musicbot
from .dashboard_manage import MAX_IMAGE_BODY, parse_image
from .panels import PanelError
from .plugins import CATEGORIES, PLUGINS

log = logging.getLogger(__name__)

BRAND = Path(__file__).resolve().parent / "web" / "brand"
ACTIONS = ("join", "add", "playlist", "folder", "pause", "resume", "skip", "stop", "leave", "shuffle", "clear", "loop", "volume", "remove")


class Extra:
    """The routes of these pages. Access checks, sessions and audit come from the dashboard."""

    def __init__(self, dash: Any):
        """Keep the dashboard."""
        self.dash, self.bot = dash, dash.bot

    def routes(self, app: web.Application) -> None:
        """Register the routes."""
        g = "/api/guild/{gid:\\d+}"
        app.router.add_get(g + "/music", self.music)
        app.router.add_post(g + "/music/control", self.music_control)
        app.router.add_post(g + "/music/playlist", self.music_playlist)
        app.router.add_post(g + "/look", self.look_save)
        app.router.add_post(g + "/look/wallpaper", self.look_wallpaper)
        app.router.add_get(g + "/look/wallpaper/{name:[0-9a-f]{16}\\.(png|jpg|gif|webp)}", self.look_wallpaper_file)
        app.router.add_get("/static/brand/{name:(discord|github)}.svg", self.brand)

    # ---- music

    def music_cog(self) -> Any:
        """The music cog, on Guard Music or on GuardBot."""
        return self.bot.music_cog()

    async def music(self, request: web.Request) -> web.Response:
        """Player, queue, playlists and which bot plays the music."""
        s = self.dash.require(request)
        guild = self.dash.guild_for(request, s, need="viewer")
        mb = getattr(self.bot, "music_bot", None)
        info: dict[str, Any] = {"second_bot": mb is not None, "enabled_in_settings": bool(musicbot.settings_of(self.bot.settings)["enabled"])}
        if mb is not None:
            ready = mb.is_ready()
            info.update({
                "bot_name": str(mb.user.name) if mb.user else "Guard Music", "bot_avatar": mb.user.display_avatar.url if mb.user else None,
                "online": ready, "on_server": bool(ready and mb.get_guild(guild.id)), "invite": mb.invite_url(),
            })
        else:
            info.update({"bot_name": str(self.bot.user.name) if self.bot.user else "GuardBot", "bot_avatar": self.bot.user.display_avatar.url if self.bot.user else None, "online": True, "on_server": True, "invite": None})
        cog = self.music_cog()
        target = (mb.get_guild(guild.id) if mb is not None else guild) if cog else None
        info["module_on"] = self.bot.module_on(guild.id, "music")
        info["player"] = cog.snapshot(target) if cog and target else None
        if info["player"] is None:
            conf = self.bot.cfg(guild.id)["music"]
            info["playlists"] = [{"name": k, "count": len(v.get("tracks", [])), "updated": v.get("updated", 0)} for k, v in sorted(conf.get("playlists", {}).items(), key=lambda kv: kv[0].casefold())]
        name = request.query.get("playlist")
        if name:
            for key, data in self.bot.cfg(guild.id)["music"].get("playlists", {}).items():
                if key.casefold() == name.casefold():
                    info["playlist"] = {"name": key, "tracks": data.get("tracks", [])[:500]}
                    break
        return web.json_response(info)

    async def music_control(self, request: web.Request) -> web.Response:
        """Control the player. Moderators and administrators may do this."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True, need="mod")
        data = await self.dash.read_json(request)
        action, value = data.get("action"), data.get("value")
        if action not in ACTIONS:
            raise web.HTTPBadRequest(text="unknown action")
        if not self.bot.module_on(guild.id, "music"):
            return web.json_response({"error": "the music module is off"}, status=409)
        cog = self.music_cog()
        mb = getattr(self.bot, "music_bot", None)
        target = mb.get_guild(guild.id) if mb is not None else guild
        if cog is None or target is None:
            return web.json_response({"error": "the music bot is not on this server"}, status=409)
        try:
            ok, text = await cog.remote(target, s["uid"], action, value)
        except (discord.DiscordException, ValueError, OSError) as exc:
            log.warning("dashboard music control failed: %s", exc)
            return web.json_response({"error": str(exc)[:300]}, status=500)
        if action in ("join", "leave", "stop", "clear"):
            self.dash.audit(guild, s, f"music: {action}")
        return web.json_response({"ok": ok, "message": text}, status=200 if ok else 409)

    async def music_playlist(self, request: web.Request) -> web.Response:
        """Create, replace, rename or delete a saved playlist. Moderators and administrators may do this."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True, need="mod")
        data = await self.dash.read_json(request)
        conf = self.bot.cfg(guild.id)["music"]
        lists = conf.setdefault("playlists", {})
        name = re.sub(r"\s+", " ", str(data.get("name") or "")).strip()[:40]
        if not name:
            return web.json_response({"error": "give the playlist a name"}, status=422)
        found = next((k for k in lists if k.casefold() == name.casefold()), None)
        if data.get("delete"):
            if found is None:
                raise web.HTTPNotFound(text="no such playlist")
            del lists[found]
            if conf.get("autoplay", "").casefold() == found.casefold():
                conf["autoplay"] = ""
            self.dash.audit(guild, s, f"music: playlist `{found}` deleted")
            return web.json_response({"ok": True})
        cog = self.music_cog()
        if cog is None:
            return web.json_response({"error": "music is not loaded"}, status=409)
        tracks = data.get("tracks", [])
        if not isinstance(tracks, list) or len(tracks) > 500:
            return web.json_response({"error": "at most 500 tracks"}, status=422)
        rename = re.sub(r"\s+", " ", str(data.get("rename") or "")).strip()[:40]
        if rename and found and rename.casefold() != found.casefold():
            if any(k.casefold() == rename.casefold() for k in lists):
                return web.json_response({"error": "a playlist with this name exists"}, status=422)
            lists[rename] = lists.pop(found)
            if conf.get("autoplay", "").casefold() == found.casefold():
                conf["autoplay"] = rename
            name = rename
        add = str(data.get("add") or "").strip()[:500]
        if add:
            found_tracks, error = await cog.find_tracks(guild.id, s["uid"], add)
            if error:
                return web.json_response({"error": error}, status=422)
            tracks = tracks + [{"title": t.title, "artist": t.artist, "kind": t.kind, "ref": t.ref, "length": t.length} for t in found_tracks]
        key, problem = cog.save_playlist(guild, s["uid"], name, tracks[:500])
        if problem:
            return web.json_response({"error": problem}, status=422)
        self.dash.audit(guild, s, f"music: playlist `{key}` saved")
        return web.json_response({"ok": True, "name": key})

    # ---- look

    async def look_save(self, request: web.Request) -> web.Response:
        """Store colours, menus and tabs. Administrators only."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        cfg = self.bot.cfg(guild.id)
        try:
            cfg["look"] = dashlook.clean(data.get("look"), set(PLUGINS), {c[0] for c in CATEGORIES}, cfg.get("look"))
        except dashlook.LookError as exc:
            return web.json_response({"error": str(exc)}, status=422)
        self.dash.audit(guild, s, "dashboard look changed")
        return web.json_response({"ok": True, "look": cfg["look"]})

    async def look_wallpaper(self, request: web.Request) -> web.Response:
        """Upload or remove the wallpaper. Administrators only."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request, limit=MAX_IMAGE_BODY)
        look = self.bot.cfg(guild.id)["look"]
        if data.get("remove"):
            dashlook.remove_wallpaper(look, self.bot.store.dir, guild.id)
            self.dash.audit(guild, s, "dashboard wallpaper removed")
            return web.json_response({"ok": True, "wallpaper": None})
        try:
            name = dashlook.store_wallpaper(look, self.bot.store.dir, guild.id, parse_image(data.get("image")))
        except (ValueError, PanelError) as exc:
            return web.json_response({"error": str(exc)}, status=422)
        self.dash.audit(guild, s, "dashboard wallpaper changed")
        return web.json_response({"ok": True, "wallpaper": name})

    async def look_wallpaper_file(self, request: web.Request) -> web.Response:
        """The wallpaper, only for signed-in users of the server."""
        s = self.dash.require(request)
        guild = self.dash.guild_for(request, s, need="viewer")
        look = self.bot.cfg(guild.id)["look"]
        path = dashlook.wallpaper_path(look, self.bot.store.dir, guild.id)
        if path is None or path.name != request.match_info["name"]:
            raise web.HTTPNotFound(text="no wallpaper")
        kind = {"png": "image/png", "jpg": "image/jpeg", "gif": "image/gif", "webp": "image/webp"}[path.suffix[1:]]
        return web.Response(body=path.read_bytes(), content_type=kind)

    async def brand(self, request: web.Request) -> web.Response:
        """An icon file for the footer links that the owner placed in guardbot/web/brand/. Missing files give 404 and the page shows its own icon."""
        path = BRAND / f"{request.match_info['name']}.svg"
        if not path.is_file() or path.stat().st_size > 64 * 1024:
            raise web.HTTPNotFound(text="no icon")
        return web.Response(body=path.read_bytes(), content_type="image/svg+xml")
