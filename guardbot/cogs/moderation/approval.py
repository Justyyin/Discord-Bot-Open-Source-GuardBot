"""Two-person rule: serious actions (ban, kick, temporary ban, bulk actions) wait until a second moderator approves them."""

import logging
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import tasks

from ...cog import BaseCog
from ... import i18n
from ...utils import AdminGroup, emb, fmt_duration, trim

log = logging.getLogger(__name__)

ACTIONS = ("ban", "tempban", "kick", "bulk")
PERMISSION = {"ban": "ban_members", "tempban": "ban_members", "kick": "kick_members", "mute": "moderate_members", "bulk": "ban_members"}


def may_decide(member, request, role_id):
    """True if a member may approve or deny a request: not the requester, with the permission of the action or the approver role."""
    if member.id == request["mod"]:
        return False
    if member.id == member.guild.owner_id or member.guild_permissions.administrator:
        return True
    if role_id:
        return any(r.id == role_id for r in member.roles)
    return getattr(member.guild_permissions, PERMISSION.get(request["bulk_kind"] or request["kind"], "ban_members"), False)


def describe(request):
    """One line that says what is waiting for approval."""
    if request["kind"] == "bulk":
        how = f" for {fmt_duration(request['seconds'])}" if request.get("seconds") else ""
        return f"{request['bulk_kind']} of {len(request['ids'])} users{how}"
    how = f" for {fmt_duration(request['seconds'])}" if request.get("seconds") else ""
    return f"{request['kind']} of {request['target_name']} ({request['target']}){how}"


