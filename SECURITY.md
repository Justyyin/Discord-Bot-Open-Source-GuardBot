# Security

Please do not report security problems in public issues.

Send a private message on Discord to justyyin with a short description and steps to reproduce.

If your bot token was exposed, reset it immediately in the Discord Developer Portal.

## What the bot does with the network

All of this was reviewed by the author of the code, not by an independent party. Treat it as a careful self-review.

- Links that members post (short link resolution, music, feeds) are only opened when the scheme is http or https, the port is a normal web port and every address the name resolves to is public. The connection itself uses a resolver that drops private, loopback, link-local and metadata addresses, so a name that changes its answer between check and use cannot reach them. Redirects are followed by hand and every step is checked again.
- Downloads are limited in size and time. Feeds are capped at 1 MB and refused when they contain a document type declaration or entity definitions.
- Music links are handled by yt-dlp and ffmpeg, which do their own name lookups. The bot checks the address first, restricts ffmpeg to web protocols and limits file sizes and playlist length, but a hostile site could still try to redirect yt-dlp. If that matters on your server, set `"music_generic": false` in `settings.json` so only the supported sites are used, or leave the music module switched off.
- A settings file that is imported is size limited and checked against the expected types before anything is applied. Loops that use stored data skip entries with the wrong shape.
- The status page (`health_port`) is off by default, listens on 127.0.0.1 and shows only counts. Do not expose it to the internet without a reverse proxy.
- Backups of the database in `data/dbbackups/` contain all stored data. Keep that folder private.
- Role menus and the shop never hand out roles with dangerous permissions, and the check is repeated at the moment of the click.

## Dashboard

The dashboard is off by default and runs inside the bot process. It was reviewed by the author, not by an independent party.

- Login uses Discord OAuth2 with the scope `identify`. The access token is revoked right after the user is read and is never stored. The `state` value is also kept in a cookie, so a forged login is refused.
- Access is decided by the bot's own view of the server on every request: the user must be the owner or have Administrator or Manage Server, and the bot must be connected and on that server. Losing the permission ends access at once, an offline bot ends everything.
- By default the server listens on 127.0.0.1. A non-loopback address is refused unless `public_url` is an https address (or `allow_insecure_http` is set on purpose, for example inside Docker with a port published only on 127.0.0.1).
- The Host header must match the configured address (against DNS rebinding), every change needs the session's CSRF token and a matching Origin, cookies are HttpOnly, SameSite=Lax and use the `__Host-` prefix under HTTPS, and responses carry a strict Content Security Policy (no inline scripts or styles), X-Frame-Options, no-store and nosniff.
- Requests are rate limited per address and bodies are limited to 256 KB. Behind a reverse proxy set `trust_proxy` so the rate limit sees the real address, and do not set it without a proxy.
- Only settings of simple types can be edited. Values are checked against the type of the setting, Discord IDs must exist on the server, and internal state (counters, tickets, stored items) is not editable. Every change is logged to the security log channel.
- Sessions live in memory for 8 hours. Anyone who can read the process memory or the `.env` file can act as the bot, so protect the machine as you would the bot token. The client secret is as sensitive as the token.
- What is not covered: there is no two-factor step of its own beyond Discord, and a compromised account of a server manager can change that server's settings, as it could with commands.

## Updates

The update function downloads and installs code, so it deserves the most care. It was reviewed by the author, not by an independent party.

- It only talks to GitHub: the release is read from `api.github.com`, and every download address and every redirect must be https on a GitHub host. The connection uses the resolver that drops private addresses.
- Only the repository from `update.repo` (or `__repository__`) is used. You trust that repository the way you trust any software you run, so set it only to a repository you trust. A release is only used when its tag is a higher version than the running one, the archive contains `main.py` and `guardbot/__init__.py`, and the version inside the archive equals the tag.
- When the release has a `.zip.sha256` file the download must match it. Set `update.require_checksum` to `true` to refuse releases without one. Without a checksum file the integrity rests on GitHub and HTTPS alone.
- The archive is checked before anything is written: no absolute paths, no `..`, no backslashes or drive letters, no links, limits for size and number of files. `.env`, `settings.json`, `data`, `music` and virtual environments are never written.
- Replaced files are saved in `data/update` first. New packages are installed with pip when `requirements.txt` changed, then the new code is imported in a fresh process. If anything fails the old files are restored.
- Installation is started only by the owner of the bot (`/server debug update`) or by `update.auto_install`, which is off by default. It is never done inside a container.
- Update and download notices go to the owner of the bot by direct message.

## Message builder

`/post message` reads JSON from text, a file up to 100 KB or an https link. Links that redirect are refused, private addresses are refused, and only http and https links are accepted inside the message. Unknown keys are dropped, only link buttons are created, mentions never ping, and the length limits of Discord are checked before anything is sent.

## Approval, history and dashboard roles

- Four-eyes approval: the person who asks cannot decide the request. A second moderator needs the permission of the action itself. Requests expire after the configured minutes. Only the owner of the bot or server can bypass it, and only when `owner_bypass` is on.
- Settings history: the name of the person is a guess from the latest commands and dashboard writes on the server and is shown as such. Rollback and copy to another server need the manage-server right on both servers, and copy starts as a dry run.
- Dashboard roles: `viewer` can read, `mod` can change a small list of sections, everything else needs the manage-server right. The levels are checked on the server for every request, not only in the page.
- Role templates never give a permission the applying person does not have. Commands inside groups lose Discord's own visibility setting, the bot checks permissions on every call.
