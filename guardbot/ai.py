"""Connection to an AI provider with the key of the server owner.

The key is stored encrypted, one per server, and is only decrypted for a request. It is never logged, never shown and never part of an export. The bot only talks to the fixed addresses below, so a server cannot point it at other hosts.
"""

import asyncio
import logging
import os
import time
from pathlib import Path
from typing import Any, Optional

import aiohttp
from cryptography.fernet import Fernet, InvalidToken

log = logging.getLogger(__name__)

PROVIDERS: dict[str, dict[str, str]] = {
    "anthropic": {"url": "https://api.anthropic.com/v1/messages", "kind": "anthropic", "model": "claude-sonnet-5-5", "label": "Anthropic"},
    "openai": {"url": "https://api.openai.com/v1/chat/completions", "kind": "openai", "model": "gpt-5", "label": "OpenAI"},
    "kimi": {"url": "https://api.moonshot.ai/v1/chat/completions", "kind": "openai", "model": "kimi-k3", "label": "Kimi (Moonshot)"},
}
TIMEOUT = 60
MAX_PROMPT = 12000
MAX_ANSWER = 20000
CONCURRENT = 3


# Messages that are shown to people and can be translated, listed so the translation check finds them
TEXTS = (
    "The stored key cannot be read. Remove it and enter it again.",
    "That does not look like an API key.",
    "Unknown provider.",
    "The provider sent an answer in an unexpected format.",
    "The provider sent an empty answer.",
    "The provider refused the key. Check that it is valid and has credit.",
    "The provider does not know this model. Change it with /support ai setup.",
    "The provider says there were too many requests or the credit is used up.",
    "The provider has a problem right now. Try again later.",
    "The AI is not set up on this server. Use /support ai setup.",
    "The daily limit of AI requests for this server is reached.",
    "The provider did not answer in time.",
    "The provider could not be reached.",
)


class AIError(Exception):
    """A request failed. The message is safe to show: it never contains the key."""


class KeyBox:
    """Encrypts the keys of the servers with a secret that stays in the data directory."""

    def __init__(self, data_dir: Any):
        """Load or create the secret file."""
        self.path = Path(data_dir) / "ai.secret"
        if self.path.exists():
            raw = self.path.read_bytes().strip()
        else:
            raw = Fernet.generate_key()
            fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "wb") as fh:
                fh.write(raw)
        self.fernet = Fernet(raw)

    def seal(self, key: str) -> str:
        """Encrypt a key."""
        return self.fernet.encrypt(key.encode()).decode()

    def open(self, token: str) -> str:
        """Decrypt a key. Raises AIError if the secret file does not fit."""
        try:
            return self.fernet.decrypt(token.encode()).decode()
        except (InvalidToken, ValueError) as exc:
            raise AIError("The stored key cannot be read. Remove it and enter it again.") from exc


def clean_key(key: str) -> str:
    """The key without spaces and line breaks. Raises AIError when it cannot be a key."""
    key = "".join(key.split())
    if not 16 <= len(key) <= 300 or not key.isascii() or not key.isprintable():
        raise AIError("That does not look like an API key.")
    return key


def scrub(text: str, key: str) -> str:
    """Remove the key from a text before it is shown or logged."""
    return text.replace(key, "***") if key else text


def build_request(provider: str, key: str, model: str, system: str, prompt: str, max_tokens: int) -> tuple[str, dict, dict]:
    """The address, headers and body of one request."""
    info = PROVIDERS[provider]
    if info["kind"] == "anthropic":
        headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        body = {"model": model, "max_tokens": max_tokens, "system": system, "messages": [{"role": "user", "content": prompt}]}
    else:
        headers = {"Authorization": f"Bearer {key}", "content-type": "application/json"}
        limit = "max_completion_tokens" if provider == "openai" else "max_tokens"
        body = {"model": model, limit: max_tokens, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]}
    return info["url"], headers, body


def read_answer(provider: str, data: Any) -> str:
    """The text of an answer. Raises AIError when the answer has an unexpected shape."""
    try:
        if PROVIDERS[provider]["kind"] == "anthropic":
            text = "".join(part.get("text", "") for part in data["content"] if part.get("type") == "text")
        else:
            text = data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError, AttributeError) as exc:
        raise AIError("The provider sent an answer in an unexpected format.") from exc
    if not text.strip():
        raise AIError("The provider sent an empty answer.")
    return text[:MAX_ANSWER]


