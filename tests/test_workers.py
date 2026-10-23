"""The lanes for heavy work."""

import asyncio
import threading
import unittest

from guardbot.workers import Busy, Workers


class WorkersTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.w = Workers({"workers": {"ocr": {"threads": 1, "limit": 3}}})

    async def asyncTearDown(self):
        self.w.close()

    async def test_result_and_counters(self):
        self.assertEqual(await self.w.run("ocr", lambda a, b: a + b, 2, 3), 5)
        s = self.w.stats()["ocr"]
        self.assertEqual((s["done"], s["running"], s["waiting"], s["failed"]), (1, 0, 0, 0))

    async def test_full_lane_refuses_new_jobs_at_once(self):
        gate = threading.Event()
        jobs = [asyncio.create_task(self.w.run("ocr", gate.wait, 5)) for _ in range(3)]
        await asyncio.sleep(0.05)
        self.assertEqual(self.w.lanes["ocr"].load, 3)
        with self.assertRaises(Busy):
            await self.w.run("ocr", lambda: 1)
        self.assertEqual(self.w.lanes["ocr"].rejected, 1)
        gate.set()
        await asyncio.gather(*jobs)
        self.assertEqual(self.w.lanes["ocr"].load, 0)
        self.assertEqual(await self.w.run("ocr", lambda: 7), 7)

    async def test_other_lanes_are_not_blocked(self):
        gate = threading.Event()
        jobs = [asyncio.create_task(self.w.run("ocr", gate.wait, 5)) for _ in range(3)]
        await asyncio.sleep(0.05)
        self.assertEqual(await self.w.run("image", lambda: "ok"), "ok")
        gate.set()
        await asyncio.gather(*jobs)

    async def test_errors_are_counted_and_passed_on(self):
        def boom():
            raise ValueError("x")

        with self.assertRaises(ValueError):
            await self.w.run("music", boom)
        s = self.w.stats()["music"]
        self.assertEqual((s["failed"], s["running"]), (1, 0))

    async def test_cancelled_waiting_job_leaves_no_trace(self):
        gate = threading.Event()
        first = asyncio.create_task(self.w.run("ocr", gate.wait, 5))
        await asyncio.sleep(0.02)
        waiting = asyncio.create_task(self.w.run("ocr", lambda: 1))
        await asyncio.sleep(0.02)
        self.assertEqual(self.w.lanes["ocr"].waiting, 1)
        waiting.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await waiting
        self.assertEqual(self.w.lanes["ocr"].waiting, 0)
        gate.set()
        await first


if __name__ == "__main__":
    unittest.main()
