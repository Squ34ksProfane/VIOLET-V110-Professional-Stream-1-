# VIOLET Kick Integration Setup Guide

## 🎯 Overview
This guide will help you set up VIOLET with complete Kick.com integration including OAuth, webhooks, chat, and real-time overlay system.

## 📋 Prerequisites
- Python 3.8 or higher
- Kick.com Developer Account
- Ngrok (for webhook testing)

## 🚀 Quick Setup (5 Minutes)

### 1. Extract and Configure
```bash
# Extract the VIOLET-KICK-CHAT folder
# Copy environment template
cp .env.template .env

# Edit .env with your credentials
```

### 2. Configure Kick.com Credentials
Edit the `.env` file with your actual Kick.com credentials:

```env
# Get these from your Kick.com Developer Dashboard
KICK_CLIENT_ID=your_actual_client_id
KICK_CLIENT_SECRET=your_actual_client_secret
KICK_REDIRECT_URI=http://localhost:8000/kick/callback

# Generate a secure webhook secret
KICK_WEBHOOK_SECRET=your_secure_webhook_secret

# Get bot token after OAuth flow
KICK_BOT_TOKEN=your_bot_token
```

### 3. Start the System
```bash
# Windows
START_VIOLET_INTEGRATED.bat

# Or manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd violet_kick
python main.py
```

## 🔧 Detailed Configuration

### Step 1: Kick.com App Registration

1. Go to [Kick.com Developer Dashboard](https://kick.com/developers)
2. Create a new application
3. Set redirect URI: `http://localhost:8000/kick/callback`
4. Request scopes: `user:read chat:read chat:send`
5. Save your Client ID and Client Secret

### Step 2: Webhook Configuration

1. In your Kick app settings, add webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
2. Set webhook secret (use the same value as `KICK_WEBHOOK_SECRET` in `.env`)
3. Enable events: follows, subscriptions, donations, raids

### Step 3: OAuth Flow & Bot Token

1. Navigate to: `http://localhost:8000/kick/login`
2. Authorize your application
3. You'll receive an access token
4. Copy the access token to your `.env` file as `KICK_BOT_TOKEN`

## 🌐 API Endpoints

Once running, VIOLET provides these endpoints:

| Endpoint | Purpose |
|----------|---------|
| `http://localhost:8000/kick/login` | OAuth login initiation |
| `http://localhost:8000/kick/callback` | OAuth callback handler |
| `http://localhost:8000/webhook` | Kick webhook receiver |
| `http://localhost:8000/overlay` | Real-time overlay interface |

## 🎮 Features

### ✅ OAuth Authentication
- Secure Kick.com authorization
- Token management
- Automatic refresh support

### ✅ Webhook System
- HMAC-SHA256 signature verification
- Event type handling
- Real-time event processing

### ✅ Chat Integration
- WebSocket chat connection
- Message sending capabilities
- Basic moderation commands

### ✅ Real-time Overlay
- Socket.IO powered
- Live event broadcasting
- Customizable HTML/CSS

## 🛠️ Testing

### Test OAuth Flow
```bash
curl http://localhost:8000/kick/login
```

### Test Webhook
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Kick-Signature: sha256=test" \
  -d '{"type":"follow","data":{"user":"test"}}'
```

### Test Chat Integration
The system will automatically connect to Kick chat when configured.

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change PORT in `.env` file
   - Kill existing processes on port 8000

2. **Invalid Webhook Signature**
   - Ensure `KICK_WEBHOOK_SECRET` matches webhook settings
   - Check signature header name

3. **OAuth Fails**
   - Verify redirect URI matches Kick app settings
   - Check client credentials

4. **Chat Connection Fails**
   - Ensure `KICK_BOT_TOKEN` is valid
   - Check chat scopes in OAuth

### Debug Mode
Set environment variable for detailed logging:
```bash
export DEBUG=1
python violet_kick/main.py
```

## 📚 Advanced Configuration

### Custom Scopes
Modify scopes in `violet_kick/oauth.py`:
```python
"scope": "user:read chat:read chat:send moderation:ban"
```

### Custom Overlay Styling
Edit `overlay_static/overlay.html` to customize the appearance.

### Database Integration
The system is ready for SQLAlchemy integration. Add database models to persist tokens and events.

## 🚀 Production Deployment

### Docker Setup
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "violet_kick/main.py"]
```

### Environment Variables
In production, use actual environment variables instead of `.env` file.

## 📞 Support

For issues:
1. Check the troubleshooting section
2. Review logs for error messages
3. Verify all credentials are correct
4. Ensure Kick.com app is properly configured

---

**VIOLET is now fully integrated with Kick.com!** 🎉