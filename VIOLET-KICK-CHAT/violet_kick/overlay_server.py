import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI()
asgi_app = socketio.ASGIApp(sio, other_asgi_app=app)

# Serve the static overlay HTML directory
app.mount("/overlay_static", StaticFiles(directory="overlay_static"), name="overlay_static")

@app.get("/overlay")
async def overlay_page():
    return FileResponse("overlay_static/overlay.html")

# Utility to emit events to overlay clients
async def emit_alert(event: dict):
    await sio.emit("alert", event)

@sio.event
async def connect(sid, environ):
    print("Overlay connected:", sid)

@sio.event
async def disconnect(sid):
    print("Overlay disconnected:", sid)