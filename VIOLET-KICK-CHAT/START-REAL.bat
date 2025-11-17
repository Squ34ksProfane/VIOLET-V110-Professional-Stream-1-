@echo off
title VIOLET - REAL Kick Chat Bot
color 0E
echo ========================================
echo VIOLET - REAL Kick Chat Bot
echo ========================================
echo.

echo [1/3] Checking Python...
python --version >nul 2>&amp;1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python detected:
python --version

echo.
echo [2/3] Installing dependencies...
pip install pygame pillow requests gtts
if errorlevel 1 (
    echo WARNING: Some dependencies may have failed to install.
    echo Continuing anyway - most features should work.
)

echo.
echo [3/3] Starting VIOLET with REAL chat connection...
echo.
echo ========================================
echo VIOLET IS STARTING...
echo ========================================
echo.
echo IMPORTANT: This connects to your REAL Kick chat!
echo - Uses your OAuth credentials
echo - Reads actual chat messages
echo - Responds to real viewers
echo - Click "Connect to Kick" when ready
echo.

python violet_kick_bot_real.py

echo.
echo ========================================
echo VIOLET has stopped
echo ========================================
echo.
pause