class ApprovalButton(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:apr:(?P<action>ok|no):(?P<id>\d+)"):
    """Persistent approve and deny buttons under a request."""

    def __init__(self, action, rid):
        """Create the button for one action of one request."""
        style = discord.ButtonStyle.success if action == "ok" else discord.ButtonStyle.danger
        super().__init__(discord.ui.Button(label="Approve" if action == "ok" else "Deny", style=style, custom_id=f"gb:apr:{action}:{rid}"))
        self.action, self.rid = action, rid

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls(match["action"], int(match["id"]))

    async def callback(self, interaction):
        """Approve or deny the request."""
        await interaction.client.get_cog("Approval").decide(interaction, self.action, self.rid)


class Approval(BaseCog):
    """Approval by a second moderator."""
    section = "approval"

    ag = AdminGroup(name="approval", description="Serious actions need a second moderator", guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and register the persistent buttons."""
        self.bot = bot
        bot.add_dynamic_items(ApprovalButton)

    async def cog_load(self):
        """Start the loop that expires old requests."""
        self.expire_loop.start()

    async def cog_unload(self):
        """Stop the loop."""
        self.expire_loop.cancel()

    def active(self, gid, kind):
        """True if an action needs approval on this server."""
        return self.bot.module_on(gid, "approval") and kind in self.conf(gid)["actions"]

    async def post(self, guild, channel, request):
        """Post the request with the buttons. Returns the message or None."""
        e = emb(f"Approval needed #{request['id']}", describe(request), discord.Color.orange())
        e.add_field(name="Requested by", value=f"<@{request['mod']}>")
        e.add_field(name="Reason", value=trim(request["reason"] or "No reason given", 500), inline=False)
        e.set_footer(text="A second moderator must decide. The requester cannot approve it.")
        view = discord.ui.View(timeout=None)
        view.add_item(ApprovalButton("ok", request["id"]))
        view.add_item(ApprovalButton("no", request["id"]))
        role = self.conf(guild.id)["role"]
        try:
            return await channel.send(f"<@&{role}>" if role else None, embed=e, view=view, allowed_mentions=discord.AllowedMentions(roles=[discord.Object(role)] if role else []))
        except discord.HTTPException as exc:
            log.warning("approval request could not be posted: %s", exc)
            return None

    def channel_for(self, guild, fallback):
        """The channel for requests: the set one, else the channel where the command was used."""
        ch = guild.get_channel(self.conf(guild.id)["channel"] or 0)
        return ch or fallback

    def create(self, guild, request):
        """Store a request and return it with its number."""
        c = self.conf(guild.id)
        request["id"] = c["next"]
        c["next"] += 1
        request.update({"ts": int(time.time()), "status": "open", "message": None, "channel": None})
        c["items"][str(request["id"])] = request
        return request

    async def gate(self, ctx, kind, target, reason, seconds=None):
        """Called by a moderation command. True if a request was created instead of acting now."""
        c = self.conf(ctx.guild.id)
        if not self.active(ctx.guild.id, kind) or (c["owner_bypass"] and ctx.author.id == ctx.guild.owner_id):
            return False
        channel = self.channel_for(ctx.guild, ctx.channel)
        request = self.create(ctx.guild, {"kind": kind, "bulk_kind": None, "target": target.id, "target_name": str(target), "mod": ctx.author.id, "reason": reason, "seconds": seconds})
        msg = await self.post(ctx.guild, channel, request)
        if msg is None:
            c["items"].pop(str(request["id"]), None)
            await ctx.send(i18n.say(ctx.bot, ctx.guild, "I could not post the request, so nothing was done."), ephemeral=True)
            return True
        request["message"], request["channel"] = msg.id, channel.id
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "This needs the approval of a second moderator. Request #{id} was posted in {mention}.", id=request['id'], mention=channel.mention), ephemeral=True)
        return True

    async def gate_bulk(self, it, kind, ids, reason, seconds):
        """Called by the bulk command after the confirmation. True if a request was created."""
        c = self.conf(it.guild_id)
        if not self.active(it.guild_id, "bulk") or (c["owner_bypass"] and it.user.id == it.guild.owner_id):
            return False
        channel = self.channel_for(it.guild, it.channel)
        request = self.create(it.guild, {"kind": "bulk", "bulk_kind": kind, "ids": ids, "target": 0, "target_name": "", "mod": it.user.id, "reason": reason, "seconds": seconds})
        msg = await self.post(it.guild, channel, request)
        if msg is None:
            c["items"].pop(str(request["id"]), None)
            return False
        request["message"], request["channel"] = msg.id, channel.id
        return True

    async def settle(self, guild, request, text, color):
        """Show the result on the original message and remove the buttons."""
        channel = guild.get_channel(request.get("channel") or 0)
        if channel is None or not request.get("message"):
            return
        try:
            msg = await channel.fetch_message(request["message"])
            e = emb(f"Request #{request['id']} {request['status']}", describe(request), color)
            e.add_field(name="Result", value=trim(text, 900), inline=False)
            await msg.edit(embed=e, view=None)
        except discord.HTTPException as exc:
            log.info("approval message could not be updated: %s", exc)

    async def decide(self, interaction, action, rid):
        """Approve or deny a request."""
        guild = interaction.guild
        c = self.conf(guild.id)
        request = c["items"].get(str(rid))
        if not self.bot.module_on(guild.id, "approval"):
            return await interaction.response.send_message(i18n.say(self.bot, guild, "This module is turned off."), ephemeral=True)
        if not request or request["status"] != "open":
            return await interaction.response.send_message(i18n.say(self.bot, guild, "This request was already decided."), ephemeral=True)
        if not may_decide(interaction.user, request, c["role"]):
            return await interaction.response.send_message(i18n.say(self.bot, guild, "You cannot decide this request. A second moderator with the right permission must do it."), ephemeral=True)
        await interaction.response.defer()
        if action == "no":
            request["status"] = "denied"
            await self.settle(guild, request, f"Denied by {interaction.user}.", discord.Color.red())
            return
        request["status"] = "approved"
        requester = guild.get_member(request["mod"]) or interaction.user
        extra = {"approved_by": interaction.user.id}
        if request["kind"] == "bulk":
            done, failed = await self.bot.get_cog("Bulk").execute(guild, requester, request["bulk_kind"], request["ids"], request["reason"], request.get("seconds"))
            text = f"Approved by {interaction.user}. Done: {len(done)}. Failed: {len(failed)}." + ("\n" + "\n".join(failed[:8]) if failed else "")
        else:
            target = guild.get_member(request["target"])
            if target is None:
                try:
                    target = await self.bot.fetch_user(request["target"])
                except discord.NotFound:
                    request["status"] = "failed"
                    return await self.settle(guild, request, "The user no longer exists.", discord.Color.red())
            ok, text, _ = await self.bot.get_cog("Moderation").punish(guild, requester, target, request["kind"], request["reason"], request.get("seconds"), extra)
            text = f"Approved by {interaction.user}. {text}"
            if not ok:
                request["status"] = "failed"
        await self.settle(guild, request, text, discord.Color.green() if request["status"] == "approved" else discord.Color.red())

    @tasks.loop(seconds=60)
    async def expire_loop(self):
        """Expire requests that nobody decided in time."""
        now = time.time()
        for guild in list(self.bot.guilds):
            c = self.conf(guild.id)
            for rid, request in list(c["items"].items()):
                try:
                    if request["status"] == "open" and now - request["ts"] > c["minutes"] * 60:
                        request["status"] = "expired"
                        await self.settle(guild, request, "Nobody decided in time. Nothing was done.", discord.Color.light_grey())
                    elif request["status"] != "open" and now - request["ts"] > 7 * 86400:
                        c["items"].pop(rid, None)
                except Exception:  # one broken request must not stop the others
                    log.exception("approval expiry of %s failed", rid)
                    c["items"].pop(rid, None)

    @expire_loop.before_loop
    async def _wait(self):
        """Wait until the bot is connected."""
        await self.bot.wait_until_ready()

    @ag.command(name="setup", description="Choose which actions need a second moderator")
    @app_commands.describe(ban="Bans", tempban="Temporary bans", kick="Kicks", bulk="Bulk actions", role="Role of the approvers, empty = anyone with the permission", channel="Channel for the requests, empty = where the command was used", minutes="Minutes until a request expires", owner_bypass="The server owner does not need approval")
    async def setup(
        self, it: discord.Interaction, ban: Optional[bool] = None, tempban: Optional[bool] = None, kick: Optional[bool] = None, bulk: Optional[bool] = None,
        role: Optional[discord.Role] = None, channel: Optional[discord.TextChannel] = None, minutes: Optional[app_commands.Range[int, 1, 10080]] = None, owner_bypass: Optional[bool] = None,
    ):
        """Choose which actions need a second moderator."""
        c = self.conf(it.guild_id)
        for name, value in (("ban", ban), ("tempban", tempban), ("kick", kick), ("bulk", bulk)):
            if value is True and name not in c["actions"]:
                c["actions"].append(name)
            elif value is False and name in c["actions"]:
                c["actions"].remove(name)
        if role is not None:
            c["role"] = role.id
        if channel is not None:
            c["channel"] = channel.id
        if minutes is not None:
            c["minutes"] = minutes
        if owner_bypass is not None:
            c["owner_bypass"] = owner_bypass
        self.bot.cfg(it.guild_id)["modules"]["approval"] = True
        await it.response.send_message(
            i18n.say(it.client, it.guild, "Approval is on for: {value}. Approvers: {value2}. Requests expire after {minutes} minutes.", value=', '.join(c['actions']) or 'nothing', value2='<@&' + str(c['role']) + '>' if c['role'] else 'anyone with the permission of the action', minutes=c['minutes']),
            ephemeral=True, allowed_mentions=discord.AllowedMentions.none(),
        )

    @ag.command(name="list", description="Show open requests")
    async def list_cmd(self, it: discord.Interaction):
        """Show open requests."""
        c = self.conf(it.guild_id)
        lines = [f"#{r['id']} {describe(r)} by <@{r['mod']}> <t:{r['ts']}:R>" for r in c["items"].values() if r["status"] == "open"]
        await it.response.send_message("\n".join(lines[:20]) or "No open requests.", ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @ag.command(name="cancel", description="Withdraw an open request")
    async def cancel(self, it: discord.Interaction, request_id: int):
        """Withdraw an open request."""
        request = self.conf(it.guild_id)["items"].get(str(request_id))
        if not request or request["status"] != "open":
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no open request with that number."), ephemeral=True)
        request["status"] = "cancelled"
        await self.settle(it.guild, request, f"Withdrawn by {it.user}.", discord.Color.light_grey())
        await it.response.send_message(i18n.say(it.client, it.guild, "Request #{request_id} withdrawn.", request_id=request_id), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Approval(bot))
