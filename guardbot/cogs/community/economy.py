"""Server currency: daily reward, work, payments, a shop with roles and a leaderboard."""

import logging
import random
import time
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from ...cog import BaseCog
from ... import i18n
from ...utils import emb

log = logging.getLogger(__name__)

MAX_SHOP = 25


def fmt_amount(conf, amount):
    """Write an amount with the name of the currency."""
    return f"{amount:,} {conf['name']}"


def cooldown_left(last, seconds, now=None):
    """Seconds until an action may be repeated, 0 when it may be done now."""
    return max(0, int(last + seconds - (now if now is not None else time.time())))


def wait_text(seconds):
    """Write a waiting time as hours and minutes."""
    h, m = divmod(max(1, seconds) // 60 + (1 if seconds % 60 else 0), 60)
    return (f"{h}h " if h else "") + f"{m}m"


class Economy(BaseCog):
    """Server currency."""
    section = "economy"

    def __init__(self, bot):
        """Keep the bot reference."""
        self.bot = bot

    def balance_of(self, gid, uid):
        """Return the balance of a user without creating a record."""
        return self.bot.store.user_data.get(str(gid), {}).get(str(uid), {}).get("coins", 0)

    def add(self, gid, uid, amount):
        """Change a balance by an amount, never below zero and never above the cap. Returns the new balance."""
        rec = self.bot.store.user(gid, uid)
        rec["coins"] = min(max(0, rec.get("coins", 0) + amount), self.conf(gid)["max_balance"])
        return rec["coins"]

    def s(self, guild, text, **values):
        """Translate a text into the language of the server."""
        return i18n.say(self.bot, guild, text, **values)

    async def cog_check(self, ctx):
        """Keep the commands to servers."""
        return ctx.guild is not None

    @commands.hybrid_group(name="economy", fallback="balance", description="Show a balance")
    @commands.guild_only()
    @app_commands.describe(member="Whose balance to show")
    async def economy(self, ctx, member: Optional[discord.Member] = None):
        """Show a balance."""
        member = member or ctx.author
        await ctx.send(self.s(ctx.guild, "{member} has {amount}.", member=member.display_name, amount=fmt_amount(self.conf(ctx.guild.id), self.balance_of(ctx.guild.id, member.id))), ephemeral=True)

    @economy.command(name="daily", description="Collect the daily reward")
    async def daily(self, ctx):
        """Collect the daily reward."""
        c = self.conf(ctx.guild.id)
        rec = self.bot.store.user(ctx.guild.id, ctx.author.id)
        left = cooldown_left(rec.get("daily_at", 0), c["daily_hours"] * 3600)
        if left:
            return await ctx.send(self.s(ctx.guild, "You can collect again in {time}.", time=wait_text(left)), ephemeral=True)
        rec["daily_at"] = int(time.time())
        total = self.add(ctx.guild.id, ctx.author.id, c["daily"])
        await ctx.send(self.s(ctx.guild, "You received {amount}. Balance: {total}.", amount=fmt_amount(c, c["daily"]), total=fmt_amount(c, total)), ephemeral=True)

    @economy.command(name="work", description="Earn a small random amount")
    async def work(self, ctx):
        """Earn a small random amount."""
        c = self.conf(ctx.guild.id)
        rec = self.bot.store.user(ctx.guild.id, ctx.author.id)
        left = cooldown_left(rec.get("work_at", 0), c["work_minutes"] * 60)
        if left:
            return await ctx.send(self.s(ctx.guild, "You can work again in {time}.", time=wait_text(left)), ephemeral=True)
        rec["work_at"] = int(time.time())
        gain = random.randint(min(c["work_min"], c["work_max"]), max(c["work_min"], c["work_max"]))
        total = self.add(ctx.guild.id, ctx.author.id, gain)
        await ctx.send(self.s(ctx.guild, "You earned {amount}. Balance: {total}.", amount=fmt_amount(c, gain), total=fmt_amount(c, total)), ephemeral=True)

    @economy.command(name="pay", description="Give some of your balance to a member")
    @app_commands.describe(member="Receiver", amount="Amount")
    async def pay(self, ctx, member: discord.Member, amount: commands.Range[int, 1, 1000000000]):
        """Give some of your balance to a member."""
        c = self.conf(ctx.guild.id)
        if member.bot or member.id == ctx.author.id:
            return await ctx.send(self.s(ctx.guild, "Choose another member."), ephemeral=True)
        if self.balance_of(ctx.guild.id, ctx.author.id) < amount:
            return await ctx.send(self.s(ctx.guild, "You do not have that much."), ephemeral=True)
        if self.balance_of(ctx.guild.id, member.id) + amount > c["max_balance"]:
            return await ctx.send(self.s(ctx.guild, "The receiver would exceed the maximum balance."), ephemeral=True)
        self.add(ctx.guild.id, ctx.author.id, -amount)
        self.add(ctx.guild.id, member.id, amount)
        await ctx.send(self.s(ctx.guild, "{giver} gave {amount} to {receiver}.", giver=ctx.author.display_name, amount=fmt_amount(c, amount), receiver=member.mention), allowed_mentions=discord.AllowedMentions(users=[member]))

    @economy.command(name="leaderboard", description="The richest members")
    async def leaderboard(self, ctx):
        """The richest members."""
        c = self.conf(ctx.guild.id)
        rows = sorted(((u.get("coins", 0), uid) for uid, u in self.bot.store.user_data.get(str(ctx.guild.id), {}).items() if u.get("coins", 0) > 0), reverse=True)[:10]
        text = "\n".join(f"{i}. <@{uid}>: {fmt_amount(c, coins)}" for i, (coins, uid) in enumerate(rows, 1)) or self.s(ctx.guild, "Nobody has anything yet.")
        await ctx.send(embed=emb(self.s(ctx.guild, "Richest members"), text), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @economy.command(name="shop", description="Show the shop")
    async def shop(self, ctx):
        """Show the shop."""
        c = self.conf(ctx.guild.id)
        lines = [
            self.s(ctx.guild, "{id}. {name} for {price}", id=iid, name=it["name"], price=fmt_amount(c, it["price"]))
            + (self.s(ctx.guild, " (gives {role})", role=f"<@&{it['role']}>") if it["role"] else "")
            + (self.s(ctx.guild, ", {n} left", n=it["stock"]) if it["stock"] is not None else "")
            for iid, it in c["shop"].items()
        ]
        await ctx.send(embed=emb(self.s(ctx.guild, "Shop"), "\n".join(lines) or self.s(ctx.guild, "The shop is empty.")), ephemeral=True, allowed_mentions=discord.AllowedMentions.none())

    @economy.command(name="buy", description="Buy something from the shop")
    @app_commands.describe(item="Number of the item in the shop")
    async def buy(self, ctx, item: int):
        """Buy something from the shop."""
        c = self.conf(ctx.guild.id)
        it = c["shop"].get(str(item))
        if not it:
            return await ctx.send(self.s(ctx.guild, "There is no such item."), ephemeral=True)
        if it["stock"] is not None and it["stock"] <= 0:
            return await ctx.send(self.s(ctx.guild, "This item is sold out."), ephemeral=True)
        if self.balance_of(ctx.guild.id, ctx.author.id) < it["price"]:
            return await ctx.send(self.s(ctx.guild, "You do not have enough."), ephemeral=True)
        role = None
        if it["role"]:
            role = ctx.guild.get_role(it["role"])
            if role is None or not role.is_assignable():
                return await ctx.send(self.s(ctx.guild, "I cannot give that role right now. Nothing was charged."), ephemeral=True)
            if role in ctx.author.roles:
                return await ctx.send(self.s(ctx.guild, "You already have that role."), ephemeral=True)
        # Charge before the first await so two quick purchases cannot both pass the balance check.
        self.add(ctx.guild.id, ctx.author.id, -it["price"])
        if it["stock"] is not None:
            it["stock"] -= 1
        if role is not None:
            try:
                await ctx.author.add_roles(role, reason="Shop purchase")
            except discord.HTTPException:
                self.add(ctx.guild.id, ctx.author.id, it["price"])
                if it["stock"] is not None:
                    it["stock"] += 1
                return await ctx.send(self.s(ctx.guild, "I could not give you the role. Nothing was charged."), ephemeral=True)
        else:
            rec = self.bot.store.user(ctx.guild.id, ctx.author.id)
            rec.setdefault("items", {})
            rec["items"][it["name"]] = rec["items"].get(it["name"], 0) + 1
        await ctx.send(self.s(ctx.guild, "You bought {item} for {amount}.", item=it["name"], amount=fmt_amount(c, it["price"])), ephemeral=True)

    @economy.command(name="inventory", description="Show what you bought")
    async def inventory(self, ctx):
        """Show what you bought."""
        items = self.bot.store.user_data.get(str(ctx.guild.id), {}).get(str(ctx.author.id), {}).get("items", {})
        await ctx.send("\n".join(f"{n} x {name}" for name, n in items.items()) or self.s(ctx.guild, "You own no items."), ephemeral=True)

    @economy.command(name="give", description="Staff: add to the balance of a member")
    @commands.has_guild_permissions(manage_guild=True)
    @app_commands.describe(member="Member", amount="Amount, negative takes away")
    async def give(self, ctx, member: discord.Member, amount: commands.Range[int, -1000000000, 1000000000]):
        """Add to the balance of a member, or take away with a negative amount."""
        total = self.add(ctx.guild.id, member.id, amount)
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "{display_name} now has {fmt_amount}.", display_name=member.display_name, fmt_amount=fmt_amount(self.conf(ctx.guild.id), total)), ephemeral=True)

    @economy.command(name="shopadd", description="Staff: add an item to the shop")
    @commands.has_guild_permissions(manage_guild=True)
    @app_commands.describe(name="Name", price="Price", role="Role the buyer gets, empty for a plain item", stock="How many can be bought, empty for unlimited")
    async def shopadd(self, ctx, name: str, price: commands.Range[int, 1, 1000000000], role: Optional[discord.Role] = None, stock: Optional[commands.Range[int, 1, 100000]] = None):
        """Add an item to the shop."""
        c = self.conf(ctx.guild.id)
        if len(c["shop"]) >= MAX_SHOP:
            return await ctx.send(i18n.say(ctx.bot, ctx.guild, "The shop is full ({MAX_SHOP} items).", MAX_SHOP=MAX_SHOP), ephemeral=True)
        if role is not None:
            if not role.is_assignable() or role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner_id:
                return await ctx.send(i18n.say(ctx.bot, ctx.guild, "That role cannot be given by me or is above your own role."), ephemeral=True)
            if any(getattr(role.permissions, p) for p in ("administrator", "manage_guild", "manage_roles", "manage_channels", "ban_members", "kick_members", "manage_webhooks")):
                return await ctx.send(i18n.say(ctx.bot, ctx.guild, "Roles with dangerous permissions cannot be sold."), ephemeral=True)
        iid = str(c["next_item"])
        c["next_item"] += 1
        c["shop"][iid] = {"name": name[:60], "price": price, "role": role.id if role else None, "stock": stock}
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Added as item {iid}.", iid=iid), ephemeral=True)

    @economy.command(name="shopremove", description="Staff: remove an item from the shop")
    @commands.has_guild_permissions(manage_guild=True)
    @app_commands.describe(item="Number of the item")
    async def shopremove(self, ctx, item: int):
        """Remove an item from the shop."""
        removed = self.conf(ctx.guild.id)["shop"].pop(str(item), None)
        await ctx.send("Removed." if removed else "There is no such item.", ephemeral=True)

    @economy.command(name="config", description="Staff: change the currency settings")
    @commands.has_guild_permissions(manage_guild=True)
    @app_commands.describe(name="Name of the currency", daily="Daily reward", daily_hours="Hours between daily rewards", work_min="Smallest work reward", work_max="Largest work reward", work_minutes="Minutes between work rewards")
    async def config(
        self, ctx, name: Optional[commands.Range[str, 1, 20]] = None, daily: Optional[commands.Range[int, 0, 1000000]] = None, daily_hours: Optional[commands.Range[int, 1, 720]] = None,
        work_min: Optional[commands.Range[int, 0, 1000000]] = None, work_max: Optional[commands.Range[int, 0, 1000000]] = None, work_minutes: Optional[commands.Range[int, 1, 10080]] = None,
    ):
        """Change the currency settings, or show them when nothing is passed."""
        c = self.conf(ctx.guild.id)
        for key, value in (("name", name), ("daily", daily), ("daily_hours", daily_hours), ("work_min", work_min), ("work_max", work_max), ("work_minutes", work_minutes)):
            if value is not None:
                c[key] = value
        await ctx.send(i18n.say(ctx.bot, ctx.guild, "Currency {name}: daily {daily} every {daily_hours}h, work {work_min} to {work_max} every {work_minutes}m, {count} shop items.", name=c['name'], daily=c['daily'], daily_hours=c['daily_hours'], work_min=c['work_min'], work_max=c['work_max'], work_minutes=c['work_minutes'], count=len(c['shop'])), ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(Economy(bot))
