#!/bin/bash

# VIOLET Kick Bot Startup Script
# This script starts the integrated bot with webhook server on port 5000

echo "============================================================"
echo "🤖 Starting VIOLET Kick Bot"
echo "============================================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "📝 Please copy .env.template to .env and configure it"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the bot
echo "🚀 Starting VIOLET..."
echo "📡 Webhook will be available at: http://localhost:5000/webhook"
echo "🔐 OAuth callback at: http://localhost:5000/kick/callback"
echo ""
echo "Press Ctrl+C to stop the bot"
echo "============================================================"

python3 kick_bot_integrated.py