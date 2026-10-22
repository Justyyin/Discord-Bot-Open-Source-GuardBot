"""AutoMod presets and server templates used by the setup assistant."""

AUTOMOD_RULES = ("flood", "caps", "mentions", "invites", "phishing", "pii", "doxxing", "threats", "shortlinks", "newlinks", "ghostping")

AUTOMOD_PRESETS = {
    "loose": {
        "phishing": {"action": "jail"},
        "mentions": {"max": 10, "action": "timeout"},
    },
    "normal": {
        "phishing": {"action": "jail"},
        "invites": {"action": "delete"},
        "mentions": {"max": 6, "action": "timeout"},
        "caps": {"percent": 70, "action": "delete"},
        "flood": {"count": 5, "seconds": 5, "timeout": 10},
        "ghostping": {"notify": True},
    },
    "strict": {
        "phishing": {"action": "jail", "lookalike": True},
        "invites": {"action": "delete"},
        "mentions": {"max": 4, "action": "timeout"},
        "caps": {"percent": 60, "action": "delete"},
        "flood": {"count": 4, "seconds": 5, "timeout": 30},
        "pii": {"action": "delete"},
        "doxxing": {"action": "delete"},
        "threats": {"action": "log"},
        "shortlinks": {"action": "delete"},
        "newlinks": {"action": "delete", "hours": 24},
        "ghostping": {"notify": True},
    },
}

# Settings outside the module switch that a module needs before it does anything.
EXTRA_SWITCHES = {"leveling": ("xp", "enabled"), "birthday": ("birthday", "enabled")}

TEMPLATES = {
    "community": {
        "text": "Welcome and boost messages, levels, birthdays, suggestions, starboard, polls, giveaways, tickets and reports.",
        "modules": ("welcome", "boosters", "leveling", "birthday", "suggestions", "starboard", "polls", "giveaways", "tickets", "reports"),
        "automod": "normal",
    },
    "gaming": {
        "text": "Levels, counting, temporary voice channels, polls, giveaways, invite tracking and statistics channels.",
        "modules": ("leveling", "counting", "tempvoice", "polls", "giveaways", "invites", "stats"),
        "automod": "normal",
    },
    "support": {
        "text": "Tickets, mod-mail, ban appeals, reports, tags, auto-responses, mod activity watch and permission audit.",
        "modules": ("tickets", "modmail", "appeals", "reports", "tags", "autoresponder", "modwatch", "permaudit"),
        "automod": "strict",
    },
}


def apply_automod_preset(cfg, name):
    """Turn the AutoMod rules of a server into one of the presets. Word lists and exemptions stay as they are."""
    preset = AUTOMOD_PRESETS[name]
    auto = cfg["automod"]
    for rule in AUTOMOD_RULES:
        auto[rule]["enabled"] = False
    for rule, options in preset.items():
        auto[rule].update(options)
        auto[rule]["enabled"] = True
    cfg["modules"]["automod"] = True
    return sorted(preset)


def apply_template(cfg, name):
    """Switch on the modules of a template and its AutoMod preset. Nothing is switched off."""
    tpl = TEMPLATES[name]
    for module in tpl["modules"]:
        cfg["modules"][module] = True
        if module in EXTRA_SWITCHES:
            section, key = EXTRA_SWITCHES[module]
            cfg[section][key] = True
    apply_automod_preset(cfg, tpl["automod"])
    return list(tpl["modules"])


# What the setup assistant can create on a server. "key" names the setting that receives the new channel or role.
MODERATOR_PERMISSIONS = ("view_audit_log", "manage_messages", "manage_nicknames", "kick_members", "moderate_members", "mute_members", "move_members", "read_message_history")

_STAFF = {"name": "Staff", "private": True, "channels": [{"name": "staff-chat", "kind": "text"}, {"name": "mod-log", "kind": "text", "key": "log"}, {"name": "Staff voice", "kind": "voice"}]}
_INFO = {"name": "Info", "channels": [{"name": "rules", "kind": "text", "key": "rules", "readonly": True}, {"name": "announcements", "kind": "text", "readonly": True}, {"name": "welcome", "kind": "text", "key": "welcome", "readonly": True}]}

BLUEPRINTS = {
    "community": {
        "roles": [{"name": "Moderator", "staff": True, "color": 0x3498DB, "permissions": MODERATOR_PERMISSIONS}],
        "categories": [
            _INFO,
            {"name": "Community", "channels": [{"name": "general", "kind": "text"}, {"name": "media", "kind": "text"}, {"name": "bot-commands", "kind": "text"}]},
            {"name": "Voice", "channels": [{"name": "Lounge", "kind": "voice"}, {"name": "Music", "kind": "voice"}]},
            _STAFF,
        ],
    },
    "gaming": {
        "roles": [{"name": "Moderator", "staff": True, "color": 0x3498DB, "permissions": MODERATOR_PERMISSIONS}],
        "categories": [
            _INFO,
            {"name": "Chat", "channels": [{"name": "general", "kind": "text"}, {"name": "looking-for-group", "kind": "text"}, {"name": "clips", "kind": "text"}]},
            {"name": "Voice", "channels": [{"name": "Lobby", "kind": "voice"}, {"name": "Squad 1", "kind": "voice"}, {"name": "Squad 2", "kind": "voice"}]},
            _STAFF,
        ],
    },
    "support": {
        "roles": [{"name": "Support", "staff": True, "color": 0x2ECC71, "permissions": MODERATOR_PERMISSIONS}],
        "categories": [
            _INFO,
            {"name": "Help", "channels": [{"name": "faq", "kind": "text", "readonly": True}, {"name": "open-a-ticket", "kind": "text", "readonly": True}, {"name": "community-help", "kind": "text"}]},
            _STAFF,
        ],
    },
}


def blueprint_missing(blueprint, role_names, channel_names, category_names):
    """What a blueprint would create: (roles, categories, channels) that do not exist yet. Names are compared without case."""
    roles = [r for r in blueprint["roles"] if r["name"].casefold() not in role_names]
    cats, chans = [], []
    for cat in blueprint["categories"]:
        if cat["name"].casefold() not in category_names:
            cats.append(cat)
        for ch in cat["channels"]:
            if ch["name"].casefold() not in channel_names:
                chans.append((cat["name"], ch))
    return roles, cats, chans


def blueprint_size(blueprint):
    """Number of roles, categories and channels in a blueprint."""
    return len(blueprint["roles"]), len(blueprint["categories"]), sum(len(c["channels"]) for c in blueprint["categories"])
