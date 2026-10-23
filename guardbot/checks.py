"""Permission, module and usage checks of the bot, plus small helpers the features share."""

import time
from collections import deque
from typing import TYPE_CHECKING, Any, Optional

import discord
from discord.ext import commands

from . import i18n
from .logsetup import CONTEXT
from .defaults import COMMAND_MODULES, FALLBACK_PERMS


class Checks:
    """Mixin for the bot: who may use a command, who did what just now, team counters."""

    if TYPE_CHECKING:  # provided by the Bot class
        canonical: dict[str, str]
        actors: dict[int, deque]
        user: Any

        def cfg(self, gid: Any) -> dict: ...
        def module_on(self, gid: Any, name: str) -> bool: ...
        def prefix_for(self, gid: Any) -> str: ...
        def get_cog(self, name: str) -> Any: ...

    def can_use(self, member: Any, root: str) -> bool:
        """Check the permission rules of a command for a member, falling back to the Discord permission."""
        if member.id == member.guild.owner_id:
            return True
        rule = self.cfg(member.guild.id)["perms"].get(root, {})
        roles = {r.id for r in member.roles}
        if member.id in rule.get("deny_users", []) or roles & set(rule.get("deny_roles", [])):
            return False
        if rule.get("roles") or rule.get("users"):
            return member.id in rule.get("users", []) or bool(roles & set(rule.get("roles", [])))
        perm = FALLBACK_PERMS.get(root)
        return getattr(member.guild_permissions, perm) if perm else True

    def check_command(self, member: Any, guild: Any, root: str) -> Optional[str]:
        """Return why a command may not be used (disabled, module off, no permission) or None."""
        root = self.canonical.get(root, root)
        g = self.cfg(guild.id)
        if root in g["disabled_commands"]:
            return i18n.say(self, guild, "This command is disabled on this server.")
        mod = COMMAND_MODULES.get(root)
        if mod and not self.module_on(guild.id, mod):
            return i18n.say(self, guild, "The module '{module}' is disabled on this server.", module=mod)
        if not self.can_use(member, root):
            return i18n.say(self, guild, "You are not allowed to use this command.")
        return None

    async def _global_check(self, ctx: Any) -> bool:
        """Apply the command checks to text commands."""
        if ctx.guild is None:
            return False
        root = (ctx.command.root_parent or ctx.command).name
        CONTEXT.set({"guild": ctx.guild.id, "command": ctx.command.qualified_name})
        ctx.gb_start = time.perf_counter()
        problem = self.check_command(ctx.author, ctx.guild, root)
        if problem:
            raise commands.CheckFailure(problem)
        self.count_use(ctx.guild.id, root)
        self.note_actor(ctx.guild.id, ctx.author.id, self.prefix_for(ctx.guild.id) + root)
        return True

    def note_actor(self, gid: int, uid: int, what: str) -> None:
        """Remember who used which command or button on a server just now. The settings history uses this to say who probably made a change."""
        dq = self.actors.setdefault(gid, deque(maxlen=8))
        dq.append((time.time(), uid, what))

    async def on_interaction(self, interaction: Any) -> None:
        """Remember buttons, menus and forms of the setup assistant and other windows."""
        if interaction.guild_id and interaction.type in (discord.InteractionType.component, discord.InteractionType.modal_submit) and interaction.user:
            self.note_actor(interaction.guild_id, interaction.user.id, "button or menu")

    def team_count(self, guild: Any, uid: int, kind: str, seconds: Optional[float] = None) -> None:
        """Count a handled case, ticket, report, appeal or mod-mail for a staff member. Does nothing when the team module is missing."""
        team = self.get_cog("Team")
        if team is not None and uid and uid != getattr(self.user, "id", None):
            team.count(guild, uid, kind, seconds)

    def team_event(self, guild: Any, name: str, amount: int = 1) -> None:
        """Count an event for the weekly report."""
        team = self.get_cog("Team")
        if team is not None:
            team.event(guild, name, amount)

    def staff_ping(self, guild: Any, feature: str, role_id: Optional[int]) -> tuple[str, list, list]:
        """Return (text, user ids, role ids) for a staff ping. With routing on, one available staff member is pinged instead of the whole role."""
        team = self.get_cog("Team")
        if team is not None:
            return team.ping(guild, feature, role_id)
        if role_id:
            return f"<@&{role_id}>", [], [role_id]
        return "", [], []

    def count_use(self, gid: int, root: str) -> None:
        """Count one use of a command, if usage statistics are on for the server."""
        d = self.cfg(gid)["debug"]
        if d["usage_stats"]:
            root = self.canonical.get(root, root)
            d["usage"][root] = d["usage"].get(root, 0) + 1
