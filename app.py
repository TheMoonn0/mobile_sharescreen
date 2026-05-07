import streamlit as st
import qrcode
import requests
import time
from io import BytesIO
from PIL import Image

st.set_page_config(layout="wide")

st.title("iPhone Screen Share")

BACKEND = "https://YOUR-RENDER.onrender.com"
ROOM = "room1"

WSS = BACKEND.replace("https://", "wss://")

upload_url = f"{WSS}/upload/{ROOM}"
frame_url = f"{BACKEND}/frame/{ROOM}"

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("QR Code")

    qr = qrcode.make(upload_url)

    buf = BytesIO()
    qr.save(buf, format="PNG")

    st.image(buf.getvalue(), width=280)
    st.code(upload_url)

with col2:
    st.subheader("Live Screen")

    screen = st.empty()

    while True:
        try:
            res = requests.get(frame_url)

            if res.status_code == 200:
                img = Image.open(BytesIO(res.content))
                screen.image(img, use_container_width=True)
            else:
                screen.info("Waiting for iPhone stream...")

        except Exception as e:
            screen.error(str(e))

        time.sleep(0.05)
