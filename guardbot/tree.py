"""Command tree that applies module, disable and permission checks to slash commands."""

import logging
import time

import discord
from discord import app_commands
from discord.ext.commands.hybrid import HybridAppCommand

from . import i18n, layout
from .logsetup import CONTEXT
from .workers import Busy

log = logging.getLogger(__name__)


class Tree(app_commands.CommandTree):
    """Command tree that applies module, disable and permission checks to slash commands."""

    def __init__(self, *args, **kwargs):
        """While the cogs load, more than 100 top-level commands are allowed, because they are folded into groups afterwards."""
        super().__init__(*args, **kwargs)
        self.loading = True

    def add_command(self, command, /, *, guild=discord.utils.MISSING, guilds=discord.utils.MISSING, override=False):
        """Add a command. During loading the limit of 100 top-level commands is not checked, arrange_commands() brings the number down."""
        if self.loading and guild is discord.utils.MISSING and guilds is discord.utils.MISSING and not isinstance(command, app_commands.ContextMenu):
            root = command.root_parent or command
            if root.name in self._global_commands and not override:
                raise app_commands.CommandAlreadyRegistered(root.name, None)
            self._global_commands[root.name] = root
            return
        super().add_command(command, guild=guild, guilds=guilds, override=override)
    async def interaction_check(self, interaction):
        """Block slash commands that are disabled or not allowed for the user."""
        cmd = interaction.command
        if cmd is None or interaction.guild is None:
            return True
        root = layout.command_key(cmd)
        CONTEXT.set({"guild": interaction.guild.id, "command": "/" + cmd.qualified_name})
        interaction.extras["gb_start"] = time.perf_counter()
        problem = interaction.client.check_command(interaction.user, interaction.guild, root)
        if problem:
            await interaction.response.send_message(problem, ephemeral=True)
            return False
        interaction.client.note_actor(interaction.guild.id, interaction.user.id, "/" + cmd.qualified_name)
        if not isinstance(cmd, HybridAppCommand):
            interaction.client.count_use(interaction.guild.id, root)
        return True

    async def on_error(self, interaction, error):
        """Log unexpected errors of slash commands and tell the user."""
        if isinstance(error, app_commands.CheckFailure):
            return
        if isinstance(getattr(error, "original", None), Busy):
            text = i18n.say(interaction.client, interaction.guild, "The bot is busy with this kind of work. Try again in a moment.")
        else:
            log.error("unhandled error in a slash command", exc_info=error)
            where = f"/{interaction.command.qualified_name}" if interaction.command else "interaction"
            interaction.client.report_error(interaction.guild, where, error)
            text = i18n.say(interaction.client, interaction.guild, "Something went wrong.")
        try:
            if interaction.response.is_done():
                await interaction.followup.send(text, ephemeral=True)
            else:
                await interaction.response.send_message(text, ephemeral=True)
        except discord.HTTPException as exc:
            log.warning("response.is_done failed: %s", exc)
