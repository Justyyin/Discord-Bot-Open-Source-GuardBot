"""Short top-level commands /security block, /security unblock and /security blocklist for the AutoMod blocklist."""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal, Optional


class Shortcuts(commands.Cog):
    """Shortcuts that call the blocklist commands of AutoMod."""

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    def automod(self):
        """The AutoMod cog that holds the blocklist."""
        return self.bot.get_cog("AutoMod")

    @app_commands.command(name="block", description="Add a link, text or image to the blocklist")
    @app_commands.describe(kind="What to block", value="Link, text or image URL", image="Upload an image")
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def block(self, it: discord.Interaction, kind: Literal["link", "message", "image"], value: Optional[str] = None, image: Optional[discord.Attachment] = None):
        """Add a link, text or image to the blocklist."""
        await self.automod().am_block.callback(self.automod(), it, kind, value, image)

    @app_commands.command(name="unblock", description="Remove an entry from the blocklist")
    @app_commands.describe(kind="Which list", number="Number from /security blocklist")
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def unblock(self, it: discord.Interaction, kind: Literal["link", "message", "image"], number: int):
        """Remove an entry from the blocklist."""
        await self.automod().am_unblock.callback(self.automod(), it, kind, number)

    @app_commands.command(name="blocklist", description="Show the blocklist")
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def blocklist(self, it: discord.Interaction):
        """Show the blocklist."""
        await self.automod().am_blocklist.callback(self.automod(), it)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Shortcuts(bot))
