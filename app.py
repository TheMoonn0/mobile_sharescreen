import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="iPhone Screen Share", layout="wide")

st.title("iPhone Screen Share")

BACKEND_WSS_URL = st.text_input(
    "Backend WebSocket URL",
    value="wss://your-backend.onrender.com/upload/room1"
)

qr = qrcode.make(BACKEND_WSS_URL)
buf = BytesIO()
qr.save(buf, format="PNG")

st.subheader("Scan QR")
st.code(BACKEND_WSS_URL)
st.image(buf.getvalue(), width=280)

st.warning("ต้องมี Backend FastAPI แยกต่างหากสำหรับรับ stream")
