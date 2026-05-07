import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="iPhone Screen Viewer", layout="wide")

st.title("iPhone Screen Share to Streamlit")

MEDIA_SERVER_HTTP = st.text_input(
    "Media Server HTTP URL",
    value="http://YOUR_SERVER_IP:8888",
)

MEDIA_SERVER_RTMP_HOST = st.text_input(
    "Media Server RTMP Host",
    value="YOUR_SERVER_IP",
)

STREAM_NAME = st.text_input("Stream name", value="iphone")

hls_url = f"{MEDIA_SERVER_HTTP.rstrip('/')}/live/{STREAM_NAME}/index.m3u8"
rtmp_url = f"rtmp://{MEDIA_SERVER_RTMP_HOST}:1935/live/{STREAM_NAME}"

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("ตั้งค่าใน Larix Screencaster")
    st.write("ใส่ URL นี้ใน Larix Screencaster เพื่อส่งหน้าจอ iPhone")
    st.code(rtmp_url)

    qr = qrcode.make(rtmp_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=280)

    st.subheader("Viewer HLS URL")
    st.code(hls_url)

with col2:
    st.subheader("Live iPhone Screen")

    html = f"""
    <video id="video" controls autoplay muted playsinline
        style="width:100%; height:auto; background:#000;"></video>

    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
    const video = document.getElementById("video");
    const src = "{hls_url}";

    if (Hls.isSupported()) {{
        const hls = new Hls({{
            lowLatencyMode: true,
            liveSyncDurationCount: 2
        }});
        hls.loadSource(src);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function () {{
            video.play();
        }});
    }} else if (video.canPlayType("application/vnd.apple.mpegurl")) {{
        video.src = src;
        video.addEventListener("loadedmetadata", function () {{
            video.play();
        }});
    }} else {{
        document.body.innerHTML = "Browser ไม่รองรับ HLS";
    }}
    </script>
    """

    st.components.v1.html(html, height=700)
