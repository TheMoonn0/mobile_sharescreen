import streamlit as st
import qrcode
import requests
import time
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="iPhone Screen Share", layout="wide")
st.title("iPhone Screen Share Viewer")

BACKEND = st.text_input(
    "Render Backend URL",
    value="https://YOUR-RENDER-NAME.onrender.com"
)

ROOM = st.text_input("Room ID", value="room1")

backend = BACKEND.rstrip("/")

sender_url = f"{backend}/send/{ROOM}"
upload_wss = backend.replace("https://", "wss://").replace("http://", "ws://") + f"/upload/{ROOM}"
frame_url = f"{backend}/frame/{ROOM}"

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("QR สำหรับ iPhone")

    st.write("อันนี้ใช้สแกนด้วย Camera/Safari เพื่อทดสอบส่งกล้องเข้า Streamlit")
    st.code(sender_url)

    qr = qrcode.make(sender_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=280)

    st.divider()

    st.write("ถ้าใช้ iOS ReplayKit app จริง ให้ส่งภาพมาที่ WebSocket นี้")
    st.code(upload_wss)

with col2:
    st.subheader("Live View")
    screen = st.empty()

    while True:
        try:
            res = requests.get(frame_url, timeout=10)

            if res.status_code == 200:
                img = Image.open(BytesIO(res.content))
                screen.image(img, use_container_width=True)
            else:
                screen.info("Waiting for mobile stream...")

        except Exception as e:
            screen.warning(f"Cannot connect backend: {e}")

        time.sleep(0.1)
