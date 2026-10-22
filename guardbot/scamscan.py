"""Fast scam detection for text and images: normalising, scoring and optional OCR with Tesseract.

The text part is pure Python with pre-compiled patterns and needs well under a millisecond per message.
OCR runs in a worker thread, so the bot keeps answering while an image is read.
"""

import hashlib
import io
import re
import shutil
import subprocess
import unicodedata
from functools import lru_cache

DEFAULT_WORDS = {
    # Names that are removed on sight, even alone. Spaces and punctuation inside the text are ignored for these.
    "instant": ["mrbeast", "beast philanthropy"],
    # People and brands that scammers pretend to be.
    "celeb": ["elon", "musk", "spacex", "vitalik", "buterin", "binance", "coinbase", "mark cuban", "jimmy donaldson"],
    # Words that promise something.
    "bait": [
        "giveaway", "giving away", "airdrop", "claim", "free", "bonus", "promo", "promo code", "prize", "winner", "double your", "triple your",
        "limited time", "hurry", "instantly", "guaranteed", "first 100", "first 1000", "withdraw", "no deposit", "100%", "scan the qr", "qr code",
        "click the link", "check my bio", "link in bio", "dm me", "reward", "get rich", "passive income", "investment",
    ],
    # Money and crypto words.
    "crypto": [
        "crypto", "bitcoin", "btc", "eth", "ethereum", "usdt", "usdc", "tether", "solana", "dogecoin", "bnb", "xrp", "wallet", "metamask",
        "trustwallet", "seed phrase", "nft", "token", "casino", "stake", "betting", "gambling", "forex", "trading signals",
    ],
}
CATEGORIES = tuple(DEFAULT_WORDS)

ZERO_WIDTH = dict.fromkeys(map(ord, "​‌‍‎‏⁠﻿­"))
# Letters from other alphabets that look like Latin letters.
HOMOGLYPHS = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x", "у": "y", "к": "k", "м": "m", "т": "t", "в": "b", "н": "h", "і": "i", "ѕ": "s", "ј": "j", "ʀ": "r", "ʙ": "b", "ᴇ": "e", "ᴀ": "a", "ꜱ": "s", "ᴛ": "t", "ɴ": "n", "ᴍ": "m", "ᴏ": "o", "ɪ": "i", "ᴜ": "u", "ʟ": "l", "ᴅ": "d", "ɢ": "g", "ᴋ": "k", "ᴘ": "p", "ʏ": "y",
    "α": "a", "ε": "e", "ο": "o", "ρ": "p", "ι": "i", "κ": "k", "μ": "m", "τ": "t", "β": "b", "ν": "v", "χ": "x",
})
LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s", "!": "i", "|": "i"})
SPLIT = re.compile(r"[^a-z0-9$€£%@!|]+")
URL = re.compile(r"https?://|www\.|\b[a-z0-9-]+\.(?:com|net|org|io|xyz|gg|app|live|top|site|online|vip|fun|club|shop)\b")
MONEY = re.compile(r"[$€£]\s?\d{3,}|\d[\d,. ]{2,}\s?(?:usd|eur|usdt|btc|eth|dollars?|euros?)\b")


def normalize(text):
    """Return (spaced, leet, compact): lower case words, the same with digit and symbol tricks undone, and the leet text without any spaces."""
    t = unicodedata.normalize("NFKD", text or "").translate(ZERO_WIDTH)
    t = "".join(ch for ch in t if not unicodedata.combining(ch)).casefold().translate(HOMOGLYPHS)
    spaced = SPLIT.sub(" ", t).strip()
    leet = SPLIT.sub(" ", t.translate(LEET)).strip()
    return spaced, leet, leet.replace(" ", "")


@lru_cache(maxsize=64)
def pattern(words):
    """Compile one pattern for a tuple of words and phrases."""
    parts = []
    for w in sorted({x.strip().lower() for x in words if x.strip()}, key=len, reverse=True):
        norm = SPLIT.sub(" ", w).strip()
        if norm:
            parts.append(r"\s+".join(re.escape(p) for p in norm.split()))
    if not parts:
        return None
    return re.compile(r"(?<![a-z0-9])(?:" + "|".join(parts) + r")(?![a-z0-9])")


