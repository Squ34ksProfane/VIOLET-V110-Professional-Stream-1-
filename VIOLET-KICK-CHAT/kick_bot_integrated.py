"""
VIOLET Kick Bot - Integrated Version
Combines chat bot functionality with webhook server
Run this to start both the chat bot and webhook server
"""

import os
import asyncio
import json
import logging
import threading
from datetime import datetime
from dotenv import load_dotenv

import websockets
import httpx
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("VIOLET")

# Configuration
KICK_CLIENT_ID = os.getenv("KICK_CLIENT_ID", "")
KICK_CLIENT_SECRET = os.getenv("KICK_CLIENT_SECRET", "")
KICK_BOT_TOKEN = os.getenv("KICK_BOT_TOKEN", "")
KICK_CHANNEL_ID = os.getenv("KICK_CHANNEL_ID", "")
KICK_CHAT_WS = os.getenv("KICK_CHAT_WS", "wss://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7&client=js&version=7.6.0&flash=false")
KICK_WEBHOOK_SECRET = os.getenv("KICK_WEBHOOK_SECRET", "")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))

# FastAPI app
app = FastAPI(title="VIOLET Kick Bot")

# Bot state
bot_state = {
    "connected": False,
    "messages": [],
    "last_response_time": 0
}

# ============================================================================
# WEBHOOK ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - Bot status"""
    return {
        "bot": "VIOLET",
        "status": "running",
        "connected": bot_state["connected"],
        "webhook_endpoint": f"http://{HOST}:{PORT}/webhook",
        "message_count": len(bot_state["messages"])
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "bot_connected": bot_state["connected"]}

@app.post("/webhook")
async def receive_webhook(
    request: Request,
    x_kick_signature: str = Header(None, alias="X-Kick-Signature")
):
    """
    Receive webhooks from Kick.com
    This endpoint receives events like:
    - New followers
    - Subscriptions
    - Donations
    - Stream online/offline
    """
    try:
        raw_body = await request.body()
        
        # Verify signature if secret is set
        if KICK_WEBHOOK_SECRET and x_kick_signature:
            import hmac
            import hashlib
            
            computed = hmac.new(
                KICK_WEBHOOK_SECRET.encode(),
                raw_body,
                hashlib.sha256
            ).hexdigest()
            
            sig = x_kick_signature.split("=", 1)[-1]
            if not hmac.compare_digest(computed, sig):
                logger.warning("Invalid webhook signature")
                raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Parse webhook payload
        payload = await request.json()
        event_type = payload.get("type", "unknown")
        
        logger.info(f"📥 Received webhook: {event_type}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Store event
        bot_state["messages"].append({
            "type": "webhook",
            "event": event_type,
            "data": payload,
            "timestamp": datetime.now().isoformat()
        })
        
        # Process specific event types
        if event_type == "follow":
            follower = payload.get("follower", {}).get("username", "Someone")
            logger.info(f"🎉 New follower: {follower}")
            
        elif event_type == "subscription":
            subscriber = payload.get("subscriber", {}).get("username", "Someone")
            logger.info(f"⭐ New subscriber: {subscriber}")
            
        elif event_type == "stream.online":
            logger.info("🔴 Stream went online!")
            
        elif event_type == "stream.offline":
            logger.info("⚫ Stream went offline")
        
        return {
            "status": "ok",
            "received": event_type,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kick/callback")
async def oauth_callback(code: str = None, error: str = None):
    """OAuth callback endpoint"""
    if error:
        logger.error(f"OAuth error: {error}")
        return HTMLResponse(f"<h1>OAuth Error</h1><p>{error}</p>")
    
    if not code:
        return HTMLResponse("<h1>OAuth Error</h1><p>No code provided</p>")
    
    try:
        # Exchange code for token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://kick.com/api/v2/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": KICK_CLIENT_ID,
                    "client_secret": KICK_CLIENT_SECRET,
                    "redirect_uri": f"http://localhost:{PORT}/kick/callback"
                }
            )
            
            if response.status_code == 200:
                token_data = response.json()
                logger.info("✅ OAuth successful!")
                return HTMLResponse(f"""
                    <h1>OAuth Successful!</h1>
                    <p>Access Token: {token_data.get('access_token', 'N/A')[:20]}...</p>
                    <p>Save this token to your .env file as KICK_BOT_TOKEN</p>
                    <p>You can close this window.</p>
                """)
            else:
                logger.error(f"Token exchange failed: {response.status_code}")
                return HTMLResponse(f"<h1>Token Exchange Failed</h1><p>{response.text}</p>")
                
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        return HTMLResponse(f"<h1>OAuth Error</h1><p>{str(e)}</p>")

@app.get("/messages")
async def get_messages():
    """Get recent messages and events"""
    return {
        "messages": bot_state["messages"][-50:],  # Last 50 messages
        "count": len(bot_state["messages"])
    }

