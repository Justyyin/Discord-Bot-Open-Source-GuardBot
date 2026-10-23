"""Detection helpers of AutoMod: personal data, card and IBAN checks, host and word matching. Pure functions, no Discord objects."""

import re

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE_RE = re.compile(r"(?<![\w/])(?:\+\d{1,3}|\(?0\d{1,4}\)?)[\s./-]?\d{2,5}(?:[\s./-]?\d{2,6}){1,3}(?!\w)")
IP_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){2,7}(?:\s?[A-Z0-9]{1,4})?\b")
CARD_RE = re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")


def luhn(num: str) -> bool:
    """Check a digit string with the Luhn algorithm used by card numbers."""
    total, flip = 0, False
    for ch in reversed(num):
        d = int(ch)
        if flip:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
        flip = not flip
    return total % 10 == 0


def iban_ok(s: str) -> bool:
    """Check an IBAN with the mod 97 test."""
    s = s.replace(" ", "").upper()
    if not 15 <= len(s) <= 34:
        return False
    moved = s[4:] + s[:4]
    return int("".join(str(int(c, 36)) for c in moved)) % 97 == 1


def find_pii(text: str, opts: dict) -> list[str]:
    """Return the kinds of personal data found in a text, limited to the enabled options."""
    found: list[str] = []
    if opts["email"] and EMAIL_RE.search(text):
        found.append("email address")
    iban = opts["iban"] and any(iban_ok(m.group()) for m in IBAN_RE.finditer(text.upper()))
    if iban:
        found.append("IBAN")
    if opts["ip"] and any(all(int(p) <= 255 for p in m.group().split(".")) for m in IP_RE.finditer(text)):
        found.append("IP address")
    if iban:
        return found
    if opts["card"]:
        for m in CARD_RE.finditer(text):
            d = re.sub(r"\D", "", m.group())
            if 13 <= len(d) <= 19 and luhn(d) and len(set(d)) > 1:
                found.append("card number")
                break
    if "card number" not in found and opts["phone"] and any(9 <= len(re.sub(r"\D", "", m.group())) <= 15 for m in PHONE_RE.finditer(text)):
        found.append("phone number")
    return found


def host_match(host: str, domain: str) -> bool:
    """True if a host is the domain itself or one of its subdomains."""
    return host == domain or host.endswith("." + domain)


def word_in(text: str, word: str) -> bool:
    """True if a word appears in a text as a whole word."""
    return re.search(r"(?<!\w)" + re.escape(word.lower()) + r"(?!\w)", text) is not None
