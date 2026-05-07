import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(
    page_title="iPhone Screen Viewer",
    layout="wide",
)

st.title("iPhone Screen Share Viewer")

st.write("ใช้ Larix Screencaster บน iPhone ส่ง RTMP เข้ามาที่ MediaMTX แล้วดูผ่าน HLS บนหน้านี้")

SERVER_URL = st.text_input(
    "Render / MediaMTX URL",
    value="https://YOUR-RENDER-NAME.onrender.com",
)

STREAM_NAME = st.text_input(
    "Stream name",
    value="iphone",
)

server = SERVER_URL.rstrip("/")

rtmp_url = server.replace("https://", "rtmp://").replace("http://", "rtmp://") + f"/live/{STREAM_NAME}"
hls_url = f"{server}/live/{STREAM_NAME}/index.m3u8"

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("ตั้งค่าใน Larix Screencaster")

    st.write("ใส่ URL นี้ใน Larix Screencaster")
    st.code(rtmp_url)

    qr = qrcode.make(rtmp_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=280)

    st.info(
        "ใน Larix Screencaster ให้เลือก RTMP/RTMPS แล้วใส่ URL ตามนี้ "
        "จากนั้นเริ่ม Screen Broadcast"
    )

    st.subheader("HLS URL")
    st.code(hls_url)

with col2:
    st.subheader("Live iPhone Screen")

    player_html = f"""
    <video
        id="video"
        controls
        autoplay
        muted
        playsinline
        style="width:100%; max-height:80vh; background:#000;"
    ></video>

    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
    const video = document.getElementById('video');
    const videoSrc = "{hls_url}";

    if (Hls.isSupported()) {{
        const hls = new Hls({{
            liveSyncDurationCount: 2,
            lowLatencyMode: true
        }});
        hls.loadSource(videoSrc);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function() {{
            video.play();
        }});
    }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
        video.src = videoSrc;
        video.addEventListener('loadedmetadata', function() {{
            video.play();
        }});
    }} else {{
        document.body.innerHTML += "<p>Browser นี้ไม่รองรับ HLS</p>";
    }}
    </script>
    """

    st.components.v1.html(player_html, height=700)