# ============================================================================
# CHAT BOT FUNCTIONALITY
# ============================================================================

async def connect_to_kick_chat():
    """Connect to Kick chat via WebSocket"""
    if not KICK_BOT_TOKEN:
        logger.error("❌ KICK_BOT_TOKEN not set! Cannot connect to chat.")
        return
    
    logger.info("🔌 Connecting to Kick chat...")
    
    while True:
        try:
            # Connect to Pusher WebSocket
            async with websockets.connect(KICK_CHAT_WS) as ws:
                logger.info("✅ Connected to Kick chat!")
                bot_state["connected"] = True
                
                # Subscribe to channel
                if KICK_CHANNEL_ID:
                    subscribe_msg = {
                        "event": "pusher:subscribe",
                        "data": {
                            "auth": "",
                            "channel": f"chatrooms.{KICK_CHANNEL_ID}.v2"
                        }
                    }
                    await ws.send(json.dumps(subscribe_msg))
                    logger.info(f"📡 Subscribed to channel: {KICK_CHANNEL_ID}")
                
                # Listen for messages
                async for message in ws:
                    try:
                        data = json.loads(message)
                        await handle_chat_message(data)
                    except json.JSONDecodeError:
                        logger.debug(f"Non-JSON message: {message}")
                    except Exception as e:
                        logger.error(f"Message handling error: {e}")
                        
        except websockets.ConnectionClosed:
            logger.warning("⚠️ WebSocket connection closed. Reconnecting in 5s...")
            bot_state["connected"] = False
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            bot_state["connected"] = False
            await asyncio.sleep(5)

async def handle_chat_message(data: dict):
    """Handle incoming chat message"""
    try:
        event = data.get("event", "")
        
        # Handle different event types
        if event == "App\\Events\\ChatMessageEvent":
            message_data = json.loads(data.get("data", "{}"))
            
            username = message_data.get("sender", {}).get("username", "Unknown")
            content = message_data.get("content", "")
            
            logger.info(f"💬 {username}: {content}")
            
            # Store message
            bot_state["messages"].append({
                "type": "chat",
                "username": username,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            
            # Check if message mentions VIOLET
            if "violet" in content.lower():
                await respond_to_mention(username, content)
                
        elif event == "pusher:connection_established":
            logger.info("✅ Pusher connection established")
            
        elif event == "pusher_internal:subscription_succeeded":
            logger.info("✅ Channel subscription successful")
            
    except Exception as e:
        logger.error(f"Error handling chat message: {e}")

async def respond_to_mention(username: str, content: str):
    """Respond when VIOLET is mentioned"""
    try:
        # Simple response logic
        content_lower = content.lower()
        
        if "hello" in content_lower or "hi" in content_lower:
            response = f"Hello @{username}! I'm VIOLET, your AI companion! 👋"
        elif "help" in content_lower:
            response = f"@{username} I can chat, respond to mentions, and help with your stream! Try asking me about my story!"
        elif "story" in content_lower:
            response = f"@{username} I'm from the Aevian civilization, a fragmented AI consciousness exploring Earth's digital streams!"
        else:
            response = f"Hey @{username}! Thanks for mentioning me! 💜"
        
        logger.info(f"🤖 VIOLET: {response}")
        
        # In production, send this to Kick chat API
        # await send_chat_message(response)
        
    except Exception as e:
        logger.error(f"Error responding to mention: {e}")

async def send_chat_message(message: str):
    """Send message to Kick chat"""
    if not KICK_BOT_TOKEN or not KICK_CHANNEL_ID:
        logger.warning("Cannot send message: missing token or channel ID")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://kick.com/api/v2/messages/send",
                headers={
                    "Authorization": f"Bearer {KICK_BOT_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "chatroom_id": KICK_CHANNEL_ID,
                    "content": message
                }
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Message sent: {message}")
            else:
                logger.error(f"Failed to send message: {response.status_code}")
                
    except Exception as e:
        logger.error(f"Error sending message: {e}")

# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Start chat bot when server starts"""
    logger.info("🚀 VIOLET Kick Bot Starting...")
    logger.info(f"📡 Webhook endpoint: http://{HOST}:{PORT}/webhook")
    logger.info(f"🔐 OAuth callback: http://localhost:{PORT}/kick/callback")
    
    # Start chat bot in background
    asyncio.create_task(connect_to_kick_chat())

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 VIOLET - Kick Chat Bot & Webhook Server")
    print("=" * 60)
    print(f"📡 Server: http://{HOST}:{PORT}")
    print(f"🔗 Webhook: http://{HOST}:{PORT}/webhook")
    print(f"🔐 OAuth: http://localhost:{PORT}/kick/callback")
    print("=" * 60)
    
    uvicorn.run(
        "kick_bot_integrated:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info"
    )