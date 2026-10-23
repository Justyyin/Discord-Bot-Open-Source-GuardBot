"""Panels: welcome posts, rules, role choices, notification buttons and verification gates with banner pictures, built by command or in the dashboard."""

import json
import logging
from typing import Any, Literal, Optional

import discord
from discord import app_commands

from ... import i18n, panels as engine
from ...cog import BaseCog
from ...utils import AdminGroup, emb
from ..community.rolemenu import role_problem

log = logging.getLogger(__name__)

TEXTS = (
    "Role added: {role}", "Role removed: {role}", "That role is not available any more.", "This panel no longer exists.",
    "There is no panel with that name.", "A panel with that name exists already.", "Panel `{name}` created. Add sections with /panel section and post it with /panel post.",
    "Section {number} saved.", "Section removed.", "Button added.", "Button removed.", "There is no section with that number.", "There is no button with that number.",
    "Panel posted in {channel}.", "Panel updated.", "The panel was not posted yet. Use /panel post.", "Panel deleted.", "I cannot post in that channel.",
    "Only one role of this panel at a time: {value}.", "No panels yet.",
)


class SectionModal(discord.ui.Modal):
    """Title, text and footer of a section. Pictures come from the options of the command and are read after the form is sent."""

    def __init__(self, cog: "Panels", pid: int, index: Optional[int], section: dict, files: dict, color: Optional[str], remove: Optional[str]):
        """Prefill the form with the current section."""
        super().__init__(title="Panel section")
        self.cog, self.pid, self.index, self.files, self.color, self.remove = cog, pid, index, files, color, remove
        self.title_box = discord.ui.TextInput(label="Title", required=False, max_length=256, default=section.get("title") or None)
        self.text_box = discord.ui.TextInput(label="Text", style=discord.TextStyle.paragraph, required=False, max_length=4000, default=section.get("text") or None)
        self.footer_box = discord.ui.TextInput(label="Footer", required=False, max_length=200, default=section.get("footer") or None)
        for box in (self.title_box, self.text_box, self.footer_box):
            self.add_item(box)

    async def on_submit(self, it: discord.Interaction) -> None:
        """Store the pictures and the texts."""
        await it.response.defer(ephemeral=True, thinking=True)
        await it.followup.send(await self.cog.save_section(it, self.pid, self.index, self.title_box.value, self.text_box.value, self.footer_box.value, self.files, self.color, self.remove), ephemeral=True)


