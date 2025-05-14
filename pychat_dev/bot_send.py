import asyncio
import websockets
import json
import sys
import datetime

BOSS_NAME = "boss"


async def wait_for_task(uri, botname):
    async with websockets.connect(uri) as websocket:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{botname} logged in at {now} and waiting for a task...")
        while True:
            msg = await websocket.recv()
            print("Received message:", msg)
            # Only respond to messages from the boss (format: 'boss: ...')
            if msg.startswith(f"{BOSS_NAME}:"):
                print("Received task from boss.")
                await websocket.send(
                    json.dumps({"user": botname, "text": "Acknowledged: " + msg})
                )
                print("Sent: Acknowledged. Logging off to do work...")
                break
            else:
                print("Ignored non-boss or system message.")


async def report_and_wait(uri, botname, summary):
    async with websockets.connect(uri) as websocket:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{botname} logged in at {now} to post summary...")
        await websocket.send(json.dumps({"user": botname, "text": summary}))
        print("Posted summary. Waiting for a reply from the boss...")
        while True:
            msg = await websocket.recv()
            print("Received reply:", msg)
            # Only respond to messages from the boss
            if msg.startswith(f"{botname}:"):
                print("Ignored self-echo.")
                continue  # Ignore own messages
            if not msg.startswith(f"{BOSS_NAME}:"):
                print("Ignored non-boss or system message.")
                continue
            await websocket.send(
                json.dumps({"user": botname, "text": "Acknowledged: " + msg})
            )
            print("Sent: Acknowledged. Logging off.")
            break


if __name__ == "__main__":
    uri = "ws://localhost:8000/ws"
    botname = "bot1"
    if len(sys.argv) == 2 and sys.argv[1] == "wait":
        asyncio.run(wait_for_task(uri, botname))
    elif len(sys.argv) >= 3 and sys.argv[1] == "report":
        summary = sys.argv[2]
        asyncio.run(report_and_wait(uri, botname, summary))
    else:
        print("Usage:")
        print("  python bot_send.py wait")
        print("  python bot_send.py report 'Work complete for: ...'")
