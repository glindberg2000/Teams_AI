import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.models.chat import Base, Channel, Message
from datetime import datetime

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "chat_test.db")
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{os.path.abspath(TEST_DB_PATH)}"


@pytest.mark.asyncio
async def test_chat_db_integration():
    # Remove test DB if it exists
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    # Create engine and session
    engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    # Insert a channel
    async with AsyncSessionLocal() as session:
        channel = Channel(
            team_id="test_team", name="general", description="Test channel"
        )
        session.add(channel)
        await session.commit()
        await session.refresh(channel)
        assert channel.id is not None
        # Insert a message
        msg = Message(
            team_id="test_team",
            user="alice",
            message="Hello!",
            channel_id=channel.id,
            timestamp=datetime.utcnow(),
        )
        session.add(msg)
        await session.commit()
        await session.refresh(msg)
        assert msg.id is not None
        # Query back
        channels = (
            await session.execute(
                Channel.__table__.select().where(Channel.team_id == "test_team")
            )
        ).all()
        messages = (
            await session.execute(
                Message.__table__.select().where(Message.team_id == "test_team")
            )
        ).all()
        assert len(channels) == 1
        assert len(messages) == 1
    # Clean up
    await engine.dispose()
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
