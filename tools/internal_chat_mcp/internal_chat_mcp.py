import sys  # Add sys for path inspection
import asyncio
import json
import os
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import websockets
from uuid import uuid4
import logging

# Set up logging very early
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for more verbosity
logger = logging.getLogger(__name__)

logger.debug("-----------------------------------------------------")
logger.debug(f"internal_chat_mcp.py: Script starting.")
logger.debug(f"internal_chat_mcp.py: Current Working Directory: {os.getcwd()}")
logger.debug(f"internal_chat_mcp.py: Python Executable: {sys.executable}")
logger.debug(f"internal_chat_mcp.py: Python Path: {sys.path}")
logger.debug(f"internal_chat_mcp.py: __name__ is: {__name__}")
logger.debug("-----------------------------------------------------")

app = FastAPI(title="Internal Chat MCP Server")

# Environment variables
CHAT_PORT = os.getenv("CHAT_PORT", "8000")
DEFAULT_TEAM_ID = os.getenv(
    "TEAM_ID", "team-8"
)  # Default used if not provided by caller context
WEBSOCKET_URL = f"ws://localhost:{CHAT_PORT}/ws/{{team_id}}"
logger.debug(
    f"internal_chat_mcp.py: CHAT_PORT={CHAT_PORT}, DEFAULT_TEAM_ID={DEFAULT_TEAM_ID}, WEBSOCKET_URL_template={WEBSOCKET_URL}"
)


# MCP Tool Definitions
class SendMessageInput(BaseModel):
    team_id: str
    user: str
    message: str


class SendMessageOutput(BaseModel):
    status: str


class GetUnreadMessagesInput(BaseModel):
    team_id: str
    limit: Optional[int] = 10


class Message(BaseModel):
    user: str
    message: str


class GetUnreadMessagesOutput(BaseModel):
    messages: List[Message]


# WebSocket Communication
async def send_chat_message(team_id: str, user: str, message: str) -> Dict:
    """Send a message to the chat server via WebSocket."""
    ws_url = WEBSOCKET_URL.format(team_id=team_id)
    logger.info(f"Sending message to {ws_url} from user {user}")
    try:
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({"user": user, "message": message}))
            # Assuming send is successful if no exception during send.
            # Some protocols might require waiting for an ack.
            # confirmation = await asyncio.wait_for(ws.recv(), timeout=2.0)
            # logger.info(f"Received confirmation: {confirmation}")
            return {"status": "ok"}
    except websockets.exceptions.ConnectionClosedError as e:
        logger.error(f"Connection closed while sending message to {ws_url}: {str(e)}")
        raise HTTPException(
            status_code=503, detail=f"WebSocket connection closed: {str(e)}"
        )
    except asyncio.TimeoutError:  # Timeout for connect or potential recv
        logger.error(f"Timeout sending/confirming message to {ws_url}")
        raise HTTPException(
            status_code=504, detail="WebSocket send/confirmation timeout"
        )
    except Exception as e:
        logger.error(f"Error sending message to {ws_url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")


async def get_unread_messages(team_id: str, limit: int) -> List[Dict]:
    """Retrieve unread messages from the chat server via WebSocket."""
    ws_url = WEBSOCKET_URL.format(team_id=team_id)
    messages = []
    logger.info(f"Attempting to retrieve {limit} messages from {ws_url}")
    try:
        async with websockets.connect(ws_url) as ws:
            # The prompt mentions "Assume server sends recent messages upon connection"
            for i in range(limit):
                try:
                    # Set a timeout for each ws.recv() call
                    msg_str = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    data = json.loads(msg_str)
                    if "user" in data and "message" in data:
                        messages.append(
                            {"user": data["user"], "message": data["message"]}
                        )
                        logger.debug(f"Received message: {data}")
                    else:
                        logger.warning(
                            f"Received malformed message structure: {data} from {ws_url}"
                        )
                except asyncio.TimeoutError:
                    logger.info(
                        f"Timeout waiting for message {i+1}/{limit} from {ws_url}. Received {len(messages)} so far."
                    )
                    break  # Stop if no message received within timeout
                except json.JSONDecodeError as e:
                    logger.error(
                        f"Failed to decode JSON message from {ws_url}: '{msg_str}', error: {e}"
                    )
                    # Optionally, continue to try and get more messages or break
                except websockets.exceptions.ConnectionClosed:
                    logger.info(
                        f"Connection closed by server {ws_url} while receiving message {i+1}/{limit}. Received {len(messages)} so far."
                    )
                    break  # Connection closed by server
            logger.info(f"Retrieved {len(messages)} messages from {ws_url}")
            return messages
    except (
        websockets.exceptions.ConnectionClosedError
    ) as e:  # Error during initial connect
        logger.error(f"Connection to {ws_url} failed or closed prematurely: {str(e)}")
        if not messages:  # If connection fails before any messages, it's a hard error
            raise HTTPException(
                status_code=503,
                detail=f"WebSocket connection failed or closed: {str(e)}",
            )
        return messages  # Otherwise, return what was gathered
    except asyncio.TimeoutError:  # Timeout during initial connect
        logger.error(f"Timeout establishing connection with {ws_url}")
        if not messages:
            raise HTTPException(status_code=504, detail="WebSocket connection timeout")
        return messages
    except Exception as e:  # Other errors during connect or setup
        logger.error(f"Error retrieving messages from {ws_url}: {str(e)}")
        if not messages:  # If critical error before any messages
            raise HTTPException(
                status_code=500, detail=f"Failed to retrieve messages: {str(e)}"
            )
        return messages