def squash(word):
    """A phrase without spaces and punctuation, as it is looked up in the compact text."""
    return normalize(word)[2]


class Verdict:
    """Result of a scan."""

    def __init__(self, points=0, hits=(), instant=False):
        """Store the points, the matched words and whether a name on the instant list was found."""
        self.points, self.hits, self.instant = points, list(hits), instant

    def flagged(self, threshold):
        """True if the text should be removed."""
        return self.instant or self.points >= threshold

    def reason(self):
        """A short explanation for the log."""
        return ("name on the instant list: " if self.instant else f"{self.points} points: ") + ", ".join(self.hits[:8])


def scan(text, words=None):
    """Score a text. Names on the instant list count at once, other words one point per different word and kind."""
    words = words or DEFAULT_WORDS
    spaced, leet, compact = normalize(text)
    if not compact:
        return Verdict()
    for term in words.get("instant", ()):
        sq = squash(term)
        if sq and sq in compact:
            return Verdict(99, [term], True)
    hits = set()
    for kind in ("celeb", "bait", "crypto"):
        rx = pattern(tuple(words.get(kind, ())))
        if rx:
            for source in (spaced, leet):
                hits.update(f"{kind}:{m}" for m in rx.findall(source))
    # a word counts once even if it was found in both versions of the text
    points = len({h for h in hits})
    if URL.search((text or "").casefold()) or "qr" in spaced.split():
        hits.add("link")
        points += 1
    if MONEY.search(text.casefold() if text else ""):
        hits.add("amount")
        points += 1
    return Verdict(points, sorted(hits))


def text_key(text):
    """Fingerprint of a longer text with spaces, case and tricks removed, so a copied scam text is found again. Short texts give None."""
    compact = normalize(text)[2]
    return hashlib.sha256(compact.encode()).hexdigest()[:32] if len(compact) >= 20 else None


def digest(data):
    """Short fingerprint of an image, used to remember images that were already judged."""
    return hashlib.sha256(data).hexdigest()[:32]


def tesseract_path(configured=None):
    """Path of the tesseract program, or None when it is not installed."""
    return shutil.which(configured or "tesseract")


def _prepare(data, invert=False):
    """Make an image easier to read for OCR: grey, scaled to a useful size, high contrast. Returns PNG bytes or None for unusable images."""
    from PIL import Image, ImageOps

    with Image.open(io.BytesIO(data)) as img:
        if img.width * img.height > 40_000_000:
            return None
        img.seek(0)
        img = ImageOps.autocontrast(img.convert("L"))
        if invert:
            img = ImageOps.invert(img)
        longest = max(img.size)
        if longest > 1800:
            img.thumbnail((1800, 1800))
        elif longest < 700:
            img = img.resize((img.width * 2, img.height * 2))
        out = io.BytesIO()
        img.save(out, "PNG")
        return out.getvalue()


def read_text(data, lang="eng", program=None, timeout=10):
    """Read the text in an image with Tesseract. Light text on dark ground is tried as a second pass when the first finds almost nothing."""
    exe = tesseract_path(program)
    if exe is None or not re.fullmatch(r"[a-z_+]{3,30}", lang):
        return ""
    text = ""
    for invert in (False, True):
        try:
            png = _prepare(data, invert)
        except (OSError, ValueError, SyntaxError):
            return ""
        if png is None:
            return ""
        try:
            run = subprocess.run([exe, "stdin", "stdout", "-l", lang, "--psm", "11"], input=png, capture_output=True, timeout=timeout, check=False)
        except (subprocess.TimeoutExpired, OSError):
            return text
        out = run.stdout.decode("utf-8", "replace")
        text += "\n" + out
        if len(re.sub(r"\W", "", out)) >= 12:
            break
    return text.strip()
