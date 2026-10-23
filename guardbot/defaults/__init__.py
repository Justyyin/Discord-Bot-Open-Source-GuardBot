"""Default settings of every module, the module list and the command to module map. The settings are kept in one file per area."""

from . import community, core, moderation, security
from .base import COMMAND_MODULES, DANGEROUS, FALLBACK_PERMS, LOG_CATEGORIES, MODULES, PROTECTED_COMMANDS

ORDER = ['prefix', 'language', 'economy', 'rolemenus', 'schedule', 'feeds', 'activity', 'probation', 'antiscam', 'modules', 'disabled_commands', 'aliases', 'perms', 'case_counter', 'log', 'log_options', 'chanlocks', 'automod', 'mod', 'jail', 'antinuke', 'raid', 'lockdown', 'xp', 'birthday', 'reaction_roles', 'notify', 'welcome', 'boosters', 'tickets', 'polls', 'giveaways', 'starboard', 'tempvoice', 'suggestions', 'backup', 'verify', 'privacy', 'tags', 'skills', 'ai', 'panels', 'autoresponder', 'reminders', 'modmail', 'appeals', 'counting', 'sticky', 'stats', 'modwatch', 'permaudit', 'reports', 'invites', 'music', 'approval', 'stickyroles', 'nicknames', 'watchlist', 'reasons', 'archive', 'temproles', 'roletemplates', 'rules', 'history', 'team', 'exceptions', 'applications', 'dashboard_access', 'look', 'debug']
_PARTS = {}
for _part in (core, security, moderation, community):
    _PARTS.update(_part.SPEC)

DEFAULTS = {key: _PARTS[key] for key in ORDER}

__all__ = ["COMMAND_MODULES", "DANGEROUS", "DEFAULTS", "FALLBACK_PERMS", "LOG_CATEGORIES", "MODULES", "PROTECTED_COMMANDS"]
