#!/usr/bin/env python3
"""
Internal Chat MCP Server (FastAPI)

- Exposes /mcp/manifest, /mcp/send_message, /mcp/get_unread_messages
- Reuses ChatClient from mcp_internal_chat.py
- Filtering for get_unread_messages: user, channel, dm_only, mention_only, content_regex
- Does not break CLI or web UI
"""
import os
import re
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import importlib.util
import sys

# Import ChatClient from mcp_internal_chat.py
spec = importlib.util.spec_from_file_location(
    "mcp_internal_chat", os.path.join(os.path.dirname(__file__), "mcp_internal_chat.py")
)
mcp_internal_chat = importlib.util.module_from_spec(spec)
sys.modules["mcp_internal_chat"] = mcp_internal_chat
spec.loader.exec_module(mcp_internal_chat)
ChatClient = mcp_internal_chat.ChatClient

app = FastAPI()


# MCP Manifest
@app.get("/mcp/manifest")
def manifest():
    return {
        "tools": [
            {
                "name": "send_message",
                "description": "Send a message to the team chat.",
                "parameters": {
                    "team_id": "string",
                    "user": "string",
                    "message": "string",
                },
            },
            {
                "name": "get_unread_messages",
                "description": "Get unread messages for a team with filters (user, channel, DM, etc).",
                "parameters": {
                    "team_id": "string",
                    "since_message_id": "string (optional)",
                    "limit": "integer (optional)",
                    "sender_id": "string (optional)",
                    "channel": "string (optional)",
                    "dm_only": "boolean (optional)",
                    "mention_only": "boolean (optional)",
                    "content_regex": "string (optional)",
                },
            },
        ]
    }


class SendMessageRequest(BaseModel):
    team_id: str
    user: str
    message: str
    channel: Optional[str] = None


@app.post("/mcp/send_message")
async def send_message(req: SendMessageRequest):
    client = ChatClient(team_id=req.team_id, user=req.user)
    await client.connect()
    await client.send(req.message, channel=req.channel)
    await asyncio.sleep(0.2)
    await client.ws.close()
    return {"status": "ok"}


class GetUnreadMessagesRequest(BaseModel):
    team_id: str
    since_message_id: Optional[str] = None
    limit: Optional[int] = 50
    sender_id: Optional[str] = None
    channel: Optional[str] = None
    dm_only: Optional[bool] = False
    mention_only: Optional[bool] = False
    content_regex: Optional[str] = None


@app.post("/mcp/get_unread_messages")
async def get_unread_messages(req: GetUnreadMessagesRequest):
    client = ChatClient(team_id=req.team_id)
    await client.connect()
    messages = []
    count = 0
    try:
        while count < (req.limit or 50):
            msg = await client.ws.recv()
            try:
                data = mcp_internal_chat.json.loads(msg)
                # Filtering
                if req.sender_id and data.get("user") != req.sender_id:
                    continue
                if req.channel and data.get("channel") != req.channel:
                    continue
                if req.dm_only and not data.get("dm", False):
                    continue
                if req.mention_only and (
                    not data.get("message") or req.team_id not in data.get("message")
                ):
                    continue
                if req.content_regex and not re.search(
                    req.content_regex, data.get("message", "")
                ):
                    continue
                messages.append(data)
                count += 1
            except Exception:
                continue
    except Exception:
        pass
    await client.ws.close()
    return {"messages": messages}


if __name__ == "__main__":
    port = int(os.environ.get("MCP_CHAT_PORT", 8790))
    uvicorn.run(
        "tools.mcp_internal_chat_mcp:app", host="0.0.0.0", port=port, reload=True
    )
