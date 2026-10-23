"""Static check of the settings: every settings key written as a literal in the code exists in the defaults, so a typo is found by the tests instead of by a user."""

import ast
import unittest
from pathlib import Path

from guardbot.defaults import DEFAULTS

ROOT = Path(__file__).resolve().parent.parent / "guardbot"


def literal(node):
    """The string of a constant subscript, or None."""
    if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
        return node.slice.value
    return None


def chain(node):
    """For X["a"]["b"] return (X, ["a", "b"]) with only literal keys."""
    keys = []
    while isinstance(node, ast.Subscript):
        k = literal(node)
        if k is None:
            return None, []
        keys.append(k)
        node = node.value
    return node, keys[::-1]


def is_cfg_call(node):
    """True for anything.cfg(...)"""
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "cfg"


def is_conf_call(node):
    """True for self.conf(...)"""
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "conf" and isinstance(node.func.value, ast.Name) and node.func.value.id == "self"


def check(keys, path, where, problems):
    """Walk the keys through the defaults. Stops at empty dicts and non-dicts, where keys are chosen by users."""
    node = DEFAULTS
    for i, key in enumerate(keys):
        if not isinstance(node, dict) or (not node and i > 0):
            return
        if key not in node:
            problems.append(f"{path}:{where}: unknown setting {'.'.join(keys[:i + 1])}")
            return
        node = node[key]


class SchemaTest(unittest.TestCase):
    def test_literal_settings_keys_exist_in_the_defaults(self):
        problems = []
        for path in sorted(ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            rel = path.relative_to(ROOT)
            for cls in [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]:
                section = None
                for stmt in cls.body:
                    if isinstance(stmt, ast.Assign) and any(getattr(t, "id", "") == "section" for t in stmt.targets) and isinstance(stmt.value, ast.Constant):
                        section = stmt.value.value
                for fn in [n for n in ast.walk(cls) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
                    bound = {}  # variable -> path of keys in the defaults
                    for node in ast.walk(fn):
                        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                            base, keys = chain(node.value)
                            if is_cfg_call(base) and keys:
                                bound[node.targets[0].id] = keys
                            elif is_cfg_call(node.value):
                                bound[node.targets[0].id] = []
                            elif section and is_conf_call(node.value):
                                bound[node.targets[0].id] = [section]
                            elif section and is_conf_call(base) and keys:
                                bound[node.targets[0].id] = [section] + keys
                            elif isinstance(node.value, ast.Subscript):
                                b2, k2 = chain(node.value)
                                if isinstance(b2, ast.Name) and b2.id in bound and k2:
                                    bound[node.targets[0].id] = bound[b2.id] + k2
                    for node in ast.walk(fn):
                        if not isinstance(node, ast.Subscript) or literal(node) is None:
                            continue
                        base, keys = chain(node)
                        if is_cfg_call(base):
                            check(keys, rel, node.lineno, problems)
                        elif section and is_conf_call(base):
                            check([section] + keys, rel, node.lineno, problems)
                        elif isinstance(base, ast.Name) and base.id in bound:
                            check(bound[base.id] + keys, rel, node.lineno, problems)
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
