@echo off
REM VIOLET Kick Bot Startup Script for Windows
REM This script starts the integrated bot with webhook server on port 5000

echo ============================================================
echo 🤖 Starting VIOLET Kick Bot
echo ============================================================

REM Check if .env exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo 📝 Please copy .env.template to .env and configure it
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed!
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

REM Start the bot
echo 🚀 Starting VIOLET...
echo 📡 Webhook will be available at: http://localhost:5000/webhook
echo 🔐 OAuth callback at: http://localhost:5000/kick/callback
echo.
echo Press Ctrl+C to stop the bot
echo ============================================================

python kick_bot_integrated.py

pause