from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frames = {}


@app.get("/")
def home():
    return {"status": "ok"}


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
        media_type="image/jpeg"
    )
