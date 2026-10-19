# Copyright (c) Justyn
import hashlib
import re
import time
from collections import deque
from datetime import timedelta
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import describe, emb, grab_files, has_image, has_video, hosts, is_image, URL_RE

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
}
RULES = ("words", "caps", "mentions", "invites", "phishing", "pii", "doxxing", "threats")
ACTIONS = ("log", "delete", "warn", "timeout", "jail")


def luhn(num):
    total, flip = 0, False
    for ch in reversed(num):
        d = int(ch)
        if flip:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
        flip = not flip
    return total % 10 == 0


def iban_ok(s):
    s = s.replace(" ", "").upper()
    if not 15 <= len(s) <= 34:
        return False
    moved = s[4:] + s[:4]
    return int("".join(str(int(c, 36)) for c in moved)) % 97 == 1


def find_pii(text, opts):
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
    return host == domain or host.endswith("." + domain)


def word_in(text, word):
    return re.search(r"(?<!\w)" + re.escape(word.lower()) + r"(?!\w)", text) is not None


class AutoMod(commands.Cog):
    grp = app_commands.Group(
        name="automod",
        description="Automatic moderation",
        default_permissions=discord.Permissions(manage_guild=True),
        guild_only=True,
    )

    def __init__(self, bot):
        self.bot = bot
        self.flood = {}

    def get_rules(self, a, channel):
        for key in (str(channel.id), str(getattr(channel, "parent_id", None)), "all"):
            if key in a["channels"]:
                return a["channels"][key]
        return None

    async def check_blocklist(self, msg, a):
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

    async def scan(self, msg, a):
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

    async def remove(self, msg, reason, notify=True):
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
                    f"{msg.author.mention} Your message was removed ({reason}).",
                    delete_after=6,
                    allowed_mentions=discord.AllowedMentions(users=[msg.author]),
                )
            except discord.HTTPException:
                pass
        return True

    async def act(self, msg, rule, reason, action):
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
                await self.bot.get_cog("Jail").send_to_jail(member, guild.me, why, auto=True)
        except (discord.HTTPException, AttributeError):
            pass

    async def check_flood(self, msg, f):
        dq = self.flood.setdefault((msg.guild.id, msg.author.id), deque())
        now = time.time()
        dq.append((now, msg))
        while dq and now - dq[0][0] > f["seconds"]:
            dq.popleft()
        if len(dq) < f["count"]:
            return
        batch = [m for _, m in dq]
        dq.clear()
        for i, m in enumerate(batch):
            await self.remove(m, "flood", notify=(i == len(batch) - 1))
        if f["timeout"] > 0:
            try:
                await msg.author.timeout(timedelta(minutes=f["timeout"]), reason="Flood")
            except discord.HTTPException:
                pass

    def exempt(self, msg, a):
        m = msg.author
        return (
            not isinstance(m, discord.Member)
            or m.guild_permissions.manage_messages
            or msg.channel.id in a["exempt_channels"]
            or any(r.id in a["exempt_roles"] for r in m.roles)
        )

    @commands.Cog.listener()
    async def on_message(self, msg):
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
    async def on_message_edit(self, before, after):
        if after.author.bot or not after.guild or not self.bot.module_on(after.guild.id, "automod"):
            return
        a = self.bot.cfg(after.guild.id)["automod"]
        if self.exempt(after, a):
            return
        hit = await self.scan(after, a)
        if hit:
            await self.act(after, *hit)

    def conf(self, it):
        return self.bot.cfg(it.guild_id)["automod"]

    @grp.command(name="channel", description="Set what is removed in a channel (no channel = all other channels)")
    @app_commands.describe(channel="Channel", links="Remove links", images="Remove images", videos="Remove videos")
    async def am_channel(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None, links: Optional[bool] = None, images: Optional[bool] = None, videos: Optional[bool] = None):
        a = self.conf(it)
        key = str(channel.id) if channel else "all"
        r = a["channels"].setdefault(key, {"links": False, "images": False, "videos": False, "blocklist": True})
        for k, v in (("links", links), ("images", images), ("videos", videos)):
            if v is not None:
                r[k] = v
        self.bot.store.mark("config")
        target = channel.mention if channel else "all other channels"
        await it.response.send_message(f"{target}: links {r['links']}, images {r['images']}, videos {r['videos']}", ephemeral=True)

    @grp.command(name="unchannel", description="Remove the channel rule")
    async def am_unchannel(self, it: discord.Interaction, channel: Optional[discord.TextChannel] = None):
        a = self.conf(it)
        if a["channels"].pop(str(channel.id) if channel else "all", None) is None:
            return await it.response.send_message("No rule found.", ephemeral=True)
        self.bot.store.mark("config")
        await it.response.send_message("Rule removed.", ephemeral=True)

    @grp.command(name="toggle", description="Turn a rule on or off and choose its action")
    @app_commands.describe(rule="Rule", enabled="On or off", action="What happens on a hit")
    async def am_toggle(self, it: discord.Interaction, rule: Literal[RULES], enabled: bool, action: Optional[Literal[ACTIONS]] = None):
        r = self.conf(it)[rule]
        r["enabled"] = enabled
        if action:
            r["action"] = action
        self.bot.store.mark("config")
        await it.response.send_message(f"{rule}: {'on' if enabled else 'off'}, action {r['action']}", ephemeral=True)

    @grp.command(name="add", description="Add an entry to a list")
    @app_commands.describe(name="List", value="Word, domain or phrase")
    async def am_add(self, it: discord.Interaction, name: Literal[tuple(LISTS)], value: str):
        sec, key = LISTS[name]
        lst = self.conf(it)[sec][key]
        if value.lower() in (x.lower() for x in lst):
            return await it.response.send_message("Already in the list.", ephemeral=True)
        lst.append(value)
        self.bot.store.mark("config")
        await it.response.send_message(f"Added to {name}: {value}", ephemeral=True)

    @grp.command(name="remove", description="Remove an entry from a list")
    async def am_remove(self, it: discord.Interaction, name: Literal[tuple(LISTS)], value: str):
        sec, key = LISTS[name]
        lst = self.conf(it)[sec][key]
        hit = next((x for x in lst if x.lower() == value.lower()), None)
        if hit is None:
            return await it.response.send_message("Not in the list.", ephemeral=True)
        lst.remove(hit)
        self.bot.store.mark("config")
        await it.response.send_message(f"Removed from {name}: {hit}", ephemeral=True)

    @grp.command(name="show", description="Show a list")
    async def am_show(self, it: discord.Interaction, name: Literal[tuple(LISTS)]):
        sec, key = LISTS[name]
        lst = self.conf(it)[sec][key]
        text = "\n".join(f"{i}. {x}" for i, x in enumerate(lst, 1)) or "empty"
        await it.response.send_message(f"{name}:\n{text}"[:1900], ephemeral=True)

    @grp.command(name="import", description="Import a list from a text file (one entry per line)")
    async def am_import(self, it: discord.Interaction, name: Literal[tuple(LISTS)], file: discord.Attachment):
        if file.size > 1024 * 1024:
            return await it.response.send_message("File too large (max 1 MB).", ephemeral=True)
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
        self.bot.store.mark("config")
        await it.response.send_message(f"Imported {new} new entries into {name}.", ephemeral=True)

    @grp.command(name="set", description="Change a number or option of a rule")
    @app_commands.describe(rule="Rule", option="Option name, for example max, percent, min_len, lookalike", value="New value")
    async def am_set(self, it: discord.Interaction, rule: Literal[RULES], option: str, value: str):
        r = self.conf(it)[rule]
        if option not in r or option in ("list", "allow", "enabled"):
            return await it.response.send_message(f"Unknown option. Available: {', '.join(k for k in r if k not in ('list', 'allow', 'enabled'))}", ephemeral=True)
        cur = r[option]
        try:
            r[option] = value.lower() in ("1", "true", "yes", "on") if isinstance(cur, bool) else type(cur)(value)
        except ValueError:
            return await it.response.send_message("Invalid value.", ephemeral=True)
        self.bot.store.mark("config")
        await it.response.send_message(f"{rule}.{option} = {r[option]}", ephemeral=True)

    @grp.command(name="exemptrole", description="Toggle a role that AutoMod ignores")
    async def am_exrole(self, it: discord.Interaction, role: discord.Role):
        lst = self.conf(it)["exempt_roles"]
        lst.remove(role.id) if role.id in lst else lst.append(role.id)
        self.bot.store.mark("config")
        await it.response.send_message(f"{role.mention} is {'exempt' if role.id in lst else 'no longer exempt'}.", ephemeral=True)

    @grp.command(name="exemptchannel", description="Toggle a channel that AutoMod ignores")
    async def am_exchan(self, it: discord.Interaction, channel: discord.TextChannel):
        lst = self.conf(it)["exempt_channels"]
        lst.remove(channel.id) if channel.id in lst else lst.append(channel.id)
        self.bot.store.mark("config")
        await it.response.send_message(f"{channel.mention} is {'exempt' if channel.id in lst else 'no longer exempt'}.", ephemeral=True)

    @grp.command(name="flood", description="Configure flood protection")
    async def am_flood(self, it: discord.Interaction, enabled: Optional[bool] = None, count: Optional[app_commands.Range[int, 2, 50]] = None, seconds: Optional[app_commands.Range[int, 1, 60]] = None, timeout: Optional[app_commands.Range[int, 0, 1440]] = None):
        f = self.conf(it)["flood"]
        for k, v in (("enabled", enabled), ("count", count), ("seconds", seconds), ("timeout", timeout)):
            if v is not None:
                f[k] = v
        self.bot.store.mark("config")
        await it.response.send_message(f"Flood: {'on' if f['enabled'] else 'off'}, {f['count']} messages in {f['seconds']}s, timeout {f['timeout']} min", ephemeral=True)

    @grp.command(name="block", description="Add a link, text or image to the blocklist")
    @app_commands.describe(kind="What to block", value="Link, text or image URL", image="Upload an image")
    async def am_block(self, it: discord.Interaction, kind: Literal["link", "message", "image"], value: Optional[str] = None, image: Optional[discord.Attachment] = None):
        d = self.conf(it)["blocklist"]
        await it.response.defer(ephemeral=True)
        if kind != "image":
            if not value:
                return await it.followup.send("Value is missing.")
            if value.lower() in (x.lower() for x in d[kind]):
                return await it.followup.send("Already blocked.")
            d[kind].append(value)
            self.bot.store.mark("config")
            return await it.followup.send(f"Blocked: {value}")
        if not value and not image:
            return await it.followup.send("Upload an image or provide a URL.")
        entry = {"label": None, "hash": None, "url": None}
        if image:
            if not is_image(image):
                return await it.followup.send("That file is not an image.")
            entry["hash"], entry["label"] = hashlib.sha256(await image.read()).hexdigest(), image.filename
        if value:
            entry["url"], entry["label"] = value, entry["label"] or value
            if not entry["hash"]:
                try:
                    async with self.bot.session.get(value, timeout=15) as r:
                        raw = await r.content.read(MAX_BYTES + 1) if r.status == 200 else b""
                    entry["hash"] = hashlib.sha256(raw).hexdigest() if 0 < len(raw) <= MAX_BYTES else None
                except Exception:
                    pass
        if any((entry["hash"] and x["hash"] == entry["hash"]) or (entry["url"] and x["url"] == entry["url"]) for x in d["image"]):
            return await it.followup.send("Already blocked.")
        d["image"].append(entry)
        self.bot.store.mark("config")
        await it.followup.send(f"Blocked: {entry['label']}")

    @grp.command(name="unblock", description="Remove an entry from the blocklist")
    async def am_unblock(self, it: discord.Interaction, kind: Literal["link", "message", "image"], number: int):
        items = self.conf(it)["blocklist"][kind]
        if not 1 <= number <= len(items):
            return await it.response.send_message("Invalid number.", ephemeral=True)
        items.pop(number - 1)
        self.bot.store.mark("config")
        await it.response.send_message("Removed.", ephemeral=True)

    @grp.command(name="blocklist", description="Show the blocklist")
    async def am_blocklist(self, it: discord.Interaction):
        d = self.conf(it)["blocklist"]

        def fmt(items, key=None):
            return "\n".join(f"{n}. {x[key] if key else x}" for n, x in enumerate(items, 1))[:1000] or "-"

        e = discord.Embed(title="Blocklist")
        e.add_field(name="Links", value=fmt(d["link"]), inline=False)
        e.add_field(name="Messages", value=fmt(d["message"]), inline=False)
        e.add_field(name="Images", value=fmt(d["image"], "label"), inline=False)
        await it.response.send_message(embed=e, ephemeral=True)


async def setup(bot):
    await bot.add_cog(AutoMod(bot))
