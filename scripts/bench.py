"""Measure the parts of the bot that matter at scale. Nothing is sent to Discord.

Usage: python scripts/bench.py [servers] [members_per_server]

Reports: time to save the settings of many servers (everything changed and nothing changed),
time to build the reminder queue of the rules, and time to dispatch messages to all listeners
with the gated modules on and off.
"""

import asyncio
import sys
import tracemalloc
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from guardbot.cogs.server.rules import ReminderQueue  # noqa: E402
from guardbot.core import EXTENSIONS, Bot  # noqa: E402


async def main(servers, members):
    """Run the measurements and print them."""
    bot = Bot({"data_dir": tempfile.mkdtemp()})

    async def never_ready():
        await asyncio.Event().wait()

    bot.wait_until_ready = never_ready
    bot.loop = asyncio.get_running_loop()
    bot._connection.user = SimpleNamespace(id=99, bot=True)
    for ext in EXTENSIONS:
        await bot.load_extension(f"guardbot.cogs.{ext}")
    bot.arrange_commands()

    tracemalloc.start()
    base = tracemalloc.get_traced_memory()[0]
    start = time.perf_counter()
    for gid in range(1, servers + 1):
        bot.cfg(gid)["prefix"] = "?"
    cfg_bytes = tracemalloc.get_traced_memory()[0] - base
    for gid in range(1, servers + 1):
        for uid in range(1, 51):
            bot.store.user(gid, uid)["xp"] = uid
    user_bytes = tracemalloc.get_traced_memory()[0] - base - cfg_bytes
    print(f"create {servers} servers with 50 users each: {time.perf_counter() - start:.2f} s")
    print(f"memory: {cfg_bytes / servers / 1024:.1f} KiB of settings per server, {user_bytes / servers / 50:.0f} bytes per user record, {(cfg_bytes + user_bytes) / 1024 / 1024:.1f} MiB in total")
    tracemalloc.stop()

    start = time.perf_counter()
    bot.store.flush()
    bot.store.flush()
    print(f"save after everything changed: {time.perf_counter() - start:.2f} s")
    for gid in range(1, servers + 1):
        bot.cfg(gid)["prefix"] = "!"
    start = time.perf_counter()
    rows = bot.store.snapshot()
    bot.store.write(rows)
    print(f"save after one setting per server changed: {time.perf_counter() - start:.2f} s, {len(rows['c'])} section rows instead of {servers} whole servers")
    bot.store.flush()
    bot.store.flush()
    start = time.perf_counter()
    for _ in range(10):
        bot.store.flush()
    print(f"save when nothing changed (average of 10): {(time.perf_counter() - start) / 10 * 1000:.1f} ms")

    start = time.perf_counter()
    q = ReminderQueue()
    for i in range(members):
        q.add(i, i)
    q.pop_due(10 ** 12, 20)
    print(f"reminder queue for {members} members: {time.perf_counter() - start:.2f} s")

    guild = SimpleNamespace(id=1, name="bench", members=[], get_member=lambda i: None)
    author = SimpleNamespace(bot=True, id=5, roles=[], guild=guild)
    msgs = 5000

    async def dispatch_round():
        before = len(asyncio.all_tasks())
        start = time.perf_counter()
        for n in range(msgs):
            msg = SimpleNamespace(guild=guild, author=author, id=n, content="hello", channel=SimpleNamespace(id=3, guild=guild), attachments=[], embeds=[])
            bot.dispatch("message", msg)
        tasks = [t for t in asyncio.all_tasks() if t.get_name().startswith("discord.py")]
        scheduled = len(tasks)
        await asyncio.gather(*tasks, return_exceptions=True)
        return time.perf_counter() - start, scheduled, before

    for state in (True, False):
        for name in ("activity", "automod", "antiscam", "utility"):
            bot.cfg(1)["modules"][name] = state
        took, scheduled, _ = await dispatch_round()
        print(f"{msgs} messages, gated modules {'on ' if state else 'off'}: {took:.2f} s, {scheduled} listener calls scheduled")

    for cog in list(bot.cogs):
        await bot.remove_cog(cog)
    bot.store.close()


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 1000, int(sys.argv[2]) if len(sys.argv) > 2 else 200000))
