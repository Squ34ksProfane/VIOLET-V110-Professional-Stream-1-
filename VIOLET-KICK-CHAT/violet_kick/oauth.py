import os
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse

router = APIRouter(prefix="/kick")

# Set these in your .env or environment (do NOT hardcode client secret)
CLIENT_ID = os.getenv("KICK_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("KICK_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("KICK_REDIRECT_URI", "http://localhost:8081/callback")

# NOTE: Replace these endpoint URLs with the exact values from Kick docs if they differ.
AUTHORIZE_URL = os.getenv("KICK_AUTHORIZE_URL", "https://kick.com/oauth/authorize")
TOKEN_URL = os.getenv("KICK_TOKEN_URL", "https://api.kick.com/oauth/token")

@router.get("/login")
async def kick_login():
    """
    Redirect the user to Kick's authorization page.
    Uses the Authorization Code flow.
    """
    # Adjust scopes to what you need. Example scopes: user:read chat:read chat:send
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "user:read chat:read chat:send",
        "state": "violet_state_please_change"  # ideally generate a real CSRF state for each request
    }
    url = AUTHORIZE_URL + "?" + urlencode(params)
    return RedirectResponse(url)

@router.get("/callback")
async def kick_callback(request: Request, code: str | None = None, state: str | None = None):
    """
    Exchange the authorization code for tokens.
    This endpoint must match the Redirect URL you registered (http://localhost:8081/callback).
    """
    if code is None:
        return JSONResponse({"error": "missing code"}, status_code=400)

    # Exchange code for token
    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
        }
        resp = await client.post(TOKEN_URL, data=data)
        resp.raise_for_status()
        token_data = resp.json()

    # TODO: persist token_data to your DB (access_token, refresh_token, expires_in, user info)
    # For quick local testing we return the token payload (NOT for production)
    return JSONResponse(token_data)