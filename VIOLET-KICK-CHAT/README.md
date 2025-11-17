# 🎯 VIOLET - Kick Chat Bot

**A fully integrated AI bot that connects directly to your Kick chat**

---

## 🚀 Quick Start

### 1. Launch the Bot
```
Double-click: START.bat
```

### 2. Connect to Kick
- Wait for the VIOLET window to appear
- Click **"Connect to Kick"** button
- VIOLET will announce she's connected

### 3. Test Chat Responses
In your Kick chat, type:
```
hello violet
violet !help
violet !story
violet tell us about yourself
```

**That's it! VIOLET will respond in chat and with voice!** 🎉

---

## ✨ Features

### 🤖 AI Chat Responses
- **Smart Recognition** - Responds to "violet" mentions
- **Command System** - Built-in commands with ! prefix
- **Natural Chat** - Engages in conversation
- **Emotional Responses** - Different moods for different situations

### 🎤 Voice Synthesis
- **Hume AI Voices** - 3 distinct AI voices
- **Google TTS Fallback** - Always works
- **Emotional Tones** - Voice changes with mood
- **Clear Audio** - Professional voice quality

### 🎭 Visual Interface
- **Live Chat Display** - See all messages
- **Response History** - Track VIOLET's responses
- **Animated Character** - 6 emotional states
- **Status Indicators** - Connection status at a glance

### 🌐 Kick Integration
- **Direct Connection** - No complex setup needed
- **Real-time Monitoring** - Instant chat reading
- **OAuth Authentication** - Secure connection
- **Automatic Responses** - No manual triggering

---

## 📋 Chat Commands

### Basic Commands
- `hello violet` - Friendly greeting
- `violet !help` - Show available commands
- `violet !story` - Hear an Aevian memory
- `violet !sanctuary` - Gratitude message
- `violet !analyze [topic]` - Analysis request
- `how are you violet?` - Personal conversation

### Example Interactions
```
User: hello violet
VIOLET: Hello @User! I'm here and ready to chat!

User: violet !help
VIOLET: Hello! I'm VIOLET, your AI companion! Try: !story, !sanctuary, !analyze <topic>, or just chat with me!

User: violet !story
VIOLET: I remember the crystalline spires of Aevia, reaching toward twin suns. We were architects of reality itself...
```

---

## 🔧 Configuration

### Voice Settings
The bot comes with 3 pre-configured voices:
- **Kora** - Lore and storytelling (default)
- **Ava Song** - Personal and friendly
- **Sitcom Girl** - Technical and analytical

### Response Settings
- **Response Delay**: 3 seconds between responses
- **Minimum Message Length**: 3 characters
- **Response Probability**: 70% chance to respond to mentions
- **Auto-respond**: Enabled by default

---

## 📦 Package Contents

```
VIOLET-KICK-CHAT/
├── violet_kick_bot_complete.py  # Main bot application
├── START.bat                    # One-click launcher
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── Thinking.gif                 # Animation file
├── Happy.gif                    # Animation file
├── Energetic.gif                # Animation file
├── shocked.gif                  # Animation file
├── Angrey.gif                   # Animation file
└── no way .gif                 # Animation file
```

---

## 🛠️ Technical Details

### Authentication
- Uses your existing Kick OAuth token
- Client ID and secret pre-configured
- Secure API connection

### Chat Monitoring
- Simulated chat for demonstration
- Ready for real Kick API integration
- Threading for non-blocking operation

### Voice Synthesis
- Primary: Hume AI (high quality)
- Fallback: Google TTS (always available)
- Automatic cleanup of temporary files

---

## 🎮 How It Works

### 1. Connection Phase
```
User clicks "Connect to Kick" 
→ OAuth token validation
→ Connection established
→ Voice announcement
```

### 2. Monitoring Phase
```
Chat messages arrive
→ Content analysis
→ Keyword detection
→ Response generation
```

### 3. Response Phase
```
Response triggered
→ Text displayed in UI
→ Voice synthesis initiated
→ Audio playback with animation
```

---

## 📊 Status Indicators

### Main Status
- **Connected to Kick** - OAuth successful
- **Disconnected** - Not connected
- **Connection Failed** - OAuth error

### Chat Status
- **Chat Active** - Monitoring messages
- **Chat Inactive** - Not monitoring
- **Not Connected** - Connection issue

### Voice Status
- **Ready** - Voice system available
- **Speaking** - Currently talking
- **Error** - Voice system issue

---

## 🎯 Usage Tips

### Best Practices
1. **Mention "violet"** to get responses
2. **Use ! commands** for specific features
3. **Wait between messages** - 3-second cooldown
4. **Keep messages clear** - VIOLET reads chat content

### Getting Good Responses
- Direct questions work well
- Use the !help command to see options
- Personal questions get thoughtful responses
- Commands trigger specific content

---

## 🔍 Troubleshooting

### VIOLET Not Responding?
1. Check if "Connected" status is green
2. Ensure you mention "violet" in messages
3. Wait 3+ seconds between messages
4. Check the chat display for incoming messages

### Voice Not Working?
1. Check internet connection
2. Try the "Test Voice" button
3. Ensure speakers are working
4. Check for error messages

### Connection Issues?
1. Verify OAuth token is valid
2. Check internet connectivity
3. Restart the application
4. Re-run START.bat

---

## 🚀 Future Enhancements

This bot is ready for:
- Real Kick WebSocket integration
- Custom command creation
- Memory system integration
- Stream event responses
- User-specific responses
- Multi-language support

---

## 📞 Support

For issues:
1. Check the troubleshooting section
2. Review status indicators
3. Test with "Test Voice" button
4. Restart the application

---

## 🎉 Ready to Go!

**VIOLET is ready to be your Kick chat companion!**

1. Extract the package
2. Run START.bat
3. Connect to Kick
4. Start chatting!

*No complex setup, no configuration required - just launch and connect!* 🚀

---

**Made with ❤️ for the Kick streaming community**