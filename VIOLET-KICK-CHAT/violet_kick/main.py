"""
VIOLET Kick Bot - Main Entry Point
Runs FastAPI server with webhook support on port 5000
"""
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the ASGI app from overlay_server (combines FastAPI + socket.io)
from violet_kick.overlay_server import asgi_app, app as fastapi_app

# Mount other routers (oauth, webhooks)
from violet_kick.oauth import router as oauth_router
from violet_kick.webhooks import router as webhook_router

fastapi_app.include_router(oauth_router)
fastapi_app.include_router(webhook_router)

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))  # Default to 5000 to avoid OBS conflict
    
    print(f"🚀 Starting VIOLET Kick Bot Server on {host}:{port}")
    print(f"📡 Webhook endpoint: http://{host}:{port}/webhook/")
    print(f"🔐 OAuth callback: http://localhost:{port}/kick/callback")
    print(f"🎨 Overlay: http://localhost:{port}/overlay")
    
    uvicorn.run("violet_kick.main:asgi_app", host=host, port=port, reload=True)