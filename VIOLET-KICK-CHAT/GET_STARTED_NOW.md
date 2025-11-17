# 🚀 GET STARTED NOW - 5 Minute Setup

## ⚡ Super Quick Start

Follow these 5 steps to get VIOLET running in minutes!

---

## 📍 Step 1: Find Your Channel ID (2 minutes)

### Method 1: From Your Kick Profile
1. Go to your Kick channel: `https://kick.com/YOUR_USERNAME`
2. Your channel ID is often your username or visible in the page source
3. Or use Kick API: `https://kick.com/api/v2/channels/YOUR_USERNAME`

### Method 2: Use Browser Console
1. Go to your Kick channel
2. Open browser console (F12)
3. Type: `window.channelId` or look for channel data in Network tab

---

## 🔑 Step 2: Update .env File (1 minute)

Open `VIOLET-KICK-CHAT/.env` and update these 3 lines:

```bash
# Line 11: Add your channel ID
KICK_CHANNEL_ID=your_channel_id_here

# Line 14: You'll get this in Step 3
KICK_BOT_TOKEN=your_bot_token_here

# Line 17: Create any random string
KICK_WEBHOOK_SECRET=my_super_secret_webhook_key_12345
```

**Example:**
```bash
KICK_CHANNEL_ID=123456
KICK_BOT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
KICK_WEBHOOK_SECRET=violet_webhook_secret_2024
```

---

## 🔐 Step 3: Get Your Bot Token (2 minutes)

### A. Start the Bot
```bash
cd VIOLET-KICK-CHAT
python kick_bot_integrated.py
```

### B. Open This URL in Your Browser
```
https://kick.com/oauth/authorize?client_id=01K9TCK0R0TQH150D4WRZJWBM6&redirect_uri=http://localhost:5000/kick/callback&response_type=code&scope=chat:read+chat:write
```

### C. Click "Authorize"

### D. Copy the Token
You'll see a page like:
```
OAuth Successful!
Access Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Save this token to your .env file as KICK_BOT_TOKEN
```

### E. Add to .env
```bash
KICK_BOT_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### F. Restart the Bot
Press `Ctrl+C` to stop, then run again:
```bash
python kick_bot_integrated.py
```

---

## ✅ Step 4: Test It Works (30 seconds)

### Test 1: Check Health
Open browser: `http://localhost:5000/health`

Should see:
```json
{
  "status": "healthy",
  "bot_connected": true
}
```

### Test 2: Chat Test
1. Go to your Kick channel
2. Type in chat: `hello violet`
3. VIOLET should respond!

---

## 🌐 Step 5: Setup Webhooks (Optional - 2 minutes)

### For Local Testing (Use ngrok)

1. **Install ngrok:** https://ngrok.com/download

2. **Start ngrok:**
   ```bash
   ngrok http 5000
   ```

3. **Copy the HTTPS URL:**
   ```
   Forwarding: https://abc123.ngrok.io -> http://localhost:5000
   ```

4. **Configure in Kick:**
   - Go to: https://kick.com/settings/developer
   - Add webhook: `https://abc123.ngrok.io/webhook`
   - Set secret: (same as in your .env)
   - Select events: Follows, Subs, Chat

### For Production

Use your server's public IP:
```
http://YOUR_SERVER_IP:5000/webhook
```

---

## 🎉 You're Done!

Your bot is now running! You should see:

```
============================================================
🤖 VIOLET - Kick Chat Bot & Webhook Server
============================================================
📡 Server: http://0.0.0.0:5000
🔗 Webhook: http://0.0.0.0:5000/webhook
🔐 OAuth: http://localhost:5000/kick/callback
============================================================
🔌 Connecting to Kick chat...
✅ Connected to Kick chat!
📡 Subscribed to channel: 123456
```

---

## 🎮 Using the Bot

### Chat Commands

| Command | Response |
|---------|----------|
| `hello violet` | Greeting response |
| `violet help` | Shows available commands |
| `violet story` | Tells Aevian story |
| `violet` (mention) | Generic response |

### Monitoring

- **Status:** http://localhost:5000/
- **Health:** http://localhost:5000/health
- **Messages:** http://localhost:5000/messages

---

## 🔧 Startup Scripts

### Windows
Double-click: `start_bot.bat`

### Linux/Mac
```bash
./start_bot.sh
```

### Manual
```bash
python kick_bot_integrated.py
```

---

## ⚠️ Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Port already in use"
Change in `.env`:
```bash
PORT=5001
```

### Bot won't connect to chat
1. Check `KICK_BOT_TOKEN` is set
2. Verify `KICK_CHANNEL_ID` is correct
3. Look at console for error messages

### Can't get bot token
1. Make sure bot is running first
2. Use the exact OAuth URL provided
3. Check redirect URI matches: `http://localhost:5000/kick/callback`

---

## 📊 What You'll See

### Console Output
```
💬 User123: hello violet
🤖 VIOLET: Hello @User123! I'm VIOLET, your AI companion! 👋

📥 Received webhook: channel.follow
🎉 New follower: NewFollower

📥 Received webhook: stream.online
🔴 Stream went online!
```

### In Kick Chat
```
User123: hello violet
VIOLET: Hello @User123! I'm VIOLET, your AI companion! 👋
```

---

## 🎯 Quick Reference

### Files You Need to Edit
- ✅ `.env` - Your configuration

### Files You Run
- ✅ `kick_bot_integrated.py` - Main bot
- ✅ `start_bot.bat` / `start_bot.sh` - Startup scripts

### Files to Read
- 📖 `QUICK_START.md` - Detailed quick start
- 📖 `SETUP_GUIDE.md` - Complete setup guide
- 📖 `WEBHOOK_SETUP.md` - Webhook configuration

---

## ✅ Checklist

- [ ] Updated `KICK_CHANNEL_ID` in .env
- [ ] Got `KICK_BOT_TOKEN` via OAuth
- [ ] Set `KICK_WEBHOOK_SECRET` in .env
- [ ] Bot starts without errors
- [ ] Bot connects to chat (see "Connected" message)
- [ ] Bot responds to "hello violet" in chat
- [ ] Health check returns "healthy"
- [ ] (Optional) Webhooks configured

---

## 🎊 Success!

If you see this in console:
```
✅ Connected to Kick chat!
📡 Subscribed to channel: your_channel_id
```

**You're ready to stream with VIOLET! 🚀**

---

## 💡 Pro Tips

1. **Keep bot running** - Use screen/tmux on Linux or run as service
2. **Monitor logs** - Watch console for errors
3. **Test regularly** - Use test_webhook.py
4. **Backup .env** - Keep credentials safe
5. **Update regularly** - Pull latest changes from GitHub

---

## 🆘 Need Help?

1. Check console logs for errors
2. Read `SETUP_GUIDE.md` for details
3. Test with `test_webhook.py`
4. Verify all values in `.env`

---

**Happy Streaming! 🎮✨**

*VIOLET is ready to enhance your Kick experience!*