from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.services import chat_service
from backend.services import chat_service as cs
from backend.services.in_memory_chat import store_message
from backend.ws_manager import manager
import os

router = APIRouter()


class MessageCreate(BaseModel):
    team_id: str
    user: str
    message: str
    channel_id: Optional[int] = None


class MessageOut(BaseModel):
    id: int
    team_id: str
    user: str
    message: str
    channel_id: int
    timestamp: str


@router.post("/messages", response_model=MessageOut)
async def post_message(data: MessageCreate):
    print(f"[DEBUG] /api/chat/messages called with: {data}")
    USE_PERSISTENT_CHAT = os.getenv("USE_PERSISTENT_CHAT", "false").lower() == "true"
    if USE_PERSISTENT_CHAT:
        # ... existing persistent logic ...
        channel_id = data.channel_id
        if channel_id is None:
            channels = await cs.list_channels(data.team_id)
            channel_obj = next((c for c in channels if c.name == "general"), None)
            if not channel_obj:
                channel_obj = await cs.create_channel(data.team_id, "general")
            channel_id = channel_obj.id
        msg = await chat_service.post_message(
            data.team_id, data.user, data.message, channel_id
        )
        # Broadcast to WebSocket clients in this team/channel
        try:
            channels = await cs.list_channels(data.team_id)
            channel_obj = next((c for c in channels if c.id == channel_id), None)
            channel_name = channel_obj.name if channel_obj else "general"
            await manager.broadcast(
                data.team_id,
                channel_name,
                {
                    "user": data.user,
                    "message": data.message,
                    "timestamp": msg.timestamp.isoformat(),
                    "channel": channel_name,
                },
            )
        except Exception as e:
            print(f"[CHAT][REST] Could not broadcast to WebSocket clients: {e}")
        return MessageOut(
            id=msg.id,
            team_id=msg.team_id,
            user=msg.user,
            message=msg.message,
            channel_id=msg.channel_id,
            timestamp=msg.timestamp.isoformat(),
        )
    else:
        # In-memory mode: always use 'general' channel and channel_id=0
        channel = "general"
        channel_id = 0
        msg = store_message(data.team_id, data.user, data.message, channel=channel)
        msg_dict = {
            "user": data.user,
            "message": data.message,
            "timestamp": msg["timestamp"],
            "channel": channel,
        }
        await manager.broadcast(data.team_id, channel, msg_dict)
        return MessageOut(
            id=msg["id"],
            team_id=data.team_id,
            user=data.user,
            message=data.message,
            channel_id=channel_id,
            timestamp=msg["timestamp"],
        )


@router.get("/config")
def get_chat_config():
    return {"persistent": os.getenv("USE_PERSISTENT_CHAT", "false").lower() == "true"}
