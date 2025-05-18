import asyncio
from internal_chat_mcp.tools.send_message import SendMessageTool, SendMessageInput
from internal_chat_mcp.tools.get_unread_messages import (
    GetUnreadMessagesTool,
    GetUnreadMessagesInput,
)
from internal_chat_mcp.tools.wait_for_message import (
    WaitForMessageTool,
    WaitForMessageInput,
)


async def test_send_message():
    print("Testing SendMessageTool...")
    tool = SendMessageTool()
    input_data = SendMessageInput(
        team_id="team-9",
        user="test-bot",
        message="Hello from test_chat_tools.py",
        backend_host="localhost:8000",
    )
    result = await tool.execute(input_data)
    print("SendMessageTool result:", result)


async def test_get_unread_messages():
    print("Testing GetUnreadMessagesTool...")
    tool = GetUnreadMessagesTool()
    input_data = GetUnreadMessagesInput(
        team_id="team-9", backend_host="localhost:8000", limit=5
    )
    result = await tool.execute(input_data)
    print("GetUnreadMessagesTool result:", result)


async def test_wait_for_message():
    print("Testing WaitForMessageTool (timeout=5s)...")
    tool = WaitForMessageTool()
    input_data = WaitForMessageInput(
        team_id="team-9", backend_host="localhost:8000", timeout=5
    )
    result = await tool.execute(input_data)
    print("WaitForMessageTool result:", result)


async def main():
    try:
        await test_send_message()
    except Exception as e:
        print("SendMessageTool error:", e)
    try:
        await test_get_unread_messages()
    except Exception as e:
        print("GetUnreadMessagesTool error:", e)
    try:
        await test_wait_for_message()
    except Exception as e:
        print("WaitForMessageTool error:", e)


if __name__ == "__main__":
    asyncio.run(main())
