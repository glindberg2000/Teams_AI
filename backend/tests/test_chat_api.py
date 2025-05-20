import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from fastapi.testclient import TestClient
from backend.main import app


def test_chat_api_endpoints():
    with TestClient(app) as client:
        # Create a channel
        resp = client.post(
            "/api/chat/channels",
            json={"team_id": "team2", "name": "random", "description": "Random chat"},
        )
        assert resp.status_code == 200
        channel = resp.json()
        assert channel["id"]
        channel_id = channel["id"]
        # List channels
        resp = client.get("/api/chat/channels", params={"team_id": "team2"})
        assert resp.status_code == 200
        channels = resp.json()
        assert any(c["name"] == "random" for c in channels)
        # Post a message
        resp = client.post(
            "/api/chat/messages",
            json={
                "team_id": "team2",
                "user": "alice",
                "message": "API test message",
                "channel_id": channel_id,
            },
        )
        assert resp.status_code == 200
        msg = resp.json()
        assert msg["id"]
        assert msg["message"] == "API test message"
        # List messages
        resp = client.get(
            "/api/chat/messages", params={"team_id": "team2", "channel_id": channel_id}
        )
        assert resp.status_code == 200
        messages = resp.json()
        assert any(m["message"] == "API test message" for m in messages)
