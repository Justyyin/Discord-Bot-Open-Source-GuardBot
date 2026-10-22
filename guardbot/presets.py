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
