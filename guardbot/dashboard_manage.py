"""Dashboard pages for commands, skills, the AI connection and the profile of the bot. Every change needs the CSRF token and is written to the audit log."""

import base64
import binascii
import io
import json
import logging
import re
import time
from typing import Any, Optional

import discord
from aiohttp import web
from discord import app_commands
from PIL import Image

from . import ai as ailib, layout, panels as panellib, skills as engine
from .defaults import COMMAND_MODULES, FALLBACK_PERMS, PROTECTED_COMMANDS
from .i18n import say as i18n_say

log = logging.getLogger(__name__)

MAX_IMAGE = 8 * 1024 * 1024
MAX_IMAGE_BODY = 12 * 1024 * 1024
MAX_PIXELS = 40_000_000
IMAGE_TYPES = {"png": b"\x89PNG\r\n\x1a\n", "jpeg": b"\xff\xd8\xff", "gif": b"GIF8", "webp": b"RIFF"}
ALIAS_RE = re.compile(r"[a-z0-9_-]{1,30}")
EDIT_GAP = 30
OWNER_CACHE = 600


def parse_image(value: Any) -> bytes:
    """Decode a data URL with a PNG, JPEG, GIF or WebP picture. Raises ValueError with a reason."""
    if not isinstance(value, str):
        raise ValueError("the picture is missing")
    m = re.fullmatch(r"data:image/(png|jpeg|gif|webp);base64,([A-Za-z0-9+/=\s]+)", value)
    if not m:
        raise ValueError("use a PNG, JPEG, GIF or WebP picture")
    try:
        raw = base64.b64decode(m.group(2), validate=False)
    except (binascii.Error, ValueError):
        raise ValueError("the picture is damaged")
    if not 100 <= len(raw) <= MAX_IMAGE:
        raise ValueError("the picture must be smaller than 8 MB")
    kind = m.group(1)
    if not raw.startswith(IMAGE_TYPES[kind]) or (kind == "webp" and raw[8:12] != b"WEBP"):
        raise ValueError("the file does not match its type")
    try:
        with Image.open(io.BytesIO(raw)) as im:
            if im.width * im.height > MAX_PIXELS:
                raise ValueError("the picture has too many pixels")
            im.verify()
    except (OSError, Image.DecompressionBombError):
        raise ValueError("the picture cannot be read")
    return raw


def command_rows(bot: Any, guild: Optional[Any] = None) -> list[dict]:
    """Every command the bot has as one row: slash commands, context menus, text commands, and with a guild the state there."""
    rows: dict[str, dict] = {}
    owners = [(bot, "")]
    if getattr(bot, "music_bot", None) is not None:
        owners.append((bot.music_bot, "Guard Music"))
    for owner, name in owners:
        for root in owner.tree.get_commands(type=discord.AppCommandType.chat_input):
            nodes = root.commands if (getattr(root, "extras", None) or {}).get("gb_container") else [root]
            for node in nodes:
                key = layout.command_key(node)
                subs = [c.qualified_name for c in node.walk_commands()] if isinstance(node, app_commands.Group) else []
                rows[key] = {"key": key, "kind": "slash", "path": "/" + layout.slash_path(owner, key), "description": str(node.description)[:200], "subcommands": subs[:60], "subcount": len(subs), "bot": name}
        for kind in (discord.AppCommandType.message, discord.AppCommandType.user):
            for menu in owner.tree.get_commands(type=kind):
                rows.setdefault(menu.name, {"key": menu.name, "kind": "menu", "path": menu.name, "description": "Context menu", "subcommands": [], "subcount": 0, "bot": name})
        for cmd in owner.commands:
            row = rows.setdefault(cmd.name, {"key": cmd.name, "kind": "text", "path": cmd.name, "description": str(cmd.short_doc or cmd.help or "")[:200], "subcommands": [], "subcount": 0, "bot": name})
            row["text"] = True
    out = []
    order = {"slash": 0, "text": 1, "menu": 2}
    for key in sorted(rows, key=lambda k: (order.get(rows[k]["kind"], 3), k)):
        row = rows[key]
        row["module"] = COMMAND_MODULES.get(key)
        row["permission"] = FALLBACK_PERMS.get(key)
        row["protected"] = key in PROTECTED_COMMANDS
        if guild is not None:
            cfg = bot.cfg(guild.id)
            rule = cfg["perms"].get(key, {})
            row["enabled"] = key not in cfg["disabled_commands"]
            row["module_on"] = bot.module_on(guild.id, row["module"]) if row["module"] else True
            row["roles"] = [str(r) for r in rule.get("roles", [])]
            row["deny_roles"] = [str(r) for r in rule.get("deny_roles", [])]
            row["aliases"] = sorted(a for a, target in cfg["aliases"].items() if target == key)
        out.append(row)
    return out


