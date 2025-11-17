@echo off
echo ========================================
echo VIOLET KICK INTEGRATION STARTUP
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.template to .env and configure your credentials.
    echo.
    copy .env.template .env
    echo Created .env file from template.
    echo Please edit .env with your Kick.com credentials.
    echo.
    pause
    exit /b 1
)

REM Start the integrated VIOLET system
echo.
echo Starting VIOLET Integrated System...
echo This will start:
echo - OAuth Authentication Server (http://localhost:8000/kick/login)
echo - Webhook Receiver (http://localhost:8000/webhook)
echo - Overlay System (http://localhost:8000/overlay)
echo - Chat Integration
echo.
echo Press Ctrl+C to stop the server.
echo.

cd violet_kick
python main.py

pause