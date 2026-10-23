"""Tests of the AI connection with a fake provider. No network."""

import json
import os
import stat
import tempfile
import unittest

import aiohttp

from guardbot import ai as A
from guardbot import configio
from guardbot.defaults import DEFAULTS
import copy

KEY = "sk-test-0123456789abcdefghij"


class FakeResp:
    def __init__(self, status, data):
        self.status, self.data = status, data

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def json(self, content_type=None):
        return self.data


class FakeSession:
    def __init__(self, status=200, data=None, exc=None):
        self.status, self.data, self.exc, self.calls = status, data, exc, []

    def post(self, url, headers=None, json=None, timeout=None):
        self.calls.append((url, headers, json))
        if self.exc:
            raise self.exc
        return FakeResp(self.status, self.data)


class FakeStore:
    def __init__(self, d):
        self.dir = d


class FakeBot:
    def __init__(self, d):
        self.store = FakeStore(d)
        self.settings = {}
        self.config = {"modules": {"ai": True}, "ai": copy.deepcopy(DEFAULTS["ai"])}

    def cfg(self, gid):
        return self.config

    def module_on(self, gid, name):
        return self.config["modules"].get(name, True)


class AITest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.bot = FakeBot(self.dir)

    def make(self, session):
        return A.AI(self.bot, session)

    def test_key_is_encrypted_and_file_is_private(self):
        ai = self.make(None)
        ai.set_key(1, "kimi", f"  {KEY}\n", "")
        stored = self.bot.config["ai"]["key_enc"]
        self.assertNotIn(KEY, stored)
        self.assertEqual(ai.box.open(stored), KEY)
        self.assertEqual(self.bot.config["ai"]["model"], "kimi-k3")
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(os.stat(ai.box.path).st_mode), 0o600)
        self.assertEqual(A.KeyBox(self.dir).open(stored), KEY)

    def test_bad_keys_and_providers(self):
        ai = self.make(None)
        with self.assertRaises(A.AIError):
            ai.set_key(1, "kimi", "short")
        with self.assertRaises(A.AIError):
            ai.set_key(1, "evil", KEY)

    def test_requests_per_provider(self):
        url, headers, body = A.build_request("anthropic", KEY, "m", "sys", "hi", 100)
        self.assertEqual(headers["x-api-key"], KEY)
        self.assertEqual(body["system"], "sys")
        url, headers, body = A.build_request("openai", KEY, "m", "sys", "hi", 100)
        self.assertIn("max_completion_tokens", body)
        self.assertEqual(headers["Authorization"], f"Bearer {KEY}")
        url, headers, body = A.build_request("kimi", KEY, "kimi-k3", "sys", "hi", 100)
        self.assertTrue(url.startswith("https://api.moonshot.ai/"))
        self.assertIn("max_tokens", body)

    def test_read_answers(self):
        self.assertEqual(A.read_answer("anthropic", {"content": [{"type": "text", "text": "ok"}]}), "ok")
        self.assertEqual(A.read_answer("kimi", {"choices": [{"message": {"content": "ok"}}]}), "ok")
        for bad in ({}, {"choices": []}, {"choices": [{"message": {"content": ""}}]}, None):
            with self.assertRaises(A.AIError):
                A.read_answer("openai", bad)

    async def test_ask_success_and_budget(self):
        session = FakeSession(data={"choices": [{"message": {"content": "hello"}}]})
        ai = self.make(session)
        ai.set_key(1, "openai", KEY)
        self.assertEqual(await ai.ask(1, "s", "p"), "hello")
        self.assertEqual(session.calls[0][1]["Authorization"], f"Bearer {KEY}")
        self.bot.config["ai"]["daily_limit"] = 1
        with self.assertRaises(A.AIError):
            await ai.ask(1, "s", "p")

    async def test_errors_never_contain_the_key(self):
        for status, data in ((401, {"error": {"message": f"bad key {KEY}"}}), (429, {}), (500, None), (400, {"error": {"message": f"oops {KEY}"}})):
            ai = self.make(FakeSession(status=status, data=data))
            ai.set_key(1, "anthropic", KEY)
            with self.assertRaises(A.AIError) as cm:
                await ai.ask(1, "s", "p")
            self.assertNotIn(KEY, str(cm.exception))
        ai = self.make(FakeSession(exc=aiohttp.ClientConnectionError(KEY)))
        ai.set_key(1, "anthropic", KEY)
        with self.assertRaises(A.AIError) as cm:
            await ai.ask(1, "s", "p")
        self.assertNotIn(KEY, str(cm.exception))

    async def test_person_cooldown_and_module_switch(self):
        ai = self.make(FakeSession(data={"choices": [{"message": {"content": "x"}}]}))
        ai.set_key(1, "openai", KEY)
        await ai.ask(1, "s", "p", uid=5)
        with self.assertRaises(A.AIError):
            await ai.ask(1, "s", "p", uid=5)
        self.bot.config["modules"]["ai"] = False
        with self.assertRaises(A.AIError):
            await ai.ask(1, "s", "p", uid=6)

    def test_remove_key_turns_ai_off(self):
        ai = self.make(None)
        ai.set_key(1, "openai", KEY)
        ai.remove_key(1)
        self.assertFalse(ai.configured(1))
        self.assertFalse(self.bot.config["modules"]["ai"])

    def test_key_is_not_exported(self):
        cfg = copy.deepcopy(DEFAULTS)
        cfg["ai"]["key_enc"] = "secret-cipher"
        self.assertNotIn("secret-cipher", json.dumps(configio.export_config(cfg)))


if __name__ == "__main__":
    unittest.main()
