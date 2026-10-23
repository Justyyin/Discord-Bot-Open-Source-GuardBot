"""Settings of the bot itself: prefix, language, modules, permissions, logs, debugging."""

from typing import Any

from .base import LOG_CATEGORIES, MODULES

SPEC: dict[str, Any] = {
    "prefix": None,
    "language": "en",
    "modules": dict(MODULES),
    "disabled_commands": [],
    "aliases": {},
    "perms": {},
    "case_counter": 0,
    "log": {c: None for c in LOG_CATEGORIES},
    "log_options": {"sent": True, "ignore_channels": [], "ignore_users": []},
    "notify": {"topics": {}},
    "backup": {"auto": False, "interval_hours": 24, "keep": 7, "last": 0, "include_members": True, "include_emojis": True},
    "privacy": {"retention_days": 0},
    "stats": {"channels": {}},
    "archive": {"days": 60, "action": "report", "category": None, "report_channel": None, "ignore_channels": [], "ignore_categories": [], "interval_hours": 24, "last_scan": 0, "reported": {}},
    "rules": {"channel": None, "message": None, "role": None, "title": "Server rules", "text": [], "version": 1, "remind": True, "remind_hours": 48, "changed": 0},
    "dashboard_access": {"viewer_roles": [], "mod_roles": []},
    "debug": {"error_channel": None, "selftest": True, "usage_stats": True, "last_hash": None, "usage": {}, "errors": 0},
}
