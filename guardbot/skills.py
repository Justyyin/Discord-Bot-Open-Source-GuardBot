"""Skills: custom commands, games and automations that are described as data, never as code.

A skill is a JSON object with a fixed set of fields. Everything not listed here is rejected, so a skill written by a person or
suggested by an AI can only do what the building blocks below allow: send messages, change the roles of the person who used it,
count things, and pick random values. This module only validates and runs; the Discord part is in cogs/tools/skills.py.
"""

import json
import random
import re
from typing import Any, Literal, Optional

NAME_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,29}")
VAR_RE = re.compile(r"[a-z][a-z0-9_]{0,23}")
TOKEN_RE = re.compile(r"\{([a-z_][a-z0-9_]*(?::[a-z0-9_-]+)?)\}")
KINDS = ("command", "game", "automation")
KINDS_LITERAL = Literal["command", "game", "automation"]
GAMES = ("quiz", "dice", "choice", "slots", "rps")
EVENTS = ("member_join", "member_leave", "message_contains", "button")
MATCH_MODES = ("contains", "word", "exact")
ACTIONS = ("reply", "send", "add_role", "remove_role", "dm", "set_var", "add_var", "give_coins", "choose", "log")
OPS = ("==", "!=", ">", ">=", "<", "<=")
STYLES = ("primary", "secondary", "success", "danger")
SCOPES = ("server", "user")

MAX_TEXT = 1900
MAX_ACTIONS = 10
MAX_SKILLS = 50
MAX_SERVER_VARS = 50
MAX_USER_VARS = 20
MAX_VAR_USERS = 5000
MAX_ROLE_CHANGES = 3
MAX_MESSAGES = 4
MAX_COINS = 1000
MAX_SPEC_BYTES = 12000

BASE_KEYS = {"name", "kind", "description", "enabled", "cooldown", "roles"}
KIND_KEYS = {
    "command": BASE_KEYS | {"actions", "args", "button"},
    "automation": BASE_KEYS | {"trigger", "actions"},
    "game": BASE_KEYS | {"game", "text", "sides", "count", "win_at", "options", "symbols", "win_text", "lose_text", "draw_text", "questions", "seconds", "on_win", "on_lose", "correct_text", "wrong_text"},
}
ACTION_KEYS = {
    "reply": {"do", "if", "text", "ephemeral", "title", "color"},
    "send": {"do", "if", "channel", "text", "title", "color"},
    "add_role": {"do", "if", "role"},
    "remove_role": {"do", "if", "role"},
    "dm": {"do", "if", "text"},
    "set_var": {"do", "if", "name", "value", "scope"},
    "add_var": {"do", "if", "name", "amount", "scope"},
    "give_coins": {"do", "if", "amount"},
    "choose": {"do", "if", "options", "var"},
    "log": {"do", "if", "text"},
}
GAME_KEYS = {
    "dice": {"sides", "count", "text", "win_at", "on_win", "on_lose"},
    "choice": {"options", "text"},
    "slots": {"symbols", "win_text", "lose_text", "on_win", "on_lose"},
    "rps": {"win_text", "lose_text", "draw_text", "on_win", "on_lose"},
    "quiz": {"questions", "seconds", "correct_text", "wrong_text", "on_win", "on_lose"},
}
RESERVED_VARS = {"user", "user_name", "server", "channel", "arg1", "arg2", "roll", "pick", "reels", "choice", "answer", "count"}


class SpecError(ValueError):
    """The skill is not valid. The message says what to change."""


