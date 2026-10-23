"use strict";
(function () {
  var TEXT = {
    en: { signin: "Sign in with Discord", intro: "Manage your GuardBot servers.", offline: "The bot is not connected right now. Try again in a moment.", server: "Server", overview: "Overview", members: "Members", cases: "Cases", modules: "Modules on", latency: "Latency", search: "Search settings", setupTitle: "Setup status", setupOpen: "On, not set up yet", setupDone: "On and set up", setupNone: "On, needs no setup", setupOff: "Off", chartsTitle: "Last 30 days", chMessages: "Messages per day", chJoins: "Joins", chLeaves: "Leaves", chCases: "Moderation cases per day", chTypes: "Cases by type", noData: "No data yet. Turn on the activity module to count messages.", searchAll: "Search all settings", noMatch: "No setting matches.", saved: "Saved", failed: "Could not save", none: "None", logout: "Log out", general: "General", modulesTitle: "Modules", moderation: "Moderation cases", backup: "Backup", export: "Download settings", import: "Import settings", importNote: "Importing replaces the settings of this server with the file. Counters, open tickets and other running data are kept.", imported: "Settings imported", noServers: "You do not manage any server where the bot is connected.", nocases: "No cases yet.", user: "User", type: "Type", reason: "Reason", moderator: "Moderator", when: "When", lines: "One entry per line", sections: "Settings", loginHelp: "Only members with the Manage Server permission can sign in, and only for servers the bot is connected to.", sure: "Replace all settings with this file?", about: "Version", readOnly: "You can read this page but not change it. Ask an administrator for more access.", adminOnly: "Only administrators can download or import settings." },
    de: { signin: "Mit Discord anmelden", intro: "Verwalte deine GuardBot-Server.", offline: "Der Bot ist gerade nicht verbunden. Versuche es gleich noch einmal.", server: "Server", overview: "Übersicht", members: "Mitglieder", cases: "Fälle", modules: "Module aktiv", latency: "Latenz", search: "Einstellungen suchen", setupTitle: "Einrichtungsstatus", setupOpen: "An, noch nicht eingerichtet", setupDone: "An und eingerichtet", setupNone: "An, braucht keine Einrichtung", setupOff: "Aus", chartsTitle: "Letzte 30 Tage", chMessages: "Nachrichten pro Tag", chJoins: "Beitritte", chLeaves: "Austritte", chCases: "Moderationsfälle pro Tag", chTypes: "Fälle nach Art", noData: "Noch keine Daten. Schalte das Aktivitätsmodul ein, um Nachrichten zu zählen.", searchAll: "Alle Einstellungen durchsuchen", noMatch: "Keine Einstellung gefunden.", saved: "Gespeichert", failed: "Speichern fehlgeschlagen", none: "Keine", logout: "Abmelden", general: "Allgemein", modulesTitle: "Module", moderation: "Moderationsfälle", backup: "Sicherung", export: "Einstellungen herunterladen", import: "Einstellungen importieren", importNote: "Der Import ersetzt die Einstellungen dieses Servers durch die Datei. Zähler, offene Tickets und andere laufende Daten bleiben erhalten.", imported: "Einstellungen importiert", noServers: "Du verwaltest keinen Server, auf dem der Bot verbunden ist.", nocases: "Noch keine Fälle.", user: "Nutzer", type: "Art", reason: "Grund", moderator: "Moderator", when: "Wann", lines: "Ein Eintrag pro Zeile", sections: "Einstellungen", loginHelp: "Nur Mitglieder mit der Berechtigung Server verwalten können sich anmelden, und nur für Server, auf denen der Bot verbunden ist.", sure: "Alle Einstellungen durch diese Datei ersetzen?", about: "Version", readOnly: "Du kannst diese Seite lesen, aber nicht ändern. Frage einen Administrator nach mehr Rechten.", adminOnly: "Nur Administratoren können Einstellungen herunterladen oder importieren." }
  };
  TEXT.en.cat = { "Basics": "Basics", "Moderation": "Moderation", "Security": "Security", "Community": "Community", "Structure and team": "Structure and team", "More": "More" };
  TEXT.de.cat = { "Basics": "Grundlagen", "Moderation": "Moderation", "Security": "Sicherheit", "Community": "Community", "Structure and team": "Struktur und Team", "More": "Weitere" };
  var lang = (navigator.language || "en").slice(0, 2);
  var T = TEXT[lang] || TEXT.en;
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
      h("p", { class: "small" }, T.loginHelp))));
  }

  function boot() {
    api("GET", "/api/me").then(function (r) {
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
      render();
    });
  }

  function go(section) { S.section = section; S.query = ""; location.hash = S.gid + "/" + section; render(); }

  function navLink(key, text, count) {
    return h("a", { class: S.section === key ? "on" : "", onclick: function () { go(key); } }, text, count !== undefined ? h("span", { class: "count" }, count) : null);
  }

  function shell(main) {
    var side = h("aside", { class: "side" },
      h("div", { class: "brand" }, icon(), "GuardBot", h("span", { class: "beta" }, "beta")),
      h("div", { class: "picker" }, h("select", { "aria-label": T.server, onchange: function (e) { openGuild(e.target.value); } },
        S.guilds.map(function (g) { return h("option", { value: g.id, selected: g.id === S.gid }, g.name); }))));
    if (S.info) {
      var nav = h("nav", { class: "nav" },
        navLink("overview", T.overview), navLink("cases", T.moderation), navLink("backup", T.backup),
        h("div", { class: "nav-title" }, T.sections));
      var cat = null;
      S.info.sections.slice().sort(function (a, b) { return (a.category || "").localeCompare(b.category || ""); }).forEach(function (s) {
        if (s.category !== cat) { cat = s.category; nav.appendChild(h("div", { class: "nav-title" }, T.cat[cat] || cat)); }
        nav.appendChild(navLink("s:" + s.key, s.title, s.fields.length));
      });
      side.appendChild(nav);
    }
    side.appendChild(h("div", { class: "spacer" }));
    if (S.user) side.appendChild(h("div", { class: "me" },
      S.user.avatar ? h("img", { src: S.user.avatar, alt: "" }) : h("span", { class: "avatar" }),
      h("span", null, S.user.name),
      h("button", { class: "link", onclick: logout }, T.logout)));
    app.replaceChildren(h("div", { class: "shell" }, side, h("main", { class: "main" }, main)));
  }

  function logout() { api("POST", "/api/logout", {}).then(function () { location.hash = ""; location.reload(); }); }

  function render() {
    var info = S.info, sec = S.section, main;
    if (sec === "overview") main = overview();
    else if (sec === "cases") main = casesView();
    else if (sec === "backup") main = backupView();
    else {
      var s = info.sections.filter(function (x) { return "s:" + x.key === sec; })[0];
      main = s ? settingsView(s) : overview();
    }
    shell(main);
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
          if (n >= 30 || (f.label + " " + f.path + " " + (f.group || "")).toLowerCase().indexOf(q) === -1) return;
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
      h("div", { class: "group" }, T.modulesTitle), fieldsBox(i.sections.filter(function (s) { return s.key === "modules"; })[0].fields.slice(0, 8), i.level === "admin"),
      h("div", { class: "group" }, T.setupTitle), setup,
      h("div", { class: "group" }, T.chartsTitle), charts,
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
    return !q || (f.label + " " + f.path + " " + (f.group || "")).toLowerCase().indexOf(q) !== -1;
  }
  function filter() {
    document.querySelectorAll("[data-find]").forEach(function (row) { row.hidden = S.query.trim() !== "" && row.getAttribute("data-find").indexOf(S.query.trim().toLowerCase()) === -1; });
  }

  function settingsView(section) {
    var box = h("div", null, top(section.title, true)), group = null, cur = null;
    var about = lang === "de" ? section.info_de : section.info;
    if (about) box.appendChild(h("p", { class: "note flat" }, about));
    section.fields.forEach(function (f) {
      var g = f.group || "";
      if (g !== group || !cur) {
        group = g;
        if (g) box.appendChild(h("div", { class: "group" }, g));
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
    if (t === "choice") return h("select", { "aria-label": f.label, onchange: function (e) { save(f.path, e.target.value, row); } }, f.choices.map(function (c) { return h("option", { value: c[0], selected: c[0] === v }, c[1]); }));
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

  function fieldRow(f) {
    var row = h("div", { class: "row", "data-find": (f.label + " " + f.path + " " + (f.group || "")).toLowerCase() });
    row.appendChild(h("div", null, h("div", { class: "name" }, f.label)));
    row.appendChild(h("div", { class: "ctl" }, control(f, row)));
    return row;
  }

  function casesView() {
    var holder = h("div", null, top(T.moderation));
    var box = h("div", { class: "fields" }, h("div", { class: "empty" }, "..."));
    holder.appendChild(box);
    api("GET", "/api/guild/" + S.gid + "/moderation cases").then(function (r) {
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

  window.addEventListener("hashchange", function () {
    var p = (location.hash || "").slice(1).split("/");
    if (S.info && p[0] === S.gid && p[1] && p[1] !== S.section) { S.section = p[1]; render(); }
  });
  boot();
})();
