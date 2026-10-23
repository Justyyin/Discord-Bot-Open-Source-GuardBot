"""Presets, templates, the overview and the setup window."""

import copy
import unittest
from types import SimpleNamespace as NS

from guardbot.cogs.server.setup import Wizard, health_embed, overview
from guardbot.defaults import DEFAULTS, MODULES
from guardbot.presets import AUTOMOD_PRESETS, AUTOMOD_RULES, EXTRA_SWITCHES, TEMPLATES, apply_automod_preset, apply_template


def fresh():
    """A new settings dict."""
    return copy.deepcopy(DEFAULTS)


class PresetTest(unittest.TestCase):
    """AutoMod presets and templates."""

    def test_presets_only_name_existing_rules_and_options(self):
        """Every option of a preset exists in the defaults, so none is silently ignored."""
        cfg = fresh()
        for name, preset in AUTOMOD_PRESETS.items():
            for rule, options in preset.items():
                self.assertIn(rule, AUTOMOD_RULES, name)
                for key in options:
                    self.assertIn(key, cfg["automod"][rule], (name, rule, key))

    def test_presets_grow_in_strength(self):
        """Loose switches on fewer rules than normal, normal fewer than strict."""
        counts = []
        for name in ("loose", "normal", "strict"):
            cfg = fresh()
            apply_automod_preset(cfg, name)
            counts.append(sum(cfg["automod"][r]["enabled"] for r in AUTOMOD_RULES))
        self.assertLess(counts[0], counts[1])
        self.assertLess(counts[1], counts[2])

    def test_preset_switches_other_rules_off_and_keeps_lists(self):
        """A lighter preset turns rules off again and never touches word lists."""
        cfg = fresh()
        cfg["automod"]["words"]["list"] = ["x"]
        cfg["automod"]["words"]["enabled"] = True
        apply_automod_preset(cfg, "strict")
        apply_automod_preset(cfg, "loose")
        self.assertFalse(cfg["automod"]["pii"]["enabled"])
        self.assertEqual(cfg["automod"]["words"]["list"], ["x"])
        self.assertTrue(cfg["automod"]["words"]["enabled"])

    def test_templates_use_real_modules_and_switch_nothing_off(self):
        """Templates name existing modules, set extra switches and keep what was already on."""
        for name, tpl in TEMPLATES.items():
            for module in tpl["modules"]:
                self.assertIn(module, MODULES, (name, module))
            self.assertIn(tpl["automod"], AUTOMOD_PRESETS)
        cfg = fresh()
        cfg["modules"]["music"] = True
        apply_template(cfg, "community")
        self.assertTrue(cfg["modules"]["music"])
        self.assertTrue(cfg["modules"]["welcome"])
        for module, (section, key) in EXTRA_SWITCHES.items():
            if module in TEMPLATES["community"]["modules"]:
                self.assertTrue(cfg[section][key])


class OverviewTest(unittest.TestCase):
    """The health overview."""

    def guild(self, channels=(), roles=()):
        """A server with some channels and roles."""
        return NS(
            id=1,
            get_channel=lambda i: NS(name=f"c{i}") if i in channels else None,
            get_role=lambda i: NS(name=f"r{i}") if i in roles else None,
        )

    def test_empty_server_lists_open_items(self):
        """A fresh server has open items and the footer names them."""
        rows = {name: ok for name, ok, _ in overview(fresh(), self.guild())}
        self.assertFalse(rows["Log channel"])
        self.assertFalse(rows["Gulag"])
        self.assertTrue(rows["Modules"])

    def test_configured_server(self):
        """Channels and roles that exist count as set up, deleted ones do not."""
        cfg = fresh()
        cfg["log"]["main"] = 5
        cfg["jail"].update({"role": 7, "channel": 6, "staff_role": 8})
        rows = {name: ok for name, ok, _ in overview(cfg, self.guild(channels=(5, 6), roles=(7, 8)))}
        self.assertTrue(rows["Log channel"] and rows["Gulag"] and rows["Staff role"])
        rows = {name: ok for name, ok, _ in overview(cfg, self.guild(channels=(6,), roles=(7, 8)))}
        self.assertFalse(rows["Log channel"])

    def test_health_embed_without_debug_cog(self):
        """The embed is built even when the debug cog is not loaded."""
        bot = NS(cfg=lambda gid: fresh(), get_cog=lambda name: None)
        e = health_embed(bot, self.guild())
        self.assertIn("todo  Log channel", e.description)
        self.assertIn("Open:", e.footer.text)


class WizardTest(unittest.IsolatedAsyncioTestCase):
    """The setup window."""

    async def test_window_layout_is_valid(self):
        """The menus have 25 options at most and the window uses 5 rows at most."""
        view = Wizard(NS(bot=NS()), 1)
        rows = {}
        for item in view.children:
            rows.setdefault(item.row, []).append(item)
            if hasattr(item, "options"):
                self.assertLessEqual(len(item.options), 25)
                self.assertGreaterEqual(len(item.options), 3)
        self.assertLessEqual(len(rows), 5)
        for row, items in rows.items():
            if any(hasattr(i, "options") for i in items):
                self.assertEqual(len(items), 1, f"row {row} mixes a menu with other items")


if __name__ == "__main__":
    unittest.main()
