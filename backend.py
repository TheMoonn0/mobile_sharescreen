from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()
frames = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "backend ok"}

@app.websocket("/upload/{room}")
async def upload(websocket: WebSocket, room: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            frames[room] = data
    except WebSocketDisconnect:
        pass

@app.get("/frame/{room}")
def frame(room: str):
    if room not in frames:
        return Response(status_code=204)
    return Response(
        content=frames[room],
        media_type="image/jpeg",
        headers={"Cache-Control": "no-store"},
    )

@app.get("/send/{room}", response_class=HTMLResponse)
def sender_page(room: str):
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mobile Sender</title>
</head>
<body>
  <h2>Mobile Sender Room: {room}</h2>
  <p>กด Start เพื่อทดสอบส่งกล้องเข้า Streamlit</p>
  <button onclick="start()">Start Camera Stream</button>
  <br><br>
  <video id="video" autoplay playsinline muted style="width:100%;max-width:420px;"></video>
  <canvas id="canvas" style="display:none;"></canvas>

<script>
async function start() {{
  const protocol = location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(`${{protocol}}://${{location.host}}/upload/{room}`);

  const stream = await navigator.mediaDevices.getUserMedia({{
    video: true,
    audio: false
  }});

  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");

  video.srcObject = stream;

  video.onloadedmetadata = () => {{
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    setInterval(() => {{
      if (ws.readyState !== WebSocket.OPEN) return;

      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob((blob) => {{
        if (blob) ws.send(blob);
      }}, "image/jpeg", 0.65);

    }}, 100);
  }};
}}
</script>
</body>
</html>
"""
