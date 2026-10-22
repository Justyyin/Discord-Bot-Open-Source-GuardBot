"""Role menus: posts with buttons or a dropdown that give and remove roles."""

import logging
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from .. import i18n
from ..defaults import DANGEROUS
from ..utils import AdminGroup, emb

log = logging.getLogger(__name__)

MAX_BUTTONS = 20
MAX_OPTIONS = 25
MAX_MENUS = 20


def role_problem(role, actor=None):
    """Return why a role cannot be offered in a menu, or None."""
    if role.is_default():
        return "The @everyone role cannot be used."
    if role.managed or not role.is_assignable():
        return "I cannot give that role. Move my bot role above it, or it belongs to an integration."
    danger = [p for p in DANGEROUS if getattr(role.permissions, p)]
    if danger:
        return f"Roles with dangerous permissions cannot be offered ({', '.join(danger)})."
    if actor is not None and actor.id != role.guild.owner_id and role >= actor.top_role:
        return "That role is not below your own highest role."
    return None


async def apply_choice(interaction, menu_id, wanted, toggle=None):
    """Give and take the roles of a menu. wanted is the set of role IDs the member should hold from this menu (dropdown), toggle is one role to flip (button)."""
    bot = interaction.client
    lang = i18n.lang_of(bot, interaction.guild)
    menu = bot.cfg(interaction.guild_id)["rolemenus"]["items"].get(str(menu_id))
    if not menu or not bot.module_on(interaction.guild_id, "rolemenu"):
        return await interaction.response.send_message(i18n.tr(lang, "This role menu no longer exists."), ephemeral=True)
    offered = {r["role"] for r in menu["roles"]}
    member = interaction.user
    have = {r.id for r in member.roles} & offered
    if toggle is not None:
        wanted = set() if toggle in have else {toggle}
        if not menu["single"]:
            wanted |= have - {toggle}
    elif menu["single"]:
        wanted = set(list(wanted)[:1])
    wanted &= offered
    add, remove = wanted - have, have - wanted
    add_roles = []
    for rid in add:
        role = interaction.guild.get_role(rid)
        if role is None or role_problem(role):
            return await interaction.response.send_message(i18n.tr(lang, "That role is not available any more."), ephemeral=True)
        add_roles.append(role)
    remove_roles = [r for r in (interaction.guild.get_role(i) for i in remove) if r is not None]
    await interaction.response.defer(ephemeral=True)
    try:
        if remove_roles:
            await member.remove_roles(*remove_roles, reason="Role menu")
        if add_roles:
            await member.add_roles(*add_roles, reason="Role menu")
    except discord.HTTPException as exc:
        log.warning("role menu failed: %s", exc)
        return await interaction.followup.send(i18n.tr(lang, "That role is not available any more."), ephemeral=True)
    names = ", ".join(r.name for r in add_roles) or "-"
    lost = ", ".join(r.name for r in remove_roles) or "-"
    await interaction.followup.send(i18n.tr(lang, "Your roles were updated.") + f" +[{names}] -[{lost}]", ephemeral=True)


