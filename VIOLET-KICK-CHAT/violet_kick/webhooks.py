import os
import hmac
import hashlib
from fastapi import APIRouter, Request, Header, HTTPException

router = APIRouter(prefix="/webhook")

# The secret you register in Kick for webhook signing. Set in .env
WEBHOOK_SECRET = os.getenv("KICK_WEBHOOK_SECRET", "please_set_a_secret")

# Header name Kick uses for signature may differ — update as needed.
SIGNATURE_HEADER = os.getenv("KICK_SIGNATURE_HEADER", "X-Kick-Signature")

def verify_signature(raw_body: bytes, signature_header_value: str | None) -> bool:
    """
    Example HMAC-SHA256 verification. Confirm the algorithm and header name with Kick docs.
    If Kick uses a different signature scheme, replace this function accordingly.
    """
    if not signature_header_value:
        return False
    # Some providers send "sha256=hex"; handle both forms.
    sig = signature_header_value.split("=", 1)[-1]
    computed = hmac.new(WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, sig)

@router.post("/")
async def receive_webhook(request: Request, x_kick_signature: str | None = Header(None)):
    raw = await request.body()
    if not verify_signature(raw, x_kick_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    payload = await request.json()
    # Example: payload may have type: "follow", "subscription", "donation", "stream.online"
    event_type = payload.get("type", "<unknown>")
    # TODO: persist to DB or forward to overlay (emit via socket.io)
    # Example: print for now
    print("Received webhook:", event_type, payload)
    return {"status": "ok", "received": event_type}