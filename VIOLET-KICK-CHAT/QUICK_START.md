# 🚀 VIOLET Kick Bot - Quick Start Guide

## ✅ What's Been Set Up

Your VIOLET bot is now fully configured to work with Kick.com on **port 5000** (avoiding OBS port 8080 conflict).

## 📦 What You Have

### Core Files
- **`kick_bot_integrated.py`** - Main bot (chat + webhooks together)
- **`.env`** - Your configuration file (UPDATE THIS!)
- **`start_bot.bat`** - Windows startup script
- **`start_bot.sh`** - Linux/Mac startup script

### Documentation
- **`SETUP_GUIDE.md`** - Complete setup instructions
- **`WEBHOOK_SETUP.md`** - Webhook configuration
- **`README_COMPLETE.md`** - Full overview
- **`QUICK_START.md`** - This file!

### Testing
- **`test_webhook.py`** - Test your webhook endpoint

## 🎯 Next Steps (Do This Now!)

### Step 1: Update Your .env File

Open `VIOLET-KICK-CHAT/.env` and update these values:

```bash
# Get these from https://kick.com/settings/developer
KICK_CLIENT_ID=01K9TCK0R0TQH150D4WRZJWBM6  # ✅ Already set
KICK_CLIENT_SECRET=d72edcb210b7ca2fbefc70cdd961c1934a06c329c570ebcf2118d8cdb28df53e  # ✅ Already set

# Get your channel ID from your Kick profile URL
KICK_CHANNEL_ID=your_channel_id_here  # ⚠️ UPDATE THIS!

# You'll get this after OAuth (see Step 2)
KICK_BOT_TOKEN=your_bot_token_here  # ⚠️ UPDATE THIS!

# Create a random secret for webhook verification
KICK_WEBHOOK_SECRET=your_random_secret_here  # ⚠️ UPDATE THIS!

# Port is already set to 5000 ✅
PORT=5000
```

### Step 2: Get Your Bot Token (OAuth)

1. **Start the bot:**
   ```bash
   cd VIOLET-KICK-CHAT
   python kick_bot_integrated.py
   ```

2. **Open this URL in your browser:**
   ```
   https://kick.com/oauth/authorize?client_id=01K9TCK0R0TQH150D4WRZJWBM6&redirect_uri=http://localhost:5000/kick/callback&response_type=code&scope=chat:read+chat:write
   ```

3. **Authorize the app** - Click "Authorize"

4. **Copy the token** from the callback page

5. **Add to .env:**
   ```bash
   KICK_BOT_TOKEN=your_token_here
   ```

6. **Restart the bot**

### Step 3: Configure Kick Webhooks

1. **Go to:** https://kick.com/settings/developer

2. **Select your application**

3. **Add webhook URL:**
   - For local testing: Use ngrok (see below)
   - For production: `http://YOUR_SERVER_IP:5000/webhook`

4. **Set webhook secret** (same as in .env)

5. **Select events:**
   - ✅ Chat messages
   - ✅ Follows
   - ✅ Subscriptions
   - ✅ Stream online/offline

### Step 4: Test Everything

1. **Test health endpoint:**
   ```bash
   curl http://localhost:5000/health
   ```

2. **Test webhook:**
   ```bash
   python test_webhook.py
   ```

3. **Test chat:**
   - Go to your Kick channel
   - Type "hello violet" in chat
   - VIOLET should respond!

## 🌐 Local Testing with ngrok

If you want to test webhooks locally:

1. **Install ngrok:**
   - Download from https://ngrok.com/download

2. **Start your bot:**
   ```bash
   python kick_bot_integrated.py
   ```

3. **Start ngrok:**
   ```bash
   ngrok http 5000
   ```

4. **Copy the HTTPS URL:**
   ```
   Forwarding: https://abc123.ngrok.io -> http://localhost:5000
   ```

5. **Use in Kick webhook settings:**
   ```
   https://abc123.ngrok.io/webhook
   ```

## 🎮 Running the Bot

### Windows
```bash
cd VIOLET-KICK-CHAT
start_bot.bat
```

### Linux/Mac
```bash
cd VIOLET-KICK-CHAT
./start_bot.sh
```

### Manual
```bash
cd VIOLET-KICK-CHAT
python kick_bot_integrated.py
```

## 📊 What You'll See

When running, you'll see:
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
📡 Subscribed to channel: your_channel_id
```

## 🔍 Monitoring

### Check Status
```bash
curl http://localhost:5000/
```

### View Messages
```bash
curl http://localhost:5000/messages
```

### Health Check
```bash
curl http://localhost:5000/health
```

## ⚠️ Important Notes

1. **Port 5000** - Bot runs on port 5000 (not 8080, so no OBS conflict)
2. **Security** - Never commit your `.env` file to GitHub
3. **Webhooks** - Need public URL for webhooks (use ngrok for testing)
4. **Token** - Get bot token through OAuth flow
5. **Channel ID** - Get from your Kick profile URL

## 🆘 Troubleshooting

### Bot won't start
- Check Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`

### Can't connect to chat
- Verify `KICK_BOT_TOKEN` is set
- Check `KICK_CHANNEL_ID` is correct
- Look at console logs for errors

### Webhooks not working
- Check webhook URL is publicly accessible
- Verify `KICK_WEBHOOK_SECRET` matches
- Test with `test_webhook.py`

### Port already in use
- Change `PORT=5001` in `.env`
- Or stop other service using port 5000

## 📚 More Help

- **Full Setup:** See `SETUP_GUIDE.md`
- **Webhooks:** See `WEBHOOK_SETUP.md`
- **Overview:** See `README_COMPLETE.md`

## ✅ Success Checklist

- [ ] Updated `.env` with your credentials
- [ ] Got bot token through OAuth
- [ ] Configured webhook in Kick dashboard
- [ ] Bot starts without errors
- [ ] Bot connects to chat
- [ ] Bot responds to mentions
- [ ] Webhooks are being received

## 🎉 You're Ready!

Once all steps are complete, VIOLET will:
- ✅ Connect to your Kick chat
- ✅ Respond to mentions and commands
- ✅ Receive webhooks on port 5000
- ✅ Work alongside OBS (no port conflict)

**Happy streaming! 🎮✨**