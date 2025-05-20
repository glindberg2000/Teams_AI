import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.models.chat import Base
from backend.services import chat_service

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "chat_service_test.db")
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{os.path.abspath(TEST_DB_PATH)}"


@pytest.mark.asyncio
async def test_channel_and_message_crud():
    # Remove test DB if it exists
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    # Create engine and session
    engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Patch AsyncSessionLocal for this test
    orig_session_local = chat_service.AsyncSessionLocal
    chat_service.AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    try:
        # Create a channel
        channel = await chat_service.create_channel("team1", "general", "General chat")
        assert channel.id is not None
        # List channels
        channels = await chat_service.list_channels("team1")
        assert len(channels) == 1
        assert channels[0].name == "general"
        # Post a message
        msg = await chat_service.post_message(
            "team1", "bob", "Hello, world!", channel.id
        )
        assert msg.id is not None
        assert msg.channel_id == channel.id
        # List messages
        messages = await chat_service.list_messages("team1", channel.id)
        assert len(messages) == 1
        assert messages[0].message == "Hello, world!"
    finally:
        chat_service.AsyncSessionLocal = orig_session_local
        await engine.dispose()
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
