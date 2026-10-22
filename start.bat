@echo off
rem Starts GuardBot on Windows. The first run creates the virtual environment and installs the packages.
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python 3.11 or newer is needed. Install it from python.org and tick "Add python.exe to PATH".
  pause
  exit /b 1
)
if not exist .venv (
  py -3 -m venv .venv
  if errorlevel 1 (
    echo Could not create the virtual environment. Python 3.11 or newer is needed.
    pause
    exit /b 1
  )
)
call .venv\Scripts\activate.bat
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
if not exist .env (
  copy .env.example .env >nul
  echo Created .env. Open it with Notepad, enter your bot token, then run start.bat again.
  pause
  exit /b 1
)
python main.py
pause