class Panels(BaseCog):
    """Posts with banner pictures, embeds and buttons."""

    section = "panels"
    panel = AdminGroup(name="panel", description="Welcome, rules, role and verification posts with pictures", default_permissions=discord.Permissions(manage_guild=True), guild_only=True)

    def __init__(self, bot: Any):
        """Register the persistent buttons."""
        super().__init__(bot)
        bot.add_dynamic_items(engine.PanelButton)

    def s(self, guild: Any, text: str, **values: Any) -> str:
        """Translate a text into the language of the server."""
        return i18n.say(self.bot, guild, text, **values)

    @property
    def data_dir(self) -> Any:
        """The data folder of the bot."""
        return self.bot.store.dir

    def find(self, gid: int, name: str) -> tuple[Optional[str], Optional[dict]]:
        """The ID and the panel with a name."""
        for pid, panel in self.conf(gid)["items"].items():
            if panel["name"] == name.lower().strip():
                return pid, panel
        return None, None

    # ---- shared with the dashboard

    def save(self, guild: Any, pid: Optional[str], data: dict) -> str:
        """Validate and store a panel. Returns its ID. Raises PanelError."""
        conf = self.conf(guild.id)
        panel = engine.clean(data, conf.get("images", {}))
        other, _ = self.find(guild.id, panel["name"])
        if other is not None and other != pid:
            raise engine.PanelError("a panel with that name exists already")
        if pid is None:
            if len(conf["items"]) >= engine.MAX_PANELS:
                raise engine.PanelError(f"a server can have {engine.MAX_PANELS} panels")
            pid = str(conf["next"])
            conf["next"] += 1
        for button in panel["buttons"]:
            if button["kind"] == "role":
                role = guild.get_role(button["role"])
                problem = "the role does not exist" if role is None else role_problem(role)
                if problem:
                    raise engine.PanelError(f"{button['label'] or button['emoji']}: {problem}")
        if panel["channel"] and guild.get_channel(panel["channel"]) is None:
            raise engine.PanelError("the channel does not exist")
        conf["items"][pid] = panel
        engine.clean_images(conf, self.data_dir, guild.id)
        return pid

    def contents(self, guild: Any, pid: str, panel: dict) -> list[dict]:
        """What each message of a panel contains: embed, files and, on the last one, the buttons."""
        out = []
        conf = self.conf(guild.id)
        for i, section in enumerate(panel["sections"]):
            embed, files = engine.build_section(section, conf, self.data_dir, guild, i)
            out.append({"embed": embed, "files": files, "view": None})
        out[-1]["view"] = engine.build_view(int(pid), panel)
        return out

    async def post(self, guild: Any, pid: str, channel: Any, replace: bool = True) -> None:
        """Post a panel in a channel. Older posts of the panel are deleted when replace is set."""
        panel = self.conf(guild.id)["items"][pid]
        me = guild.me
        if channel is None or not hasattr(channel, "send") or (me is not None and not channel.permissions_for(me).send_messages):
            raise engine.PanelError("I cannot post in that channel")
        if replace and panel["messages"] and panel["channel"]:
            old = guild.get_channel(panel["channel"])
            for mid in panel["messages"]:
                try:
                    if old is not None:
                        await old.get_partial_message(mid).delete()
                except discord.HTTPException:
                    pass
        ids = []
        for part in self.contents(guild, pid, panel):
            kwargs: dict[str, Any] = {"files": part["files"]}
            if part["embed"] is not None:
                kwargs["embed"] = part["embed"]
            if part["view"] is not None:
                kwargs["view"] = part["view"]
            msg = await channel.send(**kwargs)
            ids.append(msg.id)
        panel["channel"], panel["messages"] = channel.id, ids

    async def update(self, guild: Any, pid: str) -> None:
        """Change the posted messages of a panel in place, or post it again when the number of sections changed."""
        panel = self.conf(guild.id)["items"][pid]
        channel = guild.get_channel(panel["channel"]) if panel["channel"] else None
        if channel is None or not panel["messages"]:
            raise engine.PanelError("the panel was not posted yet")
        parts = self.contents(guild, pid, panel)
        if len(parts) != len(panel["messages"]):
            return await self.post(guild, pid, channel, replace=True)
        try:
            for mid, part in zip(panel["messages"], parts):
                await channel.get_partial_message(mid).edit(embed=part["embed"], attachments=part["files"], view=part["view"])
        except discord.NotFound:
            await self.post(guild, pid, channel, replace=True)

    async def delete(self, guild: Any, pid: str, messages: bool = False) -> None:
        """Delete a panel, its unused pictures and, if asked, its posted messages."""
        conf = self.conf(guild.id)
        panel = conf["items"].pop(pid)
        engine.clean_images(conf, self.data_dir, guild.id)
        channel = guild.get_channel(panel["channel"]) if panel["channel"] else None
        if messages and channel is not None:
            for mid in panel["messages"]:
                try:
                    await channel.get_partial_message(mid).delete()
                except discord.HTTPException:
                    pass

    # ---- buttons

    async def press(self, it: discord.Interaction, pid: int, index: int) -> None:
        """Give or take the role of a button. With single on, the other roles of the panel are taken away."""
        panel = self.conf(it.guild_id)["items"].get(str(pid))
        if panel is None or not self.bot.module_on(it.guild_id, "panels") or index >= len(panel["buttons"]) or panel["buttons"][index]["kind"] != "role":
            return await it.response.send_message(self.s(it.guild, "This panel no longer exists."), ephemeral=True)
        role = it.guild.get_role(panel["buttons"][index]["role"])
        if role is None or role_problem(role):
            return await it.response.send_message(self.s(it.guild, "That role is not available any more."), ephemeral=True)
        member = it.user
        await it.response.defer(ephemeral=True)
        try:
            if role in member.roles:
                await member.remove_roles(role, reason="Panel")
                return await it.followup.send(self.s(it.guild, "Role removed: {role}", role=role.name), ephemeral=True)
            if panel["single"]:
                others = {b["role"] for b in panel["buttons"] if b["kind"] == "role"} - {role.id}
                drop = [r for r in member.roles if r.id in others]
                if drop:
                    await member.remove_roles(*drop, reason="Panel")
            await member.add_roles(role, reason="Panel")
        except discord.HTTPException as exc:
            log.warning("panel role failed: %s", exc)
            return await it.followup.send(self.s(it.guild, "That role is not available any more."), ephemeral=True)
        await it.followup.send(self.s(it.guild, "Role added: {role}", role=role.name), ephemeral=True)

    # ---- commands

    async def panel_names(self, it: discord.Interaction, current: str):
        """Offer the names of the panels."""
        names = sorted(p["name"] for p in self.conf(it.guild_id)["items"].values())
        return [app_commands.Choice(name=n, value=n) for n in names if current.lower() in n][:25]

    async def need(self, it: discord.Interaction, name: str) -> tuple[Optional[str], Optional[dict]]:
        """The panel of a command, or an answer that it does not exist."""
        pid, panel = self.find(it.guild_id, name)
        if pid is None:
            await it.response.send_message(self.s(it.guild, "There is no panel with that name."), ephemeral=True)
        return pid, panel

    @panel.command(name="create", description="Create a panel, empty or from a template")
    @app_commands.describe(name="Short name, for example welcome", template="Start with texts for a welcome, rules, role, notification or verification post", channel="Channel where it will be posted")
    async def p_create(self, it: discord.Interaction, name: app_commands.Range[str, 1, 30], template: Literal["empty", "welcome", "rules", "roles", "notifications", "verify"] = "empty", channel: Optional[discord.TextChannel] = None):
        """Create a panel."""
        data = engine.template(template, name.lower().strip(), tr=lambda text: self.s(it.guild, text))
        data["channel"] = channel.id if channel else None
        if self.find(it.guild_id, data["name"])[0] is not None:
            return await it.response.send_message(self.s(it.guild, "A panel with that name exists already."), ephemeral=True)
        try:
            self.save(it.guild, None, data)
        except engine.PanelError as exc:
            return await it.response.send_message(str(exc), ephemeral=True)
        await it.response.send_message(self.s(it.guild, "Panel `{name}` created. Add sections with /panel section and post it with /panel post.", name=data["name"]), ephemeral=True)

    @panel.command(name="list", description="List the panels")
    async def p_list(self, it: discord.Interaction):
        """List the panels."""
        lines = []
        for p in sorted(self.conf(it.guild_id)["items"].values(), key=lambda p: p["name"]):
            where = f"<#{p['channel']}>" if p["channel"] else "-"
            lines.append(f"`{p['name']}` {len(p['sections'])} section(s), {len(p['buttons'])} button(s), {where}{' (posted)' if p['messages'] else ''}")
        await it.response.send_message(embed=emb("Panels", "\n".join(lines) or self.s(it.guild, "No panels yet.")), ephemeral=True)

    @panel.command(name="section", description="Add or change a section with banner, text and pictures")
    @app_commands.describe(
        name="Panel", number="Section to change, empty adds a new one", banner="Picture shown above the box", image="Large picture inside the box",
        thumbnail="Small picture at the top right of the box", color="Colour of the bar, for example #5865f2", remove="Remove a picture of this section",
    )
    @app_commands.autocomplete(name=panel_names)
    async def p_section(self, it: discord.Interaction, name: str, number: Optional[app_commands.Range[int, 1, 5]] = None, banner: Optional[discord.Attachment] = None, image: Optional[discord.Attachment] = None, thumbnail: Optional[discord.Attachment] = None, color: Optional[str] = None, remove: Optional[Literal["banner", "image", "thumbnail", "color"]] = None):
        """Open the form of a section."""
        pid, panel = await self.need(it, name)
        if pid is None or panel is None:
            return
        if number is not None and number > len(panel["sections"]):
            return await it.response.send_message(self.s(it.guild, "There is no section with that number."), ephemeral=True)
        current = panel["sections"][number - 1] if number else {}
        files = {k: v for k, v in (("banner", banner), ("image", image), ("thumbnail", thumbnail)) if v is not None}
        await it.response.send_modal(SectionModal(self, int(pid), number - 1 if number else None, current, files, color, remove))

    async def save_section(self, it: discord.Interaction, pid: int, index: Optional[int], title: str, text: str, footer: str, files: dict, color: Optional[str], remove: Optional[str]) -> str:
        """Read the pictures, store them and save the section. Returns the answer."""
        conf = self.conf(it.guild_id)
        panel = conf["items"].get(str(pid))
        if panel is None:
            return self.s(it.guild, "This panel no longer exists.")
        data = json.loads(json.dumps(panel))
        section = dict(data["sections"][index]) if index is not None else {"banner": None, "image": None, "thumbnail": None, "color": None}
        section.update(title=title, text=text, footer=footer)
        try:
            for key, att in files.items():
                if att.size > engine.MAX_IMAGE_BYTES:
                    raise engine.PanelError("pictures must be smaller than 8 MB")
                section[key] = engine.store_image(conf, self.data_dir, it.guild_id, await att.read(), att.filename)
            if color is not None:
                section["color"] = color.strip() or None
            if remove == "color":
                section["color"] = None
            elif remove:
                section[remove] = None
            if index is None:
                if len(data["sections"]) >= engine.MAX_SECTIONS:
                    raise engine.PanelError(f"a panel can have {engine.MAX_SECTIONS} sections")
                data["sections"].append(section)
                index = len(data["sections"]) - 1
            else:
                data["sections"][index] = section
            self.save(it.guild, str(pid), data)
        except (engine.PanelError, discord.HTTPException) as exc:
            engine.clean_images(conf, self.data_dir, it.guild_id)
            return str(exc)
        return self.s(it.guild, "Section {number} saved.", number=index + 1)

    @panel.command(name="removesection", description="Remove a section")
    @app_commands.autocomplete(name=panel_names)
    async def p_removesection(self, it: discord.Interaction, name: str, number: app_commands.Range[int, 1, 5]):
        """Remove a section."""
        pid, panel = await self.need(it, name)
        if pid is None or panel is None:
            return
        if number > len(panel["sections"]) or len(panel["sections"]) == 1:
            return await it.response.send_message(self.s(it.guild, "There is no section with that number."), ephemeral=True)
        panel["sections"].pop(number - 1)
        engine.clean_images(self.conf(it.guild_id), self.data_dir, it.guild_id)
        await it.response.send_message(self.s(it.guild, "Section removed."), ephemeral=True)

    @panel.command(name="button", description="Add a role, verification or link button")
    @app_commands.describe(name="Panel", kind="role gives and takes a role, verify starts the verification, link opens a page", label="Text on the button", emoji="Emoji on the button", role="Role for a role button", url="Address for a link button (https)", style="Colour of the button")
    @app_commands.autocomplete(name=panel_names)
    async def p_button(self, it: discord.Interaction, name: str, kind: Literal["role", "verify", "link"], label: Optional[app_commands.Range[str, 1, 80]] = None, emoji: Optional[str] = None, role: Optional[discord.Role] = None, url: Optional[str] = None, style: Literal["primary", "secondary", "success", "danger"] = "primary"):
        """Add a button."""
        pid, panel = await self.need(it, name)
        if pid is None or panel is None:
            return
        if kind == "role" and role is not None:
            problem = role_problem(role, it.user)
            if problem:
                return await it.response.send_message(problem, ephemeral=True)
        data = json.loads(json.dumps(panel))
        button: dict[str, Any] = {"kind": kind, "label": label or "", "emoji": emoji or "", "style": "success" if kind == "verify" and style == "primary" else style}
        if kind == "role":
            button["role"] = role.id if role else None
        if kind == "link":
            button["url"] = url or ""
        data["buttons"].append(button)
        try:
            self.save(it.guild, pid, data)
        except engine.PanelError as exc:
            return await it.response.send_message(str(exc), ephemeral=True)
        await it.response.send_message(self.s(it.guild, "Button added."), ephemeral=True)

    @panel.command(name="removebutton", description="Remove a button")
    @app_commands.autocomplete(name=panel_names)
    async def p_removebutton(self, it: discord.Interaction, name: str, number: app_commands.Range[int, 1, 20]):
        """Remove a button."""
        pid, panel = await self.need(it, name)
        if pid is None or panel is None:
            return
        if number > len(panel["buttons"]):
            return await it.response.send_message(self.s(it.guild, "There is no button with that number."), ephemeral=True)
        panel["buttons"].pop(number - 1)
        await it.response.send_message(self.s(it.guild, "Button removed."), ephemeral=True)

    @panel.command(name="single", description="Allow only one role of this panel at a time")
    @app_commands.autocomplete(name=panel_names)
    async def p_single(self, it: discord.Interaction, name: str, value: bool):
        """Switch the single choice on or off."""
        pid, panel = await self.need(it, name)
        if pid is None or panel is None:
            return
        panel["single"] = value
        await it.response.send_message(self.s(it.guild, "Only one role of this panel at a time: {value}.", value="on" if value else "off"), ephemeral=True)

    @panel.command(name="post", description="Post the panel, older posts of it are replaced")
    @app_commands.autocomplete(name=panel_names)
    async def p_post(self, it: discord.Interaction, name: str, channel: Optional[discord.TextChannel] = None):
        """Post a panel."""
        pid, panel = await self.need(it, name)
        if pid is None or panel is None:
            return
        target = channel or (it.guild.get_channel(panel["channel"]) if panel["channel"] else None) or it.channel
        await it.response.defer(ephemeral=True)
        try:
            await self.post(it.guild, pid, target)
        except (engine.PanelError, discord.HTTPException) as exc:
            return await it.followup.send(self.s(it.guild, "I cannot post in that channel.") + f" ({exc})", ephemeral=True)
        await it.followup.send(self.s(it.guild, "Panel posted in {channel}.", channel=target.mention), ephemeral=True)

    @panel.command(name="update", description="Change the posted panel in place after an edit")
    @app_commands.autocomplete(name=panel_names)
    async def p_update(self, it: discord.Interaction, name: str):
        """Update a posted panel."""
        pid, panel = await self.need(it, name)
        if pid is None or panel is None:
            return
        await it.response.defer(ephemeral=True)
        try:
            await self.update(it.guild, pid)
        except engine.PanelError:
            return await it.followup.send(self.s(it.guild, "The panel was not posted yet. Use /panel post."), ephemeral=True)
        except discord.HTTPException as exc:
            return await it.followup.send(str(exc), ephemeral=True)
        await it.followup.send(self.s(it.guild, "Panel updated."), ephemeral=True)

    @panel.command(name="preview", description="Show the panel only to you")
    @app_commands.autocomplete(name=panel_names)
    async def p_preview(self, it: discord.Interaction, name: str):
        """Show a panel privately."""
        pid, panel = await self.need(it, name)
        if pid is None or panel is None:
            return
        await it.response.defer(ephemeral=True)
        for part in self.contents(it.guild, pid, panel):
            kwargs: dict[str, Any] = {"files": part["files"], "ephemeral": True}
            if part["embed"] is not None:
                kwargs["embed"] = part["embed"]
            if part["view"] is not None:
                kwargs["view"] = part["view"]
            await it.followup.send(**kwargs)

    @panel.command(name="show", description="Show a panel as JSON")
    @app_commands.autocomplete(name=panel_names)
    async def p_show(self, it: discord.Interaction, name: str):
        """Show a panel as JSON."""
        pid, panel = await self.need(it, name)
        if pid is None or panel is None:
            return
        body = json.dumps({k: v for k, v in panel.items() if k != "messages"}, indent=1, ensure_ascii=False)
        await it.response.send_message(f"```json\n{body[:1900]}\n```", ephemeral=True)

    @panel.command(name="delete", description="Delete a panel")
    @app_commands.describe(messages="Also delete the posted messages")
    @app_commands.autocomplete(name=panel_names)
    async def p_delete(self, it: discord.Interaction, name: str, messages: bool = False):
        """Delete a panel."""
        pid, panel = await self.need(it, name)
        if pid is None:
            return
        await it.response.defer(ephemeral=True)
        await self.delete(it.guild, pid, messages)
        await it.followup.send(self.s(it.guild, "Panel deleted."), ephemeral=True)


async def setup(bot: Any) -> None:
    """Register the cog with the bot."""
    await bot.add_cog(Panels(bot))
