"""The /ai commands: connect a provider with your own key and let it write skills for you."""

import logging
from typing import Any, Literal

import discord
from discord import app_commands

from ... import ai as ailib, i18n, skills as engine
from ...cog import BaseCog
from ...utils import emb, require

log = logging.getLogger(__name__)

DISCLOSURE = (
    "When you use the AI features, the text you type for /support ai make, and for the anti-scam second opinion the text of a message that looks suspicious, is sent to the provider you chose, "
    "under your own account and key. The provider's own terms and privacy rules apply to it. Nothing is sent without one of these features being used. The key is stored encrypted on the bot's server."
)

TEXTS = (DISCLOSURE,)


class KeyModal(discord.ui.Modal):
    """A box for the key. Only the person who typed the command sees it."""

    def __init__(self, cog: "AICog", provider: str, model: str):
        """Create the box."""
        super().__init__(title="API key")
        self.cog, self.provider, self.model = cog, provider, model
        self.key = discord.ui.TextInput(label="API key", style=discord.TextStyle.short, min_length=16, max_length=300)
        self.add_item(self.key)

    async def on_submit(self, it: discord.Interaction) -> None:
        """Store the key encrypted and turn the module on."""
        try:
            self.cog.bot.ai.set_key(it.guild_id, self.provider, self.key.value, self.model)
        except ailib.AIError as exc:
            return await it.response.send_message(i18n.say(it.client, it.guild, str(exc)), ephemeral=True)
        self.cog.bot.cfg(it.guild_id)["modules"]["ai"] = True
        label = ailib.PROVIDERS[self.provider]["label"]
        await it.response.send_message(i18n.say(it.client, it.guild, "The key for {provider} is saved. The key is stored encrypted and is not shown anywhere. Use /support ai status to check it and /support ai make to build a skill.", provider=label), ephemeral=True)


class Preview(discord.ui.View):
    """Shows a skill the AI wrote and saves it only after the administrator confirms."""

    def __init__(self, cog: "AICog", owner: int, spec: dict):
        """Keep the validated skill."""
        super().__init__(timeout=300)
        self.cog, self.owner, self.spec = cog, owner, spec

    @discord.ui.button(label="Save", style=discord.ButtonStyle.success)
    async def save(self, it: discord.Interaction, button: discord.ui.Button) -> None:
        """Save the skill."""
        if it.user.id != self.owner:
            return await it.response.send_message("This is not your preview.", ephemeral=True)
        skills = it.client.get_cog("Skills")
        err = skills.store(it.guild, self.spec, it.user.id, replace=self.spec["name"] in skills.items(it.guild_id))
        self.stop()
        text = i18n.say(it.client, it.guild, err) if err else i18n.say(it.client, it.guild, "Skill `{name}` saved. It is on. Turn it off with /support skill disable.", name=self.spec["name"])
        await it.response.edit_message(content=text, embed=None, view=None)

    @discord.ui.button(label="Discard", style=discord.ButtonStyle.secondary)
    async def discard(self, it: discord.Interaction, button: discord.ui.Button) -> None:
        """Throw the skill away."""
        if it.user.id != self.owner:
            return await it.response.send_message("This is not your preview.", ephemeral=True)
        self.stop()
        await it.response.edit_message(content=i18n.say(it.client, it.guild, "Discarded."), embed=None, view=None)


