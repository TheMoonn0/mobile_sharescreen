import streamlit as st
import qrcode
import requests
import time
import uuid
import threading
from io import BytesIO
from PIL import Image

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
import uvicorn
from pyngrok import ngrok


API_PORT = 8000

api = FastAPI()
frames = {}


@api.websocket("/upload/{room_id}")
async def upload_screen(websocket: WebSocket, room_id: str):
    await websocket.accept()
    print(f"iPhone connected: {room_id}")

    try:
        while True:
            data = await websocket.receive_bytes()
            frames[room_id] = data

    except WebSocketDisconnect:
        print(f"iPhone disconnected: {room_id}")


@api.get("/frame/{room_id}")
def get_frame(room_id: str):
    frame = frames.get(room_id)

    if frame is None:
        return Response(status_code=204)

    return Response(
        content=frame,
        media_type="image/jpeg",
        headers={"Cache-Control": "no-store"},
    )


def run_api():
    uvicorn.run(
        api,
        host="0.0.0.0",
        port=API_PORT,
        log_level="warning",
    )


def start_ngrok():
    tunnel = ngrok.connect(API_PORT, "http")
    return tunnel.public_url


st.set_page_config(page_title="iPhone Screen Share", layout="wide")
st.title("iPhone Screen Share Realtime")

if "api_started" not in st.session_state:
    threading.Thread(target=run_api, daemon=True).start()
    st.session_state.api_started = True
    time.sleep(1)

if "public_url" not in st.session_state:
    st.session_state.public_url = start_ngrok()

if "room_id" not in st.session_state:
    st.session_state.room_id = str(uuid.uuid4())[:8]

room_id = st.session_state.room_id
public_url = st.session_state.public_url

https_url = public_url
wss_url = public_url.replace("https://", "wss://").replace("http://", "ws://")

upload_url = f"{wss_url}/upload/{room_id}"
frame_url = f"http://localhost:{API_PORT}/frame/{room_id}"

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Scan QR with iPhone")
    st.write("ให้ iPhone / ReplayKit ส่ง JPEG frame มาที่ WebSocket URL นี้")
    st.code(upload_url)

    qr = qrcode.make(upload_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=280)

    st.caption(f"Room ID: {room_id}")
    st.caption(f"Public URL: {https_url}")

with col2:
    st.subheader("2. Live Screen")
    screen = st.empty()

    while True:
        try:
            res = requests.get(frame_url, timeout=1)

            if res.status_code == 200:
                img = Image.open(BytesIO(res.content))
                screen.image(img, use_container_width=True)
            else:
                screen.info("Waiting for iPhone stream...")

        except Exception as e:
            screen.warning(f"Waiting for server... {e}")

        time.sleep(0.05)