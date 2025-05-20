from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.services import chat_service

router = APIRouter()


# Pydantic models for request/response
class ChannelCreate(BaseModel):
    team_id: str
    name: str
    description: Optional[str] = None


class ChannelOut(BaseModel):
    id: int
    team_id: str
    name: str
    description: Optional[str]
    created_at: str


class MessageCreate(BaseModel):
    team_id: str
    user: str
    message: str
    channel_id: int


class MessageOut(BaseModel):
    id: int
    team_id: str
    user: str
    message: str
    channel_id: int
    timestamp: str


# Channel endpoints
@router.post("/channels", response_model=ChannelOut)
async def create_channel(data: ChannelCreate):
    channel = await chat_service.create_channel(
        data.team_id, data.name, data.description
    )
    return ChannelOut(
        id=channel.id,
        team_id=channel.team_id,
        name=channel.name,
        description=channel.description,
        created_at=channel.created_at.isoformat(),
    )


@router.get("/channels", response_model=List[ChannelOut])
async def list_channels(team_id: str):
    channels = await chat_service.list_channels(team_id)
    return [
        ChannelOut(
            id=c.id,
            team_id=c.team_id,
            name=c.name,
            description=c.description,
            created_at=c.created_at.isoformat(),
        )
        for c in channels
    ]


@router.get("/channels/{channel_id}", response_model=ChannelOut)
async def get_channel(channel_id: int):
    channel = await chat_service.get_channel_by_id(channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return ChannelOut(
        id=channel.id,
        team_id=channel.team_id,
        name=channel.name,
        description=channel.description,
        created_at=channel.created_at.isoformat(),
    )


# Message endpoints
@router.post("/messages", response_model=MessageOut)
async def post_message(data: MessageCreate):
    msg = await chat_service.post_message(
        data.team_id, data.user, data.message, data.channel_id
    )
    return MessageOut(
        id=msg.id,
        team_id=msg.team_id,
        user=msg.user,
        message=msg.message,
        channel_id=msg.channel_id,
        timestamp=msg.timestamp.isoformat(),
    )


@router.get("/messages", response_model=List[MessageOut])
async def list_messages(team_id: str, channel_id: int, limit: int = 50):
    messages = await chat_service.list_messages(team_id, channel_id, limit)
    return [
        MessageOut(
            id=m.id,
            team_id=m.team_id,
            user=m.user,
            message=m.message,
            channel_id=m.channel_id,
            timestamp=m.timestamp.isoformat(),
        )
        for m in messages
    ]