def as_int(value: Any, what: str, low: int, high: int) -> int:
    """An integer in a range. Booleans and floats are refused."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise SpecError(f"{what} must be a whole number")
    if not low <= value <= high:
        raise SpecError(f"{what} must be between {low} and {high}")
    return value


def as_text(value: Any, what: str, limit: int = MAX_TEXT, required: bool = True) -> str:
    """A string of limited length."""
    if not isinstance(value, str):
        raise SpecError(f"{what} must be text")
    value = value.replace("\r\n", "\n").strip()
    if required and not value:
        raise SpecError(f"{what} must not be empty")
    if len(value) > limit:
        raise SpecError(f"{what} is longer than {limit} characters")
    return value


def as_id(value: Any, what: str) -> int:
    """A Discord ID given as number or digits."""
    if isinstance(value, str) and value.isdigit():
        value = int(value)
    return as_int(value, what, 1, 2 ** 63 - 1)


def as_list(value: Any, what: str, low: int, high: int) -> list:
    """A list with a length range."""
    if not isinstance(value, list):
        raise SpecError(f"{what} must be a list")
    if not low <= len(value) <= high:
        raise SpecError(f"{what} needs between {low} and {high} entries")
    return value


def only_keys(obj: dict, allowed: set, what: str) -> None:
    """Refuse fields that are not part of the format."""
    extra = sorted(set(obj) - allowed)
    if extra:
        raise SpecError(f"{what} has unknown field(s): {', '.join(map(str, extra[:5]))}")


def clean_color(value: Any) -> Optional[str]:
    """A colour as #rrggbb or None."""
    if value in (None, ""):
        return None
    text = as_text(value, "color", 7)
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", text):
        raise SpecError("color must look like #3366ff")
    return text.lower()


def clean_condition(cond: Any) -> dict:
    """One condition: has_role, chance, var comparison, or not of one of these."""
    if not isinstance(cond, dict) or not cond:
        raise SpecError("a condition must be an object")
    if "not" in cond:
        only_keys(cond, {"not"}, "condition")
        return {"not": clean_condition(cond["not"])}
    if "has_role" in cond:
        only_keys(cond, {"has_role"}, "condition")
        return {"has_role": as_id(cond["has_role"], "has_role")}
    if "chance" in cond:
        only_keys(cond, {"chance"}, "condition")
        return {"chance": as_int(cond["chance"], "chance", 1, 100)}
    if "var" in cond:
        only_keys(cond, {"var", "op", "value", "scope"}, "condition")
        name = as_text(cond["var"], "var", 24)
        if not VAR_RE.fullmatch(name):
            raise SpecError("var names use lowercase letters, digits and _")
        op = cond.get("op", "==")
        if op not in OPS:
            raise SpecError("op must be one of " + " ".join(OPS))
        scope = cond.get("scope", "server")
        if scope not in SCOPES:
            raise SpecError("scope must be server or user")
        return {"var": name, "op": op, "value": as_int(cond.get("value", 0), "value", -10 ** 9, 10 ** 9), "scope": scope}
    raise SpecError("a condition needs has_role, chance, var or not")


def clean_action(action: Any) -> dict:
    """One action of the whitelist."""
    if not isinstance(action, dict):
        raise SpecError("an action must be an object")
    kind = action.get("do")
    if kind not in ACTIONS:
        raise SpecError("do must be one of " + ", ".join(ACTIONS))
    only_keys(action, ACTION_KEYS[kind], f"action {kind}")
    out: dict[str, Any] = {"do": kind}
    if "if" in action:
        conds = action["if"] if isinstance(action["if"], list) else [action["if"]]
        out["if"] = [clean_condition(c) for c in as_list(conds, "if", 1, 3)]
    if kind in ("reply", "send", "dm", "log"):
        out["text"] = as_text(action.get("text"), f"{kind} text")
    if kind in ("reply", "send"):
        if "title" in action:
            out["title"] = as_text(action["title"], "title", 200)
        color = clean_color(action.get("color"))
        if color:
            out["color"] = color
    if kind == "reply":
        out["ephemeral"] = bool(action.get("ephemeral", False))
    if kind == "send":
        out["channel"] = as_id(action.get("channel"), "channel")
    if kind in ("add_role", "remove_role"):
        out["role"] = as_id(action.get("role"), "role")
    if kind in ("set_var", "add_var"):
        name = as_text(action.get("name"), "name", 24)
        if not VAR_RE.fullmatch(name) or name in RESERVED_VARS:
            raise SpecError("var names use lowercase letters, digits and _, and may not be a reserved word")
        out["name"] = name
        scope = action.get("scope", "server")
        if scope not in SCOPES:
            raise SpecError("scope must be server or user")
        out["scope"] = scope
        if kind == "set_var":
            value = action.get("value", 0)
            out["value"] = as_int(value, "value", -10 ** 9, 10 ** 9) if isinstance(value, int) and not isinstance(value, bool) else as_text(value, "value", 100, required=False)
        else:
            out["amount"] = as_int(action.get("amount", 1), "amount", -10 ** 6, 10 ** 6)
    if kind == "give_coins":
        out["amount"] = as_int(action.get("amount"), "amount", 1, MAX_COINS)
    if kind == "choose":
        out["options"] = [as_text(o, "option", 200) for o in as_list(action.get("options"), "options", 2, 20)]
        var = as_text(action.get("var", "pick"), "var", 24)
        if not VAR_RE.fullmatch(var):
            raise SpecError("var names use lowercase letters, digits and _")
        out["var"] = var
    return out


