#!/usr/bin/env python3
"""
Internal Chat MCP Server (MCP Python)

- Exposes send_message and get_unread_messages as MCP tools
- Uses mcp package for Cursor/Claude/Context7 compatibility
- Reuses ChatClient from mcp_internal_chat.py
- Does not affect main backend or chat server
"""
import os

if "LOG_LEVEL" in os.environ:
    os.environ["LOG_LEVEL"] = os.environ["LOG_LEVEL"].upper()
else:
    os.environ["LOG_LEVEL"] = "INFO"
import re
import asyncio
from mcp.server.fastmcp import FastMCP
from typing import Optional
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

mcp = FastMCP("Internal Chat MCP")


@mcp.tool()
async def send_message(
    team_id: str, user: str, message: str, channel: Optional[str] = None
) -> dict:
    """Send a message to the team chat."""
    client = ChatClient(team_id=team_id, user=user)
    await client.connect()
    await client.send(message, channel=channel)
    await asyncio.sleep(0.2)
    await client.ws.close()
    return {"status": "ok"}


@mcp.tool()
async def get_unread_messages(
    team_id: str,
    since_message_id: Optional[str] = None,
    limit: Optional[int] = 50,
    sender_id: Optional[str] = None,
    channel: Optional[str] = None,
    dm_only: Optional[bool] = False,
    mention_only: Optional[bool] = False,
    content_regex: Optional[str] = None,
) -> dict:
    """Get unread messages for a team with filters (user, channel, DM, etc)."""
    client = ChatClient(team_id=team_id)
    await client.connect()
    messages = []
    count = 0
    try:
        while count < (limit or 50):
            msg = await client.ws.recv()
            try:
                data = mcp_internal_chat.json.loads(msg)
                # Filtering
                if sender_id and data.get("user") != sender_id:
                    continue
                if channel and data.get("channel") != channel:
                    continue
                if dm_only and not data.get("dm", False):
                    continue
                if mention_only and (
                    not data.get("message") or team_id not in data.get("message")
                ):
                    continue
                if content_regex and not re.search(
                    content_regex, data.get("message", "")
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
    mcp.run(http=True)
