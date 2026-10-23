"use strict";
(function () {
  var TEXT = {
    en: { signin: "Sign in with Discord", intro: "Manage your GuardBot servers.", offline: "The bot is not connected right now. Try again in a moment.", server: "Server", overview: "Overview", members: "Members", cases: "Cases", modules: "Modules on", latency: "Latency", search: "Search settings", setupTitle: "Setup status", setupOpen: "On, not set up yet", setupDone: "On and set up", setupNone: "On, needs no setup", setupOff: "Off", chartsTitle: "Last 30 days", chMessages: "Messages per day", chJoins: "Joins", chLeaves: "Leaves", chCases: "Moderation cases per day", chTypes: "Cases by type", noData: "No data yet. Turn on the activity module to count messages.", searchAll: "Search all settings", noMatch: "No setting matches.", saved: "Saved", failed: "Could not save", none: "None", logout: "Log out", general: "General", modulesTitle: "Modules", moderation: "Moderation cases", backup: "Backup", export: "Download settings", import: "Import settings", importNote: "Importing replaces the settings of this server with the file. Counters, open tickets and other running data are kept.", imported: "Settings imported", noServers: "You do not manage any server where the bot is connected.", nocases: "No cases yet.", user: "User", type: "Type", reason: "Reason", moderator: "Moderator", when: "When", lines: "One entry per line", sections: "Settings", loginHelp: "Only members with the Manage Server permission can sign in, and only for servers the bot is connected to.", sure: "Replace all settings with this file?", about: "Version", readOnly: "You can read this page but not change it. Ask an administrator for more access.", adminOnly: "Only administrators can download or import settings." },
  };
  TEXT.en.cat = { "Basics": "Basics", "Moderation": "Moderation", "Security": "Security", "Community": "Community", "Structure and team": "Structure and team", "More": "More" };

  Object.assign(TEXT.en, { navCommands: "Commands", navSkills: "Skills", navAi: "AI", navProfile: "Bot profile", cmdIntro: "All commands of the bot. Switch them off, limit them to roles or give text commands a short name.", prefix: "Prefix", language: "Language", filter: "Filter", allKinds: "All", slash: "Slash", text: "Prefix", menu: "Menu", on: "On", off: "Off", module: "Module", permission: "Needs", rolesAllowed: "Only these roles", rolesDenied: "Never these roles", aliases: "Short names", aliasName: "Short name", aliasFor: "Runs command", add: "Add", remove: "Remove", custom: "Tags and skills", protectedCmd: "This command cannot be turned off.", moduleOff: "Its module is off", subs: "Subcommands", skillsIntro: "Skills are commands, games and automations made from safe building blocks. They cannot run code.", newSkill: "New", skillJson: "Skill as JSON", save: "Save", edit: "Edit", del: "Delete", surer: "Delete this?", uses: "Used", skillsNone: "No skills yet.", skillsOff: "The skills module is off. Turn it on under Modules.", aiIntro: "Connect your own account at Anthropic, OpenAI or Kimi. The key is stored encrypted and is never shown again.", provider: "Provider", model: "Model", apiKey: "API key", saveKey: "Save key", removeKey: "Delete key", keySaved: "Key saved", hasKey: "A key is stored.", noKey: "No key is stored.", daily: "Requests per day", used: "Used today", cooldown: "Seconds between requests per person", maxTokens: "Longest answer (tokens)", second: "Ask the AI about borderline anti-scam cases", errorsCount: "Errors", aiPrivacy: "The text of a request, and for the second opinion the text of a suspicious message, is sent to the provider you choose. Their terms apply.", changeProv: "To change the provider, save a key for the new one.", profIntro: "Name, picture, banner and about text of the bot.", serverProfile: "On this server", globalProfile: "Everywhere (owner of the bot only)", nick: "Name", avatar: "Picture", banner: "Banner", bio: "About text", reset: "Reset", choose: "Choose file", ownerOnly: "Only the owner of the bot can change this.", limitsNote: "Discord limits how often the name and picture may change.", navPanels: "Panels", panelsIntro: "Posts with banner pictures, text boxes and buttons: welcome, rules, role choices, notifications, verification. Pictures are stored by the bot.", newPanel: "New panel", template: "Template", name: "Name", channel: "Channel", single: "Only one role at a time", section: "Section", title: "Title", textBody: "Text", footer: "Footer", color: "Colour", noColor: "No colour", bannerPic: "Banner above", imagePic: "Large picture", thumbPic: "Small picture", upload: "Upload", buttons: "Buttons", kind: "Kind", label: "Label", emoji: "Emoji", style: "Style", role: "Role", url: "Link (https)", addSection: "Add section", addButton: "Add button", post: "Post", update: "Update posted", posted: "Posted", notPosted: "Not posted yet", back: "Back", deleteMessages: "Also delete the posted messages?", uploading: "Uploading...", plugins: "Plugins", allPlugins: "All plugins", active: "Active", activate: "Activate", settings: "Settings", settingsIntro: "Prefix, language and settings that belong to no single plugin.", commandsTitle: "Commands", commandsHint: "Switch commands of this plugin on or off and choose which roles may use them.", noCommands: "This plugin has no commands of its own.", openPage: "Open", openPageHint: "This plugin has its own page." });

  Object.assign(TEXT.en, { functions: "Functions", functionsHint: "Every function of this plugin with its own switch.", aboutTitle: "What it does", noFunctions: "This plugin has no switches of its own. The switch Active at the top turns it on or off.", nFunctions: "functions", nSettings: "settings", pluginOff: "This plugin is off. Its settings are kept and work as soon as you switch it on.", allPluginsTitle: "All plugins", configure: "Settings", navMusic: "Music", musicIntro: "Player, queue, saved playlists, 24/7 mode and the music sources of this server.", playsAs: "Plays as", secondBot: "Second bot Guard Music", sameBot: "GuardBot itself", online: "Online", offline2: "Offline", notOnServer: "Guard Music is not on this server yet.", invite: "Add Guard Music to this server", notReady: "This computer is not ready for voice:", nowPlaying: "Now playing", nothingPlaying: "Nothing is playing.", queueTitle: "Queue", waiting: "waiting", pause: "Pause", resume: "Continue", skip: "Skip", stop: "Stop", leave: "Leave", shuffle: "Mix", clearQueue: "Clear queue", loopLabel: "Repeat", loopOff: "Off", loopTrack: "Track", loopQueue: "Queue", volume: "Volume", voiceChannel: "Voice channel", join: "Join", addLabel: "Link or search", folderLabel: "From the music folder", folderHint: "Artist, album or folder, * for everything", playlists: "Playlists", newPlaylist: "Name of a new playlist", play: "Play", open: "Open", tracks: "tracks", playlistEmpty: "The playlist is empty.", addToList: "Add a link or search", saveQueue: "Save the queue as playlist", rename: "Rename", stayTitle: "24/7 mode", sourcesTitle: "Sources", guideTitle: "How to set up Guard Music", guide1: "Create a second application in the Discord Developer Portal, name it Guard Music and copy the token of its bot.", guide2: "Write the token into .env as MUSIC_TOKEN and set music_bot.enabled to true in settings.json.", guide3: "Install ffmpeg on the computer of the bot. Spotify, Apple Music and Tidal links need nothing else, Tidal albums and playlists need a free Tidal developer key.", guide4: "Restart GuardBot. Guard Music starts with it, and this page shows a button that adds Guard Music to the server.", guide5: "Switch the module Music on, choose a voice channel and press Join, or use /play in Discord.", guide6: "For 24/7 choose a channel and a saved playlist below and switch 24/7 mode on.", riskNote: "Use at your own risk. Streaming from YouTube and other services can break their terms of use, and copyright applies to what is played. Spotify, Apple Music and Tidal are never downloaded: the bot only reads title and artist and plays the same song from the search source. The operator of the bot is responsible for what is played.", musicOff: "The music module is off on this server.", inLibrary: "tracks in the music folder", refresh: "Refresh", autoplayLabel: "24/7 playlist", lookTitle: "Dashboard appearance", lookIntro: "Colours, wallpaper, own menus and tabs for this server. Everyone who opens the dashboard of this server sees them.", colorAccent: "Accent colour", colorBg: "Background", colorSurface: "Boxes", colorText: "Text", defaultColor: "Default", wallpaper: "Wallpaper", wallDim: "Darken the wallpaper", wallBlur: "Blur the wallpaper", compact: "Compact view", hideCats: "Hide categories in the side bar", menusTitle: "Own menus", menuName: "Name of the menu", menuOpen: "Open at start", addMenu: "Add menu", tabsTitle: "Own tabs", tabName: "Name of the tab", addTab: "Add tab", tabKind: "Kind", kindPlugins: "Plugins", kindPage: "Shortcut to a page", kindLink: "Link", kindNote: "Note", tabMenu: "Menu", mainList: "Main list", tabIcon: "Icon", tabPlugins: "Plugins on this tab", tabPage: "Page", tabUrl: "Link (https)", tabText: "Text of the note", up: "Up", down: "Down", saveLook: "Save appearance", lookHint: "Changes are shown at once and stored with the button at the end.", madeBy: "Made by Justyn" });

  var LANGS = { en: "English", de: "Deutsch", fr: "Français", es: "Español", pt: "Português", ru: "Русский", uk: "Українська", sv: "Svenska", da: "Dansk", zh: "中文", ja: "日本語", ko: "한국어" };
  var lang = "en";
  try { lang = localStorage.getItem("gb_lang") || ""; } catch (e) { lang = ""; }
  if (!LANGS[lang]) lang = (navigator.language || "en").slice(0, 2);
  if (!LANGS[lang]) lang = "en";
  document.documentElement.lang = lang;
  var DICT = {}, T = {};
  function applyTexts(map) {
    DICT = map || {};
    Object.keys(TEXT.en).forEach(function (k) { if (k !== "cat") T[k] = DICT[TEXT.en[k]] || TEXT.en[k]; });
    T.cat = {};
    Object.keys(TEXT.en.cat).forEach(function (k) { T.cat[k] = DICT[TEXT.en.cat[k]] || TEXT.en.cat[k]; });
  }
  applyTexts({});
  function L(text) { return (text && DICT[text]) || text; }
  function langPicker() {
    return h("select", { class: "lang", "aria-label": "Language", onchange: function (e) {
      try { localStorage.setItem("gb_lang", e.target.value); } catch (err) { /* storage may be blocked */ }
      location.reload();
    } }, Object.keys(LANGS).map(function (k) { return h("option", { value: k, selected: k === lang }, LANGS[k]); }));
  }
  var app = document.getElementById("app");
  var S = { csrf: "", user: null, guilds: [], gid: null, info: null, section: "overview", query: "", cases: null };

  function h(tag, attrs) {
    var el = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      var v = attrs[k];
      if (v === null || v === undefined || v === false) return;
      if (k === "class") el.className = v;
      else if (k.slice(0, 2) === "on") el.addEventListener(k.slice(2), v);
      else if (k === "value") el.value = v;
      else if (k === "checked") el.checked = !!v;
      else el.setAttribute(k, v === true ? "" : v);
    });
    for (var i = 2; i < arguments.length; i++) add(el, arguments[i]);
    return el;
  }
  function add(el, c) {
    if (c === null || c === undefined || c === false) return;
    if (Array.isArray(c)) return c.forEach(function (x) { add(el, x); });
    el.appendChild(typeof c === "object" ? c : document.createTextNode(String(c)));
  }
  function icon() {
    var ns = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    var p = document.createElementNS(ns, "path");
    p.setAttribute("d", "M12 3l8 3v5c0 5-3.4 8.6-8 10-4.6-1.4-8-5-8-10V6z");
    svg.appendChild(p);
    return h("span", { class: "logo" }, svg);
  }

  var toastTimer;
  function toast(text, bad) {
    var t = document.querySelector(".toast");
    if (!t) { t = h("div", { class: "toast", role: "status" }); document.body.appendChild(t); }
    t.textContent = text;
    t.className = "toast show" + (bad ? " bad" : "");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.className = "toast" + (bad ? " bad" : ""); }, 2200);
  }

  function api(method, path, body, raw) {
    var opts = { method: method, credentials: "same-origin", headers: {} };
    if (method !== "GET") opts.headers["X-CSRF-Token"] = S.csrf;
    if (body !== undefined) { opts.headers["Content-Type"] = "application/json"; opts.body = raw ? body : JSON.stringify(body); }
    return fetch(path, opts).then(function (r) {
      return r.text().then(function (txt) {
        var data = null;
        try { data = txt ? JSON.parse(txt) : null; } catch (e) { data = { error: txt }; }
        return { status: r.status, data: data };
      });
    });
  }

  function loginScreen(message) {
    app.replaceChildren(h("div", { class: "center" }, h("div", { class: "card login" },
      icon(), h("h1", null, "GuardBot ", h("span", { class: "beta" }, "beta")), h("p", null, message || T.intro),
      message ? null : h("a", { class: "btn primary block", href: "/login" }, T.signin),
      h("p", { class: "small" }, T.loginHelp), h("div", { class: "login-lang" }, langPicker())), footer()));
  }

  function brandLink(href, name, fallback) {
    var holder = h("span", { class: "brand-ico" });
    var img = h("img", { src: "/static/brand/" + name + ".svg", alt: "", width: 18, height: 18 });
    img.addEventListener("error", function () { holder.replaceChildren(ico(fallback)); });
    holder.appendChild(img);
    return h("a", { href: href, target: "_blank", rel: "noopener noreferrer", "aria-label": name === "discord" ? "Discord" : "GitHub", title: name === "discord" ? "Discord" : "GitHub" }, holder, h("span", null, name === "discord" ? "Discord" : "GitHub"));
  }

  function footer() {
    return h("footer", { class: "foot" },
      h("span", null, "\u00a9 " + new Date().getFullYear() + " Justyn"),
      h("span", { class: "foot-sep" }, "|"),
      brandLink("https://discord.com/users/1007379337663758416", "discord", "chat"),
      brandLink("https://github.com/Justyyin", "github", "code"),
      h("span", { class: "foot-right" }, "GuardBot " + (S.version || "")));
  }

  function boot() {
    var texts = lang === "en" ? Promise.resolve() : api("GET", "/api/texts/" + lang).then(function (r) { if (r.status === 200) applyTexts(r.data); }).catch(function () {});
    texts.then(function () { return api("GET", "/api/me"); }).then(function (r) {
      if (r.status === 401) return loginScreen();
      if (r.status === 503) return loginScreen(T.offline);
      if (r.status !== 200) return loginScreen(T.offline);
      S.csrf = r.data.csrf; S.user = r.data.user; S.guilds = r.data.guilds; S.version = r.data.version;
      var want = (location.hash || "").slice(1).split("/");
      var gid = S.guilds.some(function (g) { return g.id === want[0]; }) ? want[0] : (S.guilds[0] && S.guilds[0].id);
      if (!gid) return shell(h("div", { class: "empty card" }, T.noServers));
      openGuild(gid, want[1]);
    }).catch(function () { loginScreen(T.offline); });
  }

  function openGuild(gid, section) {
    api("GET", "/api/guild/" + gid).then(function (r) {
      if (r.status === 401) return loginScreen();
      if (r.status !== 200) { toast((r.data && r.data.error) || T.offline, true); return; }
      S.gid = gid; S.info = r.data; S.section = section || "overview"; S.query = ""; S.cases = null;
      applyLook(S.info.look);
      render();
    });
  }

  function go(section) { S.section = section; S.query = ""; location.hash = S.gid + "/" + section; render(); }

  function navLink(key, text, count, iconName) {
    return h("a", { class: S.section === key ? "on" : "", "data-key": key, onclick: function () { go(key); } }, iconName ? ico(iconName) : null, h("span", null, text), count !== undefined && count !== null ? h("span", { class: "count" }, count) : null);
  }

  // simple line icons, drawn for this dashboard
  var ICONS = {
    home: "M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z",
    grid: "M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z",
    terminal: "M4 5h16v14H4zM7 9l3 3-3 3M12 15h5",
    puzzle: "M9 3h4v3a2 2 0 1 0 4 0V3h4v6h-3a2 2 0 1 0 0 4h3v8h-6v-3a2 2 0 1 0-4 0v3H3v-8h3a2 2 0 1 0 0-4H3V3z",
    spark: "M12 3l2 6 6 2-6 2-2 6-2-6-6-2 6-2zM19 3v4M17 5h4",
    image: "M4 5h16v14H4zM4 16l5-5 4 4 3-3 4 4M15 9h.01",
    face: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM9 10h.01M15 10h.01M8.5 14.5a4.5 4.5 0 0 0 7 0",
    cog: "M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6zM19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1V21a2 2 0 1 1-4 0v-.1a1.6 1.6 0 0 0-2.7-1.1l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1A1.6 1.6 0 0 0 3.6 15H3a2 2 0 1 1 0-4h.1a1.6 1.6 0 0 0 1.1-2.7l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1A1.6 1.6 0 0 0 9.7 4.4V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 2.7 1.1l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0 1.1 2.7H21a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1.3z",
    hammer: "M14 4l6 6-3 3-6-6zM11 7L3 15l3 3 8-8M3 21h8",
    list: "M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01",
    save: "M5 3h11l3 3v15H5zM8 3v5h7V3M8 21v-7h8v7",
    lock: "M6 11h12v10H6zM8 11V7a4 4 0 0 1 8 0v4",
    wrench: "M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z",
    info: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 11v6M12 7h.01",
    clock: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 7v5l3 3",
    filter: "M4 5h16l-6 8v6l-4-2v-4z",
    shield: "M12 3l8 3v5c0 5-3.4 8.6-8 10-4.6-1.4-8-5-8-10V6z",
    check: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM8 12l3 3 5-6",
    mail: "M3 6h18v12H3zM3 7l9 6 9-6",
    scale: "M12 4v16M5 20h14M6 8h12M6 8l-3 6a3 3 0 0 0 6 0zM18 8l-3 6a3 3 0 0 0 6 0z",
    flag: "M5 21V4M5 4h12l-2 4 2 4H5",
    pin: "M9 3h6l-1 6 4 4H6l4-4zM12 13v8",
    tag: "M3 12V4h8l10 10-8 8zM7.5 7.5h.01",
    eye: "M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12zM12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6z",
    alert: "M12 3l10 18H2zM12 10v5M12 18h.01",
    users: "M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM2 21v-1a6 6 0 0 1 12 0v1M16 3.5a4 4 0 0 1 0 7.5M22 21v-1a6 6 0 0 0-4-5.6",
    key: "M8 14a5 5 0 1 1 3.9-8.1A5 5 0 0 1 8 14zM11.5 11.5L21 21M17 17l2-2M15 15l2-2",
    hand: "M7 11V6a1.5 1.5 0 0 1 3 0v4M10 10V4.5a1.5 1.5 0 0 1 3 0V10M13 10V5.5a1.5 1.5 0 0 1 3 0V11M16 11V8a1.5 1.5 0 0 1 3 0v6a7 7 0 0 1-7 7h-1a6 6 0 0 1-5.2-3L4 14.5a1.6 1.6 0 0 1 2.6-1.8L7 13",
    star: "M12 3l2.8 5.8 6.2.9-4.5 4.4 1 6.2L12 17.4 6.5 20.3l1-6.2L3 9.7l6.2-.9z",
    trophy: "M7 4h10v5a5 5 0 0 1-10 0zM7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4M12 14v4M8 21h8M9 18h6",
    smile: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM8.5 14a4.5 4.5 0 0 0 7 0M9 9.5h.01M15 9.5h.01",
    bell: "M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 21h4",
    cake: "M4 21h16M5 21v-8h14v8M5 16c2 1.5 4 1.5 7 0s5-1.5 7 0M12 13V9M12 6a1 1 0 0 1 0-2",
    mic: "M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3zM5 11a7 7 0 0 0 14 0M12 18v3",
    chart: "M4 20V10M10 20V4M16 20v-7M22 20H2",
    coin: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM15 8.5a3 3 0 0 0-3-1.5c-1.7 0-3 .9-3 2.2 0 3 6 1.5 6 4.6 0 1.3-1.3 2.2-3 2.2a3 3 0 0 1-3-1.5M12 5.5v13",
    gift: "M3 9h18v4H3zM5 13h14v8H5zM12 9v12M12 9c-2-4-6-4-6-1.5S10 9 12 9zM12 9c2-4 6-4 6-1.5S14 9 12 9z",
    hash: "M5 9h15M4 15h15M10 3L8 21M16 3l-2 18",
    music: "M9 18V5l11-2v13M9 18a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM20 16a3 3 0 1 1-6 0 3 3 0 0 1 6 0z",
    bulb: "M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9V16h7v-2.1A6 6 0 0 0 12 3z",
    ticket: "M3 7h18v3a2 2 0 0 0 0 4v3H3v-3a2 2 0 0 0 0-4zM14 7v10",
    chat: "M4 5h16v11H9l-5 4z",
    megaphone: "M3 10v4h3l8 5V5L6 10zM18 9a3 3 0 0 1 0 6",
    edit: "M4 20h4L19 9l-4-4L4 16zM13 7l4 4",
    rss: "M5 19h.01M5 12a7 7 0 0 1 7 7M5 5a14 14 0 0 1 14 14",
    userplus: "M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM2 21v-1a6 6 0 0 1 12 0v1M19 8v6M16 11h6",
    folder: "M3 6h6l2 2h10v11H3z",
    archive: "M3 4h18v4H3zM5 8v12h14V8M10 12h4",
    book: "M4 4h7a3 3 0 0 1 3 3v14a2.5 2.5 0 0 0-2.5-2.5H4zM20 4h-6a3 3 0 0 0-3 3",
    calendar: "M4 5h16v16H4zM4 10h16M8 3v4M16 3v4",
    form: "M6 3h12v18H6zM9 8h6M9 12h6M9 16h3",
    case: "M4 7h16v13H4zM9 7V4h6v3M4 12h16",
    plus: "M12 5v14M5 12h14",
    pencil: "M4 20h4L19 9l-4-4L4 16z",
    link: "M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1",
    note: "M5 3h10l4 4v14H5zM15 3v4h4M8 12h8M8 16h6",
    palette: "M12 3a9 9 0 1 0 0 18c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.3 0-1.1.9-2 2-2h2.3A4.7 4.7 0 0 0 21 9.7C21 5.9 17 3 12 3zM7.5 11.5h.01M10 7.5h.01M15 7.5h.01",
    code: "M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16",
    play: "M7 4l13 8-13 8z",
    pause: "M7 4h4v16H7zM14 4h4v16h-4z",
    skip: "M5 4l10 8-10 8zM18 4v16",
    stop: "M6 6h12v12H6z",
    shuffle: "M3 7h4l10 10h4M3 17h4l3-3M14 10l3-3h4M18 4l3 3-3 3M18 14l3 3-3 3",
    repeat: "M4 11V9a3 3 0 0 1 3-3h13M17 3l3 3-3 3M20 13v2a3 3 0 0 1-3 3H4M7 21l-3-3 3-3",
    door: "M10 3h9v18h-9M14 12H3M7 8l-4 4 4 4",
    external: "M14 4h6v6M20 4l-9 9M18 14v6H4V6h6"
  };
  function ico(name) {
    var ns = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("class", "i");
    svg.setAttribute("aria-hidden", "true");
    var p = document.createElementNS(ns, "path");
    p.setAttribute("d", ICONS[name] || ICONS.puzzle);
    svg.appendChild(p);
    return svg;
  }
  function tr(obj, key) { return L(obj[key]); }
  function groupName(g) { return g.split(" / ").map(L).join(" / "); }
  function plugin(key) { return (S.info.plugins || []).filter(function (p) { return p.key === key; })[0]; }

  var closedCats = {};
  try { closedCats = JSON.parse(localStorage.getItem("gb_closed") || "{}"); } catch (e) { closedCats = {}; }

  function shell(main) {
    var topbar = h("header", { class: "topbar" },
      h("div", { class: "brand" }, icon(), "GuardBot", h("span", { class: "beta" }, "beta")),
      h("div", { class: "spacer" }), langPicker(),
      S.user ? h("div", { class: "me" },
        S.user.avatar ? h("img", { src: S.user.avatar, alt: "" }) : h("span", { class: "avatar" }),
        h("span", { class: "who" }, S.user.name),
        h("button", { class: "link", onclick: logout }, T.logout)) : null);
    var side = h("aside", { class: "side" },
      h("div", { class: "picker" }, h("select", { "aria-label": T.server, onchange: function (e) { openGuild(e.target.value); } },
        S.guilds.map(function (g) { return h("option", { value: g.id, selected: g.id === S.gid }, g.name); }))));
    if (S.info) {
      var nav = h("nav", { class: "nav" },
        navLink("overview", T.overview, null, "home"), navLink("plugins", T.plugins, null, "grid"), navLink("commands", T.navCommands, null, "terminal"),
        navLink("panels", T.navPanels, null, "image"), navLink("skills", T.navSkills, null, "puzzle"), navLink("ai", T.navAi, null, "spark"),
        navLink("music", T.navMusic, null, "music"), navLink("profile", T.navProfile, null, "face"), navLink("settings", T.settings, null, "cog"),
        navLink("cases", T.moderation, null, "case"), navLink("backup", T.backup, null, "save"));
      var look = S.info.look || {};
      (look.tabs || []).filter(function (t) { return !t.menu; }).forEach(function (t) { nav.appendChild(tabLink(t)); });
      (look.menus || []).forEach(function (m) {
        var key = "menu:" + m.id, closed = closedCats[key] === undefined ? !m.open : closedCats[key];
        var head = h("div", { class: "nav-title" + (closed ? " closed" : ""), role: "button", tabindex: "0" }, m.title, h("span", { class: "chev" }));
        var list = h("div", { hidden: closed });
        head.addEventListener("click", function () {
          closedCats[key] = !list.hidden;
          head.classList.toggle("closed"); list.hidden = !list.hidden;
          try { localStorage.setItem("gb_closed", JSON.stringify(closedCats)); } catch (e) { /* storage may be blocked */ }
        });
        (look.tabs || []).filter(function (t) { return t.menu === m.id; }).forEach(function (t) { list.appendChild(tabLink(t)); });
        nav.appendChild(head); nav.appendChild(list);
      });
      (S.info.categories || []).forEach(function (c) {
        var items = S.info.plugins.filter(function (p) { return p.category === c.key; });
        if (!items.length || (look.hide_categories || []).indexOf(c.key) !== -1) return;
        var head = h("div", { class: "nav-title" + (closedCats[c.key] ? " closed" : ""), role: "button", tabindex: "0" }, tr(c, "title"), h("span", { class: "chev" }));
        var list = h("div", { hidden: !!closedCats[c.key] });
        head.addEventListener("click", function () {
          closedCats[c.key] = !closedCats[c.key];
          head.classList.toggle("closed"); list.hidden = !!closedCats[c.key];
          try { localStorage.setItem("gb_closed", JSON.stringify(closedCats)); } catch (e) { /* storage may be blocked */ }
        });
        items.forEach(function (p) {
          var link = navLink("p:" + p.key, tr(p, "title"), null, p.icon);
          link.classList.add("plug");
          link.insertBefore(h("span", { class: "dot" + (p.on ? " on" : "") }), link.firstChild);
          list.appendChild(link);
        });
        nav.appendChild(head); nav.appendChild(list);
      });
      side.appendChild(nav);
    }
    app.replaceChildren(topbar, h("div", { class: "shell" }, side, h("main", { class: "main" }, main, footer())));
  }

  function tabLink(t) {
    if (t.kind === "link") return h("a", { class: "plug", href: t.url, target: "_blank", rel: "noopener noreferrer" }, ico(t.icon), h("span", null, t.title), h("span", { class: "count" }, ico("external")));
    if (t.kind === "page") { var a = navLink(t.page, t.title, null, t.icon); a.classList.add("plug"); return a; }
    var link = navLink("t:" + t.id, t.title, null, t.icon);
    link.classList.add("plug");
    return link;
  }

  function hexToRgb(hex) { var n = parseInt(hex.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }
  function shade(hex, f) { var c = hexToRgb(hex).map(function (v) { return Math.max(0, Math.min(255, Math.round(f < 0 ? v * (1 + f) : v + (255 - v) * f))); }); return "#" + c.map(function (v) { return ("0" + v.toString(16)).slice(-2); }).join(""); }

  function applyLook(look) {
    look = look || {};
    var root = document.documentElement, body = document.body;
    function set(name, value) { if (value) root.style.setProperty(name, value); else root.style.removeProperty(name); }
    set("--accent", look.accent);
    set("--accent-soft", look.accent ? "rgba(" + hexToRgb(look.accent).join(", ") + ", .14)" : null);
    set("--bg", look.background);
    set("--side", look.background ? shade(look.background, -0.25) : null);
    set("--top", look.background ? shade(look.background, -0.25) : null);
    set("--panel", look.surface);
    set("--panel2", look.surface ? shade(look.surface, -0.3) : null);
    set("--card", look.surface ? shade(look.surface, 0.08) : null);
    set("--text", look.text);
    var wall = look.wallpaper && S.gid ? 'url("/api/guild/' + S.gid + "/look/wallpaper/" + look.wallpaper + '")' : null;
    set("--wall", wall);
    set("--dim", String((look.dim === undefined ? 55 : look.dim) / 100));
    set("--blur", (look.blur || 0) + "px");
    body.classList.toggle("wall", !!wall);
    body.classList.toggle("compact", !!look.compact);
  }

  function logout() { api("POST", "/api/logout", {}).then(function () { location.hash = ""; location.reload(); }); }

  function render() {
    var info = S.info, sec = S.section, main;
    if (S.timer) { clearInterval(S.timer); S.timer = null; }
    if (sec === "overview") main = overview();
    else if (sec === "music") main = musicView();
    else if (sec.slice(0, 2) === "t:" && ownTab(sec.slice(2))) main = tabView(ownTab(sec.slice(2)));
    else if (sec === "plugins") main = pluginsView();
    else if (sec === "settings") main = generalView();
    else if (sec === "cases") main = casesView();
    else if (sec === "backup") main = backupView();
    else if (sec === "commands") main = commandsView();
    else if (sec === "skills") main = skillsView();
    else if (sec === "ai") main = aiView();
    else if (sec === "profile") main = profileView();
    else if (sec === "panels") main = panelsView();
    else if (sec.slice(0, 2) === "p:" && plugin(sec.slice(2))) main = pluginView(plugin(sec.slice(2)));
    else {
      var s = info.sections.filter(function (x) { return "s:" + x.key === sec; })[0];
      main = s ? settingsView(s) : overview();
    }
    shell(main);
    window.scrollTo(0, 0);
  }

  function setModule(p, on, el) {
    return api("POST", "/api/guild/" + S.gid + "/set", { changes: [{ path: "modules." + p.key, value: on }] }).then(function (r) {
      if (r.status !== 200) { toast((r.data && r.data.errors && r.data.errors["modules." + p.key]) || T.failed, true); if (el) el.checked = !on; return false; }
      p.on = on; toast(T.saved); return true;
    });
  }

  function pluginSwitch(p) {
    var sw = onoff(p.on, function (on, el) {
      setModule(p, on, el).then(function (ok) {
        if (!ok) return;
        document.querySelectorAll('[data-plugin="' + p.key + '"]').forEach(function (x) {
          x.classList.toggle("is-on", on);
          var i = x.querySelector("input[type=checkbox]"); if (i && i !== el) i.checked = on;
          var st = x.querySelector(".state"); if (st) st.textContent = on ? T.on : T.off;
        });
        document.querySelectorAll(".nav a .dot").forEach(function (d) { if (d.parentNode.getAttribute("data-key") === "p:" + p.key) d.classList.toggle("on", on); });
      });
    }, tr(p, "title"));
    if (S.info.level !== "admin") sw.querySelector("input").disabled = true;
    sw.addEventListener("click", function (e) { e.stopPropagation(); });
    return sw;
  }

  function functionsOf(p) {
    var out = [];
    p.sections.forEach(function (key) {
      var s = S.info.sections.filter(function (x) { return x.key === key; })[0];
      if (s) s.fields.forEach(function (f) { if (f.type === "bool") out.push({ field: f, section: s }); });
    });
    return out;
  }

  function settingsCount(p) {
    var n = 0;
    p.sections.forEach(function (key) { var s = S.info.sections.filter(function (x) { return x.key === key; })[0]; if (s) n += s.fields.length; });
    return n;
  }

  function pluginCard(p) {
    var nf = functionsOf(p).length, ns = settingsCount(p);
    return h("div", { class: "pcard" + (p.on ? " is-on" : ""), "data-plugin": p.key, role: "link", tabindex: "0", onclick: function () { go(p.page && !p.sections.length ? p.page : "p:" + p.key); }, onkeydown: function (e) { if (e.key === "Enter") go("p:" + p.key); } },
      h("div", { class: "pcard-top" }, h("div", { class: "ptile" }, ico(p.icon)), h("div", { class: "pcard-sw" }, h("span", { class: "state" }, p.on ? T.on : T.off), pluginSwitch(p))),
      h("h3", null, tr(p, "title")), h("p", null, tr(p, "desc")),
      h("div", { class: "pcard-foot" },
        h("span", { class: "chip mute" }, nf + " " + T.nFunctions), h("span", { class: "chip mute" }, ns + " " + T.nSettings),
        h("span", { class: "pcard-go" }, T.configure, ico("external"))));
  }

  function pluginsView() {
    var tab = S.tab || "all";
    var tabs = h("div", { class: "tabs" }, [h("a", { class: tab === "all" ? "on" : "", onclick: function () { S.tab = "all"; render(); } }, T.allPlugins)].concat(
      S.info.categories.map(function (c) { return h("a", { class: tab === c.key ? "on" : "", onclick: function () { S.tab = c.key; render(); } }, tr(c, "title")); })));
    var box = h("div", null, h("div", { class: "top" }, h("h1", null, T.plugins)), tabs);
    S.info.categories.forEach(function (c) {
      if (tab !== "all" && tab !== c.key) return;
      var items = S.info.plugins.filter(function (p) { return p.category === c.key; });
      if (!items.length) return;
      box.appendChild(h("div", { class: "cat-title" }, tr(c, "title")));
      box.appendChild(h("div", { class: "pgrid" }, items.map(pluginCard)));
    });
    return box;
  }

  function collapsible(title, desc, body, closed) {
    var box = h("section", { class: "box" + (closed ? " closed" : "") });
    var head = h("div", { class: "box-head", role: "button", tabindex: "0" }, h("div", null, h("h2", null, title), desc ? h("p", null, desc) : null), h("span", { class: "chev" }));
    head.addEventListener("click", function () { box.classList.toggle("closed"); });
    box.appendChild(head);
    box.appendChild(h("div", { class: "box-body" }, body));
    return box;
  }

  function pageHead(title, desc, right) {
    return h("div", null, h("div", { class: "top" }, h("h1", null, title), right), desc ? h("p", { class: "lead" }, desc) : null);
  }

  function pluginView(p) {
    var cat = (S.info.categories || []).filter(function (c) { return c.key === p.category; })[0];
    var funcs = functionsOf(p);
    var head = h("div", { class: "phead" + (p.on ? " is-on" : ""), "data-plugin": p.key },
      h("div", { class: "ptile big" }, ico(p.icon)),
      h("div", { class: "phead-text" }, h("h1", null, tr(p, "title")), h("p", null, tr(p, "desc")),
        h("div", { class: "chips" }, cat ? h("span", { class: "chip mute" }, tr(cat, "title")) : null, h("span", { class: "chip mute" }, funcs.length + " " + T.nFunctions), h("span", { class: "chip mute" }, settingsCount(p) + " " + T.nSettings))),
      h("label", { class: "active-switch" }, h("span", { class: "state" }, p.on ? T.on : T.off), pluginSwitch(p)));
    var box = h("div", null, head);
    box.appendChild(h("p", { class: "off-note" + (p.on ? " is-on" : ""), "data-plugin": p.key }, T.pluginOff));
    box.appendChild(collapsible(T.aboutTitle, null, h("p", { class: "about" }, tr(p, "about"))));
    if (p.page) {
      box.appendChild(collapsible(tr(p, "title"), T.openPageHint, h("div", { class: "actions" }, h("button", { class: "btn primary", onclick: function () { go(p.page); } }, T.openPage))));
    }
    var fbody = h("div", { class: "fields" });
    if (!funcs.length) fbody.appendChild(note(T.noFunctions));
    funcs.forEach(function (x) {
      var row = fieldRow(x.field, x.field.group ? groupName(x.field.group) : null);
      if (!x.section.editable) lock(row, false);
      fbody.appendChild(row);
    });
    box.appendChild(collapsible(T.functions, T.functionsHint, fbody));
    p.sections.forEach(function (key) {
      var s = S.info.sections.filter(function (x) { return x.key === key; })[0];
      if (!s) return;
      var rest = s.fields.filter(function (f) { return f.type !== "bool"; });
      if (!rest.length) return;
      var fields = h("div", { class: "fields" });
      var group = null;
      rest.forEach(function (f) {
        if ((f.group || "") !== group) { group = f.group || ""; if (group) fields.appendChild(h("div", { class: "group" }, groupName(group))); }
        fields.appendChild(fieldRow(f));
      });
      var body = h("div", null, fields);
      if (!s.editable) lock(body, false);
      box.appendChild(collapsible(L(s.title), L(s.info), body));
    });
    var cmds = h("div", { class: "fields" }, h("div", { class: "empty" }, "..."));
    box.appendChild(collapsible(T.commandsTitle, T.commandsHint, cmds));
    api("GET", "/api/guild/" + S.gid + "/commands").then(function (r) {
      if (r.status !== 200) return cmds.replaceChildren(h("div", { class: "empty" }, reason(r)));
      var mine = r.data.commands.filter(function (c) { return c.module === p.key; });
      cmds.replaceChildren();
      if (!mine.length) cmds.appendChild(h("div", { class: "empty" }, T.noCommands));
      mine.forEach(function (c) { cmds.appendChild(commandRow(c, r.data)); });
      if (S.info.level !== "admin") lock(cmds, false);
    });
    return box;
  }

  function generalView() {
    var box = h("div", null, pageHead(T.settings, T.settingsIntro));
    box.appendChild(collapsible(T.lookTitle, T.lookIntro, lookEditor()));
    var general = S.info.sections.filter(function (x) { return x.key === "general"; })[0];
    if (general) {
      var body = fieldsBox(general.fields, general.editable);
      box.appendChild(collapsible(T.general, L(general.info), body));
    }
    var claimed = {};
    S.info.plugins.forEach(function (p) { p.sections.forEach(function (k) { claimed[k] = true; }); });
    S.info.sections.forEach(function (s) {
      if (s.key === "general" || s.key === "modules" || claimed[s.key]) return;
      box.appendChild(collapsible(L(s.title), L(s.info), fieldsBox(s.fields, s.editable), true));
    });
    return box;
  }

  function top(title, withSearch) {
    var search = withSearch ? h("input", { class: "search", type: "search", placeholder: T.search, value: S.query, "aria-label": T.search, oninput: function (e) { S.query = e.target.value; filter(); } }) : null;
    return h("div", { class: "top" }, h("h1", null, title), search);
  }


  function overview() {
    var i = S.info;
    function tile(v, l) { return h("div", { class: "tile" }, h("b", null, v === null ? "-" : v), h("span", null, l)); }
    var found = h("div", { class: "fields" });
    var finder = h("input", { class: "search", type: "search", placeholder: T.searchAll, "aria-label": T.searchAll, oninput: function (e) {
      var q = e.target.value.trim().toLowerCase(), n = 0;
      found.textContent = "";
      if (q.length < 2) return;
      i.sections.forEach(function (s) {
        s.fields.forEach(function (f) {
          if (n >= 30 || (f.label + " " + L(f.label) + " " + f.path + " " + (f.group || "") + " " + groupName(f.group || "")).toLowerCase().indexOf(q) === -1) return;
          n++;
          var row = fieldRow(f);
          if (!s.editable) lock(row, false);
          found.appendChild(row);
        });
      });
      if (!n) found.appendChild(h("p", { class: "note flat" }, T.noMatch));
    } });
    var setup = setupPanel(i.module_status || []);
    var charts = h("div", { class: "charts" });
    loadCharts(charts);
    return h("div", null, top(i.name), finder, found,
      h("div", { class: "tiles" }, tile(i.members, T.members), tile(i.cases, T.cases), tile(i.modules_on + " / " + i.modules_total, T.modules), tile(i.latency_ms === null ? null : i.latency_ms + " ms", T.latency)),
      h("div", { class: "group" }, T.chartsTitle), charts,
      h("div", { class: "group" }, T.setupTitle), setup,
      h("div", { class: "group" }, T.allPluginsTitle), h("div", { class: "mini-grid" }, (i.plugins || []).map(function (p) {
        return h("div", { class: "mini" + (p.on ? " is-on" : ""), "data-plugin": p.key, role: "link", tabindex: "0", onclick: function () { go("p:" + p.key); }, onkeydown: function (e) { if (e.key === "Enter") go("p:" + p.key); } },
          h("div", { class: "ptile small" }, ico(p.icon)), h("div", { class: "mini-text" }, h("b", null, tr(p, "title")), h("span", null, tr(p, "desc"))), pluginSwitch(p));
      })),
      h("p", { class: "note flat" }, T.about + " " + S.version));
  }

  function setupPanel(list) {
    var kinds = [["open", T.setupOpen, "warn"], ["done", T.setupDone, "ok"], ["none", T.setupNone, "mute"], ["off", T.setupOff, "off"]];
    var box = h("div", { class: "setup" });
    kinds.forEach(function (k) {
      var items = list.filter(function (m) { return k[0] === "off" ? !m.on : m.on && m.setup === k[0]; });
      var col = h("div", { class: "setup-col" }, h("h3", null, k[1] + " (" + items.length + ")"));
      var chips = h("div", { class: "chips" });
      items.forEach(function (m) { chips.appendChild(h("span", { class: "chip " + k[2] }, m.name)); });
      col.appendChild(chips);
      box.appendChild(col);
    });
    return box;
  }

  function svgEl(tag, attrs) {
    var el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    Object.keys(attrs || {}).forEach(function (k) { el.setAttribute(k, attrs[k]); });
    return el;
  }

  function barChart(title, days, series) {
    var W = 560, H = 140, pad = 24, max = 1, n = days.length;
    series.forEach(function (s) { s.values.forEach(function (v) { if (v > max) max = v; }); });
    var svg = svgEl("svg", { viewBox: "0 0 " + W + " " + (H + 22), role: "img", "aria-label": title, class: "chart" });
    var slot = (W - pad) / n, bar = Math.max(1, slot / series.length - 1);
    svg.appendChild(svgEl("line", { x1: pad, y1: H, x2: W, y2: H, class: "axis" }));
    var top = svgEl("text", { x: 0, y: 10, class: "tick" }); top.textContent = String(max); svg.appendChild(top);
    series.forEach(function (s, si) {
      s.values.forEach(function (v, i) {
        var hgt = v / max * (H - 12);
        var r = svgEl("rect", { x: pad + i * slot + si * (bar + 1), y: H - hgt, width: bar, height: hgt, class: "bar s" + si });
        var tip = svgEl("title", {}); tip.textContent = days[i] + ": " + v + " " + s.name; r.appendChild(tip);
        svg.appendChild(r);
      });
    });
    [0, Math.floor(n / 2), n - 1].forEach(function (i) {
      var x = svgEl("text", { x: pad + i * slot, y: H + 16, class: "tick" }); x.textContent = days[i].slice(5); svg.appendChild(x);
    });
    var legend = h("div", { class: "legend" }, series.map(function (s, si) { return h("span", null, h("i", { class: "sw s" + si }), s.name); }));
    return h("div", { class: "chart-card" }, h("h3", null, title), svg, legend);
  }

  function loadCharts(box) {
    api("GET", "/api/guild/" + S.gid + "/stats?days=30").then(function (r) {
      if (r.status !== 200) return;
      var d = r.data, any = d.messages.some(Boolean) || d.joins.some(Boolean) || d.cases.some(Boolean);
      if (!any) { box.appendChild(h("p", { class: "note flat" }, T.noData)); return; }
      box.appendChild(barChart(T.chMessages, d.days, [{ name: T.chMessages, values: d.messages }]));
      box.appendChild(barChart(T.chJoins + " / " + T.chLeaves, d.days, [{ name: T.chJoins, values: d.joins }, { name: T.chLeaves, values: d.leaves }]));
      box.appendChild(barChart(T.chCases, d.days, [{ name: T.chCases, values: d.cases }]));
      var types = Object.keys(d.case_types);
      if (types.length) {
        var list = h("div", { class: "chips" });
        types.sort(function (a, b) { return d.case_types[b] - d.case_types[a]; }).forEach(function (k) { list.appendChild(h("span", { class: "chip mute" }, k + " " + d.case_types[k])); });
        box.appendChild(h("div", { class: "chart-card" }, h("h3", null, T.chTypes), list));
      }
    });
  }

  function matches(f) {
    var q = S.query.trim().toLowerCase();
    return !q || (f.label + " " + L(f.label) + " " + f.path + " " + (f.group || "") + " " + groupName(f.group || "")).toLowerCase().indexOf(q) !== -1;
  }
  function filter() {
    document.querySelectorAll("[data-find]").forEach(function (row) { row.hidden = S.query.trim() !== "" && row.getAttribute("data-find").indexOf(S.query.trim().toLowerCase()) === -1; });
  }

  function settingsView(section) {
    var box = h("div", null, top(L(section.title), true)), group = null, cur = null;
    var about = L(section.info);
    if (about) box.appendChild(h("p", { class: "note flat" }, about));
    section.fields.forEach(function (f) {
      var g = f.group || "";
      if (g !== group || !cur) {
        group = g;
        if (g) box.appendChild(h("div", { class: "group" }, groupName(g)));
        cur = h("div", { class: "fields" });
        box.appendChild(cur);
      }
      cur.appendChild(fieldRow(f));
    });
    if (!section.editable) lock(box, true);
    return box;
  }

  function lock(box, note) {
    box.querySelectorAll("input:not(.search), select, textarea, button").forEach(function (el) { el.disabled = true; });
    if (note) box.insertBefore(h("p", { class: "note flat" }, T.readOnly), box.children[1] || null);
  }

  function fieldsBox(fields, editable) {
    var box = h("div", { class: "fields" });
    fields.forEach(function (f) { box.appendChild(fieldRow(f)); });
    if (editable === false) lock(box, false);
    return box;
  }

  function save(path, value, row) {
    return api("POST", "/api/guild/" + S.gid + "/set", { changes: [{ path: path, value: value }] }).then(function (r) {
      var hint = row.querySelector(".hint");
      if (hint) hint.remove();
      if (r.status === 200) { row.classList.remove("err"); toast(T.saved); return true; }
      row.classList.add("err");
      var why = (r.data && r.data.errors && r.data.errors[path]) || (r.data && r.data.error) || T.failed;
      row.firstChild.appendChild(h("div", { class: "hint" }, why));
      toast(T.failed, true);
      return false;
    });
  }

  function options(list, none) {
    var out = [];
    if (none !== false) out.push(h("option", { value: "" }, T.none));
    list.forEach(function (x) { out.push(h("option", { value: x[0] }, x[1])); });
    return out;
  }
  function chanName(c) { return (c.kind === "category" ? "" : c.kind === "voice" ? "voice: " : "# ") + c.name; }

  function control(f, row) {
    var t = f.type, v = f.value;
    if (t === "bool") return h("label", { class: "switch" }, h("input", { type: "checkbox", checked: v, "aria-label": f.label, onchange: function (e) { save(f.path, e.target.checked, row); } }), h("i"));
    if (t === "int" || t === "float") return h("input", { type: "number", step: t === "int" ? "1" : "any", value: v, "aria-label": f.label, onchange: function (e) { var n = e.target.value === "" ? null : Number(e.target.value); save(f.path, n, row); } });
    if (t === "text") {
      if (f.long) return h("textarea", { "aria-label": f.label, onchange: function (e) { save(f.path, e.target.value, row); } }, v || "");
      return h("input", { type: "text", value: v === null ? "" : v, maxlength: 2000, "aria-label": f.label, onchange: function (e) { save(f.path, e.target.value, row); } });
    }
    if (t === "choice") return h("select", { "aria-label": f.label, onchange: function (e) { save(f.path, e.target.value, row); } }, f.choices.map(function (c) { return h("option", { value: c[0], selected: c[0] === v }, f.path === "language" ? c[1] : L(c[1])); }));
    if (t === "channel" || t === "role") {
      var list = t === "channel" ? S.info.channels.map(function (c) { return [c.id, chanName(c)]; }) : S.info.roles.map(function (r) { return [r.id, "@" + r.name]; });
      var sel = h("select", { "aria-label": f.label, onchange: function (e) { save(f.path, e.target.value || null, row); } }, options(list));
      sel.value = v || "";
      return sel;
    }
    if (t === "channels" || t === "roles" || t === "commands") {
      var items = t === "channels" ? S.info.channels.map(function (c) { return [c.id, chanName(c)]; }) : t === "roles" ? S.info.roles.map(function (r) { return [r.id, "@" + r.name]; }) : f.choices.map(function (c) { return [c, "/" + c]; });
      var chosen = {}; (v || []).forEach(function (x) { chosen[x] = true; });
      var box = h("div", { class: "multi", role: "group", "aria-label": f.label });
      items.forEach(function (it) {
        box.appendChild(h("label", null, h("input", { type: "checkbox", value: it[0], checked: !!chosen[it[0]], onchange: function () {
          var now = Array.prototype.slice.call(box.querySelectorAll("input:checked")).map(function (i) { return i.value; });
          save(f.path, now, row);
        } }), it[1]));
      });
      return box;
    }
    if (t === "numbers") {
      var wrap = h("div", { class: "nums" });
      v.forEach(function () { wrap.appendChild(h("input", { type: "number", step: "any", "aria-label": f.label })); });
      Array.prototype.forEach.call(wrap.children, function (inp, i) { inp.value = v[i]; inp.addEventListener("change", function () { save(f.path, Array.prototype.map.call(wrap.children, function (x) { return Number(x.value); }), row); }); });
      return wrap;
    }
    return h("textarea", { placeholder: T.lines, "aria-label": f.label, onchange: function (e) { save(f.path, e.target.value.split("\n").map(function (s) { return s.trim(); }).filter(Boolean), row); } }, (v || []).join("\n"));
  }

  function fieldRow(f, prefix) {
    var row = h("div", { class: "row", "data-find": (f.label + " " + L(f.label) + " " + f.path + " " + (f.group || "") + " " + groupName(f.group || "") + " " + L(f.help || "")).toLowerCase() });
    row.appendChild(h("div", null, h("div", { class: "name" }, prefix ? h("span", { class: "pre" }, prefix + " / ") : null, L(f.label)), f.help ? h("div", { class: "help" }, L(f.help)) : null));
    row.appendChild(h("div", { class: "ctl" }, control(f, row)));
    return row;
  }

  function casesView() {
    var holder = h("div", null, top(T.moderation));
    var box = h("div", { class: "fields" }, h("div", { class: "empty" }, "..."));
    holder.appendChild(box);
    api("GET", "/api/guild/" + S.gid + "/cases").then(function (r) {
      if (r.status !== 200) return box.replaceChildren(h("div", { class: "empty" }, T.failed));
      if (!r.data.cases.length) return box.replaceChildren(h("div", { class: "empty" }, T.nocases));
      var rows = r.data.cases.map(function (c) {
        return h("tr", null, h("td", null, "#" + c.id), h("td", null, h("span", { class: "tag" }, c.type)), h("td", null, c.user), h("td", null, c.reason), h("td", null, c.mod), h("td", null, new Date(c.ts * 1000).toLocaleString()));
      });
      box.replaceChildren(h("table", null, h("thead", null, h("tr", null, ["#", T.type, T.user, T.reason, T.moderator, T.when].map(function (x) { return h("th", null, x); }))), h("tbody", null, rows)));
    });
    return holder;
  }

  function backupView() {
    var file = h("input", { type: "file", accept: "application/json,.json", hidden: true, onchange: function (e) {
      var f = e.target.files[0]; if (!f) return;
      if (!confirm(T.sure)) { e.target.value = ""; return; }
      f.text().then(function (txt) { return api("POST", "/api/guild/" + S.gid + "/import", txt, true); }).then(function (r) {
        if (r.status === 200) { toast(T.imported); openGuild(S.gid, "backup"); }
        else toast(((r.data && r.data.errors && r.data.errors[0]) || T.failed), true);
      });
    } });
    if (S.info.level !== "admin") return h("div", null, top(T.backup), h("div", { class: "fields" }, h("p", { class: "note" }, T.adminOnly)));
    return h("div", null, top(T.backup), h("div", { class: "fields" },
      h("div", { class: "actions" },
        h("a", { class: "btn", href: "/api/guild/" + S.gid + "/export", download: "" }, T.export),
        h("button", { class: "btn", onclick: function () { file.click(); } }, T.import), file),
      h("p", { class: "note" }, T.importNote)));
  }


  function post(path, body) { return api("POST", "/api/guild/" + S.gid + path, body); }
  function reason(r) { return (r.data && (r.data.error || r.data.errors && r.data.errors[0])) || (typeof (r.data && r.data.error) === "string" ? r.data.error : "") || T.failed; }
  function done(r, okText) {
    if (r.status === 200) { toast(okText || T.saved); return true; }
    toast(reason(r), true); return false;
  }
  function note(text) { return h("p", { class: "note flat" }, text); }
  function simpleRow(label, control) { return h("div", { class: "row" }, h("div", null, h("div", { class: "name" }, label)), h("div", { class: "ctl" }, control)); }
  function onoff(value, handler, label) {
    return h("label", { class: "switch" }, h("input", { type: "checkbox", checked: value, "aria-label": label, onchange: function (e) { handler(e.target.checked, e.target); } }), h("i"));
  }
  function textInput(value, handler, attrs) {
    return h("input", Object.assign({ type: "text", value: value || "", onchange: function (e) { handler(e.target.value); } }, attrs || {}));
  }

  function commandsView() {
    var holder = h("div", null, top(T.navCommands)), body = h("div", null, "...");
    holder.appendChild(note(T.cmdIntro)); holder.appendChild(body);
    api("GET", "/api/guild/" + S.gid + "/commands").then(function (r) {
      if (r.status !== 200) return body.replaceChildren(note(reason(r)));
      var d = r.data, query = "", kind = "all", editable = S.info.level === "admin";
      var general = h("div", { class: "fields" },
        simpleRow(T.prefix, textInput(d.prefix, function (v) { api("POST", "/api/guild/" + S.gid + "/set", { changes: [{ path: "prefix", value: v }] }).then(function (x) { done(x); }); }, { maxlength: 5 })));
      var list = h("div", { class: "fields" });
      function draw() {
        list.textContent = "";
        d.commands.forEach(function (c) {
          var hay = (c.key + " " + c.path + " " + (c.description || "") + " " + (c.module || "")).toLowerCase();
          if (query && hay.indexOf(query) === -1) return;
          if (kind !== "all" && c.kind !== kind && !(kind === "text" && c.text)) return;
          list.appendChild(commandRow(c, d));
        });
        if (!list.children.length) list.appendChild(note(T.noMatch));
      }
      var kinds = h("select", { "aria-label": T.filter, onchange: function (e) { kind = e.target.value; draw(); } },
        [["all", T.allKinds], ["slash", T.slash], ["text", T.text], ["menu", T.menu]].map(function (k) { return h("option", { value: k[0] }, k[1]); }));
      var find = h("input", { class: "search", type: "search", placeholder: T.filter, "aria-label": T.filter, oninput: function (e) { query = e.target.value.trim().toLowerCase(); draw(); } });
      var aliasBox = aliasPanel(d, editable);
      var custom = h("div", { class: "chips" }, d.custom.map(function (c) { return h("span", { class: "chip " + (c.enabled === false ? "off" : "mute") }, (c.kind === "skill" ? "skill " : "tag ") + c.key + " (" + c.uses + ")"); }));
      body.replaceChildren(general, h("div", { class: "group" }, T.navCommands), h("div", { class: "actions" }, find, kinds), list, h("div", { class: "group" }, T.aliases), aliasBox, h("div", { class: "group" }, T.custom), d.custom.length ? custom : note(T.none));
      draw();
      if (!editable) lock(body, false);
    });
    return holder;
  }

  function commandRow(c, d) {
    var row = h("div", { class: "row cmd" });
    var info = h("div", null, h("div", { class: "name" }, c.path, " ", h("span", { class: "tag" }, c.kind === "slash" && c.text ? "slash + " + T.text : c.kind), c.bot ? h("span", { class: "tag accent" }, c.bot) : null),
      c.description ? h("div", { class: "small" }, c.description) : null,
      h("div", { class: "small" }, [c.module ? T.module + ": " + c.module + (c.module_on ? "" : " (" + T.moduleOff + ")") : null, c.permission ? T.permission + ": " + c.permission : null, c.subcount ? T.subs + ": " + c.subcount : null].filter(Boolean).join(" | ")));
    var ctl = h("div", { class: "ctl" });
    var sw = onoff(c.enabled, function (on, el) {
      post("/commands/set", { key: c.key, enabled: on }).then(function (x) { if (!done(x)) el.checked = !on; else c.enabled = on; });
    }, c.key);
    if (c.protected) { sw.querySelector("input").disabled = true; sw.title = T.protectedCmd; }
    ctl.appendChild(sw);
    var pencil = h("button", { class: "btn icon-btn", "aria-label": T.rolesAllowed, title: T.rolesAllowed + " / " + T.rolesDenied }, ico("pencil"));
    ctl.appendChild(pencil);
    var more = h("details", { class: "more" }, h("summary", null, T.rolesAllowed + " / " + T.rolesDenied));
    [["roles", T.rolesAllowed], ["deny_roles", T.rolesDenied]].forEach(function (f) {
      var chosen = {}; (c[f[0]] || []).forEach(function (x) { chosen[x] = true; });
      var box = h("div", { class: "multi", role: "group", "aria-label": f[1] });
      S.info.roles.forEach(function (role) {
        box.appendChild(h("label", null, h("input", { type: "checkbox", value: role.id, checked: !!chosen[role.id], onchange: function () {
          var now = Array.prototype.slice.call(box.querySelectorAll("input:checked")).map(function (i) { return i.value; });
          post("/commands/set", { key: c.key, [f[0]]: now }).then(function (x) { if (done(x)) c[f[0]] = now; });
        } }), "@" + role.name));
      });
      more.appendChild(h("div", { class: "name" }, f[1])); more.appendChild(box);
    });
    pencil.addEventListener("click", function () { more.open = !more.open; });
    row.appendChild(info); row.appendChild(ctl); row.appendChild(more);
    return row;
  }

  function aliasPanel(d, editable) {
    var box = h("div", { class: "fields" });
    var textCmds = d.commands.filter(function (c) { return c.text; }).map(function (c) { return c.key; });
    function redraw() {
      box.textContent = "";
      var any = false;
      d.commands.forEach(function (c) {
        (c.aliases || []).forEach(function (a) {
          any = true;
          box.appendChild(simpleRow(d.prefix + a + " -> " + c.key, h("button", { class: "btn", onclick: function () {
            post("/commands/alias", { alias: a, command: null }).then(function (x) { if (done(x)) { c.aliases = c.aliases.filter(function (y) { return y !== a; }); redraw(); } });
          } }, T.remove)));
        });
      });
      if (!any) box.appendChild(note(T.none));
      var name = h("input", { type: "text", placeholder: T.aliasName, maxlength: 30, "aria-label": T.aliasName });
      var target = h("select", { "aria-label": T.aliasFor }, textCmds.map(function (k) { return h("option", { value: k }, k); }));
      box.appendChild(h("div", { class: "actions" }, name, target, h("button", { class: "btn", onclick: function () {
        post("/commands/alias", { alias: name.value, command: target.value }).then(function (x) {
          if (done(x)) { var c = d.commands.filter(function (y) { return y.key === target.value; })[0]; (c.aliases = c.aliases || []).push(name.value.toLowerCase()); redraw(); }
        });
      } }, T.add)));
    }
    redraw();
    return box;
  }

  function skillsView() {
    var holder = h("div", null, top(T.navSkills)), body = h("div", null, "...");
    holder.appendChild(note(T.skillsIntro)); holder.appendChild(body);
    function load() {
      api("GET", "/api/guild/" + S.gid + "/skills").then(function (r) {
        if (r.status !== 200) return body.replaceChildren(note(reason(r)));
        var d = r.data, editable = S.info.level === "admin";
        var editor = h("textarea", { class: "code", rows: 16, spellcheck: "false", "aria-label": T.skillJson });
        var msg = h("p", { class: "note flat" });
        var list = h("div", { class: "fields" });
        if (!d.module_on) list.appendChild(note(T.skillsOff));
        if (!d.skills.length) list.appendChild(note(T.skillsNone));
        d.skills.forEach(function (s) {
          var sp = s.spec;
          list.appendChild(h("div", { class: "row" },
            h("div", null, h("div", { class: "name" }, sp.name, " ", h("span", { class: "tag" }, sp.kind)), h("div", { class: "small" }, (sp.description || s.summary) + " | " + T.uses + ": " + (s.meta.uses || 0))),
            h("div", { class: "ctl" },
              onoff(sp.enabled, function (on, el) { post("/skills/toggle", { name: sp.name, enabled: on }).then(function (x) { if (!done(x)) el.checked = !on; }); }, sp.name),
              h("button", { class: "btn", onclick: function () { editor.value = JSON.stringify(sp, null, 2); editor.scrollIntoView(); } }, T.edit),
              h("button", { class: "btn", onclick: function () { if (confirm(T.surer)) post("/skills/delete", { name: sp.name }).then(function (x) { if (done(x)) load(); }); } }, T.del))));
        });
        var starters = h("div", { class: "actions" }, Object.keys(d.starters).map(function (k) {
          return h("button", { class: "btn", onclick: function () { editor.value = JSON.stringify(d.starters[k], null, 2); msg.textContent = ""; } }, T.newSkill + ": " + k);
        }));
        var saveBtn = h("button", { class: "btn primary", onclick: function () {
          var spec; try { spec = JSON.parse(editor.value); } catch (e) { msg.textContent = String(e.message).slice(0, 200); return; }
          post("/skills/save", { spec: spec }).then(function (x) {
            if (x.status === 200) { toast(T.saved); load(); } else { msg.textContent = reason(x); toast(T.failed, true); }
          });
        } }, T.save);
        var edit = h("div", null, h("div", { class: "group" }, T.skillJson), starters, editor, msg, h("div", { class: "actions" }, saveBtn));
        if (!editable) lock(edit, false);
        body.replaceChildren(list, edit);
      });
    }
    load();
    return holder;
  }

  function aiView() {
    var holder = h("div", null, top(T.navAi)), body = h("div", null, "...");
    holder.appendChild(note(T.aiIntro)); holder.appendChild(note(T.aiPrivacy)); holder.appendChild(body);
    function load() {
      api("GET", "/api/guild/" + S.gid + "/ai").then(function (r) {
        if (r.status !== 200) return body.replaceChildren(note(reason(r)));
        var d = r.data, editable = S.info.level === "admin";
        var prov = h("select", { "aria-label": T.provider }, Object.keys(d.providers).map(function (k) { return h("option", { value: k, selected: k === d.provider }, d.providers[k].label); }));
        var model = h("input", { type: "text", placeholder: d.providers[prov.value].model, value: d.model || "", maxlength: 80, "aria-label": T.model });
        prov.addEventListener("change", function () { model.placeholder = d.providers[prov.value].model; });
        var key = h("input", { type: "password", autocomplete: "off", placeholder: T.apiKey, "aria-label": T.apiKey });
        var keyBtn = h("button", { class: "btn primary", onclick: function () {
          post("/ai/key", { provider: prov.value, key: key.value, model: model.value }).then(function (x) { key.value = ""; if (done(x, T.keySaved)) load(); });
        } }, T.saveKey);
        var rm = h("button", { class: "btn", onclick: function () { post("/ai/remove", {}).then(function (x) { if (done(x)) load(); }); } }, T.removeKey);
        function num(label, field, min, max) {
          return simpleRow(label, h("input", { type: "number", min: min, max: max, value: d[field], "aria-label": label, onchange: function (e) { var b = {}; b[field] = Number(e.target.value); post("/ai/set", b).then(function (x) { done(x); }); } }));
        }
        var box = h("div", { class: "fields" },
          note((d.has_key ? T.hasKey : T.noKey) + " " + T.used + ": " + d.used + " / " + d.daily_limit + ", " + T.errorsCount + ": " + d.errors),
          simpleRow(T.provider, prov), simpleRow(T.model, h("div", null, model, h("button", { class: "btn", onclick: function () { post("/ai/set", { model: model.value || d.providers[prov.value].model }).then(function (x) { done(x); }); } }, T.save))),
          simpleRow(T.apiKey, h("div", null, key, keyBtn, d.has_key ? rm : null)), note(T.changeProv),
          num(T.daily, "daily_limit", 1, 1000), num(T.cooldown, "user_cooldown", 0, 3600), num(T.maxTokens, "max_tokens", 100, 4000),
          simpleRow(T.second, onoff(d.second_opinion, function (on, el) { post("/ai/set", { second_opinion: on }).then(function (x) { if (!done(x)) el.checked = !on; }); }, T.second)));
        if (!editable) lock(box, false);
        body.replaceChildren(box);
      });
    }
    load();
    return holder;
  }

  function readImage(input) {
    return new Promise(function (resolve) {
      var f = input.files[0];
      if (!f) return resolve(undefined);
      var fr = new FileReader();
      fr.onload = function () { resolve(String(fr.result)); };
      fr.readAsDataURL(f);
    });
  }

  function profileView() {
    var holder = h("div", null, top(T.navProfile)), body = h("div", null, "...");
    holder.appendChild(note(T.profIntro)); holder.appendChild(note(T.limitsNote)); holder.appendChild(body);
    api("GET", "/api/guild/" + S.gid + "/profile").then(function (r) {
      if (r.status !== 200) return body.replaceChildren(note(reason(r)));
      var d = r.data, editable = S.info.level === "admin";
      function form(title, current, send, fields) {
        var inputs = {}, initial = {}, box = h("div", { class: "fields" });
        box.appendChild(h("div", { class: "row" }, h("div", null, h("div", { class: "name" }, title)), h("div", { class: "ctl" }, current.avatar ? h("img", { class: "preview", src: current.avatar, alt: "" }) : null)));
        fields.forEach(function (f) {
          var el = f.file ? h("input", { type: "file", accept: "image/png,image/jpeg,image/gif,image/webp", "aria-label": f.label }) : (f.long ? h("textarea", { "aria-label": f.label, maxlength: f.max }, f.value || "") : h("input", { type: "text", value: f.value || "", maxlength: f.max, "aria-label": f.label }));
          inputs[f.key] = el; initial[f.key] = f.value || "";
          var reset = f.file ? h("button", { class: "btn", onclick: function () { send(f.reset(), el); } }, T.reset) : null;
          box.appendChild(simpleRow(f.label, h("div", null, el, reset)));
        });
        box.appendChild(h("div", { class: "actions" }, h("button", { class: "btn primary", onclick: function () {
          var keys = Object.keys(inputs), body = {}, jobs = keys.map(function (k) {
            var el = inputs[k];
            if (el.type === "file") return readImage(el).then(function (v) { if (v !== undefined) body[k] = v; });
            if (el.value !== (initial[k] || "")) body[k] = el.value;
            return Promise.resolve();
          });
          Promise.all(jobs).then(function () { if (Object.keys(body).length) send(body); });
        } }, T.save)));
        return box;
      }
      function sendServer(b) { post("/profile/server", b).then(function (x) { done(x); }); }
      function sendGlobal(b) { api("POST", "/api/bot/profile", b).then(function (x) { done(x); }); }
      var server = form(T.serverProfile, d.server, sendServer, [
        { key: "nick", label: T.nick, value: d.server.nick, max: 32 },
        { key: "avatar", label: T.avatar, file: true, reset: function () { return { avatar: null }; } },
        { key: "banner", label: T.banner, file: true, reset: function () { return { banner: null }; } },
        { key: "bio", label: T.bio, long: true, max: 190, value: "" }]);
      if (!editable) lock(server, false);
      var out = [server];
      out.push(h("div", { class: "group" }, T.globalProfile));
      if (d.owner) out.push(form(T.globalProfile, d.global, sendGlobal, [
        { key: "name", label: T.nick, value: d.global.name, max: 32 },
        { key: "avatar", label: T.avatar, file: true, reset: function () { return { avatar: null }; } },
        { key: "banner", label: T.banner, file: true, reset: function () { return { banner: null }; } },
        { key: "bio", label: T.bio, long: true, max: 400, value: d.global.bio || "" }]));
      else out.push(note(T.ownerOnly));
      body.replaceChildren.apply(body, out);
    });
    return holder;
  }


  function panelsView() {
    var holder = h("div", null, top(T.navPanels)), body = h("div", null, "...");
    holder.appendChild(note(T.panelsIntro)); holder.appendChild(body);
    var base = "/api/guild/" + S.gid + "/panels";
    function load(openId) {
      api("GET", base).then(function (r) {
        if (r.status !== 200) return body.replaceChildren(note(reason(r)));
        var d = r.data, editable = S.info.level === "admin";
        if (openId) { var p = d.panels.filter(function (x) { return x.id === openId; })[0]; if (p) return editor(p, d); }
        var list = h("div", { class: "fields" });
        if (!d.panels.length) list.appendChild(note(T.none));
        d.panels.forEach(function (item) {
          var p = item.panel;
          list.appendChild(h("div", { class: "row" },
            h("div", null, h("div", { class: "name" }, p.name), h("div", { class: "small" }, p.sections.length + " " + T.section + ", " + p.buttons.length + " " + T.buttons + " | " + (p.messages.length ? T.posted : T.notPosted))),
            h("div", { class: "ctl" },
              h("button", { class: "btn", onclick: function () { editor(item, d); } }, T.edit),
              h("button", { class: "btn", onclick: function () {
                var keep = confirm(T.surer); if (!keep) return;
                post("/panels/delete", { id: item.id, messages: p.messages.length ? confirm(T.deleteMessages) : false }).then(function (x) { if (done(x)) load(); });
              } }, T.del))));
        });
        var name = h("input", { type: "text", placeholder: T.name, maxlength: 30, "aria-label": T.name });
        var tpl = h("select", { "aria-label": T.template }, d.templates.map(function (t) { return h("option", { value: t }, t); }));
        var create = h("div", { class: "actions" }, name, tpl, h("button", { class: "btn primary", onclick: function () {
          post("/panels/create", { name: name.value, template: tpl.value }).then(function (x) { if (done(x)) load(x.data.id); });
        } }, T.newPanel));
        if (!editable) lock(create, false);
        body.replaceChildren(list, h("div", { class: "group" }, T.newPanel), create);
      });
    }

    function picture(sec, key, label, pid) {
      var img = h("img", { class: "preview wide", alt: "", src: sec[key] ? base + "/image/" + sec[key] : null, hidden: !sec[key] });
      var file = h("input", { type: "file", accept: "image/png,image/jpeg,image/gif,image/webp", "aria-label": label, onchange: function () {
        if (!file.files[0]) return;
        toast(T.uploading);
        readImage(file).then(function (data) { return post("/panels/image", { image: data, name: file.files[0].name }); }).then(function (x) {
          if (!done(x)) return;
          sec[key] = x.data.id; img.src = base + "/image/" + x.data.id; img.hidden = false;
        });
      } });
      var rm = h("button", { class: "btn", onclick: function () { sec[key] = null; img.hidden = true; file.value = ""; } }, T.remove);
      return simpleRow(label, h("div", null, img, file, rm));
    }

    function editor(item, d) {
      var p = JSON.parse(JSON.stringify(item.panel)), box = h("div", null);
      var chans = S.info.channels.filter(function (c) { return c.kind === "text"; });
      function redraw() {
        box.textContent = "";
        var head = h("div", { class: "fields" },
          simpleRow(T.name, textInput(p.name, function (v) { p.name = v; }, { maxlength: 30 })),
          simpleRow(T.channel, (function () {
            var sel = h("select", { "aria-label": T.channel, onchange: function (e) { p.channel = e.target.value || null; } }, options(chans.map(function (c) { return [c.id, "# " + c.name]; })));
            sel.value = p.channel ? String(p.channel) : ""; return sel;
          })()),
          simpleRow(T.single, onoff(p.single, function (on) { p.single = on; }, T.single)));
        box.appendChild(head);
        p.sections.forEach(function (sec, i) {
          box.appendChild(h("div", { class: "group" }, T.section + " " + (i + 1)));
          var color = h("input", { type: "color", value: sec.color || "#5865f2", "aria-label": T.color, onchange: function (e) { sec.color = e.target.value; } });
          box.appendChild(h("div", { class: "fields" },
            picture(sec, "banner", T.bannerPic),
            simpleRow(T.title, textInput(sec.title, function (v) { sec.title = v; }, { maxlength: 256 })),
            simpleRow(T.textBody, h("textarea", { rows: 6, maxlength: 4000, "aria-label": T.textBody, onchange: function (e) { sec.text = e.target.value; } }, sec.text || "")),
            simpleRow(T.color, h("div", null, color, h("button", { class: "btn", onclick: function () { sec.color = null; } }, T.noColor))),
            picture(sec, "image", T.imagePic), picture(sec, "thumbnail", T.thumbPic),
            simpleRow(T.footer, textInput(sec.footer, function (v) { sec.footer = v; }, { maxlength: 200 })),
            p.sections.length > 1 ? h("div", { class: "actions" }, h("button", { class: "btn", onclick: function () { p.sections.splice(i, 1); redraw(); } }, T.remove)) : null));
        });
        if (p.sections.length < 5) box.appendChild(h("div", { class: "actions" }, h("button", { class: "btn", onclick: function () {
          p.sections.push({ title: "", text: "", footer: "", color: null, banner: null, image: null, thumbnail: null }); redraw();
        } }, T.addSection)));
        box.appendChild(h("div", { class: "group" }, T.buttons));
        var btns = h("div", { class: "fields" });
        p.buttons.forEach(function (b, i) {
          var kind = h("select", { "aria-label": T.kind, onchange: function (e) { b.kind = e.target.value; redraw(); } }, ["role", "verify", "link"].map(function (k) { return h("option", { value: k, selected: k === b.kind }, k); }));
          var style = h("select", { "aria-label": T.style, onchange: function (e) { b.style = e.target.value; } }, ["primary", "secondary", "success", "danger"].map(function (k) { return h("option", { value: k, selected: k === b.style }, k); }));
          var extra = null;
          if (b.kind === "role") { extra = h("select", { "aria-label": T.role, onchange: function (e) { b.role = e.target.value; } }, options(S.info.roles.map(function (r) { return [r.id, "@" + r.name]; }))); extra.value = b.role ? String(b.role) : ""; }
          if (b.kind === "link") extra = textInput(b.url, function (v) { b.url = v; }, { placeholder: T.url, maxlength: 512 });
          btns.appendChild(h("div", { class: "actions" }, kind,
            textInput(b.label, function (v) { b.label = v; }, { placeholder: T.label, maxlength: 80 }),
            textInput(b.emoji, function (v) { b.emoji = v; }, { placeholder: T.emoji, maxlength: 60, class: "short" }),
            b.kind === "link" ? null : style, extra,
            h("button", { class: "btn", onclick: function () { p.buttons.splice(i, 1); redraw(); } }, T.remove)));
        });
        if (p.buttons.length < 20) btns.appendChild(h("div", { class: "actions" }, h("button", { class: "btn", onclick: function () {
          p.buttons.push({ kind: "role", label: "", emoji: "", style: "primary", role: null }); redraw();
        } }, T.addButton)));
        box.appendChild(btns);
        var target = h("select", { "aria-label": T.channel }, options(chans.map(function (c) { return [c.id, "# " + c.name]; }), false));
        if (p.channel) target.value = String(p.channel);
        function clean() {
          var out = JSON.parse(JSON.stringify(p));
          delete out.messages;
          out.buttons.forEach(function (b) { if (b.kind !== "role") delete b.role; if (b.kind !== "link") delete b.url; });
          return out;
        }
        function save() { return post("/panels/save", { id: item.id, panel: clean() }); }
        var actions = h("div", { class: "actions" },
          h("button", { class: "btn", onclick: function () { load(); } }, T.back),
          h("button", { class: "btn primary", onclick: function () { save().then(function (x) { done(x); }); } }, T.save),
          target,
          h("button", { class: "btn", onclick: function () { save().then(function (x) { if (done(x)) return post("/panels/post", { id: item.id, channel: target.value }).then(function (y) { if (done(y)) load(item.id); }); }); } }, T.post),
          item.panel.messages.length ? h("button", { class: "btn", onclick: function () { save().then(function (x) { if (done(x)) return post("/panels/update", { id: item.id }).then(function (y) { done(y); }); }); } }, T.update) : null);
        box.appendChild(actions);
        if (S.info.level !== "admin") lock(box, false);
      }
      redraw();
      body.replaceChildren(box);
    }
    load();
    return holder;
  }

  // ---- own tabs

  function ownTab(id) { return ((S.info.look || {}).tabs || []).filter(function (t) { return t.id === id; })[0]; }

  function tabView(t) {
    var box = h("div", null, top(t.title));
    if (t.kind === "note") {
      box.appendChild(h("div", { class: "box" }, h("div", { class: "box-body plain" }, h("p", { class: "about pre-wrap" }, t.text))));
      return box;
    }
    var items = (t.plugins || []).map(plugin).filter(Boolean);
    box.appendChild(h("div", { class: "pgrid" }, items.map(pluginCard)));
    return box;
  }

  // ---- appearance

  var PAGE_KEYS = ["overview", "plugins", "commands", "panels", "skills", "ai", "music", "profile", "settings", "cases", "backup"];
  var TAB_ICONS = ["home", "grid", "terminal", "puzzle", "spark", "image", "face", "cog", "hammer", "list", "save", "lock", "wrench", "info", "clock", "filter", "shield", "check", "mail", "scale", "flag", "pin", "tag", "eye", "alert", "users", "key", "hand", "star", "trophy", "smile", "bell", "cake", "mic", "chart", "coin", "gift", "hash", "music", "bulb", "ticket", "chat", "megaphone", "edit", "rss", "userplus", "folder", "archive", "book", "calendar", "form", "case", "plus", "pencil", "link", "note", "palette"];
  function pageName(k) { return { overview: T.overview, plugins: T.plugins, commands: T.navCommands, panels: T.navPanels, skills: T.navSkills, ai: T.navAi, music: T.navMusic, profile: T.navProfile, settings: T.settings, cases: T.moderation, backup: T.backup }[k] || k; }

  function lookEditor() {
    var lk = JSON.parse(JSON.stringify(S.info.look || {})), body = h("div", null), admin = S.info.level === "admin";
    lk.menus = lk.menus || []; lk.tabs = lk.tabs || []; lk.hide_categories = lk.hide_categories || [];
    function preview() { applyLook(lk); }
    function colorRow(key, label) {
      var base = { accent: "#4f8cff", background: "#23252c", surface: "#1e1f25", text: "#f1f2f5" }[key];
      var input = h("input", { type: "color", value: lk[key] || base, "aria-label": label, oninput: function (e) { lk[key] = e.target.value; preview(); } });
      return simpleRow(label, h("div", null, input, h("button", { class: "btn", onclick: function () { lk[key] = null; input.value = base; preview(); } }, T.defaultColor)));
    }
    function range(key, label, max) {
      var out = h("span", { class: "small" }, String(lk[key] || 0));
      return simpleRow(label, h("div", null, h("input", { type: "range", min: 0, max: max, value: lk[key] || 0, "aria-label": label, oninput: function (e) { lk[key] = Number(e.target.value); out.textContent = e.target.value; preview(); } }), out));
    }
    function draw() {
      body.textContent = "";
      body.appendChild(note(T.lookHint));
      var wallImg = h("img", { class: "preview wide", alt: "", hidden: !lk.wallpaper, src: lk.wallpaper ? "/api/guild/" + S.gid + "/look/wallpaper/" + lk.wallpaper : null });
      var file = h("input", { type: "file", accept: "image/png,image/jpeg,image/gif,image/webp", "aria-label": T.wallpaper, onchange: function () {
        if (!file.files[0]) return;
        toast(T.uploading);
        readImage(file).then(function (data) { return post("/look/wallpaper", { image: data }); }).then(function (x) {
          if (!done(x)) return;
          lk.wallpaper = S.info.look.wallpaper = x.data.wallpaper; preview(); draw();
        });
      } });
      body.appendChild(h("div", { class: "fields" },
        colorRow("accent", T.colorAccent), colorRow("background", T.colorBg), colorRow("surface", T.colorSurface), colorRow("text", T.colorText),
        simpleRow(T.wallpaper, h("div", null, wallImg, file, lk.wallpaper ? h("button", { class: "btn", onclick: function () { post("/look/wallpaper", { remove: true }).then(function (x) { if (done(x)) { lk.wallpaper = S.info.look.wallpaper = null; preview(); draw(); } }); } }, T.remove) : null)),
        range("dim", T.wallDim, 90), range("blur", T.wallBlur, 20),
        simpleRow(T.compact, onoff(!!lk.compact, function (on) { lk.compact = on; preview(); }, T.compact))));
      var cats = h("div", { class: "multi", role: "group", "aria-label": T.hideCats });
      (S.info.categories || []).forEach(function (c) {
        cats.appendChild(h("label", null, h("input", { type: "checkbox", checked: lk.hide_categories.indexOf(c.key) !== -1, onchange: function (e) {
          lk.hide_categories = lk.hide_categories.filter(function (x) { return x !== c.key; }); if (e.target.checked) lk.hide_categories.push(c.key);
        } }), tr(c, "title")));
      });
      body.appendChild(h("div", { class: "group" }, T.hideCats)); body.appendChild(cats);
      body.appendChild(h("div", { class: "group" }, T.menusTitle));
      var menus = h("div", { class: "fields" });
      lk.menus.forEach(function (m, i) {
        menus.appendChild(h("div", { class: "actions editor-row" },
          textInput(m.title, function (v) { m.title = v; }, { placeholder: T.menuName, maxlength: 40 }),
          h("label", { class: "inline" }, onoff(m.open !== false, function (on) { m.open = on; }, T.menuOpen), T.menuOpen),
          moveButtons(lk.menus, i, draw),
          h("button", { class: "btn", onclick: function () { lk.tabs.forEach(function (t) { if (t.menu === m.id) t.menu = ""; }); lk.menus.splice(i, 1); draw(); } }, T.remove)));
      });
      menus.appendChild(h("div", { class: "actions" }, h("button", { class: "btn", onclick: function () {
        var n = 1; while (lk.menus.some(function (m) { return m.id === "m" + n; })) n++;
        lk.menus.push({ id: "m" + n, title: T.menuName, open: true }); draw();
      } }, ico("plus"), T.addMenu)));
      body.appendChild(menus);
      body.appendChild(h("div", { class: "group" }, T.tabsTitle));
      var tabs = h("div", { class: "fields" });
      lk.tabs.forEach(function (t, i) {
        var kind = h("select", { "aria-label": T.tabKind, onchange: function (e) { t.kind = e.target.value; draw(); } },
          [["plugins", T.kindPlugins], ["page", T.kindPage], ["link", T.kindLink], ["note", T.kindNote]].map(function (k) { return h("option", { value: k[0], selected: t.kind === k[0] }, k[1]); }));
        var iconSel = h("select", { "aria-label": T.tabIcon, onchange: function (e) { t.icon = e.target.value; draw(); } }, TAB_ICONS.map(function (k) { return h("option", { value: k, selected: t.icon === k }, k); }));
        var menuSel = h("select", { "aria-label": T.tabMenu, onchange: function (e) { t.menu = e.target.value; } }, [h("option", { value: "" }, T.mainList)].concat(lk.menus.map(function (m) { return h("option", { value: m.id, selected: t.menu === m.id }, m.title); })));
        var extra;
        if (t.kind === "plugins") {
          extra = h("div", { class: "multi", role: "group", "aria-label": T.tabPlugins });
          S.info.plugins.forEach(function (p) {
            extra.appendChild(h("label", null, h("input", { type: "checkbox", checked: (t.plugins || []).indexOf(p.key) !== -1, onchange: function (e) {
              t.plugins = (t.plugins || []).filter(function (x) { return x !== p.key; }); if (e.target.checked) t.plugins.push(p.key);
            } }), tr(p, "title")));
          });
        } else if (t.kind === "page") {
          extra = h("select", { "aria-label": T.tabPage, onchange: function (e) { t.page = e.target.value; } }, PAGE_KEYS.map(function (k) { return h("option", { value: k, selected: t.page === k }, pageName(k)); }));
          if (!t.page) t.page = PAGE_KEYS[0];
        } else if (t.kind === "link") {
          extra = textInput(t.url, function (v) { t.url = v; }, { placeholder: "https://", maxlength: 300, class: "wide" });
        } else {
          extra = h("textarea", { rows: 4, maxlength: 4000, "aria-label": T.tabText, placeholder: T.tabText, onchange: function (e) { t.text = e.target.value; } }, t.text || "");
        }
        tabs.appendChild(h("div", { class: "tab-card" },
          h("div", { class: "actions" }, h("span", { class: "tab-ico" }, ico(t.icon)), textInput(t.title, function (v) { t.title = v; }, { placeholder: T.tabName, maxlength: 40 }), kind, iconSel, menuSel, moveButtons(lk.tabs, i, draw),
            h("button", { class: "btn", onclick: function () { lk.tabs.splice(i, 1); draw(); } }, T.remove)),
          extra));
      });
      tabs.appendChild(h("div", { class: "actions" }, h("button", { class: "btn", onclick: function () {
        var n = 1; while (lk.tabs.some(function (t) { return t.id === "t" + n; })) n++;
        lk.tabs.push({ id: "t" + n, title: T.tabName, icon: "star", menu: "", kind: "plugins", plugins: [], page: "", url: "", text: "" }); draw();
      } }, ico("plus"), T.addTab)));
      body.appendChild(tabs);
      body.appendChild(h("div", { class: "actions" }, h("button", { class: "btn primary", onclick: function () {
        post("/look", { look: lk }).then(function (x) { if (done(x, T.saved)) { S.info.look = x.data.look; applyLook(S.info.look); render(); } });
      } }, T.saveLook)));
      if (!admin) lock(body, false);
    }
    draw();
    return body;
  }

  function moveButtons(list, i, redraw) {
    return [
      h("button", { class: "btn icon-btn", "aria-label": T.up, title: T.up, disabled: i === 0, onclick: function () { var x = list.splice(i, 1)[0]; list.splice(i - 1, 0, x); redraw(); } }, "\u2191"),
      h("button", { class: "btn icon-btn", "aria-label": T.down, title: T.down, disabled: i === list.length - 1, onclick: function () { var x = list.splice(i, 1)[0]; list.splice(i + 1, 0, x); redraw(); } }, "\u2193")];
  }

  // ---- music

  function fmtTime(sec) { sec = Math.max(0, Math.round(sec || 0)); var m = Math.floor(sec / 60), s2 = sec % 60, hr = Math.floor(m / 60); return (hr ? hr + ":" + ("0" + (m % 60)).slice(-2) : m) + ":" + ("0" + s2).slice(-2); }

  function musicView() {
    var holder = h("div", null, pageHead(T.navMusic, T.musicIntro, h("button", { class: "btn", onclick: function () { load(); } }, ico("repeat"), T.refresh)));
    var body = h("div", null, "...");
    holder.appendChild(body);
    var openList = null, mod = S.info.level === "admin" || S.info.level === "mod";
    var section = S.info.sections.filter(function (x) { return x.key === "music"; })[0] || { fields: [], editable: false };
    function spec(path) { return section.fields.filter(function (f) { return f.path === path; })[0]; }
    function control(action, value) {
      return post("/music/control", { action: action, value: value }).then(function (x) {
        if (x.status === 200) toast((x.data && x.data.message) || T.saved);
        else toast((x.data && (x.data.message || x.data.error)) || T.failed, true);
        setTimeout(load, 600);
      });
    }
    function btn(icon, label, action, value) { return h("button", { class: "btn", onclick: function () { control(action, value); } }, ico(icon), label); }
    function load() {
      var q = openList ? "?playlist=" + encodeURIComponent(openList) : "";
      api("GET", "/api/guild/" + S.gid + "/music" + q).then(function (r) {
        if (r.status !== 200) return body.replaceChildren(note(reason(r)));
        draw(r.data);
      });
    }
    function draw(d) {
      var out = [], pl = d.player;
      var who = h("div", { class: "who-box" }, d.bot_avatar ? h("img", { class: "preview round", src: d.bot_avatar, alt: "" }) : h("span", { class: "avatar" }),
        h("div", null, h("b", null, d.bot_name), h("div", { class: "small" }, (d.second_bot ? T.secondBot : T.sameBot) + " | " + (d.online ? T.online : T.offline2))));
      var status = h("div", { class: "fields" }, simpleRow(T.playsAs, who));
      if (d.second_bot && d.online && !d.on_server && d.invite) status.appendChild(h("div", { class: "row" }, h("div", null, h("div", { class: "name" }, T.notOnServer)), h("div", { class: "ctl" }, h("a", { class: "btn primary", href: d.invite, target: "_blank", rel: "noopener noreferrer" }, T.invite))));
      if (!d.module_on) status.appendChild(h("div", { class: "row" }, h("div", null, h("div", { class: "name" }, T.musicOff)), h("div", { class: "ctl" }, plugin("music") ? pluginSwitch(plugin("music")) : null)));
      if (pl && pl.ready) status.appendChild(note(T.notReady + " " + pl.ready));
      if (pl) status.appendChild(note(pl.library + " " + T.inLibrary));
      out.push(collapsible(T.playsAs, null, status));
      if (pl) {
        var cur = pl.current;
        var nowBox = h("div", { class: "now" },
          h("div", { class: "now-art" }, ico("music")),
          h("div", { class: "now-text" }, h("div", { class: "small" }, T.nowPlaying + (pl.channel_name ? " | " + pl.channel_name : "")),
            h("b", null, cur ? cur.title : T.nothingPlaying), cur && cur.artist ? h("div", { class: "small" }, cur.artist) : null,
            cur ? h("div", { class: "small" }, fmtTime(pl.position) + " / " + (cur.length ? fmtTime(cur.length) : "stream") + (cur.detail ? " | " + cur.detail : "")) : null));
        var loop = h("select", { "aria-label": T.loopLabel, onchange: function (e) { control("loop", e.target.value); } }, [["off", T.loopOff], ["track", T.loopTrack], ["queue", T.loopQueue]].map(function (k) { return h("option", { value: k[0], selected: pl.loop === k[0] }, T.loopLabel + ": " + k[1]); }));
        var vol = h("input", { type: "range", min: 1, max: 150, value: pl.volume, "aria-label": T.volume, onchange: function (e) { control("volume", Number(e.target.value)); } });
        var ctl = h("div", { class: "actions" }, pl.paused ? btn("play", T.resume, "resume") : btn("pause", T.pause, "pause"), btn("skip", T.skip, "skip"), btn("stop", T.stop, "stop"), btn("shuffle", T.shuffle, "shuffle"), btn("door", T.leave, "leave"), loop, h("label", { class: "inline" }, T.volume, vol));
        var voices = S.info.channels.filter(function (c) { return c.kind === "voice"; });
        var chan = h("select", { "aria-label": T.voiceChannel }, voices.map(function (c) { return h("option", { value: c.id, selected: c.id === pl.channel }, c.name); }));
        var query = h("input", { type: "text", placeholder: T.addLabel, maxlength: 500, "aria-label": T.addLabel, class: "wide" });
        var folder = h("input", { type: "text", placeholder: T.folderHint, maxlength: 200, "aria-label": T.folderLabel });
        var listSel = h("select", { "aria-label": T.playlists }, (pl.playlists || []).map(function (x) { return h("option", { value: x.name }, x.name + " (" + x.count + ")"); }));
        var adds = h("div", { class: "fields" },
          simpleRow(T.voiceChannel, h("div", null, chan, h("button", { class: "btn primary", onclick: function () { control("join", chan.value); } }, T.join))),
          simpleRow(T.addLabel, h("div", null, query, h("button", { class: "btn", onclick: function () { if (query.value.trim()) control("add", query.value.trim()); } }, ico("plus"), T.add))),
          simpleRow(T.folderLabel, h("div", null, folder, h("button", { class: "btn", onclick: function () { if (folder.value.trim()) control("folder", folder.value.trim()); } }, ico("folder"), T.add))),
          (pl.playlists || []).length ? simpleRow(T.playlists, h("div", null, listSel, h("button", { class: "btn", onclick: function () { control("playlist", listSel.value); } }, ico("play"), T.play))) : null);
        var queue = h("div", { class: "fields" });
        if (!pl.queue.length) queue.appendChild(note(T.none));
        pl.queue.forEach(function (t, i) {
          queue.appendChild(h("div", { class: "row slim" }, h("div", null, h("div", { class: "name" }, (i + 1) + ". " + t.title), h("div", { class: "small" }, (t.artist || "") + (t.length ? " | " + fmtTime(t.length) : ""))),
            h("div", { class: "ctl" }, h("button", { class: "btn", onclick: function () { control("remove", i + 1); } }, T.remove))));
        });
        var player = h("div", null, nowBox, ctl, adds, h("div", { class: "group" }, T.queueTitle + " (" + pl.waiting + " " + T.waiting + ")"), queue,
          pl.queue.length ? h("div", { class: "actions" }, btn("list", T.clearQueue, "clear")) : null);
        if (!mod) lock(player, false);
        out.push(collapsible(T.nowPlaying, null, player));
      }
      out.push(collapsible(T.playlists, null, playlistBox(d, pl)));
      var stay = h("div", { class: "fields" });
      ["music.stay", "music.home_channel"].forEach(function (pth) { var f = spec(pth); if (f) stay.appendChild(fieldRow(f)); });
      var auto = spec("music.autoplay");
      if (auto) {
        var row = h("div", { class: "row" }), names = ((pl && pl.playlists) || d.playlists || []).map(function (x) { return x.name; });
        var sel = h("select", { "aria-label": T.autoplayLabel, onchange: function (e) { save("music.autoplay", e.target.value, row); } }, [h("option", { value: "" }, T.none)].concat(names.map(function (n) { return h("option", { value: n, selected: n === auto.value }, n); })));
        row.appendChild(h("div", null, h("div", { class: "name" }, L(auto.label)), h("div", { class: "help" }, L(auto.help))));
        row.appendChild(h("div", { class: "ctl" }, sel));
        stay.appendChild(row);
      }
      if (!section.editable) lock(stay, false);
      out.push(collapsible(T.stayTitle, null, stay));
      var src = h("div", { class: "fields" });
      ["music.youtube", "music.soundcloud", "music.spotify", "music.apple_music", "music.tidal", "music.search_source"].forEach(function (pth) { var f = spec(pth); if (f) src.appendChild(fieldRow(f)); });
      if (!section.editable) lock(src, false);
      out.push(collapsible(T.sourcesTitle, null, src));
      var guide = h("div", null, h("ol", { class: "steps" }, [T.guide1, T.guide2, T.guide3, T.guide4, T.guide5, T.guide6].map(function (x) { return h("li", null, x); })), h("p", { class: "risk" }, T.riskNote));
      out.push(collapsible(T.guideTitle, null, guide, d.second_bot && d.on_server));
      body.replaceChildren.apply(body, out);
    }
    function playlistBox(d, pl) {
      var box = h("div", { class: "fields" }), lists = (pl && pl.playlists) || d.playlists || [];
      if (d.playlist) {
        var p = d.playlist, tracks = p.tracks.slice(), name = p.name;
        var rename = textInput(name, function (v) { name = v; }, { maxlength: 40 });
        var listEl = h("div", { class: "fields" });
        function redraw() {
          listEl.textContent = "";
          if (!tracks.length) listEl.appendChild(note(T.playlistEmpty));
          tracks.forEach(function (t, i) {
            listEl.appendChild(h("div", { class: "row slim" }, h("div", null, h("div", { class: "name" }, (i + 1) + ". " + t.title), h("div", { class: "small" }, (t.artist || "") + (t.length ? " | " + fmtTime(t.length) : ""))),
              h("div", { class: "ctl" }, moveButtons(tracks, i, redraw), h("button", { class: "btn", onclick: function () { tracks.splice(i, 1); redraw(); } }, T.remove))));
          });
        }
        redraw();
        var addq = h("input", { type: "text", placeholder: T.addToList, maxlength: 500, "aria-label": T.addToList, class: "wide" });
        box.appendChild(h("div", { class: "actions" }, h("button", { class: "btn", onclick: function () { openList = null; load(); } }, T.back), rename,
          h("button", { class: "btn primary", onclick: function () { post("/music/playlist", { name: p.name, rename: name, tracks: tracks }).then(function (x) { if (done(x)) { openList = x.data.name; load(); } }); } }, T.save),
          h("button", { class: "btn", onclick: function () { control("playlist", p.name); } }, ico("play"), T.play)));
        box.appendChild(h("div", { class: "actions" }, addq, h("button", { class: "btn", onclick: function () {
          if (!addq.value.trim()) return;
          post("/music/playlist", { name: p.name, tracks: tracks, add: addq.value.trim() }).then(function (x) { if (done(x)) load(); });
        } }, ico("plus"), T.add)));
        box.appendChild(listEl);
      } else {
        if (!lists.length) box.appendChild(note(T.none));
        lists.forEach(function (x) {
          box.appendChild(h("div", { class: "row slim" }, h("div", null, h("div", { class: "name" }, x.name), h("div", { class: "small" }, x.count + " " + T.tracks)),
            h("div", { class: "ctl" }, h("button", { class: "btn", onclick: function () { control("playlist", x.name); } }, ico("play"), T.play),
              h("button", { class: "btn", onclick: function () { openList = x.name; load(); } }, T.open),
              h("button", { class: "btn", onclick: function () { if (confirm(T.surer)) post("/music/playlist", { name: x.name, "delete": true }).then(function (y) { if (done(y)) load(); }); } }, T.del))));
        });
        var newName = h("input", { type: "text", placeholder: T.newPlaylist, maxlength: 40, "aria-label": T.newPlaylist });
        box.appendChild(h("div", { class: "actions" }, newName,
          h("button", { class: "btn", onclick: function () { if (newName.value.trim()) post("/music/playlist", { name: newName.value.trim(), tracks: [] }).then(function (y) { if (done(y)) { openList = y.data.name; load(); } }); } }, ico("plus"), T.add),
          pl && (pl.current || pl.queue.length) ? h("button", { class: "btn", onclick: function () {
            var all = (pl.current ? [pl.current] : []).concat(pl.queue);
            if (newName.value.trim()) post("/music/playlist", { name: newName.value.trim(), tracks: all }).then(function (y) { if (done(y)) load(); });
            else toast(T.newPlaylist, true);
          } }, ico("save"), T.saveQueue) : null));
      }
      if (!mod) lock(box, false);
      return box;
    }
    load();
    S.timer = setInterval(function () { if (S.section === "music" && !openList && !document.hidden) load(); }, 15000);
    return holder;
  }

  window.addEventListener("hashchange", function () {
    var p = (location.hash || "").slice(1).split("/");
    if (S.info && p[0] === S.gid && p[1] && p[1] !== S.section) { S.section = p[1]; render(); }
  });
  boot();
})();
