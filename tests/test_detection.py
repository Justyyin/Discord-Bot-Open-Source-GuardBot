"""Pure helper functions: personal data detection, hosts, durations, levels."""

import unittest

import discord

from guardbot.detect import find_pii, host_match, iban_ok, luhn, word_in
from guardbot.cogs.community.birthday import next_date
from guardbot.cogs.community.leveling import TOTALS, level_of
from guardbot.cogs.community.roles import ekey, parse_msg
from guardbot.utils import bulk, fmt_duration, hosts, parse_duration, trim

ALL = {"email": True, "phone": True, "ip": True, "iban": True, "card": True}


class PiiTest(unittest.TestCase):
    def test_email(self):
        self.assertEqual(find_pii("write to a.b@example.com", ALL), ["email address"])

    def test_iban(self):
        self.assertEqual(find_pii("DE89 3704 0044 0532 0130 00", ALL), ["IBAN"])
        self.assertFalse(iban_ok("DE00 3704 0044 0532 0130 00"))

    def test_card(self):
        self.assertTrue(luhn("4111111111111111"))
        self.assertFalse(luhn("4111111111111112"))
        self.assertIn("card number", find_pii("4111 1111 1111 1111", ALL))

    def test_ip_needs_valid_octets(self):
        self.assertEqual(find_pii("host 192.168.1.20", ALL), ["IP address"])
        self.assertEqual(find_pii("version 999.1.1.1", ALL), [])

    def test_phone(self):
        self.assertEqual(find_pii("call 0151 1234567", ALL), ["phone number"])

    def test_plain_text_is_clean(self):
        self.assertEqual(find_pii("hello world, see you at 2024-10-19", ALL), [])

    def test_options_can_disable_detection(self):
        self.assertEqual(find_pii("a@b.de", {**ALL, "email": False}), [])


class HostTest(unittest.TestCase):
    def test_hosts(self):
        self.assertEqual(hosts("see discord.gg/abc and https://Evil.com/x?y=1 www.test.org"), ["discord.gg", "evil.com", "www.test.org"])

    def test_host_match(self):
        self.assertTrue(host_match("a.discord.com", "discord.com"))
        self.assertFalse(host_match("discord.com.evil.io", "discord.com"))

    def test_word_in(self):
        self.assertTrue(word_in("this is bad.", "bad"))
        self.assertFalse(word_in("badge", "bad"))


class TextTest(unittest.TestCase):
    def test_duration(self):
        self.assertEqual(parse_duration("30m"), 1800)
        self.assertEqual(parse_duration("2h"), 7200)
        self.assertEqual(parse_duration("1d"), 86400)
        self.assertEqual(parse_duration("10"), 600)
        self.assertIsNone(parse_duration("soon"))
        self.assertEqual(fmt_duration(7200), "2h")

    def test_trim(self):
        self.assertEqual(trim(""), "-")
        self.assertEqual(len(trim("x" * 50, 10)), 10)

    def test_message_link(self):
        self.assertEqual(parse_msg(None, "https://discord.com/channels/1/2/3", None), (2, 3))
        self.assertIsNone(parse_msg(None, "nonsense", None))

    def test_emoji_key(self):
        self.assertEqual(ekey(discord.PartialEmoji.from_str("\u2764\ufe0f")), "\u2764")
        self.assertEqual(ekey(discord.PartialEmoji.from_str("<:x:123456789012345678>")), "123456789012345678")

    def test_leap_day_birthday(self):
        from datetime import date

        self.assertEqual(next_date(2, 29, date(2027, 1, 1)), date(2027, 2, 28))
        self.assertEqual(next_date(3, 14, date(2027, 3, 15)), date(2028, 3, 14))


class LevelTest(unittest.TestCase):
    def test_curve(self):
        self.assertEqual(TOTALS[1], 100)
        self.assertEqual(level_of(0), 0)
        self.assertEqual(level_of(99), 0)
        self.assertEqual(level_of(100), 1)
        self.assertEqual(level_of(TOTALS[100]), 100)
        self.assertEqual(level_of(10**9), 100)

    def test_cap(self):
        self.assertEqual(level_of(10**9, 50), 50)


class FakeResponse:
    status = 500
    reason = "boom"


class BulkTest(unittest.IsolatedAsyncioTestCase):
    async def test_counts_success_and_failure(self):
        async def good():
            return None

        async def bad():
            raise discord.HTTPException(FakeResponse(), "boom")

        ok, failed = await bulk([good, bad, good, bad, bad], limit=2)
        self.assertEqual((ok, failed), (2, 3))

    async def test_unexpected_errors_are_not_hidden(self):
        async def broken():
            raise KeyError("bug")

        with self.assertRaises(KeyError):
            await bulk([broken])


if __name__ == "__main__":
    unittest.main()
