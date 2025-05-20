from backend.services.db import AsyncSessionLocal
from backend.models.chat import Channel, Message
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import List, Optional


# Channel CRUD
async def create_channel(
    team_id: str, name: str, description: Optional[str] = None
) -> Channel:
    async with AsyncSessionLocal() as session:
        channel = Channel(team_id=team_id, name=name, description=description)
        session.add(channel)
        await session.commit()
        await session.refresh(channel)
        return channel


async def list_channels(team_id: str) -> List[Channel]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Channel).where(Channel.team_id == team_id)
        )
        return result.scalars().all()


async def get_channel_by_id(channel_id: int) -> Optional[Channel]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Channel).where(Channel.id == channel_id))
        return result.scalar_one_or_none()


# Message CRUD
async def post_message(
    team_id: str, user: str, message: str, channel_id: int
) -> Message:
    async with AsyncSessionLocal() as session:
        msg = Message(
            team_id=team_id,
            user=user,
            message=message,
            channel_id=channel_id,
            timestamp=datetime.utcnow(),
        )
        session.add(msg)
        await session.commit()
        await session.refresh(msg)
        return msg


async def list_messages(
    team_id: str, channel_id: int, limit: int = 50
) -> List[Message]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Message)
            .where((Message.team_id == team_id) & (Message.channel_id == channel_id))
            .order_by(Message.timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()