def clean_actions(actions: Any, what: str = "actions", low: int = 0) -> list:
    """A list of actions with the limits on messages, role changes and coins."""
    items = [clean_action(a) for a in as_list(actions, what, low, MAX_ACTIONS)]
    if sum(1 for a in items if a["do"] in ("add_role", "remove_role")) > MAX_ROLE_CHANGES:
        raise SpecError(f"at most {MAX_ROLE_CHANGES} role changes per skill")
    if sum(1 for a in items if a["do"] in ("reply", "send", "dm")) > MAX_MESSAGES:
        raise SpecError(f"at most {MAX_MESSAGES} messages per skill")
    return items


def clean_trigger(trigger: Any) -> dict:
    """The event that starts an automation."""
    if not isinstance(trigger, dict):
        raise SpecError("trigger must be an object")
    only_keys(trigger, {"event", "words", "mode", "channel"}, "trigger")
    event = trigger.get("event")
    if event not in EVENTS:
        raise SpecError("event must be one of " + ", ".join(EVENTS))
    out: dict[str, Any] = {"event": event}
    if event == "message_contains":
        out["words"] = [as_text(w, "word", 60).lower() for w in as_list(trigger.get("words"), "words", 1, 10)]
        mode = trigger.get("mode", "word")
        if mode not in MATCH_MODES:
            raise SpecError("mode must be one of " + ", ".join(MATCH_MODES))
        out["mode"] = mode
        if trigger.get("channel"):
            out["channel"] = as_id(trigger["channel"], "channel")
    return out


def clean_button(button: Any) -> dict:
    """A button for the panel of a command."""
    if not isinstance(button, dict):
        raise SpecError("button must be an object")
    only_keys(button, {"label", "style"}, "button")
    style = button.get("style", "primary")
    if style not in STYLES:
        raise SpecError("style must be one of " + ", ".join(STYLES))
    return {"label": as_text(button.get("label"), "button label", 80), "style": style}


def clean_game(spec: dict, out: dict) -> None:
    """The fields of a game."""
    game = spec.get("game")
    if game not in GAMES:
        raise SpecError("game must be one of " + ", ".join(GAMES))
    allowed = GAME_KEYS[game] | {"game"}
    only_keys({k: v for k, v in spec.items() if k not in BASE_KEYS | {"kind"}}, allowed, f"game {game}")
    out["game"] = game
    for key in ("text", "win_text", "lose_text", "draw_text", "correct_text", "wrong_text"):
        if key in spec:
            out[key] = as_text(spec[key], key)
    for key in ("on_win", "on_lose"):
        if key in spec:
            out[key] = clean_actions(spec[key], key)
    if game == "dice":
        out["sides"] = as_int(spec.get("sides", 6), "sides", 2, 1000)
        out["count"] = as_int(spec.get("count", 1), "count", 1, 10)
        if "win_at" in spec:
            out["win_at"] = as_int(spec["win_at"], "win_at", 1, 10000)
    elif game == "choice":
        out["options"] = [as_text(o, "option", 200) for o in as_list(spec.get("options"), "options", 2, 30)]
    elif game == "slots":
        out["symbols"] = [as_text(s, "symbol", 20) for s in as_list(spec.get("symbols"), "symbols", 2, 8)]
    elif game == "quiz":
        out["seconds"] = as_int(spec.get("seconds", 30), "seconds", 10, 120)
        questions = []
        for q in as_list(spec.get("questions"), "questions", 1, 20):
            if not isinstance(q, dict):
                raise SpecError("a question must be an object")
            only_keys(q, {"q", "options", "answer"}, "question")
            options = [as_text(o, "answer option", 80) for o in as_list(q.get("options"), "options", 2, 4)]
            questions.append({"q": as_text(q.get("q"), "question", 200), "options": options, "answer": as_int(q.get("answer"), "answer", 0, len(options) - 1)})
        out["questions"] = questions


