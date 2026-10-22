"""Anti-scam and anti-crypto detection for text and images. Removes fake giveaways such as the typical MrBeast scam at once."""

import asyncio
import logging
import re
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from .. import i18n, scamscan
from ..utils import AdminGroup

log = logging.getLogger(__name__)

IMAGE_TYPES = ("image/png", "image/jpeg", "image/webp", "image/gif")
MAX_HASHES = 300
MAX_PENDING = 20
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif")
ACTIONS = ("delete", "log", "warn", "timeout", "jail")


def embed_text(msg):
    """The readable text of the embeds of a message."""
    parts = []
    for e in msg.embeds:
        parts += [e.title or "", e.description or "", getattr(e.author, "name", "") or "", getattr(e.footer, "text", "") or ""]
        parts += [f"{f.name} {f.value}" for f in e.fields]
    return " ".join(p for p in parts if p)


class AntiScam(commands.Cog):
    """Scam and crypto detection."""

    ag = AdminGroup(name="antiscam", description="Anti-scam and anti-crypto detection", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference, prepare the image cache and the context menu for moderators."""
        self.bot = bot
        self.menu = app_commands.ContextMenu(name="Mark as scam", callback=self.menu_learn)
        self.menu.guild_only = True
        self.ocr_slots = asyncio.Semaphore(2)
        self.verdicts = {}
        self.pending = 0

    async def cog_load(self):
        """Add the context menu to the command tree."""
        self.bot.tree.add_command(self.menu)

    async def cog_unload(self):
        """Remove the context menu from the command tree."""
        self.bot.tree.remove_command(self.menu.name, type=self.menu.type)

    def conf(self, gid):
        """Return the anti-scam settings of a server."""
        return self.bot.cfg(gid)["antiscam"]

    def lists(self, c):
        """The word lists of a server."""
        return {k: c["words"][k] for k in scamscan.CATEGORIES}

    def program(self):
        """Path of tesseract from settings.json or the system path."""
        return scamscan.tesseract_path(self.bot.settings.get("tesseract"))

    def remember(self, c, key, bad):
        """Remember that an image is a scam, so it is removed without reading it again."""
        self.verdicts[key] = bad
        if len(self.verdicts) > 2000:
            self.verdicts.pop(next(iter(self.verdicts)))
        if bad and key not in c["hashes"]:
            c["hashes"].append(key)
            del c["hashes"][:-MAX_HASHES]

    async def handle(self, msg, reason):
        """Carry out the configured action on a message."""
        c = self.conf(msg.guild.id)
        c["hits"] += 1
        automod = self.bot.get_cog("AutoMod")
        if automod is None:
            try:
                await msg.delete()
            except discord.HTTPException as exc:
                log.warning("msg.delete failed: %s", exc)
            return
        await automod.act(msg, "antiscam", reason, c["action"])

    async def image_bad(self, att, c):
        """Download an image and decide whether it is a scam. Returns (bad, reason)."""
        if att.size > c["max_mb"] * 1024 * 1024:
            return False, ""
        try:
            data = await att.read()
        except discord.HTTPException:
            return False, ""
        key = scamscan.digest(data)
        if key in c["hashes"] or self.verdicts.get(key):
            return True, "image already known as scam"
        if key in self.verdicts:
            return False, ""
        if self.pending >= MAX_PENDING:
            log.warning("too many images waiting for OCR, skipping one")
            return False, ""
        self.pending += 1
        try:
            async with self.ocr_slots:
                text = await asyncio.to_thread(scamscan.read_text, data, c["ocr_lang"], self.program())
        finally:
            self.pending -= 1
        v = scamscan.scan(text, self.lists(c))
        bad = v.flagged(c["threshold"])
        self.remember(c, key, bad)
        return bad, "text in image, " + v.reason() if bad else ""

    async def check(self, msg, with_images=True):
        """Scan the text and the images of a message and act on the first hit."""
        if msg.author.bot or not msg.guild or not self.bot.module_on(msg.guild.id, "antiscam"):
            return
        automod = self.bot.get_cog("AutoMod")
        a = self.bot.cfg(msg.guild.id)["automod"]
        if automod is not None and automod.exempt(msg, a):
            return
        c = self.conf(msg.guild.id)
        if c["text"]:
            names = " ".join(att.filename for att in msg.attachments)
            full = f"{msg.content}\n{embed_text(msg)}\n{names}"
            if scamscan.text_key(msg.content) in c["texts"] and c["texts"]:
                return await self.handle(msg, "scam text, a moderator marked the same text before")
            v = scamscan.scan(full, self.lists(c))
            if v.flagged(c["threshold"]):
                return await self.handle(msg, "scam text, " + v.reason())
        if with_images and c["images"] and self.program() is not None:
            images = [att for att in msg.attachments if (att.content_type or "").split(";")[0] in IMAGE_TYPES or (not att.content_type and att.filename.lower().endswith(IMAGE_EXT))][:c["max_images"]]
            if images:
                for done in asyncio.as_completed([self.image_bad(att, c) for att in images]):
                    bad, why = await done
                    if bad:
                        return await self.handle(msg, "scam " + why)

    async def learn(self, message, moderator):
        """Remember the images and the text of a scam message, delete it and report it. Returns (images, text remembered)."""
        c = self.conf(message.guild.id)
        images = 0
        for att in message.attachments[:c["max_images"]]:
            if att.size > c["max_mb"] * 1024 * 1024 or not ((att.content_type or "").split(";")[0] in IMAGE_TYPES or att.filename.lower().endswith(IMAGE_EXT)):
                continue
            try:
                key = scamscan.digest(await att.read())
            except discord.HTTPException:
                continue
            self.remember(c, key, True)
            images += 1
        tkey = scamscan.text_key(message.content)
        if tkey and tkey not in c["texts"]:
            c["texts"].append(tkey)
            del c["texts"][:-MAX_HASHES]
        self.bot.bot_deleted.add(message.id)
        try:
            await message.delete()
        except discord.HTTPException as exc:
            self.bot.bot_deleted.discard(message.id)
            log.warning("learn: message could not be deleted: %s", exc)
        e = discord.Embed(title="Scam learned", description=f"{moderator.mention} marked a message of {message.author.mention} as scam. {images} image(s) and {'the text' if tkey else 'no text'} will be removed at once from now on.", color=discord.Color.red())
        self.bot.log(message.guild, "security", e)
        return images, bool(tkey)

    async def menu_learn(self, it: discord.Interaction, message: discord.Message):
        """Context menu entry for moderators: this message is a scam."""
        if not it.user.guild_permissions.manage_messages:
            return await it.response.send_message(i18n.say(it.client, it.guild, "You need the Manage Messages permission for this."), ephemeral=True)
        if not self.bot.module_on(it.guild_id, "antiscam"):
            return await it.response.send_message(i18n.say(it.client, it.guild, "The antiscam module is off."), ephemeral=True)
        if message.author.bot or message.author.id == it.user.id:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Choose a message of a member."), ephemeral=True)
        await it.response.defer(ephemeral=True)
        images, text = await self.learn(message, it.user)
        await it.followup.send(f"Learned: {images} image(s), text {'yes' if text else 'too short'}. The message was deleted.")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """A moderator reacts with the learn emoji to mark a message as scam."""
        if payload.guild_id is None or payload.member is None or payload.member.bot:
            return
        c = self.conf(payload.guild_id)
        if not c["learn_emoji"] or str(payload.emoji) != c["learn_emoji"] or not self.bot.module_on(payload.guild_id, "antiscam"):
            return
        if not payload.member.guild_permissions.manage_messages:
            return
        channel = self.bot.get_channel(payload.channel_id)
        if channel is None:
            return
        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.HTTPException:
            return
        if not message.author.bot and message.author.id != payload.member.id:
            await self.learn(message, payload.member)

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Check every new message."""
        await self.check(msg)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Check edited messages and embeds that Discord adds afterwards."""
        if before.content != after.content or len(before.embeds) != len(after.embeds):
            await self.check(after, with_images=False)

    @ag.command(name="status", description="Show the settings")
    async def status(self, it: discord.Interaction):
        """Show the settings."""
        c = self.conf(it.guild_id)
        ocr = "ready" if self.program() else "not installed (install tesseract-ocr), images are not read"
        lines = [
            f"Module: {'on' if self.bot.module_on(it.guild_id, 'antiscam') else 'off'}, action: {c['action']}, threshold: {c['threshold']} points",
            f"Text check: {c['text']}, image check: {c['images']} (OCR {ocr}), up to {c['max_images']} images of {c['max_mb']} MB, language {c['ocr_lang']}",
            f"Removed so far: {c['hits']}, known scam images: {len(c['hashes'])}, known scam texts: {len(c['texts'])}, learn emoji: {c['learn_emoji'] or 'off'}",
        ] + [f"{k}: {len(c['words'][k])} words" for k in scamscan.CATEGORIES]
        await it.response.send_message("\n".join(lines), ephemeral=True)

    @ag.command(name="set", description="Change the settings")
    @app_commands.describe(action="What happens to a scam message (the message is always removed except for log)", threshold="Points needed when no name from the instant list is found", text="Check text", images="Check images with OCR", ocr_lang="Tesseract language, for example eng or eng+deu", max_images="Images per message", learn_emoji="Emoji a moderator reacts with to mark a message as scam, off = none")
    async def set(
        self, it: discord.Interaction, action: Optional[Literal["delete", "log", "warn", "timeout", "jail"]] = None, threshold: Optional[app_commands.Range[int, 1, 10]] = None,
        text: Optional[bool] = None, images: Optional[bool] = None, ocr_lang: Optional[app_commands.Range[str, 3, 30]] = None, max_images: Optional[app_commands.Range[int, 1, 6]] = None,
        learn_emoji: Optional[app_commands.Range[str, 1, 60]] = None,
    ):
        """Change the settings."""
        c = self.conf(it.guild_id)
        if ocr_lang is not None and not re.fullmatch(r"[a-z_+]{3,30}", ocr_lang):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Use letters, _ and + only, for example eng+deu."), ephemeral=True)
        if learn_emoji is not None:
            c["learn_emoji"] = None if learn_emoji.lower() == "off" else learn_emoji
        for key, value in (("action", action), ("threshold", threshold), ("text", text), ("images", images), ("ocr_lang", ocr_lang), ("max_images", max_images)):
            if value is not None:
                c[key] = value
        await it.response.send_message(f"Saved. Action {c['action']}, threshold {c['threshold']}, text {c['text']}, images {c['images']}, language {c['ocr_lang']}.", ephemeral=True)

    @ag.command(name="words", description="Add or remove words in one of the lists")
    @app_commands.describe(action="Add or remove", kind="instant = removed at once, celeb = names scammers use, bait = promises, crypto = money words", word="Word or phrase")
    async def words(self, it: discord.Interaction, action: Literal["add", "remove"], kind: Literal["instant", "celeb", "bait", "crypto"], word: app_commands.Range[str, 2, 60]):
        """Add or remove words in one of the lists."""
        lst = self.conf(it.guild_id)["words"][kind]
        w = word.strip().lower()
        if action == "add":
            if w in lst:
                return await it.response.send_message(i18n.say(it.client, it.guild, "Already in the list."), ephemeral=True)
            if len(lst) >= 300:
                return await it.response.send_message(i18n.say(it.client, it.guild, "The list is full (300)."), ephemeral=True)
            lst.append(w)
        else:
            if w not in lst:
                return await it.response.send_message(i18n.say(it.client, it.guild, "That word is not in the list."), ephemeral=True)
            lst.remove(w)
        await it.response.send_message(f"{kind}: {len(lst)} words.", ephemeral=True)

    @ag.command(name="test", description="Try a text and see the score")
    @app_commands.describe(text="Text to test")
    async def test(self, it: discord.Interaction, text: str):
        """Try a text and see the score."""
        c = self.conf(it.guild_id)
        v = scamscan.scan(text, self.lists(c))
        await it.response.send_message(f"{'Would be removed' if v.flagged(c['threshold']) else 'Would stay'}: {v.reason() if v.hits else 'nothing found'} (threshold {c['threshold']}).", ephemeral=True)

    @ag.command(name="testimage", description="Read the text of an image and show the score")
    @app_commands.describe(image="Image to test")
    async def testimage(self, it: discord.Interaction, image: discord.Attachment):
        """Read the text of an image and show the score."""
        c = self.conf(it.guild_id)
        if self.program() is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "tesseract is not installed."), ephemeral=True)
        if image.size > c["max_mb"] * 1024 * 1024:
            return await it.response.send_message(i18n.say(it.client, it.guild, "The image is too large."), ephemeral=True)
        await it.response.defer(ephemeral=True)
        data = await image.read()
        async with self.ocr_slots:
            text = await asyncio.to_thread(scamscan.read_text, data, c["ocr_lang"], self.program())
        v = scamscan.scan(text, self.lists(c))
        await it.followup.send(f"{'Would be removed' if v.flagged(c['threshold']) else 'Would stay'}: {v.reason() if v.hits else 'nothing found'}\nText read: {text[:600] or 'nothing'}")

    @ag.command(name="forget", description="Forget all remembered scam images")
    async def forget(self, it: discord.Interaction):
        """Forget all remembered scam images."""
        self.conf(it.guild_id)["hashes"].clear()
        self.conf(it.guild_id)["texts"].clear()
        self.verdicts.clear()
        await it.response.send_message(i18n.say(it.client, it.guild, "Done."), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(AntiScam(bot))
