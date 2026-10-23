"""Restore the database from a backup in data/dbbackups.

Usage: python scripts/restore_db.py BACKUP_FILE [--data-dir data] [--check]

Stop the bot first. The current database is kept as a backup named before-restore, the chosen backup is checked,
copied into place and opened once to make sure it loads (older backups are migrated on that first start).
With --check the backup is only verified, nothing is changed.
"""

import argparse
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from guardbot.health import heartbeat_fresh  # noqa: E402
from guardbot.store import Store, verify_backup  # noqa: E402


def restore(backup: Path, data_dir: Path, check_only: bool = False) -> str:
    """Verify and restore a backup. Returns a message. Raises RuntimeError when it must not go on."""
    counts = verify_backup(backup)
    summary = f"backup is healthy: {counts['config_sections']} setting rows, {counts['users']} user records, {counts['cases']} cases"
    if check_only:
        return summary
    if heartbeat_fresh(data_dir / "heartbeat"):
        raise RuntimeError("the bot seems to be running (fresh heartbeat). Stop it first.")
    live = data_dir / "guardbot.db"
    safe = None
    if live.exists():
        folder = data_dir / "dbbackups"
        folder.mkdir(parents=True, exist_ok=True)
        safe = folder / f"guardbot-{time.strftime('%Y%m%d-%H%M%S')}-before-restore.db"
        shutil.copy2(live, safe)
    for suffix in ("", "-wal", "-shm"):
        (data_dir / f"guardbot.db{suffix}").unlink(missing_ok=True)
    shutil.copy2(backup, live)
    try:
        store = Store(data_dir)
        store.close()
    except Exception as exc:
        if safe is not None:
            shutil.copy2(safe, live)
        raise RuntimeError(f"the restored database could not be opened ({exc}). The previous database was put back.") from exc
    return summary + (f". The previous database is kept as {safe.name}." if safe else ".")


def main() -> None:
    """Command line entry."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("backup", type=Path)
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--check", action="store_true", help="only verify the backup")
    args = ap.parse_args()
    try:
        print(restore(args.backup, args.data_dir, args.check))
    except RuntimeError as exc:
        sys.exit(f"error: {exc}")


if __name__ == "__main__":
    main()
