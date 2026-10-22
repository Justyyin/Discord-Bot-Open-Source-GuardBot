"""Automatic moderation rules, blocklist, flood protection and personal data detection."""

import asyncio
import hashlib
import logging
import re
import time
from collections import deque
from datetime import timedelta
from types import SimpleNamespace
from typing import Literal, Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from .. import i18n
from ..linkcheck import Resolver, host_of
from ..utils import URL_RE, describe, emb, grab_files, has_image, has_video, hosts, is_image

log = logging.getLogger(__name__)

MAX_BYTES = 10 * 1024 * 1024
OFFICIAL = (
    "discord.com", "discord.gg", "discordapp.com", "discordapp.net", "discord.media",
    "discordstatus.com", "discord.gift", "discord.new", "dis.gd", "steampowered.com", "steamcommunity.com",
)
BRANDS = ("discord", "nitro", "steam")
INVITE_RE = re.compile(r"(?:discord\.gg|discord(?:app)?\.com/invite)/([\w-]+)", re.I)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE_RE = re.compile(r"(?<![\w/])(?:\+\d{1,3}|\(?0\d{1,4}\)?)[\s./-]?\d{2,5}(?:[\s./-]?\d{2,6}){1,3}(?!\w)")
IP_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){2,7}(?:\s?[A-Z0-9]{1,4})?\b")
CARD_RE = re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")
LISTS = {
    "words": ("words", "list"),
    "phishing": ("phishing", "list"),
    "phishing_allow": ("phishing", "allow"),
    "invites_allow": ("invites", "allow"),
    "doxxing": ("doxxing", "list"),
    "threats": ("threats", "list"),
    "shortlink_domains": ("shortlinks", "domains"),
    "newlinks_allow": ("newlinks", "allow"),
}
RULES = ("words", "caps", "mentions", "invites", "phishing", "pii", "doxxing", "threats", "shortlinks", "newlinks")
DRY_RUN_RULES = ("all", "words", "caps", "mentions", "invites", "phishing", "pii", "doxxing", "threats", "shortlinks", "newlinks", "blocklist", "channel_rule", "flood", "antiscam")
MAX_RESOLVES = 3
ID_RE = re.compile(r"<@!?(\d+)>")
ROLE_RE = re.compile(r"<@&(\d+)>")
ACTIONS = ("log", "delete", "warn", "timeout", "jail")


def luhn(num):
    """Check a digit string with the Luhn algorithm used by card numbers."""
    total, flip = 0, False
    for ch in reversed(num):
        d = int(ch)
        if flip:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
        flip = not flip
    return total % 10 == 0


def iban_ok(s):
    """Check an IBAN with the mod 97 test."""
    s = s.replace(" ", "").upper()
    if not 15 <= len(s) <= 34:
        return False
    moved = s[4:] + s[:4]
    return int("".join(str(int(c, 36)) for c in moved)) % 97 == 1


def find_pii(text, opts):
    """Return the kinds of personal data found in a text, limited to the enabled options."""
    found = []
    if opts["email"] and EMAIL_RE.search(text):
        found.append("email address")
    iban = opts["iban"] and any(iban_ok(m.group()) for m in IBAN_RE.finditer(text.upper()))
    if iban:
        found.append("IBAN")
    if opts["ip"] and any(all(int(p) <= 255 for p in m.group().split(".")) for m in IP_RE.finditer(text)):
        found.append("IP address")
    if iban:
        return found
    if opts["card"]:
        for m in CARD_RE.finditer(text):
            d = re.sub(r"\D", "", m.group())
            if 13 <= len(d) <= 19 and luhn(d) and len(set(d)) > 1:
                found.append("card number")
                break
    if "card number" not in found and opts["phone"] and any(9 <= len(re.sub(r"\D", "", m.group())) <= 15 for m in PHONE_RE.finditer(text)):
        found.append("phone number")
    return found


def host_match(host, domain):
    """True if a host is the domain itself or one of its subdomains."""
    return host == domain or host.endswith("." + domain)


def word_in(text, word):
    """True if a word appears in a text as a whole word."""
    return re.search(r"(?<!\w)" + re.escape(word.lower()) + r"(?!\w)", text) is not None


