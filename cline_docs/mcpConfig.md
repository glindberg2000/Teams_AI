# MCP Configuration for Cursor (Local OpenMemory)

This document describes how to connect Cursor to a local OpenMemory MCP server for unified memory.

---

## MCP Server Endpoint

- **MCP Server URL:**
  - `http://localhost:8765/mcp/cursor/sse/<username>`
    - Replace `<username>` with your actual username (e.g., `greg`).

- **Example for this setup:**
  - `http://localhost:8765/mcp/cursor/sse/greg`

---

## Cursor Integration Command

To connect Cursor to the local OpenMemory MCP server, run:

```sh
npx install-mcp i http://localhost:8765/mcp/cursor/sse/greg --client cursor
```

- This will register Cursor as an MCP client with the OpenMemory server running locally.
- Make sure the server is running and accessible at the specified port.

---

## Notes
- If you change the MCP server port, update the URL accordingly.
- You can use this config as a template for other MCP-compatible clients.
- For team-wide or containerized deployments, document the shared endpoint and any authentication details here.

---

**Last updated:** $(date) 