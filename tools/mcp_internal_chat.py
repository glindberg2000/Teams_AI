#!/usr/bin/env python3
"""
MCP Internal Chat Tool (Python)

Usage (CLI):
  python tools/mcp_internal_chat.py --team Team8 --user Alice --send "Hello, world!"
  python tools/mcp_internal_chat.py --team Team8 --user Alice  # interactive mode

Env/config:
  TEAM_ID: team name (default: Team8)
  USER: username (default: Agent)
  CHAT_SERVER_URL: ws://host:port/ws/{team_id} (default: ws://localhost:8787/ws/{team_id})
  CHAT_PORT: port (default: 8787)

Importable:
  from mcp_internal_chat import ChatClient

"""
import asyncio
import argparse
import os
import sys
import json
import websockets


class ChatClient:
    def __init__(self, team_id=None, user=None, url=None, port=None):
        self.team_id = team_id or os.environ.get("TEAM_ID", "Team8")
        self.user = user or os.environ.get("USER", "Agent")
        self.port = port or os.environ.get("CHAT_PORT", 8787)
        self.url = (
            url
            or os.environ.get("CHAT_SERVER_URL")
            or f"ws://localhost:{self.port}/ws/{self.team_id}"
        )
        self.ws = None
        self.messages = []

    async def connect(self):
        self.ws = await websockets.connect(self.url)
        print(f"[Connected to {self.url} as {self.user}]")

    async def send(self, message, channel=None):
        data = {"user": self.user, "message": message}
        if channel:
            data["channel"] = channel
        await self.ws.send(json.dumps(data))

    async def receive(self, filter_user=None, filter_channel=None):
        while True:
            msg = await self.ws.recv()
            try:
                data = json.loads(msg)
                self.messages.append(data)
                if (not filter_user or data.get("user") == filter_user) and (
                    not filter_channel or data.get("channel") == filter_channel
                ):
                    print(f"[{data.get('user')}] {data.get('message')}")
            except Exception as e:
                print(f"[Error parsing message: {e}] {msg}")

    async def interactive(self):
        await self.connect()
        loop = asyncio.get_event_loop()
        recv_task = loop.create_task(self.receive())
        try:
            while True:
                msg = await loop.run_in_executor(None, sys.stdin.readline)
                msg = msg.strip()
                if msg:
                    await self.send(msg)
        except (KeyboardInterrupt, EOFError):
            print("\n[Exiting chat]")
        finally:
            recv_task.cancel()
            await self.ws.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Internal Chat Tool")
    parser.add_argument("--team", type=str, help="Team ID (default: Team8)")
    parser.add_argument("--user", type=str, help="Username (default: Agent)")
    parser.add_argument("--send", type=str, help="Send a single message and exit")
    parser.add_argument("--port", type=int, help="Chat server port (default: 8787)")
    parser.add_argument(
        "--url", type=str, help="Full WebSocket URL (overrides port/team)"
    )
    args = parser.parse_args()

    client = ChatClient(team_id=args.team, user=args.user, url=args.url, port=args.port)

    async def main():
        await client.connect()
        if args.send:
            await client.send(args.send)
            await asyncio.sleep(0.5)
            await client.ws.close()
        else:
            await client.interactive()

    asyncio.run(main())
