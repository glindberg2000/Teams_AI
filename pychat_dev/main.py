from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>PyChat</title>
    </head>
    <body>
        <h1>PyChat Room</h1>
        <input id="username" placeholder="Username" />
        <input id="messageText" placeholder="Message" />
        <button onclick="sendMessage()">Send</button>
        <ul id="messages"></ul>
        <script>
            let ws;
            function connect() {
                ws = new WebSocket(`ws://${location.host}/ws`);
                ws.onmessage = function(event) {
                    const messages = document.getElementById('messages');
                    const msg = document.createElement('li');
                    msg.textContent = event.data;
                    messages.appendChild(msg);
                };
            }
            function sendMessage() {
                const user = document.getElementById('username').value;
                const text = document.getElementById('messageText').value;
                ws.send(JSON.stringify({user, text}));
            }
            connect();
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"[SERVER] Client connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"[SERVER] Client disconnected: {websocket.client}")

    async def broadcast(self, message: str):
        print(f"[SERVER] Broadcasting message: {message}")
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get(request: Request):
    print(f"[SERVER] Web UI loaded from {request.client.host}")
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"[SERVER] Received raw data: {data}")
            # Expecting JSON: {"user": ..., "text": ...}
            import json

            msg = json.loads(data)
            user = msg.get("user", "anonymous")
            text = msg.get("text", "")
            print(f"[SERVER] Message from {user}: {text}")
            await manager.broadcast(f"{user}: {text}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"[SERVER] WebSocketDisconnect for {websocket.client}")
        await manager.broadcast("A user left the chat")
