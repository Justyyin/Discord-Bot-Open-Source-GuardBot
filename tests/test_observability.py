"""Structured logging and metrics."""

import asyncio
import json
import logging
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from aiohttp.test_utils import TestClient, TestServer

from guardbot import logsetup, metrics
from guardbot.core import Bot
from guardbot.health import StatusServer


class LoggingTest(unittest.TestCase):
    def logger(self, settings):
        """A fresh logger with the handlers built from the settings."""
        log = logging.getLogger(f"guardbot.test.{id(settings)}")
        log.handlers = []
        log.propagate = False
        log.setLevel(logging.INFO)
        for h in logsetup.build_handlers(settings):
            if type(h) is not logging.StreamHandler:
                log.addHandler(h)
        return log

    def test_json_lines_carry_guild_command_and_error(self):
        d = tempfile.mkdtemp()
        log = self.logger({"data_dir": d, "log_format": "json"})
        token = logsetup.CONTEXT.set({"guild": 42, "command": "/moderation ban"})
        try:
            log.info("hello %s", "world")
            try:
                1 / 0
            except ZeroDivisionError:
                log.exception("failed")
        finally:
            logsetup.CONTEXT.reset(token)
        for h in log.handlers:
            h.flush()
        lines = [json.loads(x) for x in Path(d, "guardbot.log").read_text(encoding="utf-8").splitlines() if x.startswith("{")]
        self.assertEqual(lines[0]["message"], "hello world")
        self.assertEqual((lines[0]["guild"], lines[0]["command"], lines[0]["level"]), (42, "/moderation ban", "INFO"))
        self.assertIn("ZeroDivisionError", lines[1]["error"])
        for h in log.handlers:
            h.close()

    def test_text_format_appends_the_context_and_stays_one_line(self):
        d = tempfile.mkdtemp()
        log = self.logger({"data_dir": d, "log_format": "text"})
        token = logsetup.CONTEXT.set({"guild": 7, "command": "on_message"})
        try:
            log.info("x")
        finally:
            logsetup.CONTEXT.reset(token)
        for h in log.handlers:
            h.flush()
        text = Path(d, "guardbot.log").read_text(encoding="utf-8")
        self.assertIn("[guild=7 command=on_message]", text)
        for h in log.handlers:
            h.close()

    def test_file_rotates_at_the_configured_size(self):
        d = tempfile.mkdtemp()
        log = self.logger({"data_dir": d, "log_max_mb": 0.001, "log_backups": 2})
        for n in range(200):
            log.info("line %d %s", n, "x" * 50)
        for h in log.handlers:
            h.close()
        files = sorted(p.name for p in Path(d).glob("guardbot.log*"))
        self.assertEqual(files, ["guardbot.log", "guardbot.log.1", "guardbot.log.2"])

    def test_log_file_can_be_switched_off(self):
        d = tempfile.mkdtemp()
        log = self.logger({"data_dir": d, "log_file": False})
        log.info("x")
        self.assertFalse(Path(d, "guardbot.log").exists())


class MetricsTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = Bot({"data_dir": tempfile.mkdtemp(), "metrics_token": "secret"})
        self.bot.loop = asyncio.get_running_loop()
        self.bot._connection.user = SimpleNamespace(id=1, bot=True)

    async def asyncTearDown(self):
        self.bot.store.close()
        self.bot.work.close()

    def test_histogram_buckets_are_cumulative(self):
        m = metrics.Metrics()
        m.observe("/a", 0.04)
        m.observe("/a", 0.3)
        row = m.durations["/a"]
        self.assertEqual((row[0], row[3], row[-1]), (1, 2, 2))

    async def test_render_has_the_expected_series_and_no_names(self):
        self.bot.cfg(1)["debug"]["usage"]["warn"] = 3
        self.bot.cfg(2)["debug"]["usage"]["warn"] = 4
        self.bot.metrics.observe("/moderation warn", 0.2)
        self.bot.metrics.error()
        text = metrics.render(self.bot)
        for needle in ('guardbot_info{version="', "guardbot_up 0", "guardbot_errors_total 1", 'guardbot_command_uses_total{command="warn"} 7',
                       'guardbot_command_duration_seconds_count{command="/moderation warn"} 1', 'guardbot_lane_rejected_total{lane="ocr"} 0', "guardbot_database_size_bytes"):
            self.assertIn(needle, text)
        self.assertNotIn("guild", text.replace("guardbot_guilds", ""))

    async def test_endpoint_needs_the_token_when_one_is_set(self):
        server = StatusServer(self.bot)
        from aiohttp import web
        app = web.Application()
        app.router.add_get("/metrics", server.metrics_page)
        async with TestClient(TestServer(app)) as client:
            self.assertEqual((await client.get("/metrics")).status, 401)
            self.assertEqual((await client.get("/metrics", headers={"Authorization": "Bearer wrong"})).status, 401)
            ok = await client.get("/metrics", headers={"Authorization": "Bearer secret"})
            self.assertEqual(ok.status, 200)
            self.assertIn("guardbot_up", await ok.text())

    async def test_endpoint_is_open_without_a_token(self):
        self.bot.settings.pop("metrics_token")
        server = StatusServer(self.bot)
        from aiohttp import web
        app = web.Application()
        app.router.add_get("/metrics", server.metrics_page)
        async with TestClient(TestServer(app)) as client:
            self.assertEqual((await client.get("/metrics")).status, 200)


if __name__ == "__main__":
    unittest.main()
