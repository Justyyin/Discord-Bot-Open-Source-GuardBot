"""Images drawn with Pillow: rank cards and captchas."""

import io
import logging
import random

try:
    from PIL import Image, ImageDraw, ImageFont

    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

log = logging.getLogger(__name__)

CAPTCHA_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
FONT_FILES = ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf", "arialbd.ttf", "arial.ttf", "Arial.ttf")


def font(size):
    """Load a TrueType font if one is installed, otherwise the built-in font."""
    for name in FONT_FILES:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def circle(img, size):
    """Crop an image to a circle with a transparent background."""
    img = img.convert("RGBA").resize((size, size))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    img.putalpha(mask)
    return img


def rank_card(name, avatar, level, rank, cur, span, total, maxed):
    """Draw the rank card and return it as PNG bytes."""
    w, h = 800, 230
    img = Image.new("RGB", (w, h), (30, 32, 38))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((10, 10, w - 10, h - 10), radius=22, fill=(43, 45, 52))
    try:
        av = circle(Image.open(io.BytesIO(avatar)), 150)
    except (OSError, ValueError) as exc:
        log.warning("avatar could not be decoded for the rank card: %s", exc)
        av = circle(Image.new("RGB", (150, 150), (88, 101, 242)), 150)
    img.paste(av, (40, 40), av)
    d.text((220, 38), name[:24], font=font(36), fill=(255, 255, 255))
    d.text((220, 90), f"Level {level}", font=font(28), fill=(200, 205, 255))
    d.text((430, 90), f"Rank #{rank}", font=font(28), fill=(200, 205, 255))
    d.rounded_rectangle((220, 145, 760, 175), radius=15, fill=(70, 73, 82))
    ratio = 1.0 if maxed else (cur / span if span else 0)
    if ratio > 0:
        d.rounded_rectangle((220, 145, 220 + max(30, int(540 * ratio)), 175), radius=15, fill=(88, 101, 242))
    label = "MAX" if maxed else f"{cur} / {span} XP"
    d.text((220, 182), f"{label}    total {total} XP", font=font(20), fill=(180, 184, 195))
    d.text((590, 200), "GuardBot \u00a9 Justyn", font=font(14), fill=(110, 114, 125))
    out = io.BytesIO()
    img.save(out, "PNG")
    return out.getvalue()


def captcha(text):
    """Draw a captcha image for a code and return it as PNG bytes."""
    w, h = 280, 110
    img = Image.new("RGB", (w, h), (238, 238, 242))
    d = ImageDraw.Draw(img)
    for _ in range(7):
        d.line([(random.randint(0, w), random.randint(0, h)), (random.randint(0, w), random.randint(0, h))], fill=(random.randint(90, 180),) * 3, width=2)
    f = font(54)
    x = 18
    for ch in text:
        tile = Image.new("RGBA", (60, 80), (0, 0, 0, 0))
        ImageDraw.Draw(tile).text((8, 6), ch, font=f, fill=(random.randint(10, 90), random.randint(10, 90), random.randint(10, 90), 255))
        tile = tile.rotate(random.randint(-22, 22), expand=False, resample=Image.BICUBIC)
        img.paste(tile, (x, random.randint(8, 22)), tile)
        x += 48
    for _ in range(220):
        d.point((random.randint(0, w - 1), random.randint(0, h - 1)), fill=(random.randint(60, 200),) * 3)
    out = io.BytesIO()
    img.save(out, "PNG")
    return out.getvalue()


def new_code(n=5):
    """Create a random code without easily confused characters."""
    return "".join(random.choice(CAPTCHA_CHARS) for _ in range(n))
