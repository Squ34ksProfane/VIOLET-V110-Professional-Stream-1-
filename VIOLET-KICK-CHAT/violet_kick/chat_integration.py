import os
import asyncio
import json
import httpx
import websockets

# These endpoints are placeholders. Verify exact endpoints and required auth/handshake in Kick docs.
KICK_CHAT_WS = os.getenv("KICK_CHAT_WS", "wss://chat.kick.com/socket")
KICK_CHAT_SEND = os.getenv("KICK_CHAT_SEND", "https://api.kick.com/v1/chat/send")
BOT_TOKEN = os.getenv("KICK_BOT_TOKEN", "")

async def send_chat_message(channel_id: str, message: str):
    """
    Fallback REST send; some platforms require REST or websocket command.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            KICK_CHAT_SEND,
            json={"channel_id": channel_id, "message": message},
            headers={"Authorization": f"Bearer {BOT_TOKEN}"}
        )
        resp.raise_for_status()
        return resp.json()

async def run_chat_bot(message_handler=None):
    """
    Simple websocket receiver loop. Implement the real handshake if Kick requires it.
    """
    if BOT_TOKEN == "":
        raise RuntimeError("BOT_TOKEN not configured in env")
    headers = {"Authorization": f"Bearer {BOT_TOKEN}"}
    while True:
        try:
            async with websockets.connect(KICK_CHAT_WS, extra_headers=headers) as ws:
                print("Connected to Kick chat websocket")
                async for raw in ws:
                    try:
                        data = json.loads(raw)
                    except Exception:
                        print("non-json chat message:", raw)
                        continue
                    # Example handler: print or call provided coroutine
                    if message_handler:
                        await message_handler(data)
                    else:
                        print("chat event:", data)
        except Exception as e:
            print("chat ws error:", e, "— reconnecting in 5s")
            await asyncio.sleep(5)

# Example moderation command handler
async def basic_moderation_handler(msg):
    # Inspect msg structure to find text, user, channel
    text = msg.get("message", {}).get("text") or msg.get("text")
    user = msg.get("user", {}).get("username") if msg.get("user") else None
    channel = msg.get("channel_id") or msg.get("room_id")
    if not text:
        return
    if text.startswith("!hello"):
        await send_chat_message(channel, f"Hello {user or 'there'} — VIOLET bot here!")
    # Add ban/timeout calls using Kick moderation APIs (requires proper scopes)