"""Base class of the cogs: access to the settings of the cog's section and the lanes for heavy work."""

from typing import Any, Callable, Optional

from discord.ext import commands


class BaseCog(commands.Cog):
    """A cog with a section in the server settings. Set `section` and conf(gid) returns that part of the settings. `gate` maps an event name to a module name, so the event is skipped when the module is off."""

    section: Optional[str] = None
    gate: dict[str, str] = {}

    def __init__(self, bot: Any) -> None:
        """Keep the bot."""
        self.bot = bot

    def conf(self, gid: Any) -> dict:
        """Return the settings of this cog for a server."""
        assert self.section is not None, "a cog needs a section to use conf()"
        return self.bot.cfg(gid)[self.section]

    async def work(self, lane: str, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Run heavy work in a lane. Raises workers.Busy when the lane is full."""
        return await self.bot.work.run(lane, fn, *args, **kwargs)
