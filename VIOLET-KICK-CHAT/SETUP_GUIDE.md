# VIOLET Kick Bot - Complete Setup Guide

## 🚀 Quick Start

This guide will help you set up VIOLET to connect to your Kick.com chat and receive webhooks on port 5000 (avoiding OBS port 8080 conflict).

## 📋 Prerequisites

1. Python 3.8 or higher
2. A Kick.com account
3. Kick Developer Application (for OAuth)

## 🔧 Step 1: Install Dependencies

```bash
cd VIOLET-KICK-CHAT
pip install -r requirements.txt
```

## 🔑 Step 2: Configure Your Bot

### 2.1 Get Your Kick Credentials

1. **Create a Kick Developer Application:**
   - Go to https://kick.com/settings/developer
   - Create a new application
   - Set redirect URI to: `http://localhost:5000/kick/callback`
   - Note your Client ID and Client Secret

2. **Get Your Channel Information:**
   - Go to your Kick channel
   - Your channel ID is in the URL: `kick.com/YOUR_CHANNEL_NAME`
   - You'll need this for the bot to connect

### 2.2 Update .env File

Edit the `.env` file in the `VIOLET-KICK-CHAT` directory:

```bash
# Your Kick OAuth credentials
KICK_CLIENT_ID=your_client_id_here
KICK_CLIENT_SECRET=your_client_secret_here

# Your channel information
KICK_CHANNEL_ID=your_channel_id_here

# Bot token (you'll get this after OAuth)
KICK_BOT_TOKEN=your_bot_token_here

# Webhook secret (create a random string)
KICK_WEBHOOK_SECRET=your_random_secret_here

# Server runs on port 5000 (not 8080 to avoid OBS conflict)
PORT=5000
```

## 🔐 Step 3: Authenticate Your Bot

### Option A: OAuth Flow (Recommended)

1. Start the bot server:
```bash
python kick_bot_integrated.py
```

2. Open your browser and go to:
```
https://kick.com/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:5000/kick/callback&response_type=code&scope=chat:read+chat:write
```

3. Authorize the application
4. Copy the access token from the callback page
5. Add it to your `.env` file as `KICK_BOT_TOKEN`
6. Restart the bot

### Option B: Manual Token (Alternative)

If you already have a bot token, simply add it to your `.env` file.

## 🌐 Step 4: Configure Kick Webhooks

1. Go to your Kick Developer Dashboard
2. Find your application
3. Add webhook URL: `http://YOUR_PUBLIC_IP:5000/webhook`
   - If testing locally, use ngrok or similar: `https://your-ngrok-url.ngrok.io/webhook`
4. Set the webhook secret (same as in your `.env` file)
5. Select events to receive:
   - Chat messages
   - Follows
   - Subscriptions
   - Stream online/offline

## 🎮 Step 5: Run the Bot

### Integrated Version (Recommended)

This runs both the chat bot and webhook server together:

```bash
python kick_bot_integrated.py
```

You should see:
```
🤖 VIOLET - Kick Chat Bot & Webhook Server
============================================================
📡 Server: http://0.0.0.0:5000
🔗 Webhook: http://0.0.0.0:5000/webhook
🔐 OAuth: http://localhost:5000/kick/callback
============================================================
```

### Separate Components (Advanced)

If you want to run components separately:

1. **Webhook Server:**
```bash
cd violet_kick
python main.py
```

2. **Chat Bot (in another terminal):**
```bash
python violet_kick_bot.py
```

## 🧪 Step 6: Test Your Setup

### Test Webhook Endpoint

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "bot_connected": true
}
```

### Test Chat Connection

1. Go to your Kick channel
2. Type a message mentioning "violet"
3. Check the bot console for the message
4. VIOLET should respond in chat

### Test Webhook

Send a test webhook from Kick Developer Dashboard or use curl:

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Kick-Signature: sha256=test" \
  -d '{"type":"test","data":"hello"}'
```

## 📊 Monitoring

### View Bot Status

Open in browser: `http://localhost:5000/`

### View Recent Messages

Open in browser: `http://localhost:5000/messages`

### Check Logs

The bot logs all activity to console:
- 💬 Chat messages
- 📥 Webhook events
- ✅ Connection status
- ❌ Errors

## 🔧 Troubleshooting

### Bot Won't Connect to Chat

1. **Check your credentials:**
   - Verify `KICK_CLIENT_ID` and `KICK_CLIENT_SECRET`
   - Ensure `KICK_BOT_TOKEN` is valid

2. **Check channel ID:**
   - Make sure `KICK_CHANNEL_ID` is correct
   - Try getting it from Kick API

3. **Check WebSocket URL:**
   - Kick's WebSocket URL may change
   - Current: `wss://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7&client=js&version=7.6.0&flash=false`

### Webhooks Not Receiving

1. **Check webhook URL:**
   - Must be publicly accessible
   - Use ngrok for local testing: `ngrok http 5000`

2. **Verify webhook secret:**
   - Must match in both Kick dashboard and `.env`

3. **Check signature verification:**
   - Ensure `X-Kick-Signature` header is correct

### Port 5000 Already in Use

If port 5000 is taken, change it in `.env`:
```bash
PORT=5001  # or any other available port
```

Then update your webhook URL in Kick dashboard.

## 🎨 OBS Integration

Since the bot runs on port 5000 (not 8080), it won't conflict with OBS.

### Add Chat Overlay to OBS

1. Add Browser Source in OBS
2. URL: `http://localhost:5000/overlay` (if you have overlay files)
3. Width: 400, Height: 600
4. Check "Shutdown source when not visible"

## 🔒 Security Notes

1. **Never commit your `.env` file** - it contains secrets
2. **Use strong webhook secrets** - generate random strings
3. **Use HTTPS in production** - especially for webhooks
4. **Rotate tokens regularly** - if compromised

## 📝 Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `KICK_CLIENT_ID` | Your Kick OAuth client ID | Yes |
| `KICK_CLIENT_SECRET` | Your Kick OAuth client secret | Yes |
| `KICK_BOT_TOKEN` | Bot access token from OAuth | Yes |
| `KICK_CHANNEL_ID` | Your Kick channel ID | Yes |
| `KICK_WEBHOOK_SECRET` | Secret for webhook verification | Recommended |
| `PORT` | Server port (default: 5000) | No |
| `HOST` | Server host (default: 0.0.0.0) | No |

## 🆘 Getting Help

If you encounter issues:

1. Check the console logs for error messages
2. Verify all credentials in `.env`
3. Test each component separately
4. Check Kick API documentation for updates

## 🎉 Success!

Once everything is running, you should see:
- ✅ Bot connected to chat
- ✅ Webhook server running on port 5000
- ✅ VIOLET responding to mentions
- ✅ Webhooks being received

Your VIOLET bot is now fully integrated with Kick.com! 🚀