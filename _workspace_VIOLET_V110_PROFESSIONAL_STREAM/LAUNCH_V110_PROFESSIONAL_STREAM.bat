@echo off
title VIOLET V110 Professional Stream Overlay - Clean Display
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║       VIOLET V110 - Professional Stream Overlay System       ║
echo ║     Clean Interface: Just Character + Green Text V110       ║
echo ║                                                              ║
echo ║  V110 Evolution Features:                                    ║
echo ║  ✅ Completely Transparent Background - No Visible UI       ║
echo ║  ✅ Big Character Display (350x350) - Stream Optimized      ║
echo ║  ✅ Green Text Only - Clean Reading Experience              ║
echo ║  ✅ 8-Second Display Time - Perfect for Stream Viewers      ║
echo ║  ✅ DeepSeek AI Brain V110 - Every Response 100%% Unique    ║
echo ║  ✅ Kick Integration V110 - Real-time Stream Events         ║
echo ║  ✅ 6 Voice Triggers V110 - Vi, V, Olet, Vio!, Vi-oh-shit, Violet║
echo ║  ✅ 600+ Expression System V110                             ║
echo ║  ✅ Position Memory V110                                     ║
echo ║  ✅ Professional Stream Appearance V110                     ║
echo ║  ✅ Enhanced Intelligence V110                               ║
echo ║  ✅ Stream-Optimized Design V110                             ║
echo ║                                                              ║
echo ║  V110 Visual Specifications:                                 ║
echo ║  🖼️ Window: 500x600px (stream-optimized V110)             ║
echo ║  👤 Character: 350x350px (large and visible V110)          ║
echo ║  📝 Text: 16pt bold Consolas (easy to read V110)           ║
echo ║  🎨 Background: 100%% transparent V110                      ║
echo ║  🌈 Text Color: #00ff00 (classic green V110)                ║
echo ║  🧠 AI Model: DeepSeek Chat V110                            ║
echo ║                                                              ║
echo ║  V110 Connected Systems:                                     ║
echo ║  🧠 DeepSeek AI: sk-67bfa2a2a2ad4858a3ac164ae4fcf01d        ║
echo ║  🎮 Kick Webhook: https://e5e1-2601-2c1-100-6420-00e-65b2-4ee1.ngrok.io/webhook ║
echo ║  🌐 Local Server: http://localhost:8080/webhook V110         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🌟 Initializing VIOLET V110 Professional Stream Overlay...
echo    This is V110 - The pinnacle of stream overlay technology!
echo.

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check required modules
echo 📦 Checking V110 required modules...
python -c "import tkinter, speech_recognition, gtts, pygame, requests, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Missing V110 modules. Installing...
    pip install speechrecognition gtts pygame pillow requests
    if %errorlevel% neq 0 (
        echo ❌ Failed to install V110 modules.
        pause
        exit /b 1
    )
)

:: Check for mood images
echo 🎨 Checking V110 mood images...
if not exist "violet_neutral.png" (
    echo ⚠️ Warning: Some V110 mood images may be missing.
    echo    VIOLET V110 will work but visual mood changes may be limited.
)

:: Check if main program exists
if not exist "VIOLET_V110_STREAM_OVERLAY.py" (
    echo ❌ V110 Main program file not found: VIOLET_V110_STREAM_OVERLAY.py
    pause
    exit /b 1
)

echo ✅ All V110 checks passed. Starting VIOLET V110 Professional Stream...
echo.

:: Launch VIOLET V110 with error handling
:launch_loop
echo 🚀 Launching VIOLET V110 Professional Stream Overlay...
echo    Version: V110 - The ultimate professional streaming companion
echo    Features: Clean transparent interface, big character, green text only
echo    Perfect for: Professional streaming with no visual clutter
echo    Voice Triggers: Vi, V, Olet, Vio!, Vi-oh-shit, Violet
echo    Press Ctrl+C to stop, or close the window
echo.
python VIOLET_V110_STREAM_OVERLAY.py

if %errorlevel% neq 0 (
    echo.
    echo ⚠️ VIOLET V110 encountered an error.
    echo.
    set /p retry="Would you like to restart VIOLET V110? (y/n): "
    if /i "%retry%"=="y" (
        echo.
        goto launch_loop
    )
)

echo.
echo 🌙 VIOLET V110 Professional Stream Overlay shutdown complete.
echo    V110 Stream overlay is now hidden.
echo    Thank you for using VIOLET V110 - Professional Stream Edition!
pause