def known_commands(bot: Any) -> set[str]:
    """Names that may be switched or given permission rules."""
    keys = layout.all_keys(bot.tree) | {c.name for c in bot.commands}
    music = getattr(bot, "music_bot", None)
    if music is not None:
        keys |= layout.all_keys(music.tree) | {c.name for c in music.commands}
    return keys


class Manage:
    """The routes of these pages. Access checks, sessions and audit come from the dashboard."""

    def __init__(self, dash: Any):
        """Keep the dashboard."""
        self.dash, self.bot = dash, dash.bot
        self.owner_cache: tuple[float, set[int]] = (0.0, set())
        self.last_edit = 0.0

    def routes(self, app: web.Application) -> None:
        """Register the routes."""
        g = "/api/guild/{gid:\\d+}"
        app.router.add_get(g + "/commands", self.commands)
        app.router.add_post(g + "/commands/set", self.command_set)
        app.router.add_post(g + "/commands/alias", self.command_alias)
        app.router.add_get(g + "/skills", self.skills)
        app.router.add_post(g + "/skills/save", self.skill_save)
        app.router.add_post(g + "/skills/toggle", self.skill_toggle)
        app.router.add_post(g + "/skills/delete", self.skill_delete)
        app.router.add_get(g + "/ai", self.ai_info)
        app.router.add_post(g + "/ai/set", self.ai_set)
        app.router.add_post(g + "/ai/key", self.ai_key)
        app.router.add_post(g + "/ai/remove", self.ai_remove)
        app.router.add_get(g + "/profile", self.profile)
        app.router.add_post(g + "/profile/server", self.profile_server)
        app.router.add_post("/api/bot/profile", self.profile_global)
        app.router.add_get(g + "/panels", self.panels)
        app.router.add_get(g + "/panels/image/{pid:[0-9a-f]{16}}", self.panel_image)
        app.router.add_post(g + "/panels/image", self.panel_upload)
        app.router.add_post(g + "/panels/create", self.panel_create)
        app.router.add_post(g + "/panels/save", self.panel_save)
        app.router.add_post(g + "/panels/post", self.panel_post)
        app.router.add_post(g + "/panels/update", self.panel_update)
        app.router.add_post(g + "/panels/delete", self.panel_delete)

    # ---- commands

    async def commands(self, request: web.Request) -> web.Response:
        """All commands with their state on this server, plus tags and skills."""
        s = self.dash.require(request)
        guild = self.dash.guild_for(request, s, need="viewer")
        cfg = self.bot.cfg(guild.id)
        custom = [{"key": n, "kind": "tag", "uses": t.get("uses", 0)} for n, t in sorted(cfg["tags"]["items"].items())]
        custom += [{"key": n, "kind": "skill", "enabled": sp["enabled"], "uses": cfg["skills"]["meta"].get(n, {}).get("uses", 0), "description": sp["description"]} for n, sp in sorted(cfg["skills"]["items"].items())]
        return web.json_response({
            "prefix": self.bot.prefix_for(guild.id), "language": cfg["language"], "commands": command_rows(self.bot, guild), "custom": custom,
            "modules": {k: bool(v) for k, v in cfg["modules"].items()},
        })

    async def command_set(self, request: web.Request) -> web.Response:
        """Turn a command on or off and set which roles may or may not use it."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        key = data.get("key")
        if not isinstance(key, str) or key not in known_commands(self.bot):
            raise web.HTTPBadRequest(text="unknown command")
        cfg = self.bot.cfg(guild.id)
        role_ids = {r.id for r in guild.roles if not r.is_default()}
        self.bot.note_actor(guild.id, s["uid"], "dashboard")
        if "enabled" in data:
            if not isinstance(data["enabled"], bool):
                raise web.HTTPBadRequest(text="enabled must be true or false")
            if not data["enabled"] and key in PROTECTED_COMMANDS:
                raise web.HTTPUnprocessableEntity(text="this command cannot be turned off")
            lst = cfg["disabled_commands"]
            if data["enabled"] and key in lst:
                lst.remove(key)
            elif not data["enabled"] and key not in lst:
                lst.append(key)
                lst.sort()
            self.dash.audit(guild, s, f"command `{key}` is now {'on' if data['enabled'] else 'off'}")
        for field in ("roles", "deny_roles"):
            if field in data:
                ids = self.ids(data[field], role_ids)
                rule = cfg["perms"].setdefault(key, {})
                if ids:
                    rule[field] = ids
                else:
                    rule.pop(field, None)
                if not rule:
                    cfg["perms"].pop(key, None)
                self.dash.audit(guild, s, f"`{key}` {field}: {len(ids)} role(s)")
        return web.json_response({"ok": True})

    @staticmethod
    def ids(value: Any, allowed: set[int]) -> list[int]:
        """A list of role IDs given as numbers or digit strings, all of which must exist."""
        if not isinstance(value, list) or len(value) > 25:
            raise web.HTTPBadRequest(text="a list of at most 25 roles is needed")
        try:
            ids = sorted({int(v) for v in value})
        except (TypeError, ValueError):
            raise web.HTTPBadRequest(text="invalid role")
        if not set(ids) <= allowed:
            raise web.HTTPUnprocessableEntity(text="a role does not exist on this server")
        return ids

    async def command_alias(self, request: web.Request) -> web.Response:
        """Create or delete a short name for a text command."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        alias, target = data.get("alias"), data.get("command")
        if not isinstance(alias, str) or not ALIAS_RE.fullmatch(alias.lower()):
            raise web.HTTPBadRequest(text="the alias uses letters, digits, - and _")
        alias = alias.lower()
        aliases = self.bot.cfg(guild.id)["aliases"]
        if target in (None, ""):
            aliases.pop(alias, None)
            self.dash.audit(guild, s, f"alias `{alias}` removed")
            return web.json_response({"ok": True})
        if not isinstance(target, str) or self.bot.get_command(target) is None:
            raise web.HTTPUnprocessableEntity(text="that text command does not exist")
        if self.bot.get_command(alias) or alias in self.bot.cfg(guild.id)["tags"]["items"] or alias in self.bot.cfg(guild.id)["skills"]["items"]:
            raise web.HTTPUnprocessableEntity(text="that name is already used")
        if len(aliases) >= 100 and alias not in aliases:
            raise web.HTTPUnprocessableEntity(text="at most 100 aliases")
        aliases[alias] = target
        self.dash.audit(guild, s, f"alias `{alias}` now runs `{target}`")
        return web.json_response({"ok": True})

    # ---- skills

    def skills_cog(self) -> Any:
        """The skills cog, or a 503."""
        cog = self.bot.get_cog("Skills")
        if cog is None:
            raise web.HTTPServiceUnavailable(text="skills are not loaded")
        return cog

    async def skills(self, request: web.Request) -> web.Response:
        """All skills with their numbers, and a starter for each kind."""
        s = self.dash.require(request)
        guild = self.dash.guild_for(request, s, need="viewer")
        conf = self.bot.cfg(guild.id)["skills"]
        items = [{"spec": spec, "meta": conf["meta"].get(name, {}), "summary": engine.describe(spec)} for name, spec in sorted(conf["items"].items())]
        return web.json_response({
            "skills": items, "limit": engine.MAX_SKILLS, "module_on": self.bot.module_on(guild.id, "skills"),
            "starters": {k: engine.starter(k, "example") for k in engine.KINDS},
        })

    async def skill_save(self, request: web.Request) -> web.Response:
        """Validate a skill strictly and save it."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        try:
            spec = engine.clean(data.get("spec"))
        except engine.SpecError as exc:
            return web.json_response({"error": str(exc)}, status=422)
        cog = self.skills_cog()
        self.bot.note_actor(guild.id, s["uid"], "dashboard")
        err = cog.store(guild, spec, s["uid"], replace=True)
        if err:
            return web.json_response({"error": err}, status=422)
        self.dash.audit(guild, s, f"skill `{spec['name']}` saved ({engine.describe(spec)})")
        return web.json_response({"ok": True, "spec": spec})

    def skill_of(self, guild: Any, data: dict) -> dict:
        """The skill named in a request or a 404."""
        name = data.get("name")
        spec = self.bot.cfg(guild.id)["skills"]["items"].get(name) if isinstance(name, str) else None
        if spec is None:
            raise web.HTTPNotFound(text="no such skill")
        return spec

    async def skill_toggle(self, request: web.Request) -> web.Response:
        """Turn a skill on or off."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        spec = self.skill_of(guild, data)
        if not isinstance(data.get("enabled"), bool):
            raise web.HTTPBadRequest(text="enabled must be true or false")
        spec["enabled"] = data["enabled"]
        self.dash.audit(guild, s, f"skill `{spec['name']}` is now {'on' if spec['enabled'] else 'off'}")
        return web.json_response({"ok": True})

    async def skill_delete(self, request: web.Request) -> web.Response:
        """Delete a skill."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        spec = self.skill_of(guild, await self.dash.read_json(request))
        conf = self.bot.cfg(guild.id)["skills"]
        conf["items"].pop(spec["name"], None)
        conf["meta"].pop(spec["name"], None)
        self.dash.audit(guild, s, f"skill `{spec['name']}` deleted")
        return web.json_response({"ok": True})

    # ---- AI

    async def ai_info(self, request: web.Request) -> web.Response:
        """The AI settings of the server. The key itself is never sent, only whether one exists."""
        s = self.dash.require(request)
        guild = self.dash.guild_for(request, s, need="viewer")
        c = self.bot.ai.conf(guild.id)
        used, limit = self.bot.ai.budget(guild.id)
        return web.json_response({
            "providers": {k: {"label": v["label"], "model": v["model"]} for k, v in ailib.PROVIDERS.items()},
            "provider": c["provider"], "model": c["model"], "has_key": self.bot.ai.configured(guild.id), "module_on": self.bot.module_on(guild.id, "ai"),
            "daily_limit": c["daily_limit"], "used": used, "user_cooldown": c["user_cooldown"], "max_tokens": c["max_tokens"], "second_opinion": c["second_opinion"], "errors": c["errors"],
        })

    async def ai_set(self, request: web.Request) -> web.Response:
        """Change model and limits. The provider can only change together with a new key."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        c = self.bot.ai.conf(guild.id)
        limits = {"daily_limit": (1, 1000), "user_cooldown": (0, 3600), "max_tokens": (100, 4000)}
        for key, (low, high) in limits.items():
            if key in data:
                v = data[key]
                if isinstance(v, bool) or not isinstance(v, int) or not low <= v <= high:
                    raise web.HTTPUnprocessableEntity(text=f"{key} must be between {low} and {high}")
                c[key] = v
        if "second_opinion" in data:
            if not isinstance(data["second_opinion"], bool):
                raise web.HTTPBadRequest(text="second_opinion must be true or false")
            c["second_opinion"] = data["second_opinion"]
        if "model" in data:
            model = data["model"]
            if not isinstance(model, str) or not re.fullmatch(r"[A-Za-z0-9._:/-]{1,80}", model):
                raise web.HTTPUnprocessableEntity(text="invalid model name")
            c["model"] = model
        self.dash.audit(guild, s, "AI settings changed")
        return web.json_response({"ok": True})

    async def ai_key(self, request: web.Request) -> web.Response:
        """Store a key, write only. It is never sent back and never written to a log."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        try:
            self.bot.ai.set_key(guild.id, str(data.get("provider")), str(data.get("key", "")), str(data.get("model", "")))
        except ailib.AIError as exc:
            return web.json_response({"error": str(exc)}, status=422)
        self.bot.cfg(guild.id)["modules"]["ai"] = True
        self.dash.audit(guild, s, f"stored a key for {ailib.PROVIDERS[data['provider']]['label']}")
        return web.json_response({"ok": True})

    async def ai_remove(self, request: web.Request) -> web.Response:
        """Delete the key."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        self.bot.ai.remove_key(guild.id)
        self.dash.audit(guild, s, "deleted the AI key")
        return web.json_response({"ok": True})

    # ---- profile

    async def owners(self) -> set[int]:
        """The people who own the bot's application, from Discord, plus owner_ids in settings.json."""
        at, ids = self.owner_cache
        if time.time() - at < OWNER_CACHE and ids:
            return ids
        found = {int(x) for x in self.bot.settings.get("owner_ids", []) if str(x).isdigit()}
        try:
            info = await self.bot.application_info()
            if info.team:
                found.add(info.team.owner_id)
            elif info.owner:
                found.add(info.owner.id)
        except discord.HTTPException as exc:
            log.warning("could not read the owner of the application: %s", exc)
        self.owner_cache = (time.time(), found)
        return found

    async def profile(self, request: web.Request) -> web.Response:
        """The profile of the bot: global values for its owner, the server profile for everyone with access."""
        s = self.dash.require(request)
        guild = self.dash.guild_for(request, s, need="viewer")
        me = guild.me
        owner = s["uid"] in await self.owners()
        out: dict[str, Any] = {
            "owner": owner,
            "server": {"nick": me.nick or "", "avatar": me.display_avatar.url, "banner": me.guild_banner.url if getattr(me, "guild_banner", None) else None},
        }
        user = self.bot.user
        out["global"] = {"name": user.name, "avatar": user.display_avatar.url, "banner": user.banner.url if user.banner else None, "bio": None}
        if owner:
            try:
                out["global"]["bio"] = (await self.bot.application_info()).description
            except discord.HTTPException:
                pass
        return web.json_response(out)

    def throttle(self) -> None:
        """Discord limits profile changes. Allow one every few seconds."""
        wait = EDIT_GAP - (time.time() - self.last_edit)
        if wait > 0:
            raise web.HTTPTooManyRequests(text=f"wait {int(wait) + 1} seconds before the next profile change")
        self.last_edit = time.time()

    @staticmethod
    def discord_error(exc: discord.HTTPException) -> web.Response:
        """Show the reason Discord gave."""
        return web.json_response({"error": f"Discord refused it: {exc.text[:200]}"}, status=422)

    async def profile_server(self, request: web.Request) -> web.Response:
        """Change name, picture, banner and bio of the bot on this server only."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request, limit=MAX_IMAGE_BODY)
        fields: dict[str, Any] = {}
        try:
            if "nick" in data:
                nick = data["nick"]
                if nick is not None and (not isinstance(nick, str) or len(nick) > 32):
                    raise ValueError("the name has at most 32 characters")
                fields["nick"] = nick or None
            for key in ("avatar", "banner"):
                if key in data:
                    fields[key] = None if data[key] is None else parse_image(data[key])
            if "bio" in data:
                if data["bio"] is not None and (not isinstance(data["bio"], str) or len(data["bio"]) > 190):
                    raise ValueError("the bio has at most 190 characters")
                fields["bio"] = data["bio"] or None
        except ValueError as exc:
            return web.json_response({"error": str(exc)}, status=422)
        if not fields:
            raise web.HTTPBadRequest(text="nothing to change")
        self.throttle()
        try:
            await guild.me.edit(reason="Dashboard", **fields)
        except discord.HTTPException as exc:
            return self.discord_error(exc)
        self.dash.audit(guild, s, "changed the profile of the bot on this server: " + ", ".join(sorted(fields)))
        return web.json_response({"ok": True})

    async def profile_global(self, request: web.Request) -> web.Response:
        """Change name, picture, banner and bio of the bot everywhere. Only for the owner of the bot application."""
        s = self.dash.require(request, change=True)
        if s["uid"] not in await self.owners():
            raise web.HTTPForbidden(text="only the owner of the bot can change this")
        data = await self.dash.read_json(request, limit=MAX_IMAGE_BODY)
        fields: dict[str, Any] = {}
        try:
            if "name" in data:
                name = data["name"]
                if not isinstance(name, str) or not 2 <= len(name.strip()) <= 32:
                    raise ValueError("the name needs 2 to 32 characters")
                fields["username"] = name.strip()
            for key in ("avatar", "banner"):
                if key in data:
                    fields[key] = None if data[key] is None else parse_image(data[key])
            if "bio" in data and (not isinstance(data["bio"], str) or len(data["bio"]) > 400):
                raise ValueError("the bio has at most 400 characters")
        except ValueError as exc:
            return web.json_response({"error": str(exc)}, status=422)
        if not fields and "bio" not in data:
            raise web.HTTPBadRequest(text="nothing to change")
        self.throttle()
        try:
            if fields:
                await self.bot.user.edit(**fields)
            if "bio" in data:
                await self.bot.http.edit_application_info(reason=None, payload={"description": data["bio"]})
        except discord.HTTPException as exc:
            return self.discord_error(exc)
        log.info("dashboard: user %d changed the global profile of the bot: %s", s["uid"], ", ".join(sorted(list(fields) + (["bio"] if "bio" in data else []))))
        return web.json_response({"ok": True})

    # ---- panels

    def panels_cog(self) -> Any:
        """The panels cog, or a 503."""
        cog = self.bot.get_cog("Panels")
        if cog is None:
            raise web.HTTPServiceUnavailable(text="panels are not loaded")
        return cog

    async def panels(self, request: web.Request) -> web.Response:
        """All panels of the server with their pictures."""
        s = self.dash.require(request)
        guild = self.dash.guild_for(request, s, need="viewer")
        conf = self.bot.cfg(guild.id)["panels"]
        items = [{"id": pid, "panel": p} for pid, p in sorted(conf["items"].items(), key=lambda kv: kv[1]["name"])]
        images = {k: {"name": v.get("name", ""), "size": v.get("size", 0)} for k, v in conf.get("images", {}).items()}
        return web.json_response({"panels": items, "images": images, "templates": list(panellib.TEMPLATES), "module_on": self.bot.module_on(guild.id, "panels"),
                                  "limits": {"panels": panellib.MAX_PANELS, "sections": panellib.MAX_SECTIONS, "buttons": panellib.MAX_BUTTONS, "images": panellib.MAX_IMAGES}},
                                 dumps=lambda o: json.dumps(o, default=str))

    async def panel_image(self, request: web.Request) -> web.Response:
        """One stored picture."""
        s = self.dash.require(request)
        guild = self.dash.guild_for(request, s, need="viewer")
        path = panellib.image_path(self.bot.cfg(guild.id)["panels"], self.bot.store.dir, guild.id, request.match_info["pid"])
        if path is None:
            raise web.HTTPNotFound(text="no such picture")
        kind = {"png": "image/png", "jpg": "image/jpeg", "gif": "image/gif", "webp": "image/webp"}[path.suffix[1:]]
        return web.Response(body=path.read_bytes(), content_type=kind, headers={"Cache-Control": "private, max-age=3600"})

    async def panel_upload(self, request: web.Request) -> web.Response:
        """Store a picture and return its ID."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request, limit=MAX_IMAGE_BODY)
        try:
            raw = parse_image(data.get("image"))
            pid = panellib.store_image(self.bot.cfg(guild.id)["panels"], self.bot.store.dir, guild.id, raw, str(data.get("name", "")))
        except (ValueError, panellib.PanelError) as exc:
            return web.json_response({"error": str(exc)}, status=422)
        return web.json_response({"ok": True, "id": pid})

    async def panel_create(self, request: web.Request) -> web.Response:
        """A new panel from a template."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        kind = data.get("template", "empty")
        if kind not in panellib.TEMPLATES:
            raise web.HTTPBadRequest(text="unknown template")
        tr = lambda text: i18n_say(self.bot, guild, text)  # noqa: E731
        try:
            pid = self.panels_cog().save(guild, None, panellib.template(kind, str(data.get("name", "")).lower().strip(), tr=tr))
        except panellib.PanelError as exc:
            return web.json_response({"error": str(exc)}, status=422)
        self.dash.audit(guild, s, f"panel `{data.get('name')}` created")
        return web.json_response({"ok": True, "id": pid})

    def panel_id(self, guild: Any, data: dict) -> str:
        """The ID of an existing panel from a request, or a 404."""
        pid = str(data.get("id", ""))
        if pid not in self.bot.cfg(guild.id)["panels"]["items"]:
            raise web.HTTPNotFound(text="no such panel")
        return pid

    async def panel_save(self, request: web.Request) -> web.Response:
        """Validate and save a whole panel."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        pid = self.panel_id(guild, data)
        panel = data.get("panel")
        if isinstance(panel, dict):
            panel = dict(panel, messages=self.bot.cfg(guild.id)["panels"]["items"][pid]["messages"])
        try:
            self.panels_cog().save(guild, pid, panel)
        except panellib.PanelError as exc:
            return web.json_response({"error": str(exc)}, status=422)
        self.dash.audit(guild, s, f"panel `{panel['name']}` saved")
        return web.json_response({"ok": True})

    async def panel_post(self, request: web.Request) -> web.Response:
        """Post a panel in a channel."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        pid = self.panel_id(guild, data)
        try:
            channel = guild.get_channel(int(data.get("channel") or 0))
        except (TypeError, ValueError):
            channel = None
        try:
            await self.panels_cog().post(guild, pid, channel)
        except panellib.PanelError as exc:
            return web.json_response({"error": str(exc)}, status=422)
        except discord.HTTPException as exc:
            return self.discord_error(exc)
        self.dash.audit(guild, s, f"panel `{self.bot.cfg(guild.id)['panels']['items'][pid]['name']}` posted in <#{channel.id}>")
        return web.json_response({"ok": True})

    async def panel_update(self, request: web.Request) -> web.Response:
        """Change a posted panel in place."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        pid = self.panel_id(guild, await self.dash.read_json(request))
        try:
            await self.panels_cog().update(guild, pid)
        except panellib.PanelError as exc:
            return web.json_response({"error": str(exc)}, status=422)
        except discord.HTTPException as exc:
            return self.discord_error(exc)
        self.dash.audit(guild, s, f"panel `{self.bot.cfg(guild.id)['panels']['items'][pid]['name']}` updated")
        return web.json_response({"ok": True})

    async def panel_delete(self, request: web.Request) -> web.Response:
        """Delete a panel."""
        s = self.dash.require(request, change=True)
        guild = self.dash.guild_for(request, s, change=True)
        data = await self.dash.read_json(request)
        pid = self.panel_id(guild, data)
        name = self.bot.cfg(guild.id)["panels"]["items"][pid]["name"]
        await self.panels_cog().delete(guild, pid, bool(data.get("messages")))
        self.dash.audit(guild, s, f"panel `{name}` deleted")
        return web.json_response({"ok": True})
