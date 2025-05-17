## Team Chat Server Port

The internal team chat server (WebSocket) now defaults to port 8787 to avoid conflicts with other services.

- To change the port, set the `TEAM_CHAT_PORT` environment variable:
  
  ```sh
  export TEAM_CHAT_PORT=9001
  uvicorn backend.main:app --port $TEAM_CHAT_PORT
  ```

- The MCP tool and UI should connect to the port specified by `TEAM_CHAT_PORT` (default: 8787). 