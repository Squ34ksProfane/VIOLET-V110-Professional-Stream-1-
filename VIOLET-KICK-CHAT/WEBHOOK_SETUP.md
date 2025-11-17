# Kick.com Webhook Configuration Guide

## 🎯 Overview

This guide explains how to configure Kick.com webhooks to work with your VIOLET bot running on port 5000.

## 📡 Webhook Endpoint

Your webhook endpoint is:
```
http://YOUR_SERVER_IP:5000/webhook
```

For local testing with ngrok:
```
https://your-subdomain.ngrok.io/webhook
```

## 🔧 Setting Up Webhooks in Kick

### Step 1: Access Developer Dashboard

1. Go to https://kick.com/settings/developer
2. Select your application
3. Navigate to "Webhooks" section

### Step 2: Add Webhook URL

1. Click "Add Webhook"
2. Enter your webhook URL:
   - Production: `http://YOUR_PUBLIC_IP:5000/webhook`
   - Local testing: `https://your-ngrok-url.ngrok.io/webhook`
3. Set webhook secret (must match `KICK_WEBHOOK_SECRET` in your `.env`)

### Step 3: Select Events

Choose which events you want to receive:

#### Chat Events
- ✅ `chat.message` - New chat messages
- ✅ `chat.delete` - Message deletions
- ✅ `chat.clear` - Chat cleared

#### Channel Events
- ✅ `channel.follow` - New followers
- ✅ `channel.unfollow` - Unfollows
- ✅ `channel.subscription` - New subscriptions
- ✅ `channel.subscription.gift` - Gifted subscriptions

#### Stream Events
- ✅ `stream.online` - Stream goes live
- ✅ `stream.offline` - Stream ends
- ✅ `stream.update` - Stream info updated

#### Moderation Events
- ✅ `channel.ban` - User banned
- ✅ `channel.unban` - User unbanned
- ✅ `channel.timeout` - User timed out

### Step 4: Save Configuration

1. Click "Save Webhook"
2. Test the webhook using Kick's test feature
3. Check your bot console for the test event

## 🧪 Testing Webhooks Locally

### Using ngrok (Recommended)

1. **Install ngrok:**
   ```bash
   # Download from https://ngrok.com/download
   # Or use package manager
   brew install ngrok  # macOS
   choco install ngrok  # Windows
   ```

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

5. **Update Kick webhook URL:**
   - Use: `https://abc123.ngrok.io/webhook`

### Manual Testing

Test your webhook endpoint with curl:

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Kick-Signature: sha256=test_signature" \
  -d '{
    "type": "channel.follow",
    "data": {
      "follower": {
        "id": "12345",
        "username": "TestUser"
      },
      "followed_at": "2024-01-01T00:00:00Z"
    }
  }'
```

## 📋 Webhook Event Examples

### New Follower
```json
{
  "type": "channel.follow",
  "data": {
    "follower": {
      "id": "12345",
      "username": "NewFollower",
      "avatar": "https://..."
    },
    "followed_at": "2024-01-01T12:00:00Z"
  }
}
```

### New Subscription
```json
{
  "type": "channel.subscription",
  "data": {
    "subscriber": {
      "id": "67890",
      "username": "Subscriber",
      "avatar": "https://..."
    },
    "tier": 1,
    "months": 1,
    "subscribed_at": "2024-01-01T12:00:00Z"
  }
}
```

### Stream Online
```json
{
  "type": "stream.online",
  "data": {
    "stream": {
      "id": "stream123",
      "title": "My Stream Title",
      "category": "Gaming",
      "started_at": "2024-01-01T12:00:00Z"
    }
  }
}
```

### Chat Message
```json
{
  "type": "chat.message",
  "data": {
    "message": {
      "id": "msg123",
      "content": "Hello VIOLET!",
      "sender": {
        "id": "user123",
        "username": "ChatUser"
      },
      "sent_at": "2024-01-01T12:00:00Z"
    }
  }
}
```

## 🔒 Security

### Webhook Signature Verification

The bot automatically verifies webhook signatures using HMAC-SHA256:

1. Kick sends signature in `X-Kick-Signature` header
2. Format: `sha256=<hex_digest>`
3. Bot computes HMAC of request body using your secret
4. Compares signatures to verify authenticity

### Best Practices

1. **Use HTTPS in production** - Never use HTTP for webhooks in production
2. **Keep secrets secure** - Never commit `.env` file
3. **Rotate secrets regularly** - Change webhook secret periodically
4. **Validate payloads** - Always validate webhook data structure
5. **Rate limiting** - Implement rate limiting for webhook endpoints

## 🐛 Troubleshooting

### Webhooks Not Being Received

1. **Check URL accessibility:**
   ```bash
   curl http://YOUR_SERVER_IP:5000/health
   ```

2. **Verify firewall rules:**
   - Port 5000 must be open
   - Allow incoming connections from Kick's IP ranges

3. **Check webhook configuration:**
   - URL is correct
   - Events are selected
   - Webhook is enabled

### Signature Verification Failing

1. **Check webhook secret:**
   - Must match in Kick dashboard and `.env`
   - No extra spaces or characters

2. **Check header name:**
   - Default: `X-Kick-Signature`
   - Verify in Kick documentation

3. **Debug signature:**
   ```python
   # Add to webhook handler
   logger.info(f"Received signature: {x_kick_signature}")
   logger.info(f"Computed signature: {computed}")
   ```

### Webhook Timeouts

1. **Respond quickly:**
   - Process webhooks asynchronously
   - Return 200 OK immediately
   - Process data in background

2. **Check bot performance:**
   - Monitor CPU/memory usage
   - Optimize webhook handlers

## 📊 Monitoring Webhooks

### View Recent Webhooks

```bash
curl http://localhost:5000/messages
```

### Check Bot Status

```bash
curl http://localhost:5000/health
```

### Console Logs

The bot logs all webhook events:
```
📥 Received webhook: channel.follow
🎉 New follower: TestUser
```

## 🚀 Production Deployment

### Using a Reverse Proxy (Recommended)

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /webhook {
        proxy_pass http://localhost:5000/webhook;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Apache Configuration

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    
    ProxyPass /webhook http://localhost:5000/webhook
    ProxyPassReverse /webhook http://localhost:5000/webhook
</VirtualHost>
```

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "kick_bot_integrated.py"]
```

```bash
docker build -t violet-kick-bot .
docker run -p 5000:5000 --env-file .env violet-kick-bot
```

## 📝 Webhook URL Checklist

Before going live, verify:

- [ ] Webhook URL is publicly accessible
- [ ] Port 5000 is open and forwarded
- [ ] HTTPS is configured (production)
- [ ] Webhook secret is set correctly
- [ ] Events are selected in Kick dashboard
- [ ] Signature verification is working
- [ ] Bot responds within timeout (< 5 seconds)
- [ ] Error handling is implemented
- [ ] Logging is configured
- [ ] Monitoring is set up

## 🎉 Success!

Once configured, your bot will receive real-time events from Kick.com on port 5000, completely separate from your OBS setup on port 8080!