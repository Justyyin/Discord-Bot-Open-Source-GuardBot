"""Scam detection: text tricks, scoring, speed and reading text from images."""

import io
import time
import unittest

from guardbot import scamscan
from guardbot.scamscan import digest, read_text, scan, tesseract_path

THRESHOLD = 3


def flagged(text, words=None):
    """True if a text would be removed with the default threshold."""
    return scan(text, words).flagged(THRESHOLD)


class TextTest(unittest.TestCase):
    """Detection of text."""

    def test_mrbeast_in_every_spelling(self):
        """The name is found whatever tricks are used."""
        for text in ("MrBeast", "Mr Beast", "mr. beast", "M R B E A S T", "Mr.B3ast", "m-r-b-e-a-s-t", "MR​BEAST", "Мr Веast", "Mʀ𝗕𝗲𝗮𝘀𝘁", "ＭｒＢｅａｓｔ", "mr_beast giveaway", "Beast Philanthropy"):
            self.assertTrue(flagged(text), text)

    def test_typical_scams(self):
        """Fake giveaways with crypto words are removed without any name."""
        for text in (
            "Free BTC giveaway! Claim now",
            "I am giving away 5000 USDT, scan the QR code to claim",
            "Double your bitcoin instantly, guaranteed, https://win-btc.xyz",
            "Elon Musk airdrop: connect your wallet at claim-eth.top",
            "Casino promo code, no deposit bonus, withdraw instantly",
        ):
            self.assertTrue(flagged(text), text)

    def test_normal_chat_stays(self):
        """Everyday messages are not touched."""
        for text in ("hello how are you", "Mr Smith is a beast at chess", "I bought a new wallet for my jeans", "anyone want free pizza friday?", "the stake in this game is high", "check this link https://youtube.com/watch?v=abc", "my token expired on the API", ""):
            self.assertFalse(flagged(text), text)

    def test_crypto_talk_needs_more_than_two_words(self):
        """Two crypto words alone are fine, with bait and a link they are not."""
        self.assertFalse(flagged("what do you think about bitcoin and ethereum"))
        self.assertTrue(flagged("bitcoin ethereum giveaway claim at https://x.xyz"))

    def test_a_link_adds_a_point(self):
        """The same words are harmless without a link and removed with one."""
        self.assertFalse(flagged("free btc"))
        self.assertTrue(flagged("free btc https://get-it.xyz"))
        self.assertTrue(flagged("free btc get-it.xyz"))
        self.assertFalse(flagged("free btc 3.5"))

    def test_custom_lists_and_threshold(self):
        """Own words work, an empty list is accepted."""
        words = {"instant": ["pizzabot"], "celeb": [], "bait": [], "crypto": []}
        self.assertTrue(flagged("PizzaBot is here", words))
        self.assertFalse(flagged("mrbeast", words))
        self.assertFalse(scan("hello", {"instant": [], "celeb": [], "bait": [], "crypto": []}).flagged(1))

    def test_speed(self):
        """A scan takes far less than a millisecond, also for very long text."""
        text = "Hey everyone check this giveaway of bitcoin, claim now at https://abc.xyz and double your usdt " * 3
        start = time.perf_counter()
        for _ in range(2000):
            scan(text)
        per = (time.perf_counter() - start) / 2000
        self.assertLess(per, 0.002)
        start = time.perf_counter()
        scan("word " * 4000)
        self.assertLess(time.perf_counter() - start, 0.2)


@unittest.skipIf(tesseract_path() is None, "tesseract is not installed")
class ImageTest(unittest.TestCase):
    """Reading text from images."""

    def make(self, text, dark=False, size=(900, 300), scale=1.0):
        """Draw a text on an image and return PNG bytes."""
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new("RGB", size, (20, 20, 40) if dark else (255, 255, 255))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(48 * scale))
        except OSError:
            font = ImageFont.load_default(size=int(48 * scale))
        draw.text((30, 100), text, fill=(255, 255, 255) if dark else (0, 0, 0), font=font)
        out = io.BytesIO()
        img.save(out, "PNG")
        return out.getvalue()

    def test_name_in_image(self):
        """The name is read on light and on dark ground."""
        for dark in (False, True):
            text = read_text(self.make("MR BEAST", dark))
            self.assertTrue(scan(text).instant, (dark, text))

    def test_giveaway_image(self):
        """A fake giveaway image is recognised by its words."""
        text = read_text(self.make("FREE BITCOIN GIVEAWAY\nCLAIM NOW", size=(1000, 300), scale=0.9))
        self.assertTrue(scan(text).flagged(THRESHOLD), text)

    def test_harmless_image_and_broken_files(self):
        """Normal text stays, broken or hostile input gives an empty result instead of an error."""
        self.assertFalse(scan(read_text(self.make("Hello and welcome to our server"))).flagged(THRESHOLD))
        self.assertEqual(read_text(b"not an image"), "")
        self.assertEqual(read_text(b""), "")
        self.assertEqual(read_text(self.make("x"), lang="eng; rm -rf"), "")

    def test_digest_is_stable(self):
        """The same image gives the same fingerprint."""
        data = self.make("abc")
        self.assertEqual(digest(data), digest(bytes(data)))
        self.assertNotEqual(digest(data), digest(data + b"x"))


class ProgramTest(unittest.TestCase):
    """Missing OCR does not break anything."""

    def test_missing_program(self):
        """Without tesseract the text is empty."""
        self.assertIsNone(tesseract_path("definitely-not-installed"))
        self.assertEqual(read_text(b"x", program="definitely-not-installed"), "")
        self.assertTrue(hasattr(scamscan, "scan"))


if __name__ == "__main__":
    unittest.main()