class AutoMod(commands.Cog):
    """Applies the automatic moderation rules to every message."""
    grp = app_commands.Group(
        name="automod",
        description="Automatic moderation",
        default_permissions=discord.Permissions(manage_guild=True),
        guild_only=True,
    )

    def __init__(self, bot):
        """Keep the bot reference and prepare the state of this cog."""
        self.bot = bot
        self.flood = {}
        self.resolver = Resolver()
        self.removed = deque(maxlen=300)

    async def cog_unload(self):
        """Close the HTTP session used to follow short links."""
        await self.resolver.close()

    def get_rules(self, a, channel):
        """Find the channel rule for a channel, its parent or the default rule."""
        for key in (str(channel.id), str(getattr(channel, "parent_id", None)), "all"):
            if key in a["channels"]:
                return a["channels"][key]
        return None

    async def check_blocklist(self, msg, a):
        """Check a message against the blocked links, texts and image hashes and return the reason or None."""
        b = a["blocklist"]
        text = msg.content.lower()
        urls = [text] + [e.url.lower() for e in msg.embeds if e.url] + [x.url.lower() for x in msg.attachments]
        blob = "\n".join(urls)
        if any(x.lower() in blob for x in b["link"]):
            return "blocked link"
        if any(x.lower() in text for x in b["message"]):
            return "blocked message"
        if any(i["url"] and i["url"].split("?")[0].lower() in blob for i in b["image"]):
            return "blocked image"
        hashes = {i["hash"] for i in b["image"] if i["hash"]}
        if hashes:
            for x in msg.attachments:
                if is_image(x) and x.size <= MAX_BYTES and hashlib.sha256(await x.read()).hexdigest() in hashes:
                    return "blocked image"
        return None

    async def check_shortlinks(self, text, a):
        """Follow shortened links and return the reason if they lead to a listed or unverifiable target, else None."""
        sl = a["shortlinks"]
        if not sl["enabled"]:
            return None
        checked = 0
        for url in URL_RE.findall(text):
            host = host_of(url)
            if not host or not any(host_match(host, d.lower()) for d in sl["domains"]):
                continue
            if not sl["resolve"]:
                return f"short link {host}"
            checked += 1
            if checked > MAX_RESOLVES:
                return "too many short links"
            final = await self.resolver.final_url(url.rstrip(".,)>"))
            if final is None:
                if sl["block_unresolved"]:
                    return f"short link {host} could not be verified"
                continue
            target = host_of(final) or ""
            ph = a["phishing"]
            if any(host_match(target, d.lower()) for d in ph["list"]) and not any(host_match(target, d.lower()) for d in ph["allow"]):
                return f"short link leads to phishing domain {target}"
            if any(x.lower() in final.lower() for x in a["blocklist"]["link"]):
                return f"short link leads to a blocked link ({target})"
            if ph["enabled"] and ph["lookalike"] and any(b in target for b in BRANDS) and not any(host_match(target, o) for o in OFFICIAL):
                return f"short link leads to lookalike domain {target}"
        return None

    def check_newlinks(self, msg, found, a):
        """Return the reason if a member who joined recently posts a link that is not allowed, else None."""
        nl = a["newlinks"]
        member = msg.author
        joined = getattr(member, "joined_at", None)
        if not nl["enabled"] or not found or joined is None:
            return None
        if (discord.utils.utcnow() - joined).total_seconds() >= nl["hours"] * 3600:
            return None
        if all(any(host_match(h, d.lower()) for d in nl["allow"]) for h in found):
            return None
        return f"links are not allowed in the first {nl['hours']} hours"

    async def scan(self, msg, a):
        """Run every enabled rule on a message and return (rule, reason, action) for the first hit."""
        text, low = msg.content, msg.content.lower()
        found = hosts(text) + [h for e in msg.embeds if e.url for h in hosts(e.url)]
        ph = a["phishing"]
        if ph["enabled"]:
            for h in found:
                if any(host_match(h, d.lower()) for d in ph["allow"]):
                    continue
                if any(host_match(h, d.lower()) for d in ph["list"]):
                    return "phishing", f"phishing domain {h}", ph["action"]
                if ph["lookalike"] and any(b in h for b in BRANDS) and not any(host_match(h, o) for o in OFFICIAL):
                    return "phishing", f"lookalike domain {h}", ph["action"]
        hit = await self.check_blocklist(msg, a)
        if hit:
            return "blocklist", hit, "jail" if a["jail_on_blocklist"] else "delete"
        hit = await self.check_shortlinks(text, a)
        if hit:
            return "shortlinks", hit, a["shortlinks"]["action"]
        hit = self.check_newlinks(msg, found, a)
        if hit:
            return "newlinks", hit, a["newlinks"]["action"]
        rules = self.get_rules(a, msg.channel)
        if rules:
            if rules["links"] and URL_RE.search(text):
                return "channel rule", "links not allowed", "delete"
            if rules["images"] and has_image(msg):
                return "channel rule", "images not allowed", "delete"
            if rules["videos"] and has_video(msg):
                return "channel rule", "videos not allowed", "delete"
        w = a["words"]
        if w["enabled"] and any(word_in(low, x) for x in w["list"]):
            return "words", "filtered word", w["action"]
        inv = a["invites"]
        if inv["enabled"]:
            allow = {x.lower() for x in inv["allow"]}
            if any(c.lower() not in allow for c in INVITE_RE.findall(text)):
                return "invites", "invite link", inv["action"]
        pii = a["pii"]
        if pii["enabled"]:
            kinds_found = find_pii(text, pii)
            if kinds_found:
                return "pii", "personal data: " + ", ".join(kinds_found), pii["action"]
        for key, label in (("doxxing", "doxxing"), ("threats", "threat")):
            r = a[key]
            if r["enabled"] and any(x.lower() in low for x in r["list"]):
                return key, label, r["action"]
        caps = a["caps"]
        if caps["enabled"]:
            letters = [c for c in text if c.isalpha()]
            if len(letters) >= caps["min_len"] and sum(c.isupper() for c in letters) * 100 / len(letters) >= caps["percent"]:
                return "caps", "too many capital letters", caps["action"]
        men = a["mentions"]
        if men["enabled"] and len(set(msg.mentions)) + len(msg.role_mentions) >= men["max"]:
            return "mentions", "mention spam", men["action"]
        return None

    @staticmethod
    def dry(a, rule):
        """True if a rule only reports because dry-run mode is on for it or for everything."""
        dry = a["dry_run"]
        return "all" in dry or rule.replace(" ", "_") in dry

    async def remove(self, msg, reason, notify=True):
        """Delete a message, log it with its attachments and tell the author. Returns False if it could not be deleted."""
        self.removed.append(msg.id)
        self.bot.bot_deleted.add(msg.id)
        files = await grab_files(msg)
        try:
            await msg.delete()
        except (discord.NotFound, discord.Forbidden):
            self.bot.bot_deleted.discard(msg.id)
            return False
        e = emb("Message removed by AutoMod", color=discord.Color.red(), user=msg.author)
        e.add_field(name="Reason", value=reason, inline=False)
        describe(e, msg)
        self.bot.log(msg.guild, "moderation", e, files)
        if notify:
            try:
                await msg.channel.send(
                    i18n.say(self.bot, msg.guild, "{user} Your message was removed ({reason}).", user=msg.author.mention, reason=reason),
                    delete_after=6,
                    allowed_mentions=discord.AllowedMentions(users=[msg.author]),
                )
            except discord.HTTPException as exc:
                log.warning("channel.send failed: %s", exc)
        return True

    async def act(self, msg, rule, reason, action):
        """Carry out the action of a rule: log only, delete, warn, timeout or jail. Rules in dry-run mode only report."""
        a = self.bot.cfg(msg.guild.id)["automod"]
        a["hits"][rule] = a["hits"].get(rule, 0) + 1
        if self.dry(a, rule):
            e = emb(f"AutoMod dry run: {rule}", color=discord.Color.light_grey(), user=msg.author)
            e.add_field(name="Reason", value=reason, inline=False)
            e.add_field(name="Would have done", value=action)
            describe(e, msg)
            e.add_field(name="Link", value=f"[Jump]({msg.jump_url})")
            self.bot.log(msg.guild, "security", e)
            return
        if action == "log":
            e = emb(f"AutoMod alert: {rule}", color=discord.Color.orange(), user=msg.author)
            e.add_field(name="Reason", value=reason, inline=False)
            describe(e, msg)
            e.add_field(name="Link", value=f"[Jump]({msg.jump_url})")
            self.bot.log(msg.guild, "security", e)
            return
        await self.remove(msg, f"{rule}: {reason}")
        member, guild = msg.author, msg.guild
        why = f"AutoMod: {rule} ({reason})"
        try:
            if action == "warn":
                await self.bot.get_cog("Moderation").warn_member(guild, member, guild.me, why)
            elif action == "timeout":
                await member.timeout(timedelta(minutes=10), reason=why)
                await self.bot.get_cog("Moderation").add_case(guild, "mute", member, guild.me, why, {"auto": True})
            elif action == "jail":
                ok, text = await self.bot.get_cog("Jail").send_to_jail(member, guild.me, why, auto=True)
                if not ok:
                    self.bot.log(guild, "moderation", emb("AutoMod could not jail a member", f"{member.mention}: {text}", discord.Color.red()))
        except discord.HTTPException as exc:
            log.warning("automod action %s on %s failed: %s", action, member, exc)
            self.bot.log(guild, "moderation", emb("AutoMod action failed", f"{action} for {member.mention}: {exc}", discord.Color.red()))

    async def check_flood(self, msg, f):
        """Delete and punish a member who sent too many messages in a short time."""
        dq = self.flood.setdefault((msg.guild.id, msg.author.id), deque())
        now = time.time()
        dq.append((now, msg))
        while dq and now - dq[0][0] > f["seconds"]:
            dq.popleft()
        if len(dq) < f["count"]:
            return
        batch = [m for _, m in dq]
        dq.clear()
        a = self.bot.cfg(msg.guild.id)["automod"]
        a["hits"]["flood"] = a["hits"].get("flood", 0) + 1
        if self.dry(a, "flood"):
            e = emb("AutoMod dry run: flood", color=discord.Color.light_grey(), user=msg.author)
            e.add_field(name="Reason", value=f"{len(batch)} messages in {f['seconds']} seconds")
            e.add_field(name="Link", value=f"[Jump]({msg.jump_url})")
            self.bot.log(msg.guild, "security", e)
            return
        for i, m in enumerate(batch):
            await self.remove(m, "flood", notify=(i == len(batch) - 1))
        if f["timeout"] > 0:
            try:
                await msg.author.timeout(timedelta(minutes=f["timeout"]), reason="Flood")
            except discord.HTTPException as exc:
                log.warning("author.timeout failed: %s", exc)

    def exempt(self, msg, a):
        """True if the author is a moderator or sits in an exempt role or channel."""
        m = msg.author
        return (
            not isinstance(m, discord.Member)
            or m.guild_permissions.manage_messages
            or msg.channel.id in a["exempt_channels"]
            or any(r.id in a["exempt_roles"] for r in m.roles)
        )

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Runs for every new message."""
        if msg.author.bot or not msg.guild or not self.bot.module_on(msg.guild.id, "automod"):
            return
        a = self.bot.cfg(msg.guild.id)["automod"]
        if self.exempt(msg, a):
            return
        hit = await self.scan(msg, a)
        if hit:
            await self.act(msg, *hit)
        elif a["flood"]["enabled"]:
            await self.check_flood(msg, a["flood"])

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        """Report messages that pinged someone and were deleted shortly after."""
        if msg.author.bot or not msg.guild or msg.id in self.removed or not self.bot.module_on(msg.guild.id, "automod"):
            return
        a = self.bot.cfg(msg.guild.id)["automod"]
        g = a["ghostping"]
        if not g["enabled"] or (discord.utils.utcnow() - msg.created_at).total_seconds() > g["max_age"]:
            return
        if msg.channel.id in a["exempt_channels"] or any(r.id in a["exempt_roles"] for r in getattr(msg.author, "roles", [])):
            return
        targets = [m for m in msg.mentions if not m.bot and m.id != msg.author.id]
        roles = list(msg.role_mentions)
        if not targets and not roles and not msg.mention_everyone:
            return
        names = [m.mention for m in targets[:10]] + [r.mention for r in roles[:5]] + (["@everyone"] if msg.mention_everyone else [])
        e = emb("Ghost ping", color=discord.Color.orange(), user=msg.author)
        e.add_field(name="Pinged", value=" ".join(names), inline=False)
        e.add_field(name="Channel", value=msg.channel.mention)
        e.add_field(name="Deleted after", value=f"{int((discord.utils.utcnow() - msg.created_at).total_seconds())} seconds")
        self.bot.log(msg.guild, "security", e)
        if g["notify"]:
            try:
                await msg.channel.send(i18n.say(self.bot, msg.guild, "{user} pinged {names} and deleted the message.", user=msg.author.mention, names=" ".join(names)), delete_after=30, allowed_mentions=discord.AllowedMentions.none())
            except discord.HTTPException as exc:
                log.warning("ghost ping notice failed: %s", exc)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Runs when a message is edited."""
        if after.author.bot or not after.guild or not self.bot.module_on(after.guild.id, "automod"):
            return
        a = self.bot.cfg(after.guild.id)["automod"]
        if self.exempt(after, a):
            return
        hit = await self.scan(after, a)
        if hit:
            await self.act(after, *hit)

    def conf(self, it):
        """Return the automod settings of the server of an interaction."""
        return self.bot.cfg(it.guild_id)["automod"]

    @grp.command(name="status", description="Show which rules are on and what they do")
    async def am_status(self, it: discord.Interaction):
        """Show which rules are on and what they do."""
        a = self.conf(it)
        on = self.bot.module_on(it.guild_id, "automod")
        lines = [f"Module: {'on' if on else 'off'}"]
        for rule in RULES:
            r = a[rule]
            extra = {"caps": f", from {r.get('min_len')} letters, {r.get('percent')} percent", "mentions": f", max {r.get('max')}"}.get(rule, "")
            size = len(r["list"]) if "list" in r else (len(r["allow"]) if "allow" in r else None)
            lines.append(f"{rule}: {'on' if r['enabled'] else 'off'}, action {r['action']}{extra}" + (f", {size} entries" if size is not None else ""))
        g = a["ghostping"]
        lines.append(f"ghostping: {'on' if g['enabled'] else 'off'}, deleted within {g['max_age']}s, notice in channel {g['notify']}")
        if a["dry_run"]:
            lines.append("dry run: " + ", ".join(a["dry_run"]))
        f = a["flood"]
        lines.append(f"flood: {'on' if f['enabled'] else 'off'}, {f['count']} messages in {f['seconds']}s, timeout {f['timeout']} min")
        b = a["blocklist"]
        lines.append(f"blocklist: {len(b['link'])} links, {len(b['message'])} texts, {len(b['image'])} images")
        lines.append(f"channel rules: {len(a['channels'])}, exempt roles: {len(a['exempt_roles'])}, exempt channels: {len(a['exempt_channels'])}")
        await it.response.send_message("\n".join(lines), ephemeral=True)

    @grp.command(name="channel", description="Set what is removed in a channel (no channel = all other channels)")
    @app_commands.describe(channel="Channel", links="Remove links", images="Remove images", videos="Remove videos")
    async def am_channel(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None, links: Optional[bool] = None, images: Optional[bool] = None, videos: Optional[bool] = None):
        """Set what is removed in a channel (no channel = all other channels)."""
        a = self.conf(it)
        key = str(channel.id) if channel else "all"
        r = a["channels"].setdefault(key, {"links": False, "images": False, "videos": False, "blocklist": True})
        for k, v in (("links", links), ("images", images), ("videos", videos)):
            if v is not None:
                r[k] = v
        target = channel.mention if channel else "all other channels"
        await it.response.send_message(f"{target}: links {r['links']}, images {r['images']}, videos {r['videos']}", ephemeral=True)

    @grp.command(name="unchannel", description="Remove the channel rule")
    async def am_unchannel(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None):
        """Remove the channel rule."""
        a = self.conf(it)
        if a["channels"].pop(str(channel.id) if channel else "all", None) is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "No rule found."), ephemeral=True)
        await it.response.send_message(i18n.say(it.client, it.guild, "Rule removed."), ephemeral=True)

    @grp.command(name="toggle", description="Turn a rule on or off and choose its action")
    @app_commands.describe(rule="Rule", enabled="On or off", action="What happens on a hit")
    async def am_toggle(self, it: discord.Interaction, rule: Literal[RULES], enabled: bool, action: Optional[Literal[ACTIONS]] = None):
        """Turn a rule on or off and choose its action."""
        r = self.conf(it)[rule]
        r["enabled"] = enabled
        if action:
            r["action"] = action
        await it.response.send_message(f"{rule}: {'on' if enabled else 'off'}, action {r['action']}", ephemeral=True)

    @grp.command(name="add", description="Add an entry to a list")
    @app_commands.describe(name="List", value="Word, domain or phrase")
    async def am_add(self, it: discord.Interaction, name: Literal[tuple(LISTS)], value: str):
        """Add an entry to a list."""
        sec, key = LISTS[name]
        lst = self.conf(it)[sec][key]
        if value.lower() in (x.lower() for x in lst):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Already in the list."), ephemeral=True)
        lst.append(value)
        await it.response.send_message(f"Added to {name}: {value}", ephemeral=True)

    @grp.command(name="remove", description="Remove an entry from a list")
    async def am_remove(self, it: discord.Interaction, name: Literal[tuple(LISTS)], value: str):
        """Remove an entry from a list."""
        sec, key = LISTS[name]
        lst = self.conf(it)[sec][key]
        hit = next((x for x in lst if x.lower() == value.lower()), None)
        if hit is None:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Not in the list."), ephemeral=True)
        lst.remove(hit)
        await it.response.send_message(f"Removed from {name}: {hit}", ephemeral=True)

    @grp.command(name="show", description="Show a list")
    async def am_show(self, it: discord.Interaction, name: Literal[tuple(LISTS)]):
        """Show a list."""
        sec, key = LISTS[name]
        lst = self.conf(it)[sec][key]
        text = "\n".join(f"{i}. {x}" for i, x in enumerate(lst, 1)) or "empty"
        await it.response.send_message(f"{name}:\n{text}"[:1900], ephemeral=True)

    @grp.command(name="import", description="Import a list from a text file (one entry per line)")
    async def am_import(self, it: discord.Interaction, name: Literal[tuple(LISTS)], file: discord.Attachment):
        """Import a list from a text file (one entry per line)."""
        if file.size > 1024 * 1024:
            return await it.response.send_message(i18n.say(it.client, it.guild, "File too large (max 1 MB)."), ephemeral=True)
        sec, key = LISTS[name]
        lst = self.conf(it)[sec][key]
        have = {x.lower() for x in lst}
        new = 0
        for line in (await file.read()).decode("utf-8", "ignore").splitlines():
            v = line.strip()
            if v and v.lower() not in have:
                lst.append(v)
                have.add(v.lower())
                new += 1
        await it.response.send_message(f"Imported {new} new entries into {name}.", ephemeral=True)

    @grp.command(name="set", description="Change a number or option of a rule")
    @app_commands.describe(rule="Rule", option="Option name, for example max, percent, min_len, lookalike", value="New value")
    async def am_set(self, it: discord.Interaction, rule: Literal[RULES], option: str, value: str):
        """Change a number or option of a rule."""
        r = self.conf(it)[rule]
        if option not in r or option in ("list", "allow", "enabled", "domains"):
            return await it.response.send_message(f"Unknown option. Available: {', '.join(k for k in r if k not in ('list', 'allow', 'enabled', 'domains'))}", ephemeral=True)
        cur = r[option]
        try:
            r[option] = value.lower() in ("1", "true", "yes", "on") if isinstance(cur, bool) else type(cur)(value)
        except ValueError:
            return await it.response.send_message(i18n.say(it.client, it.guild, "Invalid value."), ephemeral=True)
        await it.response.send_message(f"{rule}.{option} = {r[option]}", ephemeral=True)

    @grp.command(name="exemptrole", description="Toggle a role that AutoMod ignores")
    async def am_exrole(self, it: discord.Interaction, role: discord.Role):
        """Toggle a role that AutoMod ignores."""
        lst = self.conf(it)["exempt_roles"]
        lst.remove(role.id) if role.id in lst else lst.append(role.id)
        await it.response.send_message(f"{role.mention} is {'exempt' if role.id in lst else 'no longer exempt'}.", ephemeral=True)

    @grp.command(name="exemptchannel", description="Toggle a channel that AutoMod ignores")
    async def am_exchan(self, it: discord.Interaction, channel: discord.TextChannel):
        """Toggle a channel that AutoMod ignores."""
        lst = self.conf(it)["exempt_channels"]
        lst.remove(channel.id) if channel.id in lst else lst.append(channel.id)
        await it.response.send_message(f"{channel.mention} is {'exempt' if channel.id in lst else 'no longer exempt'}.", ephemeral=True)

    @grp.command(name="flood", description="Configure flood protection")
    async def am_flood(self, it: discord.Interaction, enabled: Optional[bool] = None, count: Optional[app_commands.Range[int, 2, 50]] = None, seconds: Optional[app_commands.Range[int, 1, 60]] = None, timeout: Optional[app_commands.Range[int, 0, 1440]] = None):
        """Configure flood protection."""
        f = self.conf(it)["flood"]
        for k, v in (("enabled", enabled), ("count", count), ("seconds", seconds), ("timeout", timeout)):
            if v is not None:
                f[k] = v
        await it.response.send_message(f"Flood: {'on' if f['enabled'] else 'off'}, {f['count']} messages in {f['seconds']}s, timeout {f['timeout']} min", ephemeral=True)

    @grp.command(name="ghostping", description="Report messages that pinged someone and were deleted quickly")
    @app_commands.describe(enabled="On or off", notify="Post a notice in the channel", max_age="Only count messages deleted within this many seconds")
    async def am_ghost(self, it: discord.Interaction, enabled: Optional[bool] = None, notify: Optional[bool] = None, max_age: Optional[app_commands.Range[int, 5, 3600]] = None):
        """Report messages that pinged someone and were deleted quickly."""
        g = self.conf(it)["ghostping"]
        for k, v in (("enabled", enabled), ("notify", notify), ("max_age", max_age)):
            if v is not None:
                g[k] = v
        await it.response.send_message(f"Ghost ping: {'on' if g['enabled'] else 'off'}, notice {g['notify']}, within {g['max_age']} seconds", ephemeral=True)

    @grp.command(name="dryrun", description="Let a rule only report what it would do, without deleting or punishing")
    @app_commands.describe(rule="Rule, or all", enabled="Dry run on or off")
    async def am_dry(self, it: discord.Interaction, rule: Literal[DRY_RUN_RULES], enabled: bool):
        """Let a rule only report what it would do, without deleting or punishing."""
        dry = self.conf(it)["dry_run"]
        if enabled and rule not in dry:
            dry.append(rule)
        if not enabled and rule in dry:
            dry.remove(rule)
        await it.response.send_message(f"Dry run: {', '.join(dry) or 'off for every rule'}. Hits are posted to the security log.", ephemeral=True)

    @grp.command(name="test", description="Show which rule a text would trigger, without deleting anything")
    @app_commands.describe(text="The message text to check", member="Check as this member (default: you)")
    async def am_test(self, it: discord.Interaction, text: app_commands.Range[str, 1, 2000], member: Optional[discord.Member] = None):
        """Show which rule a text would trigger, without deleting anything."""
        await it.response.defer(ephemeral=True)
        who = member or it.user
        a = self.conf(it)
        fake = SimpleNamespace(
            content=text, embeds=[], attachments=[], channel=it.channel, author=who, guild=it.guild,
            mentions={int(i) for i in ID_RE.findall(text)}, role_mentions=set(ROLE_RE.findall(text)),
        )
        hit = await self.scan(fake, a)
        lines = [f"Tested as {who.mention}. Nothing was deleted."]
        if self.exempt(fake, a):
            lines.append("This member is exempt (Manage Messages, an exempt role or an exempt channel), so no rule would act.")
        if hit:
            rule, reason, action = hit
            lines.append(f"Rule: {rule}\nReason: {reason}\nAction: {action}" + ("\nDry run is on for this rule, it would only be reported." if self.dry(a, rule) else ""))
        else:
            lines.append("No rule would trigger. Flood protection and image rules need real messages and are not part of this test.")
        await it.followup.send("\n".join(lines), allowed_mentions=discord.AllowedMentions.none())

    @grp.command(name="block", description="Add a link, text or image to the blocklist")
    @app_commands.describe(kind="What to block", value="Link, text or image URL", image="Upload an image")
    async def am_block(self, it: discord.Interaction, kind: Literal["link", "message", "image"], value: Optional[str] = None, image: Optional[discord.Attachment] = None):
        """Add a link, text or image to the blocklist."""
        d = self.conf(it)["blocklist"]
        await it.response.defer(ephemeral=True)
        if kind != "image":
            if not value:
                return await it.followup.send(i18n.say(it.client, it.guild, "Value is missing."))
            if value.lower() in (x.lower() for x in d[kind]):
                return await it.followup.send(i18n.say(it.client, it.guild, "Already blocked."))
            d[kind].append(value)
            return await it.followup.send(f"Blocked: {value}")
        if not value and not image:
            return await it.followup.send(i18n.say(it.client, it.guild, "Upload an image or provide a URL."))
        entry = {"label": None, "hash": None, "url": None}
        if image:
            if not is_image(image):
                return await it.followup.send(i18n.say(it.client, it.guild, "That file is not an image."))
            entry["hash"], entry["label"] = hashlib.sha256(await image.read()).hexdigest(), image.filename
        if value:
            entry["url"], entry["label"] = value, entry["label"] or value
            if not entry["hash"]:
                try:
                    async with self.bot.session.get(value, timeout=15) as r:
                        raw = await r.content.read(MAX_BYTES + 1) if r.status == 200 else b""
                    entry["hash"] = hashlib.sha256(raw).hexdigest() if 0 < len(raw) <= MAX_BYTES else None
                except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
                    log.warning("could not download %s to hash it: %s", value, exc)
        if any((entry["hash"] and x["hash"] == entry["hash"]) or (entry["url"] and x["url"] == entry["url"]) for x in d["image"]):
            return await it.followup.send(i18n.say(it.client, it.guild, "Already blocked."))
        d["image"].append(entry)
        await it.followup.send(f"Blocked: {entry['label']}")

    @grp.command(name="unblock", description="Remove an entry from the blocklist")
    async def am_unblock(self, it: discord.Interaction, kind: Literal["link", "message", "image"], number: int):
        """Remove an entry from the blocklist."""
        items = self.conf(it)["blocklist"][kind]
        if not 1 <= number <= len(items):
            return await it.response.send_message(i18n.say(it.client, it.guild, "Invalid number."), ephemeral=True)
        items.pop(number - 1)
        await it.response.send_message(i18n.say(it.client, it.guild, "Removed."), ephemeral=True)

    @grp.command(name="blocklist", description="Show the blocklist")
    async def am_blocklist(self, it: discord.Interaction):
        """Show the blocklist."""
        d = self.conf(it)["blocklist"]

        def fmt(items, key=None):
            """Format a list of blocklist entries as numbered lines."""
            return "\n".join(f"{n}. {x[key] if key else x}" for n, x in enumerate(items, 1))[:1000] or "-"

        e = discord.Embed(title="Blocklist")
        e.add_field(name="Links", value=fmt(d["link"]), inline=False)
        e.add_field(name="Messages", value=fmt(d["message"]), inline=False)
        e.add_field(name="Images", value=fmt(d["image"], "label"), inline=False)
        await it.response.send_message(embed=e, ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(AutoMod(bot))