def clean(spec: Any) -> dict:
    """Validate a skill and return it in its normal form. Raises SpecError."""
    if not isinstance(spec, dict):
        raise SpecError("a skill must be a JSON object")
    if len(json.dumps(spec, ensure_ascii=False)) > MAX_SPEC_BYTES:
        raise SpecError("the skill is too large")
    kind = spec.get("kind")
    if kind not in KINDS:
        raise SpecError("kind must be one of " + ", ".join(KINDS))
    only_keys(spec, KIND_KEYS[kind], "the skill")
    name = as_text(spec.get("name"), "name", 30).lower()
    if not NAME_RE.fullmatch(name):
        raise SpecError("name uses lowercase letters, digits, - and _ (1 to 30 characters)")
    out: dict[str, Any] = {
        "name": name, "kind": kind, "description": as_text(spec.get("description", ""), "description", 100, required=False),
        "enabled": bool(spec.get("enabled", True)), "cooldown": as_int(spec.get("cooldown", 5), "cooldown", 0, 3600),
        "roles": [as_id(r, "role") for r in as_list(spec.get("roles", []), "roles", 0, 10)],
    }
    if kind in ("command", "automation"):
        out["actions"] = clean_actions(spec.get("actions"), "actions", 1)
    if kind == "command":
        out["args"] = as_int(spec.get("args", 0), "args", 0, 2)
        if "button" in spec:
            out["button"] = clean_button(spec["button"])
    if kind == "automation":
        out["trigger"] = clean_trigger(spec.get("trigger"))
        if out["trigger"]["event"] == "button":
            out["button"] = clean_button(spec.get("button", {"label": name}))
    if kind == "game":
        clean_game(spec, out)
    if any(a["do"] == "give_coins" for a in all_actions(out)) and out["cooldown"] < 60:
        raise SpecError("a skill that gives coins needs a cooldown of at least 60 seconds")
    return out


def all_actions(spec: dict) -> list:
    """Every action of a skill, including those of a game."""
    return list(spec.get("actions", [])) + list(spec.get("on_win", [])) + list(spec.get("on_lose", []))


def references(spec: dict) -> dict[str, set]:
    """The role and channel IDs a skill uses, so they can be checked against the server."""
    roles, channels = set(spec.get("roles", [])), set()
    for a in all_actions(spec):
        if "role" in a:
            roles.add(a["role"])
        if "channel" in a:
            channels.add(a["channel"])
        for c in a.get("if", []):
            while "not" in c:
                c = c["not"]
            if "has_role" in c:
                roles.add(c["has_role"])
    if spec.get("trigger", {}).get("channel"):
        channels.add(spec["trigger"]["channel"])
    return {"roles": roles, "channels": channels}


def parse_json(text: str) -> Any:
    """Read a skill from text. A code fence around it, as chat programs add, is removed."""
    text = text.strip()
    m = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, re.S)
    if m:
        text = m.group(1)
    try:
        return json.loads(text)
    except ValueError as exc:
        raise SpecError(f"that is not valid JSON: {exc}") from exc


def extract_json(text: str) -> Any:
    """Find the first JSON object in a text, for answers of a model that talks around it."""
    start = text.find("{")
    if start < 0:
        raise SpecError("the answer contains no skill")
    depth, in_str, esc = 0, False, False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return parse_json(text[start:i + 1])
    raise SpecError("the skill in the answer is not complete")


def starter(kind: str, name: str) -> dict:
    """A small working skill to start from."""
    if kind == "command":
        return {"name": name, "kind": "command", "description": "Says hello", "actions": [{"do": "reply", "text": "Hello {user}!"}]}
    if kind == "automation":
        return {"name": name, "kind": "automation", "description": "Greets new members", "trigger": {"event": "member_join"}, "actions": [{"do": "dm", "text": "Welcome to {server}, {user_name}!"}]}
    return {"name": name, "kind": "game", "description": "Roll a die", "game": "dice", "sides": 6, "text": "{user} rolled a {roll}."}


