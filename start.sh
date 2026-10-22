#!/usr/bin/env sh
# Starts GuardBot on Linux and macOS. The first run creates the virtual environment and installs the packages.
set -e
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
if ! "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
  echo "Python 3.11 or newer is needed. Install it first (see docs/en/GUIDE.md)." >&2
  exit 1
fi
if [ ! -d .venv ]; then
  "$PY" -m venv .venv
fi
. .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env. Open it, enter your bot token, then run ./start.sh again." >&2
  exit 1
fi
exec python main.py