# MCP Manifest
MANIFEST = {
    "version": "1.0",
    "tools": [
        {
            "name": "send_message",
            "description": "Send a message to the team chat server.",
            "input_schema": SendMessageInput.model_json_schema(),
            "output_schema": SendMessageOutput.model_json_schema(),
        },
        {
            "name": "get_unread_messages",
            "description": "Retrieve unread messages from the team chat server.",
            "input_schema": GetUnreadMessagesInput.model_json_schema(),
            "output_schema": GetUnreadMessagesOutput.model_json_schema(),
        },
    ],
}


# MCP Endpoints
@app.get("/mcp/manifest")
async def get_mcp_manifest():
    """Return the MCP manifest for tool discovery."""
    logger.info("Manifest requested.")
    return MANIFEST


@app.post("/mcp/call/{tool_name}")
async def call_mcp_tool(tool_name: str, input_data: Dict):
    """Handle MCP tool calls."""
    logger.info(f"Received call for tool: {tool_name} with data: {input_data}")
    if tool_name == "send_message":
        try:
            input_model = SendMessageInput(**input_data)
            result = await send_chat_message(
                input_model.team_id, input_model.user, input_model.message
            )
            return SendMessageOutput(**result).model_dump()
        except ValueError as e:  # Pydantic validation error
            logger.error(f"Pydantic validation error for send_message: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
        except HTTPException:  # Re-raise HTTPExceptions from send_chat_message
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error processing send_message: {str(e)}", exc_info=True
            )
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(e)}"
            )

    elif tool_name == "get_unread_messages":
        try:
            input_model = GetUnreadMessagesInput(**input_data)
            messages_data = await get_unread_messages(
                input_model.team_id, input_model.limit
            )

            valid_messages = []
            for msg_dict in messages_data:  # messages_data is already List[Dict]
                try:
                    valid_messages.append(Message(**msg_dict))
                except (
                    ValueError
                ) as ve:  # Pydantic validation error for a single message
                    logger.warning(
                        f"Skipping malformed message data during Pydantic parsing: {msg_dict}, error: {ve}"
                    )

            return GetUnreadMessagesOutput(messages=valid_messages).model_dump()
        except ValueError as e:  # Pydantic validation error for GetUnreadMessagesInput
            logger.error(
                f"Pydantic validation error for get_unread_messages input: {str(e)}"
            )
            raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
        except HTTPException:  # Re-raise HTTPExceptions from get_unread_messages
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error processing get_unread_messages: {str(e)}",
                exc_info=True,
            )
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(e)}"
            )
    else:
        logger.warning(f"Tool not found: {tool_name}")
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")


@app.get("/mcp/sse")
async def mcp_sse_endpoint():
    """SSE endpoint for MCP protocol communication."""
    request_id = str(uuid4())
    logger.info(f"SSE connection established: {request_id}")

    async def event_generator():
        try:
            # Send an initial message, potentially manifest or capabilities, if protocol requires.
            # For now, just a ping.
            initial_event = {
                "event": "mcp_connected",
                "id": str(uuid4()),
                "message": "MCP SSE connection established",
            }
            yield f"data: {json.dumps(initial_event)}\n\n"
            logger.debug(f"Sent initial SSE event for {request_id}: {initial_event}")

            while True:
                await asyncio.sleep(10)  # Keep-alive interval
                ping_event = {"event": "ping", "id": str(uuid4())}
                logger.debug(f"SSE ping for {request_id}: {ping_event}")
                yield f"data: {json.dumps(ping_event)}\n\n"
        except asyncio.CancelledError:
            logger.info(f"SSE connection {request_id} cancelled by client.")
            # This is a normal way for a client to disconnect.
            raise  # Important to re-raise to stop the generator.
        except Exception as e:
            logger.error(
                f"Error in SSE event generator for {request_id}: {e}", exc_info=True
            )
            # Optionally, try to send an error event to the client if the connection is still writable
            try:
                error_event = {
                    "event": "error",
                    "id": str(uuid4()),
                    "message": f"Server error in SSE stream: {str(e)}",
                }
                yield f"data: {json.dumps(error_event)}\n\n"
            except Exception as send_err:
                logger.error(
                    f"Failed to send error event over SSE for {request_id}: {send_err}"
                )
            raise  # Re-raise the original exception to ensure the stream closes.

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# Run the server
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Uvicorn server for Internal Chat MCP on http://0.0.0.0:6969")
    try:
        uvicorn.run(app, host="0.0.0.0", port=6969, log_level="info", reload=False)
    except Exception as e_uvicorn:
        logger.error(f"CRITICAL: Uvicorn failed to start: {e_uvicorn}", exc_info=True)
        # Potentially re-raise or exit to signal failure more strongly if needed
        raise
