# MCP Tool Setup & Extension Guide

*Author: Cline AI | Date: 2025-05-17*

---

## Overview
This guide documents the process for setting up, extending, and maintaining custom MCP (Model Context Protocol) tools in the LedgerFlow_AI_Team codebase. It is intended for developers and maintainers who need to add new automation, integrations, or agent capabilities via MCP.

---

## MCP Tool Architecture
- Each MCP tool is a Python package (directory with __init__.py) under `tools/` (e.g., `tools/internal_chat_mcp/`).
- Each tool exposes one or more callable "tools" (Python classes) in a `tools/` submodule.
- The MCP server is started via a CLI entrypoint, defined in `pyproject.toml`.
- Tools are registered in `tools/__init__.py` and exposed to the MCP runtime.

---

## Scaffolding a New MCP Tool
1. **Create the directory structure:**
   ```
   tools/my_new_mcp/
     pyproject.toml
     my_new_mcp/
       __init__.py
       server.py
       tools/
         __init__.py
         my_tool.py
   ```
2. **Add a `pyproject.toml`:**
   - Set `[project]` metadata.
   - Add `[project.scripts]` for the CLI entrypoint:
     ```toml
     [project.scripts]
     my-new-mcp = "my_new_mcp.server:main"
     ```
3. **Implement the server entrypoint:**
   - In `my_new_mcp/server.py`, define a `main()` function that starts the MCP server.
   - Support `--mode sse` and/or `--mode stdio` for server operation.
4. **Register tools:**
   - In `my_new_mcp/tools/__init__.py`, import and add your tool classes to `__all__`.
   - Each tool should subclass the base `Tool` class and implement `execute()`.

---

## Registering and Exposing Tools
- Tools are discovered via the `__all__` list in `tools/__init__.py`.
- Each tool must have a unique `name` and a clear `description`.
- Input/output schemas should use Pydantic models for validation.

---

## CLI Entrypoint & MCP Server
- The CLI entrypoint is created via `[project.scripts]` in `pyproject.toml`.
- After editing, reinstall the package:
  ```sh
  pip install -e .
  ```
- The CLI executable will appear in `.venv/bin/` (e.g., `.venv/bin/my-new-mcp`).
- Run with `--mode sse` or `--mode stdio` to start the server.

---

## Updating .cursor/mcp.json
- Add a new entry for your tool:
  ```json
  "my_new_mcp": {
    "command": "/path/to/.venv/bin/my-new-mcp",
    "args": ["--mode", "sse", "--port", "8001"],
    "cwd": "/path/to/project/root",
    "env": {"MY_ENV_VAR": "value"}
  }
  ```
- Adjust `args`, `cwd`, and `env` as needed for your tool.

---

## Testing & Verifying Tools
- Start the MCP tool via your tool manager (Cursor, etc.).
- The dot should turn green if the server starts successfully.
- Use the MCP tool interface to call your tool and verify correct results.

---

## Best Practices
- Use clear, unique names for tools and entrypoints.
- Document each tool in `cline_docs/mcp_tool_setup.md` and reference in `mcp_tools.md`.
- Keep input/output schemas strict and well-documented.
- Remove or comment out test tools in production.
- Use virtual environments for isolation.

---

## Troubleshooting
- **No CLI executable?**
  - Check `[project.scripts]` in `pyproject.toml` and reinstall with `pip install -e .`.
- **Import errors?**
  - Ensure all modules are in the correct package structure and `__init__.py` files exist.
- **Server won't start?**
  - Run the CLI manually and check for errors.
- **Tool not visible?**
  - Ensure it is imported and listed in `__all__` in `tools/__init__.py`.
- **Port conflicts?**
  - Change the `--port` argument in `.cursor/mcp.json`.

---

## Example: Adding a New Tool
1. Create `tools/my_new_mcp/tools/my_tool.py`:
   ```python
   from ..interfaces.tool import Tool, BaseToolInput, ToolResponse
   from pydantic import Field

   class MyToolInput(BaseToolInput):
       value: int = Field(..., description="A value to process")

   class MyToolOutput(BaseModel):
       result: int

   class MyTool(Tool):
       name = "MyTool"
       description = "Doubles the input value."
       input_model = MyToolInput
       output_model = MyToolOutput

       async def execute(self, input_data: MyToolInput) -> ToolResponse:
           return ToolResponse.from_model(MyToolOutput(result=input_data.value * 2))
   ```
2. Import and add to `__all__` in `tools/__init__.py`:
   ```python
   from .my_tool import MyTool
   __all__ = ["MyTool"]
   ```
3. Restart the MCP server and verify the tool is available.

---

## Reference
- See [docs/projects/ledgerflow/mcp_tools.md](../docs/projects/ledgerflow/mcp_tools.md) for high-level tool descriptions.
- Document new tools and changes in this file for team visibility. 