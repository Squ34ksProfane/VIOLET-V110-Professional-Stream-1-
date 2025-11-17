# 🤖 VIOLET - Complete Kick.com Integration

## 🎯 What This Does

VIOLET is now fully integrated with Kick.com, providing:

1. **Real-time Chat Bot** - Connects to your Kick chat via WebSocket
2. **Webhook Server** - Receives events from Kick (followers, subs, etc.)
3. **OAuth Integration** - Secure authentication with Kick
4. **Port 5000** - Runs on port 5000 to avoid OBS conflict (port 8080)

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies

```bash
cd VIOLET-KICK-CHAT
pip install -r requirements.txt
```

### 2. Configure Your Bot

Edit `.env` file with your Kick credentials:

```bash
KICK_CLIENT_ID=your_client_id
KICK_CLIENT_SECRET=your_client_secret
KICK_CHANNEL_ID=your_channel_id
KICK_BOT_TOKEN=your_bot_token
KICK_WEBHOOK_SECRET=your_random_secret
PORT=5000
```

### 3. Start the Bot

**Windows:**
```bash
start_bot.bat
```

**Linux/Mac:**
```bash
./start_bot.sh
```

**Or manually:**
```bash
python kick_bot_integrated.py
```

## 📡 What You Get

Once running, you'll have:

- **Webhook Endpoint:** `http://localhost:5000/webhook`
- **OAuth Callback:** `http://localhost:5000/kick/callback`
- **Health Check:** `http://localhost:5000/health`
- **Message History:** `http://localhost:5000/messages`

## 🔧 Configuration Files

### Main Files

| File | Purpose |
|------|---------|
| `kick_bot_integrated.py` | Main bot - runs everything together |
| `.env` | Your configuration (credentials, secrets) |
| `requirements.txt` | Python dependencies |
| `start_bot.bat` / `start_bot.sh` | Easy startup scripts |

### Documentation

| File | Purpose |
|------|---------|
| `SETUP_GUIDE.md` | Complete setup instructions |
| `WEBHOOK_SETUP.md` | Webhook configuration guide |
| `README_COMPLETE.md` | This file - overview |

### Testing

| File | Purpose |
|------|---------|
| `test_webhook.py` | Test your webhook endpoint |

## 🎮 Features

### Chat Bot Features

- ✅ Connects to Kick chat via WebSocket
- ✅ Responds to mentions ("violet", "!violet")
- ✅ Handles commands (!hello, !help, !story)
- ✅ Automatic reconnection on disconnect
- ✅ Message logging and history

### Webhook Features

- ✅ Receives Kick events (follows, subs, etc.)
- ✅ HMAC signature verification
- ✅ Event logging and storage
- ✅ RESTful API endpoints

### OAuth Features

- ✅ Secure authentication flow
- ✅ Token exchange
- ✅ Automatic callback handling

## 🔐 Security

- **Webhook signatures** - Verifies all incoming webhooks
- **Environment variables** - Secrets stored in `.env` (not committed)
- **HTTPS ready** - Works with reverse proxies
- **Token rotation** - Easy to update credentials

## 🧪 Testing

### Test Webhook Locally

```bash
python test_webhook.py
```

### Test Chat Connection

1. Start the bot
2. Go to your Kick channel
3. Type "hello violet" in chat
4. VIOLET should respond!

### Test Health Endpoint

```bash
curl http://localhost:5000/health
```

## 📊 Monitoring

### Console Output

The bot logs everything:
```
🚀 VIOLET Kick Bot Starting...
✅ Connected to Kick chat!
💬 User123: hello violet
🤖 VIOLET: Hello @User123! I'm VIOLET, your AI companion! 👋
📥 Received webhook: channel.follow
🎉 New follower: NewFollower
```

### API Endpoints

- **Status:** `GET /` - Bot status and info
- **Health:** `GET /health` - Health check
- **Messages:** `GET /messages` - Recent messages/events
- **Webhook:** `POST /webhook` - Receives Kick events

## 🌐 Production Deployment

### Using ngrok (Local Testing)

```bash
# Start bot
python kick_bot_integrated.py

# In another terminal
ngrok http 5000

# Use the ngrok URL in Kick webhook settings
```

### Using Docker

```bash
docker build -t violet-kick-bot .
docker run -p 5000:5000 --env-file .env violet-kick-bot
```

### Using Reverse Proxy

See `WEBHOOK_SETUP.md` for Nginx/Apache configuration.

## 🎨 OBS Integration

Since VIOLET runs on port 5000, it won't conflict with OBS (port 8080).

### Add to OBS

1. Add Browser Source
2. URL: `http://localhost:5000/overlay` (if you have overlay)
3. Width: 400, Height: 600

## 🆘 Troubleshooting

### Bot Won't Connect

1. Check `.env` credentials
2. Verify `KICK_BOT_TOKEN` is valid
3. Check `KICK_CHANNEL_ID` is correct
4. Look at console logs for errors

### Webhooks Not Working

1. Check webhook URL is publicly accessible
2. Verify `KICK_WEBHOOK_SECRET` matches Kick dashboard
3. Test with `test_webhook.py`
4. Check firewall/port forwarding

### Port Already in Use

Change port in `.env`:
```bash
PORT=5001  # or any other available port
```

## 📚 Documentation

- **Setup Guide:** `SETUP_GUIDE.md` - Complete setup instructions
- **Webhook Guide:** `WEBHOOK_SETUP.md` - Webhook configuration
- **Kick API Docs:** https://docs.kick.com/

## 🔄 Updates

### Updating the Bot

```bash
git pull
pip install -r requirements.txt --upgrade
```

### Updating Credentials

1. Edit `.env` file
2. Restart the bot

## 🎉 Success Checklist

- [ ] Dependencies installed
- [ ] `.env` configured with credentials
- [ ] Bot starts without errors
- [ ] Connects to Kick chat
- [ ] Responds to mentions
- [ ] Webhook endpoint accessible
- [ ] Webhooks being received
- [ ] No port conflicts with OBS

## 💡 Tips

1. **Use ngrok for testing** - Makes local webhooks accessible
2. **Check logs regularly** - Console shows all activity
3. **Test incrementally** - Test chat first, then webhooks
4. **Keep secrets secure** - Never commit `.env` file
5. **Monitor performance** - Check CPU/memory usage

## 🤝 Support

If you need help:

1. Check console logs for errors
2. Review `SETUP_GUIDE.md`
3. Test with `test_webhook.py`
4. Verify all credentials in `.env`

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `KICK_CLIENT_ID` | Yes | Your Kick OAuth client ID |
| `KICK_CLIENT_SECRET` | Yes | Your Kick OAuth client secret |
| `KICK_BOT_TOKEN` | Yes | Bot access token |
| `KICK_CHANNEL_ID` | Yes | Your Kick channel ID |
| `KICK_WEBHOOK_SECRET` | Recommended | Webhook verification secret |
| `PORT` | No | Server port (default: 5000) |
| `HOST` | No | Server host (default: 0.0.0.0) |

## 🚀 Next Steps

1. **Customize responses** - Edit `kick_bot_integrated.py`
2. **Add more commands** - Extend the command handler
3. **Create overlays** - Build custom OBS overlays
4. **Add voice** - Integrate Hume AI for voice responses
5. **Database** - Store chat history and analytics

---

**VIOLET is ready to enhance your Kick streams! 🎮✨**