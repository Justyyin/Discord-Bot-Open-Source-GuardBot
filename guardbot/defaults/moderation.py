"""Settings of moderation and team work: cases, gulag, tickets, appeals, mod-mail."""

from typing import Any


SPEC: dict[str, Any] = {
    "mod": {
        "dm_user": True,
        "warn_expiry_days": 0,
        "default_mute_minutes": 60,
        "tempbans": {},
        "escalation": [
            {"warns": 3, "action": "timeout", "minutes": 60},
            {"warns": 5, "action": "kick"},
            {"warns": 7, "action": "ban"},
        ],
    },
    "jail": {
        "role": None,
        "channel": None,
        "staff_role": None,
        "notice": None,
        "timed": {},
    },
    "tickets": {
        "category": None,
        "support_role": None,
        "log_channel": None,
        "max_open": 1,
        "counter": 0,
        "types": {
            "support": {"label": "Support", "desc": "Ask for help"},
            "application": {"label": "Application", "desc": "Apply for a position"},
        },
        "open": {},
    },
    "modmail": {"category": None, "staff_role": None, "log_channel": None, "anonymous": False, "open": {}, "blocked": []},
    "appeals": {"main_guild": None, "staff_channel": None, "invite": None, "rejoin_invite": None, "cooldown_days": 7, "items": {}, "next": 1, "last": {}},
    "stickyroles": {"roles": True, "punishments": True, "days": 30, "exclude": [], "dangerous": False},
    "nicknames": {"dehoist": True, "words": [], "action": "rename", "rename_to": "Moderated name", "usernames": False, "exempt_roles": [], "notify": True},
    "watchlist": {"channel": None, "ping_role": None, "repeat": False, "items": {}},
    "reasons": {"items": {}},
    "temproles": {"items": {}},
    "roletemplates": {"items": {}},
    "history": {"items": [], "next": 1, "keep": 40},
    "team": {"stats": {}, "week": {}, "report_channel": None, "report_day": 0, "report_hour": 9, "last_report": 0, "inactive_days": 14, "away": {}, "assigned": {}, "roster_roles": [], "route": []},
    "exceptions": {"items": {}},
    "applications": {"channel": None, "staff_role": None, "accept_role": None, "questions": ["Why do you want to join the team?", "How old are you and what is your time zone?", "Which experience do you have?"], "votes": 2, "cooldown_days": 14, "open": True, "items": {}, "next": 1, "last": {}},
}