def error_text(status: int, data: Any, key: str = "") -> str:
    """A short, safe reason for a failed request."""
    if status in (401, 403):
        return "The provider refused the key. Check that it is valid and has credit."
    if status == 404:
        return "The provider does not know this model. Change it with /support ai setup."
    if status == 429:
        return "The provider says there were too many requests or the credit is used up."
    if status >= 500:
        return "The provider has a problem right now. Try again later."
    detail = ""
    if isinstance(data, dict):
        err = data.get("error")
        detail = str(err.get("message", "") if isinstance(err, dict) else err or "")[:200]
    return scrub(f"The provider rejected the request ({status}). {detail}".strip(), key)


class AI:
    """Asks the provider of a server, with daily and per person limits."""

    def __init__(self, bot: Any, session: Optional[aiohttp.ClientSession] = None):
        """Keep the bot; the HTTP session is the one of the bot unless given."""
        self.bot = bot
        self.box = KeyBox(bot.store.dir)
        self.session = session
        self.slots = asyncio.Semaphore(CONCURRENT)
        self.last: dict[tuple, float] = {}

    def conf(self, gid: int) -> dict:
        """The AI settings of a server."""
        return self.bot.cfg(gid)["ai"]

    def configured(self, gid: int) -> bool:
        """True if provider and key are set."""
        c = self.conf(gid)
        return bool(c["provider"] in PROVIDERS and c["key_enc"])

    def set_key(self, gid: int, provider: str, key: str, model: str = "") -> None:
        """Store a key for a server."""
        if provider not in PROVIDERS:
            raise AIError("Unknown provider.")
        c = self.conf(gid)
        c["provider"], c["model"] = provider, model.strip()[:80] or PROVIDERS[provider]["model"]
        c["key_enc"] = self.box.seal(clean_key(key))

    def remove_key(self, gid: int) -> None:
        """Delete the key and turn the AI off."""
        c = self.conf(gid)
        c["key_enc"] = ""
        c["second_opinion"] = False
        self.bot.cfg(gid)["modules"]["ai"] = False

    def budget(self, gid: int) -> tuple[int, int]:
        """Requests used today and the daily limit."""
        c = self.conf(gid)
        today = time.strftime("%Y-%m-%d", time.gmtime())
        if c["day"] != today:
            c["day"], c["used"] = today, 0
        return c["used"], c["daily_limit"]

    def check_person(self, gid: int, uid: int) -> None:
        """Raise AIError while a person must wait."""
        wait = self.conf(gid)["user_cooldown"]
        now = time.time()
        if now - self.last.get((gid, uid), 0) < wait:
            raise AIError(f"Please wait {wait} seconds between requests.")
        self.last[(gid, uid)] = now
        if len(self.last) > 2000:
            self.last = {k: t for k, t in self.last.items() if now - t < 3600}

    async def ask(self, gid: int, system: str, prompt: str, uid: Optional[int] = None, max_tokens: Optional[int] = None) -> str:
        """Send a prompt and return the answer text. Raises AIError with a safe message."""
        c = self.conf(gid)
        if not self.bot.module_on(gid, "ai") or not self.configured(gid):
            raise AIError("The AI is not set up on this server. Use /support ai setup.")
        used, limit = self.budget(gid)
        if used >= limit:
            raise AIError("The daily limit of AI requests for this server is reached.")
        if uid is not None:
            self.check_person(gid, uid)
        key = self.box.open(c["key_enc"])
        url, headers, body = build_request(c["provider"], key, c["model"], system[:MAX_PROMPT], prompt[:MAX_PROMPT], min(max_tokens or c["max_tokens"], 4000))
        c["used"] += 1
        session = self.session or self.bot.session
        try:
            async with self.slots:
                async with session.post(url, headers=headers, json=body, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
                    try:
                        data = await resp.json(content_type=None)
                    except (aiohttp.ContentTypeError, ValueError):
                        data = None
                    if resp.status != 200:
                        c["errors"] += 1
                        raise AIError(error_text(resp.status, data, key))
        except asyncio.TimeoutError as exc:
            c["errors"] += 1
            raise AIError("The provider did not answer in time.") from exc
        except aiohttp.ClientError as exc:
            c["errors"] += 1
            raise AIError("The provider could not be reached.") from exc
        return read_answer(c["provider"], data)