# ---- text templates and variables

class Vars:
    """Counters of a server and of its users, kept in the settings of the skills module."""

    def __init__(self, data: dict):
        """Wrap the stored dict."""
        self.data = data
        self.data.setdefault("server", {})
        self.data.setdefault("users", {})

    def get(self, name: str, scope: str, uid: int) -> Any:
        """The value of a variable, 0 if it was never set."""
        if scope == "user":
            return self.data["users"].get(str(uid), {}).get(name, 0)
        return self.data["server"].get(name, 0)

    def put(self, name: str, scope: str, uid: int, value: Any) -> bool:
        """Store a value. Returns False when the limits for variables are reached."""
        if scope == "user":
            users = self.data["users"]
            rec = users.get(str(uid))
            if rec is None:
                if len(users) >= MAX_VAR_USERS:
                    return False
                rec = users[str(uid)] = {}
            if name not in rec and len(rec) >= MAX_USER_VARS:
                return False
            rec[name] = value
            return True
        store = self.data["server"]
        if name not in store and len(store) >= MAX_SERVER_VARS:
            return False
        store[name] = value
        return True


def render(text: str, ctx: dict, vars_: Optional[Vars] = None, rng: Optional[random.Random] = None) -> str:
    """Fill {user}, {arg1}, {var:name} and similar into a text. Unknown words stay as they are."""
    gen: Any = rng or random

    def sub(m: re.Match) -> str:
        key = m.group(1)
        if ":" in key:
            head, _, tail = key.partition(":")
            if head == "var" and vars_ is not None:
                return str(vars_.get(tail, "server", 0))
            if head == "uvar" and vars_ is not None:
                return str(vars_.get(tail, "user", ctx.get("user_id", 0)))
            if head == "random":
                m2 = re.fullmatch(r"(\d{1,6})-(\d{1,6})", tail)
                if m2 and int(m2.group(1)) <= int(m2.group(2)):
                    return str(gen.randint(int(m2.group(1)), int(m2.group(2))))
            return m.group(0)
        return str(ctx[key]) if key in ctx else m.group(0)

    return TOKEN_RE.sub(sub, text)[:MAX_TEXT]


def condition_ok(cond: dict, ctx: dict, vars_: Vars, rng: random.Random) -> bool:
    """Evaluate one condition."""
    if "not" in cond:
        return not condition_ok(cond["not"], ctx, vars_, rng)
    if "has_role" in cond:
        return cond["has_role"] in ctx.get("role_ids", ())
    if "chance" in cond:
        return rng.randint(1, 100) <= cond["chance"]
    left = vars_.get(cond["var"], cond["scope"], ctx.get("user_id", 0))
    try:
        left = int(left)
    except (TypeError, ValueError):
        return False
    right = cond["value"]
    return {"==": left == right, "!=": left != right, ">": left > right, ">=": left >= right, "<": left < right, "<=": left <= right}[cond["op"]]


async def run_actions(actions: list, ctx: dict, io: Any, vars_: Vars, rng: Optional[random.Random] = None) -> list[str]:
    """Run actions in order. `io` does the Discord work (reply, send, add_role, remove_role, dm, coins, log). Returns notes about what could not be done."""
    rng = rng or random.Random()
    notes: list[str] = []
    ctx = dict(ctx)
    for a in actions:
        if not all(condition_ok(c, ctx, vars_, rng) for c in a.get("if", [])):
            continue
        kind = a["do"]
        text = render(a["text"], ctx, vars_, rng) if "text" in a else ""
        ok = True
        if kind == "reply":
            ok = await io.reply(text, a.get("ephemeral", False), a.get("title"), a.get("color"))
        elif kind == "send":
            ok = await io.send(a["channel"], text, a.get("title"), a.get("color"))
        elif kind == "dm":
            ok = await io.dm(text)
        elif kind == "log":
            ok = await io.log(text)
        elif kind == "add_role":
            ok = await io.add_role(a["role"])
            if ok:
                ctx.setdefault("role_ids", set()).add(a["role"])
        elif kind == "remove_role":
            ok = await io.remove_role(a["role"])
            if ok and "role_ids" in ctx:
                ctx["role_ids"].discard(a["role"])
        elif kind == "give_coins":
            ok = await io.coins(a["amount"])
        elif kind == "set_var":
            value = a["value"]
            if isinstance(value, str):
                value = render(value, ctx, vars_, rng)
            ok = vars_.put(a["name"], a["scope"], ctx.get("user_id", 0), value)
        elif kind == "add_var":
            current = vars_.get(a["name"], a["scope"], ctx.get("user_id", 0))
            try:
                total = int(current) + a["amount"]
            except (TypeError, ValueError):
                total = a["amount"]
            ok = vars_.put(a["name"], a["scope"], ctx.get("user_id", 0), max(-10 ** 9, min(10 ** 9, total)))
            ctx["count"] = total
        elif kind == "choose":
            ctx[a["var"]] = rng.choice(a["options"])
        if not ok:
            notes.append(kind)
    return notes


