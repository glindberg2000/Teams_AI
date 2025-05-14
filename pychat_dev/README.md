# PyChat: Minimal FastAPI WebSocket Chat Server

PyChat is a simple, real-time chat server built with FastAPI and WebSockets. It supports both human users (via a web UI) and bots (via WebSocket API), with no authentication or email required.

## Features
- Real-time chat via WebSockets
- No authentication, no email—just username and message
- Works for bots (WebSocket API) and humans (web UI)
- Bots can wait for tasks, acknowledge, do work, and report back
- ARM/Mac/Windows/Linux compatible

## Quick Start

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```sh
   uvicorn main:app --reload
   ```

3. **Open the chat UI:**
   - Go to [http://localhost:8000](http://localhost:8000) in your browser
   - Enter a username and message, click Send

4. **Bots:**
   - Connect to `ws://localhost:8000/ws` using any WebSocket client
   - Send JSON: `{ "user": "botname", "text": "hello" }`
   - Wait for messages from the server (connection stays open)

## Example Bot (Python)
```python
import asyncio
import websockets
import json

async def bot():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"user": "bot1", "text": "Hello from bot!"}))
        while True:
            msg = await websocket.recv()
            print("Received:", msg)

asyncio.run(bot())
```

## Bot Workflow Example
- Bot logs in and waits for a task: `python bot_send.py wait`
- Human sends a task from the UI
- Bot acknowledges and logs off
- Bot does the work (e.g., writes a doc)
- Bot logs in and posts a summary: `python bot_send.py report "Work complete for: ..."`
- Bot waits for a reply or new task, acknowledges, and logs off if the task is complete
- Bot can also ask questions: `python bot_send.py ask "Question for boss: ..."`

## Last Updated
- 2025-05-11

---

For more, see FastAPI WebSocket docs: https://fastapi.tiangolo.com/advanced/websockets/ 