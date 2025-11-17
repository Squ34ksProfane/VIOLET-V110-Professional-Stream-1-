@echo off
title VIOLET - Kick Chat Bot
color 0E
echo ========================================
echo VIOLET - Kick Chat Bot
echo ========================================
echo.

echo [1/3] Checking Python...
python --version >nul 2>&1
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
echo [3/3] Starting VIOLET...
echo.
echo ========================================
echo VIOLET IS STARTING...
echo ========================================
echo.
echo Features:
echo - Connects directly to Kick chat
echo - Responds to chat messages
echo - Voice synthesis with Hume AI
echo - Animated character overlay
echo - Real-time chat monitoring
echo.
echo Click "Connect to Kick" in the app to start!
echo.

python violet_kick_bot_complete.py

echo.
echo ========================================
echo VIOLET has stopped
echo ========================================
echo.
pause