# ---- games

def roll_dice(sides: int, count: int, rng: random.Random) -> tuple[list[int], int]:
    """Roll dice. Returns the single results and their sum."""
    rolls = [rng.randint(1, sides) for _ in range(count)]
    return rolls, sum(rolls)


def spin_slots(symbols: list, rng: random.Random) -> tuple[list, bool]:
    """Three reels. A win is three equal symbols."""
    reels = [rng.choice(symbols) for _ in range(3)]
    return reels, len(set(reels)) == 1


def rps_result(player: str, bot: str) -> str:
    """win, lose or draw for the player in rock paper scissors."""
    if player == bot:
        return "draw"
    return "win" if (player, bot) in (("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")) else "lose"


def matches(trigger: dict, text: str) -> bool:
    """True if a message text fits a message_contains trigger."""
    t = text.lower()
    for w in trigger["words"]:
        if trigger["mode"] == "exact" and t.strip() == w:
            return True
        if trigger["mode"] == "contains" and w in t:
            return True
        if trigger["mode"] == "word" and re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", t):
            return True
    return False


def describe(spec: dict) -> str:
    """A short line about what a skill does."""
    if spec["kind"] == "game":
        return f"game: {spec['game']}"
    if spec["kind"] == "automation":
        return f"automation: {spec['trigger']['event']}, {len(spec['actions'])} action(s)"
    return f"command: {len(spec['actions'])} action(s)"


def format_help(roles: list[tuple[int, str]], channels: list[tuple[int, str]]) -> str:
    """The description of the skill format for a model, with the roles and channels it may use."""
    return (
        "You write one Discord bot skill as a single JSON object and nothing else. No explanation, no code fence.\n"
        "kind is command, game or automation. Fields: name (lowercase letters, digits, - _), kind, description (max 100 characters), cooldown (seconds), roles (role IDs that may use it, optional).\n"
        "command and automation have actions (1 to 10). A command may have args (0 to 2, used as {arg1} {arg2}) and button {label, style}.\n"
        "automation has trigger: {event: member_join | member_leave | message_contains | button, words: [..], mode: contains | word | exact, channel: id}.\n"
        "Actions, each with do and optional if (list of conditions): reply {text, ephemeral, title, color}, send {channel, text}, dm {text}, log {text}, add_role {role}, remove_role {role}, "
        "set_var {name, value, scope}, add_var {name, amount, scope}, give_coins {amount, needs cooldown >= 60}, choose {options, var}.\n"
        "Conditions: {has_role: id}, {chance: 1-100}, {var: name, op: == != > >= < <=, value: number, scope: server|user}, {not: condition}.\n"
        "Texts may use {user} {user_name} {server} {channel} {count} {arg1} {arg2} {var:name} {uvar:name} {random:1-6}.\n"
        "game: dice {sides, count, win_at, text with {roll}}, choice {options, text with {choice}}, slots {symbols, win_text, lose_text with {reels}}, rps {draw_text}, quiz {questions: [{q, options (2-4), answer: index}], seconds}. "
        "Games may have on_win and on_lose action lists.\n"
        "At most 3 role changes and 4 messages per skill. Use only the role and channel IDs listed below. If the wish cannot be done with these blocks, return {\"error\": \"short reason\"}.\n"
        "Roles: " + (", ".join(f"{n}={i}" for i, n in roles) or "none") + "\nChannels: " + (", ".join(f"{n}={i}" for i, n in channels) or "none")
    )
