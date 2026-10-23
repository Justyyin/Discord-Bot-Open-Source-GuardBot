"""The plugin catalog of the dashboard: every module with its category, icon, short description and the settings sections that belong to it."""

from typing import Any

from .dashhelp import ABOUT

CATEGORIES = (
    ("basics", "Basics", "Grundlagen"),
    ("moderation", "Moderation", "Moderation"),
    ("security", "Security", "Sicherheit"),
    ("community", "Community", "Community"),
    ("fun", "Games and fun", "Spiele und Spaß"),
    ("server", "Server management", "Server-Verwaltung"),
    ("team", "Team", "Team"),
)

# module: (category, icon, settings sections, special page, title en, title de, description en, description de)
PLUGINS: dict[str, tuple] = {
    "logging": ("basics", "list", ("log", "log_options"), None, "Logging", "Protokolle", "Write joins, leaves, edits, deletions and moderation to log channels.", "Beitritte, Austritte, Änderungen, Löschungen und Moderation in Log-Kanäle schreiben."),
    "backup": ("basics", "save", ("backup",), None, "Backups", "Sicherungen", "Automatic backups of roles, channels and emojis with a restore that only adds what is missing.", "Automatische Sicherung von Rollen, Kanälen und Emojis mit einer Wiederherstellung, die nur Fehlendes ergänzt."),
    "privacy": ("basics", "lock", ("privacy",), None, "Privacy", "Datenschutz", "Members export and delete their data, data of members who left is removed after a while.", "Mitglieder exportieren und löschen ihre Daten, Daten ausgetretener Mitglieder werden nach einer Zeit entfernt."),
    "debug": ("basics", "wrench", ("debug",), None, "Diagnostics", "Diagnose", "Error reports, usage statistics, health check and updates.", "Fehlerberichte, Nutzungsstatistik, Statusprüfung und Updates."),
    "info": ("basics", "info", (), None, "Information", "Informationen", "Profiles of members, roles and the server, avatar, ping and bot information.", "Profile von Mitgliedern, Rollen und dem Server, Avatar, Ping und Bot-Informationen."),
    "history": ("basics", "clock", (), None, "Settings history", "Einstellungsverlauf", "Shows who changed which setting and rolls a section back.", "Zeigt, wer welche Einstellung geändert hat, und setzt einen Bereich zurück."),
    "exceptions": ("basics", "filter", (), None, "Exceptions", "Ausnahmen", "Leave channels and roles out of AutoMod rules and the anti-scam check.", "Kanäle und Rollen von AutoMod-Regeln und dem Anti-Scam ausnehmen."),
    "moderation": ("moderation", "hammer", ("mod",), None, "Moderation", "Moderation", "Warn, mute, kick and ban with cases, escalation and expiry of warnings.", "Verwarnen, stummschalten, kicken und bannen mit Fällen, Eskalation und Ablauf von Verwarnungen."),
    "automod": ("moderation", "shield", ("automod",), None, "AutoMod", "AutoMod", "Automatic rules against spam, links, invites, bad words, caps, mentions and personal data.", "Automatische Regeln gegen Spam, Links, Einladungen, Schimpfwörter, Großschreibung, Erwähnungen und persönliche Daten."),
    "jail": ("moderation", "lock", ("jail",), None, "Gulag", "Gulag", "A closed room for hacked accounts with security steps, reminder and release requests.", "Ein geschlossener Raum für gehackte Konten mit Sicherheitsschritten, Erinnerung und Freilassungsanfragen."),
    "reasons": ("moderation", "list", (), None, "Reason templates", "Grundvorlagen", "Short codes for frequent reasons of punishments.", "Kurzcodes für häufige Gründe von Strafen."),
    "approval": ("moderation", "check", ("approval",), None, "Four-eyes approval", "Vier-Augen-Freigabe", "A second moderator must agree to bans and other serious actions.", "Ein zweiter Moderator muss Bans und anderen schweren Aktionen zustimmen."),
    "modmail": ("moderation", "mail", ("modmail",), None, "Mod-mail", "Mod-Mail", "Members write to the team through a direct message to the bot.", "Mitglieder schreiben dem Team per Direktnachricht an den Bot."),
    "appeals": ("moderation", "scale", ("appeals",), None, "Ban appeals", "Ban-Einsprüche", "Banned members can appeal, the team decides.", "Gebannte Mitglieder können Einspruch einlegen, das Team entscheidet."),
    "reports": ("moderation", "flag", ("reports",), None, "Reports", "Meldungen", "Members report messages to the staff with the context menu.", "Mitglieder melden Nachrichten über das Kontextmenü an das Team."),
    "stickyroles": ("moderation", "pin", ("stickyroles",), None, "Sticky roles", "Bleibende Rollen", "Roles, timeouts and mutes come back when a member rejoins.", "Rollen, Timeouts und Mutes kommen zurück, wenn ein Mitglied wieder beitritt."),
    "nicknames": ("moderation", "tag", ("nicknames",), None, "Nicknames", "Spitznamen", "Removes hoisting characters and banned words from names.", "Entfernt Sonderzeichen am Anfang und verbotene Wörter aus Namen."),
    "watchlist": ("moderation", "eye", ("watchlist",), None, "Watch list", "Beobachtungsliste", "Silent watch list, the team is alerted at the first message.", "Stille Beobachtungsliste, das Team wird bei der ersten Nachricht gewarnt."),
    "antiscam": ("security", "alert", ("antiscam",), None, "Anti-scam", "Anti-Scam", "Removes fake giveaways and crypto scams in text and pictures, learns from your moderators.", "Entfernt Fake-Gewinnspiele und Krypto-Betrug in Text und Bildern und lernt von deinen Moderatoren."),
    "antinuke": ("security", "shield", ("antinuke",), None, "Anti-nuke", "Anti-Nuke", "Stops mass deletions, mass bans, dangerous permissions and new bots.", "Stoppt Massenlöschungen, Massenbans, gefährliche Rechte und neue Bots."),
    "raid": ("security", "users", ("raid",), None, "Raid protection", "Raid-Schutz", "Detects join swarms and new accounts and reacts automatically.", "Erkennt Beitrittswellen und neue Konten und reagiert automatisch."),
    "lockdown": ("security", "lock", ("lockdown",), None, "Lockdown", "Lockdown", "Close the whole server or single channels in an emergency.", "Den ganzen Server oder einzelne Kanäle im Notfall schließen."),
    "verification": ("security", "check", ("verify",), None, "Verification", "Verifizierung", "New members prove that they are human with a button, captcha or math question.", "Neue Mitglieder beweisen mit Button, Captcha oder Rechenaufgabe, dass sie Menschen sind."),
    "probation": ("security", "clock", ("probation",), None, "Probation", "Probezeit", "New members may not post links or files until they wrote normal messages.", "Neue Mitglieder dürfen keine Links oder Dateien posten, bis sie normale Nachrichten geschrieben haben."),
    "modwatch": ("security", "eye", ("modwatch",), None, "Moderator limits", "Moderatoren-Grenzen", "Too many bans or kicks by one moderator raise an alert.", "Zu viele Bans oder Kicks eines Moderators lösen Alarm aus."),
    "permaudit": ("security", "key", ("permaudit",), None, "Permission audit", "Rechteprüfung", "Reports roles and channels with dangerous permissions.", "Meldet Rollen und Kanäle mit gefährlichen Rechten."),
    "welcome": ("community", "hand", ("welcome",), None, "Welcome", "Begrüßung", "Welcome and goodbye messages, auto roles and a direct message for new members.", "Begrüßungs- und Abschiedsnachrichten, Auto-Rollen und eine Direktnachricht für neue Mitglieder."),
    "boosters": ("community", "star", ("boosters",), None, "Boosters", "Booster", "Thank members who boost the server and give them a role.", "Mitgliedern danken, die den Server boosten, und ihnen eine Rolle geben."),
    "leveling": ("community", "trophy", ("xp",), None, "Levels", "Level", "XP for messages and voice, levels, level roles and rank cards.", "XP für Nachrichten und Sprachkanäle, Level, Level-Rollen und Rangkarten."),
    "reactionroles": ("community", "smile", (), None, "Reaction roles", "Reaktionsrollen", "Members get roles by reacting to a message.", "Mitglieder bekommen Rollen, indem sie auf eine Nachricht reagieren."),
    "rolemenu": ("community", "list", (), None, "Role menus", "Rollenmenüs", "Buttons or a dropdown that give and take roles.", "Buttons oder ein Dropdown, die Rollen geben und nehmen."),
    "notify": ("community", "bell", (), None, "Notifications", "Benachrichtigungen", "Members switch notification roles on and off themselves.", "Mitglieder schalten Benachrichtigungsrollen selbst an und aus."),
    "birthday": ("community", "cake", ("birthday",), None, "Birthdays", "Geburtstage", "Birthday message and a birthday role for the day.", "Geburtstagsnachricht und eine Geburtstagsrolle für den Tag."),
    "tempvoice": ("community", "mic", ("tempvoice",), None, "Temporary channels", "Temporäre Kanäle", "Members create their own voice rooms with one click.", "Mitglieder erstellen mit einem Klick eigene Sprachräume."),
    "activity": ("community", "chart", (), None, "Activity", "Aktivität", "Counts messages and joins per day for the charts.", "Zählt Nachrichten und Beitritte pro Tag für die Diagramme."),
    "stats": ("community", "chart", (), None, "Statistic channels", "Statistik-Kanäle", "Channel names that show the member count and other numbers.", "Kanalnamen, die Mitgliederzahl und andere Werte anzeigen."),
    "economy": ("fun", "coin", ("economy",), None, "Economy", "Wirtschaft", "Currency, daily reward, work and a shop for roles.", "Währung, tägliche Belohnung, Arbeit und ein Shop für Rollen."),
    "giveaways": ("fun", "gift", (), None, "Giveaways", "Gewinnspiele", "Giveaways with a button, timer and winner draw.", "Gewinnspiele mit Button, Timer und Gewinnerauslosung."),
    "polls": ("fun", "chart", (), None, "Polls", "Umfragen", "Polls with buttons and up to ten options.", "Umfragen mit Buttons und bis zu zehn Optionen."),
    "counting": ("fun", "hash", ("counting",), None, "Counting", "Zählen", "A channel where members count up together.", "Ein Kanal, in dem Mitglieder gemeinsam hochzählen."),
    "starboard": ("fun", "star", ("starboard",), None, "Starboard", "Starboard", "Popular messages are shown in their own channel.", "Beliebte Nachrichten werden in einem eigenen Kanal gezeigt."),
    "music": ("fun", "music", ("music",), "music", "Music", "Musik", "Plays YouTube, SoundCloud, Spotify, Apple Music and Tidal links, playlists and your own music folder, also as a second bot around the clock.", "Spielt Links von YouTube, SoundCloud, Spotify, Apple Music und Tidal, Playlists und deinen eigenen Musikordner, auch als zweiter Bot rund um die Uhr."),
    "suggestions": ("fun", "bulb", ("suggestions",), None, "Suggestions", "Vorschläge", "Members suggest, others vote, the team decides.", "Mitglieder schlagen vor, andere stimmen ab, das Team entscheidet."),
    "skills": ("fun", "puzzle", (), "skills", "Skills", "Skills", "Custom commands, games and automations from safe building blocks.", "Eigene Befehle, Spiele und Automatisierungen aus sicheren Bausteinen."),
    "ai": ("fun", "spark", (), "ai", "AI", "KI", "Your own AI key writes skills and gives a second opinion on scams.", "Dein eigener KI-Schlüssel schreibt Skills und gibt eine Zweitmeinung zu Scams."),
    "tickets": ("server", "ticket", ("tickets",), None, "Tickets", "Ticketsystem", "Members open tickets for support, reports and requests.", "Mitglieder öffnen Tickets für Support, Meldungen und Anfragen."),
    "panels": ("server", "image", (), "panels", "Panels", "Panels", "Welcome posts, rules, role choices and verification with banner pictures and buttons.", "Willkommensbeiträge, Regeln, Rollenauswahl und Verifizierung mit Bannerbildern und Buttons."),
    "tags": ("server", "tag", (), None, "Custom commands", "Eigene Befehle", "Short text commands everyone can use, such as !faq.", "Kurze Textbefehle für alle, zum Beispiel !faq."),
    "autoresponder": ("server", "chat", (), None, "Auto responses", "Automatische Antworten", "Answers messages that contain certain words.", "Beantwortet Nachrichten, die bestimmte Wörter enthalten."),
    "announce": ("server", "megaphone", (), None, "Announcements", "Ankündigungen", "Post messages and embeds as the bot.", "Nachrichten und Embeds als Bot posten."),
    "builder": ("server", "edit", (), None, "Message builder", "Nachrichten-Baukasten", "Post and edit messages from JSON with several embeds and link buttons.", "Nachrichten aus JSON mit mehreren Embeds und Link-Buttons posten und bearbeiten."),
    "schedule": ("server", "clock", (), None, "Scheduled messages", "Geplante Nachrichten", "Messages that are posted once or again and again at set times.", "Nachrichten, die einmalig oder regelmäßig zu festen Zeiten gepostet werden."),
    "feeds": ("server", "rss", (), None, "Feeds", "Feeds", "New videos, streams and posts from YouTube, Twitch and RSS.", "Neue Videos, Streams und Beiträge von YouTube, Twitch und RSS."),
    "sticky": ("server", "pin", (), None, "Sticky messages", "Angepinnte Nachrichten", "A message that always stays at the bottom of a channel.", "Eine Nachricht, die immer unten im Kanal bleibt."),
    "utility": ("server", "wrench", (), None, "Reminders and AFK", "Erinnerungen und AFK", "Reminders and an away status for members.", "Erinnerungen und ein Abwesenheitsstatus für Mitglieder."),
    "invites": ("server", "userplus", ("invites",), None, "Invite tracking", "Einladungsverfolgung", "Shows who joined with which invite and who invites the most.", "Zeigt, wer mit welcher Einladung beigetreten ist und wer am meisten einlädt."),
    "structure": ("server", "folder", (), None, "Structure", "Struktur", "Create, clone and sort channels and categories by command.", "Kanäle und Kategorien per Befehl erstellen, klonen und sortieren."),
    "archive": ("server", "archive", ("archive",), None, "Archive", "Archiv", "Moves channels without activity into an archive.", "Verschiebt Kanäle ohne Aktivität in ein Archiv."),
    "temproles": ("server", "clock", (), None, "Timed roles", "Zeitrollen", "Roles that are removed after a set time.", "Rollen, die nach einer festgelegten Zeit entfernt werden."),
    "rules": ("server", "book", ("rules",), None, "Rules", "Regeln", "Rules with a button to accept them and a reminder.", "Regeln mit Button zum Annehmen und einer Erinnerung."),
    "team": ("team", "users", ("team",), None, "Team statistics", "Team-Statistik", "Work of every moderator and a weekly report.", "Arbeit jedes Moderators und ein Wochenbericht."),
    "duty": ("team", "calendar", (), None, "Duty roster", "Dienstplan", "Moderators sign off, tickets and pings go to those available.", "Moderatoren melden sich ab, Tickets und Pings gehen an die Verfügbaren."),
    "applications": ("team", "form", ("applications",), None, "Applications", "Bewerbungen", "Staff applications with a form and a vote of the team.", "Team-Bewerbungen mit Formular und Abstimmung des Teams."),
}


def catalog(modules: dict, defaults: dict, sections: set) -> list[dict[str, Any]]:
    """The plugins for the dashboard with their state on one server. Unknown modules are listed under Basics so none is missing."""
    out = []
    for key, default_on in defaults.items():
        cat, icon, secs, page, title, title_de, desc, desc_de = PLUGINS.get(key, ("basics", "puzzle", (), None, key, key, "", ""))
        out.append({
            "key": key, "category": cat, "icon": icon, "page": page, "title": title, "title_de": title_de, "desc": desc, "desc_de": desc_de, "about": ABOUT.get(key, desc),
            "on": bool(modules.get(key, default_on)), "sections": [s for s in secs if s in sections],
        })
    return out
