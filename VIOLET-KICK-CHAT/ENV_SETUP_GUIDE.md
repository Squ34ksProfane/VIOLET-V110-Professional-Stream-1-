# 📋 VIOLET .env File Setup Guide

## 🎯 Quick Setup (2 Minutes)

### Step 1: Get Your Kick.com Credentials

1. Go to **https://kick.com/developers**
2. Sign in with your Kick account
3. Click **"Create New Application"**
4. Fill in:
   - **Name**: `VIOLET Stream Bot`
   - **Description**: `AI streaming companion`
   - **Redirect URI**: `http://localhost:8000/kick/callback`
5. **Save** - you'll get your Client ID and Secret

### Step 2: Configure Your .env File

Replace ONLY these 3 values in your `.env` file:

```env
# Replace these 3 values:
KICK_CLIENT_ID=your_actual_client_id_here
KICK_CLIENT_SECRET=your_actual_client_secret_here
KICK_WEBHOOK_SECRET=your_secure_webhook_secret_here
```

#### What to put in each:

**KICK_CLIENT_ID:**
- Get from Kick Developer Dashboard
- Example: `01K9TCK0R0TQH150D4WRZJWBM6`

**KICK_CLIENT_SECRET:**
- Get from Kick Developer Dashboard  
- Example: `d72edcb210b7ca2fbefc70cdd961c1934a06c329c570ebcf2118d8cdb28df53e`

**KICK_WEBHOOK_SECRET:**
- Generate a random string
- Use: https://www.allkeysgenerator.com/Random/Security-Encryption-Key-Generator.aspx
- Example: `9f8s7d6f5g4h3j2k1l0m9n8b7v6c5x4z3a2s1d`

### Step 3: Start VIOLET

```bash
# Double-click this file
START_VIOLET_INTEGRATED.bat
```

### Step 4: Get Your Bot Token

1. Open browser: **http://localhost:8000/kick/login**
2. Click "Authorize" 
3. Copy the `access_token` value
4. Add it to your `.env` file:
```env
KICK_BOT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Step 5: Restart VIOLET

Run `START_VIOLET_INTEGRATED.bat` again with the complete configuration.

## 📝 Complete Example

Here's what your final `.env` should look like:

```env
KICK_CLIENT_ID=01K9TCK0R0TQH150D4WRZJWBM6
KICK_CLIENT_SECRET=d72edcb210b7ca2fbefc70cdd961c1934a06c329c570ebcf2118d8cdb28df53e
KICK_REDIRECT_URI=http://localhost:8000/kick/callback
KICK_AUTHORIZE_URL=https://kick.com/oauth/authorize
KICK_TOKEN_URL=https://api.kick.com/oauth/token

KICK_BOT_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJraWNrLmNvbSIsInN1YiI6IjEyMzQ1Njc4OTAiLCJhdWQiOiJ5b3VyLWNsaWVudC1pZCIsImlhdCI6MTYzMzA0NjQwMCwiZXhwIjoxNjMzMTMyODAwfQ.example

KICK_CHAT_WS=wss://chat.kick.com/socket
KICK_CHAT_SEND=https://api.kick.com/v1/chat/send

KICK_WEBHOOK_SECRET=9f8s7d6f5g4h3j2k1l0m9n8b7v6c5x4z3a2s1d
KICK_SIGNATURE_HEADER=X-Kick-Signature

HOST=0.0.0.0
PORT=8000
```

## 🚨 Important Notes

- **NEVER share** your `KICK_CLIENT_SECRET`
- **Keep webhook secret** random and unique
- **Redirect URI must match exactly** in Kick dashboard
- **Bot token is obtained after** first OAuth login
- **Restart VIOLET after** changing any values

## 🔧 Troubleshooting

**"Invalid client credentials"**
→ Double-check Client ID and Secret from Kick dashboard

**"Redirect URI mismatch"** 
→ Ensure it's exactly `http://localhost:8000/kick/callback` in Kick settings

**"Port already in use"**
→ Change `PORT=8001` in .env file

**Need help?**
→ Check the INTEGRATED_SETUP_GUIDE.md for detailed instructions

---
**Ready to go!** 🚀 Just configure the 3 values and you're set!