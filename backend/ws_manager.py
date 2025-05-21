from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # Now tracks (team_id, channel_id) -> list of websockets
        self.active_connections: Dict[tuple, List[WebSocket]] = {}

    async def connect(self, team_id: str, channel_id: str, websocket: WebSocket):
        await websocket.accept()
        key = (team_id, channel_id)
        if key not in self.active_connections:
            self.active_connections[key] = []
        self.active_connections[key].append(websocket)

    def disconnect(self, team_id: str, channel_id: str, websocket: WebSocket):
        key = (team_id, channel_id)
        if key in self.active_connections:
            self.active_connections[key].remove(websocket)
            if not self.active_connections[key]:
                del self.active_connections[key]

    async def broadcast(self, team_id: str, channel_id: str, message: dict):
        key = (team_id, channel_id)
        if key in self.active_connections:
            for connection in self.active_connections[key]:
                await connection.send_json(message)


manager = ConnectionManager()