class AICog(BaseCog):
    """Own AI key per server."""

    section = "ai"
    ai = app_commands.Group(name="ai", description="Connect an AI provider with your own key", guild_only=True)

    @ai.command(name="setup", description="Connect a provider with your own API key")
    @app_commands.describe(provider="Anthropic, OpenAI or Kimi", model="Model name, empty for the suggestion", agree="I understand what is sent to the provider (see /support ai privacy)")
    async def ai_setup(self, it: discord.Interaction, provider: Literal["anthropic", "openai", "kimi"], agree: bool, model: str = ""):
        """Open a private box for the key."""
        if not await require(it):
            return
        if not agree:
            return await it.response.send_message(i18n.say(it.client, it.guild, DISCLOSURE), ephemeral=True)
        await it.response.send_modal(KeyModal(self, provider, model))

    @ai.command(name="privacy", description="What is sent to the provider")
    async def ai_privacy(self, it: discord.Interaction):
        """Explain what leaves the bot."""
        await it.response.send_message(i18n.say(it.client, it.guild, DISCLOSURE), ephemeral=True)

    @ai.command(name="status", description="Show the AI settings and today's use")
    async def ai_status(self, it: discord.Interaction):
        """Show provider, model and use. The key is never shown."""
        if not await require(it):
            return
        c = self.conf(it.guild_id)
        used, limit = self.bot.ai.budget(it.guild_id)
        if not self.bot.ai.configured(it.guild_id):
            return await it.response.send_message(i18n.say(it.client, it.guild, "No key is set. Use /support ai setup."), ephemeral=True)
        e = emb("AI", footer="the key is stored encrypted and never shown")
        e.add_field(name="Provider", value=ailib.PROVIDERS[c["provider"]]["label"])
        e.add_field(name="Model", value=c["model"])
        e.add_field(name="Today", value=f"{used} / {limit}")
        e.add_field(name="Errors", value=str(c["errors"]))
        e.add_field(name="Anti-scam second opinion", value="on" if c["second_opinion"] else "off")
        await it.response.send_message(embed=e, ephemeral=True)

    @ai.command(name="remove", description="Delete the stored key")
    async def ai_remove(self, it: discord.Interaction):
        """Delete the key."""
        if not await require(it):
            return
        self.bot.ai.remove_key(it.guild_id)
        await it.response.send_message(i18n.say(it.client, it.guild, "The key is deleted and the AI is off."), ephemeral=True)

    @ai.command(name="limits", description="Set how much the AI may be used")
    @app_commands.describe(daily="Requests per day for the whole server", cooldown="Seconds a person must wait between requests", second_opinion="Ask the AI about borderline anti-scam cases")
    async def ai_limits(self, it: discord.Interaction, daily: app_commands.Range[int, 1, 1000] = 50, cooldown: app_commands.Range[int, 0, 3600] = 30, second_opinion: bool = False):
        """Change the limits."""
        if not await require(it):
            return
        c = self.conf(it.guild_id)
        c["daily_limit"], c["user_cooldown"], c["second_opinion"] = daily, cooldown, second_opinion
        await it.response.send_message(i18n.say(it.client, it.guild, "Saved."), ephemeral=True)

    @ai.command(name="make", description="Let the AI build a skill from your description")
    @app_commands.describe(wish="What the skill should do, in your own words")
    async def ai_make(self, it: discord.Interaction, wish: app_commands.Range[str, 10, 800]):
        """Ask the AI for a skill, check it strictly and show a preview."""
        if not await require(it):
            return
        await it.response.defer(ephemeral=True, thinking=True)
        skills = it.client.get_cog("Skills")
        probe = skills_runner(skills, it.guild)
        roles = [(r.id, r.name) for r in it.guild.roles if probe.role(r.id) is not None][:40]
        channels = [(c.id, c.name) for c in it.guild.text_channels][:40]
        try:
            answer = await self.bot.ai.ask(it.guild_id, engine.format_help(roles, channels), wish, uid=it.user.id, max_tokens=1500)
            raw = engine.extract_json(answer)
            if isinstance(raw, dict) and "error" in raw and len(raw) == 1:
                return await it.followup.send(i18n.say(it.client, it.guild, "The AI says this cannot be built with the available blocks: {reason}", reason=str(raw["error"])[:300]), ephemeral=True)
            spec = engine.clean(raw)
            problem = skills.check_references(it.guild, spec)
            if problem:
                raise engine.SpecError(problem)
        except ailib.AIError as exc:
            return await it.followup.send(i18n.say(it.client, it.guild, str(exc)), ephemeral=True)
        except engine.SpecError as exc:
            return await it.followup.send(i18n.say(it.client, it.guild, "The AI wrote something that is not a valid skill ({error}). Nothing was saved. Try to describe it more simply.", error=str(exc)), ephemeral=True)
        import json
        body = json.dumps(spec, indent=1, ensure_ascii=False)
        e = emb("Preview", f"```json\n{body[:3500]}\n```", footer=engine.describe(spec))
        e.add_field(name="Check before you save", value=i18n.say(it.client, it.guild, "The skill was written by an AI. It can only use the safe building blocks, but read what it does."), inline=False)
        await it.followup.send(embed=e, view=Preview(self, it.user.id, spec), ephemeral=True)


def skills_runner(skills: Any, guild: discord.Guild) -> Any:
    """A runner without a person, used to test which roles may be handed out."""
    from .skills import Runner
    return Runner(skills, guild, guild.me, None)


async def setup(bot: Any) -> None:
    """Register the cog with the bot."""
    await bot.add_cog(AICog(bot))
