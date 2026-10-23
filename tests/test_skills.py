"""Tests for the skills engine: validation, templates, actions, games."""

import asyncio
import random
import unittest

from guardbot import skills as S


class FakeIO:
    """Collects what a skill would do on Discord."""

    def __init__(self, fail=()):
        self.log, self.fail = [], set(fail)

    async def _do(self, name, *args):
        self.log.append((name, *args))
        return name not in self.fail

    async def reply(self, text, eph, title, color):
        return await self._do("reply", text)

    async def send(self, channel, text, title, color):
        return await self._do("send", channel, text)

    async def dm(self, text):
        return await self._do("dm", text)

    async def log_(self, text):
        return await self._do("log", text)

    async def add_role(self, role):
        return await self._do("add_role", role)

    async def remove_role(self, role):
        return await self._do("remove_role", role)

    async def coins(self, amount):
        return await self._do("coins", amount)


FakeIO.log = FakeIO.log_  # the engine calls io.log


def run(coro):
    return asyncio.new_event_loop().run_until_complete(coro)


class TestValidation(unittest.TestCase):
    def test_starters_are_valid(self):
        for kind in S.KINDS:
            S.clean(S.starter(kind, "demo"))

    def test_unknown_fields_rejected(self):
        spec = S.starter("command", "x")
        spec["exec"] = "import os"
        with self.assertRaises(S.SpecError):
            S.clean(spec)

    def test_unknown_action_rejected(self):
        spec = S.starter("command", "x")
        spec["actions"] = [{"do": "eval", "text": "1"}]
        with self.assertRaises(S.SpecError):
            S.clean(spec)

    def test_limits(self):
        spec = S.starter("command", "x")
        spec["actions"] = [{"do": "add_role", "role": 1}] * 4
        with self.assertRaises(S.SpecError):
            S.clean(spec)
        spec["actions"] = [{"do": "reply", "text": "a"}] * 5
        with self.assertRaises(S.SpecError):
            S.clean(spec)

    def test_coins_need_cooldown(self):
        spec = S.starter("command", "x")
        spec["actions"] = [{"do": "give_coins", "amount": 5}]
        spec["cooldown"] = 10
        with self.assertRaises(S.SpecError):
            S.clean(spec)
        spec["cooldown"] = 60
        S.clean(spec)

    def test_bad_names_and_types(self):
        for name in ("Bad Name", "", "a" * 40):
            spec = S.starter("command", "x")
            spec["name"] = name
            with self.assertRaises(S.SpecError):
                S.clean(spec)
        spec = S.starter("command", "x")
        spec["cooldown"] = True
        with self.assertRaises(S.SpecError):
            S.clean(spec)

    def test_parse_and_extract(self):
        raw = '```json\n{"a": 1}\n```'
        self.assertEqual(S.parse_json(raw), {"a": 1})
        self.assertEqual(S.extract_json('Here: {"a": {"b": "}"}} done'), {"a": {"b": "}"}})
        with self.assertRaises(S.SpecError):
            S.extract_json("no json")

    def test_quiz_validation(self):
        spec = {"name": "q", "kind": "game", "game": "quiz", "questions": [{"q": "1+1", "options": ["1", "2"], "answer": 5}]}
        with self.assertRaises(S.SpecError):
            S.clean(spec)
        spec["questions"][0]["answer"] = 1
        S.clean(spec)

    def test_references(self):
        spec = S.clean({"name": "r", "kind": "command", "actions": [{"do": "add_role", "role": 5, "if": [{"not": {"has_role": 7}}]}, {"do": "send", "channel": 9, "text": "x"}]})
        refs = S.references(spec)
        self.assertEqual(refs["roles"], {5, 7})
        self.assertEqual(refs["channels"], {9})


class TestEngine(unittest.TestCase):
    def test_render(self):
        v = S.Vars({})
        v.put("n", "server", 0, 4)
        self.assertEqual(S.render("{user} {var:n} {nope}", {"user": "A"}, v), "A 4 {nope}")
        self.assertRegex(S.render("{random:3-3}", {}, v), "^3$")

    def test_actions_and_conditions(self):
        io = FakeIO()
        v = S.Vars({})
        actions = S.clean_actions([
            {"do": "add_var", "name": "hits", "amount": 2},
            {"do": "reply", "text": "hits {var:hits}"},
            {"do": "reply", "text": "big", "if": [{"var": "hits", "op": ">=", "value": 5}]},
            {"do": "add_role", "role": 3, "if": [{"not": {"has_role": 3}}]},
        ])
        notes = run(S.run_actions(actions, {"user_id": 1, "role_ids": set()}, io, v, random.Random(1)))
        self.assertEqual(notes, [])
        self.assertEqual([x[0] for x in io.log], ["reply", "add_role"])
        self.assertEqual(io.log[0][1], "hits 2")

    def test_failed_action_reported(self):
        io = FakeIO(fail={"add_role"})
        notes = run(S.run_actions(S.clean_actions([{"do": "add_role", "role": 3}]), {"user_id": 1}, io, S.Vars({})))
        self.assertEqual(notes, ["add_role"])

    def test_variable_limits(self):
        v = S.Vars({})
        for i in range(S.MAX_SERVER_VARS):
            self.assertTrue(v.put(f"v{i}", "server", 0, 1))
        self.assertFalse(v.put("extra", "server", 0, 1))
        self.assertTrue(v.put("v0", "server", 0, 2))

    def test_games(self):
        rolls, total = S.roll_dice(6, 3, random.Random(2))
        self.assertEqual(sum(rolls), total)
        reels, won = S.spin_slots(["a"], random.Random(1))
        self.assertTrue(won)
        self.assertEqual(S.rps_result("rock", "scissors"), "win")
        self.assertEqual(S.rps_result("rock", "paper"), "lose")
        self.assertEqual(S.rps_result("rock", "rock"), "draw")

    def test_matches(self):
        t = {"words": ["hello"], "mode": "word"}
        self.assertTrue(S.matches(t, "oh Hello there"))
        self.assertFalse(S.matches(t, "hellos"))


if __name__ == "__main__":
    unittest.main()
