import os
import uvicorn

# Import the ASGI app from overlay_server (combines FastAPI + socket.io)
from violet_kick.overlay_server import asgi_app, app as fastapi_app

# Mount other routers (oauth, webhooks)
from violet_kick.oauth import router as oauth_router
from violet_kick.webhooks import router as webhook_router

fastapi_app.include_router(oauth_router)
fastapi_app.include_router(webhook_router)

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:asgi_app", host=host, port=port, reload=True)