class RoleButton(discord.ui.DynamicItem[discord.ui.Button], template=r"gb:rm:(?P<m>\d+):(?P<r>\d+)"):
    """One persistent button of a role menu."""

    def __init__(self, menu_id, role_id, label="Role"):
        """Create the button for one role of one menu."""
        super().__init__(discord.ui.Button(label=label[:80], style=discord.ButtonStyle.secondary, custom_id=f"gb:rm:{menu_id}:{role_id}"))
        self.menu_id, self.role_id = menu_id, role_id

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the button from its custom id after a restart."""
        return cls(int(match["m"]), int(match["r"]), item.label or "Role")

    async def callback(self, interaction):
        """Flip the role."""
        await apply_choice(interaction, self.menu_id, set(), toggle=self.role_id)


class RoleDrop(discord.ui.DynamicItem[discord.ui.Select], template=r"gb:rms:(?P<m>\d+)"):
    """The persistent dropdown of a role menu."""

    def __init__(self, menu_id, options=(), single=False, placeholder="Choose your roles"):
        """Create the dropdown with one option per role."""
        select = discord.ui.Select(custom_id=f"gb:rms:{menu_id}", placeholder=placeholder, min_values=0, max_values=1 if single else max(1, len(options)), options=list(options) or [discord.SelectOption(label="-", value="0")])
        super().__init__(select)
        self.menu_id = menu_id

    @classmethod
    async def from_custom_id(cls, interaction, item, match, /):
        """Rebuild the dropdown from its custom id after a restart."""
        return cls(int(match["m"]))

    async def callback(self, interaction):
        """Give the chosen roles and take the other roles of the menu."""
        values = {int(v) for v in interaction.data.get("values", []) if v.isdigit()}
        await apply_choice(interaction, self.menu_id, values)


def build_view(menu_id, menu, lang="en"):
    """Create the view of a menu from its stored data."""
    view = discord.ui.View(timeout=None)
    if menu["kind"] == "buttons":
        for r in menu["roles"]:
            view.add_item(RoleButton(menu_id, r["role"], r["label"]))
    elif menu["roles"]:
        options = [discord.SelectOption(label=r["label"][:100], value=str(r["role"])) for r in menu["roles"]]
        view.add_item(RoleDrop(menu_id, options, menu["single"], i18n.tr(lang, "Choose your roles")))
    return view


def build_embed(menu, guild, lang="en"):
    """Create the text of a menu post."""
    lines = []
    for r in menu["roles"]:
        role = guild.get_role(r["role"])
        lines.append(f"{r['label']}: {role.mention if role else i18n.tr(lang, 'deleted role')}")
    return emb(menu["title"], "\n".join(lines) or i18n.tr(lang, "No roles yet."))


class RoleMenus(commands.Cog):
    """Role menus with buttons or a dropdown."""

    rm = AdminGroup(name="rolemenu", description="Role menus with buttons or a dropdown", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot):
        """Keep the bot reference and register the persistent items."""
        self.bot = bot
        bot.add_dynamic_items(RoleButton, RoleDrop)

    def conf(self, gid):
        """Return the role menu data of a server."""
        return self.bot.cfg(gid)["rolemenus"]

    async def refresh(self, guild, menu_id):
        """Edit the posted message of a menu. Returns False if the message is gone."""
        menu = self.conf(guild.id)["items"][str(menu_id)]
        ch = guild.get_channel(menu["channel"])
        if ch is None:
            return False
        try:
            msg = await ch.fetch_message(menu["message"])
            lang = i18n.lang_of(self.bot, guild)
            await msg.edit(embed=build_embed(menu, guild, lang), view=build_view(menu_id, menu, lang), allowed_mentions=discord.AllowedMentions.none())
        except discord.NotFound:
            return False
        except discord.HTTPException as exc:
            log.warning("role menu refresh failed: %s", exc)
            return False
        return True

    @rm.command(name="create", description="Post a new role menu")
    @app_commands.describe(title="Title of the post", kind="Buttons or a dropdown", single="Members may hold only one role of the menu", channel="Channel for the post")
    async def create(self, it: discord.Interaction, title: app_commands.Range[str, 1, 200], kind: Literal["buttons", "dropdown"] = "buttons", single: bool = False, channel: Optional[discord.TextChannel] = None):
        """Post a new role menu. Roles are added with /post rolemenu add."""
        c = self.conf(it.guild_id)
        if len(c["items"]) >= MAX_MENUS:
            return await it.response.send_message(f"A server can have {MAX_MENUS} menus.", ephemeral=True)
        channel = channel or it.channel
        if not channel.permissions_for(it.guild.me).send_messages:
            return await it.response.send_message(i18n.say(it.client, it.guild, "I cannot post in that channel."), ephemeral=True)
        mid = c["next"]
        menu = {"title": title, "kind": kind, "single": single, "channel": channel.id, "message": 0, "roles": []}
        msg = await channel.send(embed=build_embed(menu, it.guild, i18n.lang_of(self.bot, it.guild)))
        menu["message"] = msg.id
        c["next"] += 1
        c["items"][str(mid)] = menu
        await it.response.send_message(f"Menu {mid} posted in {channel.mention}. Add roles with /post rolemenu add menu:{mid}.", ephemeral=True)

    @rm.command(name="add", description="Add a role to a menu")
    @app_commands.describe(menu="Menu number", role="Role", label="Text of the button or option")
    async def add(self, it: discord.Interaction, menu: int, role: discord.Role, label: app_commands.Range[str, 1, 80]):
        """Add a role to a menu."""
        c = self.conf(it.guild_id)
        m = c["items"].get(str(menu))
        if not m:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no such menu."), ephemeral=True)
        problem = role_problem(role, it.user)
        if problem:
            return await it.response.send_message(problem, ephemeral=True)
        if any(r["role"] == role.id for r in m["roles"]):
            return await it.response.send_message(i18n.say(it.client, it.guild, "That role is already in the menu."), ephemeral=True)
        if len(m["roles"]) >= (MAX_BUTTONS if m["kind"] == "buttons" else MAX_OPTIONS):
            return await it.response.send_message(i18n.say(it.client, it.guild, "The menu is full."), ephemeral=True)
        m["roles"].append({"role": role.id, "label": label})
        await it.response.defer(ephemeral=True)
        ok = await self.refresh(it.guild, menu)
        await it.followup.send("Added." if ok else "Added, but I could not edit the post. Does it still exist?")

    @rm.command(name="remove", description="Remove a role from a menu")
    @app_commands.describe(menu="Menu number", role="Role")
    async def remove(self, it: discord.Interaction, menu: int, role: discord.Role):
        """Remove a role from a menu."""
        m = self.conf(it.guild_id)["items"].get(str(menu))
        if not m:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no such menu."), ephemeral=True)
        before = len(m["roles"])
        m["roles"] = [r for r in m["roles"] if r["role"] != role.id]
        if len(m["roles"]) == before:
            return await it.response.send_message(i18n.say(it.client, it.guild, "That role is not in the menu."), ephemeral=True)
        await it.response.defer(ephemeral=True)
        await self.refresh(it.guild, menu)
        await it.followup.send(i18n.say(it.client, it.guild, "Removed."))

    @rm.command(name="delete", description="Delete a menu and its post")
    @app_commands.describe(menu="Menu number")
    async def delete(self, it: discord.Interaction, menu: int):
        """Delete a menu and its post."""
        c = self.conf(it.guild_id)
        m = c["items"].pop(str(menu), None)
        if not m:
            return await it.response.send_message(i18n.say(it.client, it.guild, "There is no such menu."), ephemeral=True)
        await it.response.defer(ephemeral=True)
        ch = it.guild.get_channel(m["channel"])
        try:
            if ch:
                await (await ch.fetch_message(m["message"])).delete()
        except discord.HTTPException as exc:
            log.warning("role menu post could not be deleted: %s", exc)
        await it.followup.send(i18n.say(it.client, it.guild, "Deleted."))

    @rm.command(name="list", description="Show all menus")
    async def list(self, it: discord.Interaction):
        """Show all menus."""
        items = self.conf(it.guild_id)["items"]
        lines = [f"{mid}. {m['title']} ({m['kind']}{', one role only' if m['single'] else ''}) in <#{m['channel']}>, {len(m['roles'])} roles" for mid, m in items.items()]
        await it.response.send_message("\n".join(lines) or "No menus yet.", ephemeral=True)


async def setup(bot):
    """Register the cog with the bot."""
    await bot.add_cog(RoleMenus(bot))
