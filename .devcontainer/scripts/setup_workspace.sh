#!/bin/bash
set -e

# --- Robust DevContainer Setup Script ---

# 1. Ensure .venv exists (use uv if available, fallback to python)
if [ ! -d "/workspaces/project/.venv" ]; then
  echo "[setup] Creating Python venv in /workspaces/project/.venv..."
  if command -v uv &> /dev/null; then
    uv venv /workspaces/project/.venv
  else
    python3 -m venv /workspaces/project/.venv
  fi
fi

# 2. Source .env or export needed variables
if [ -f "/workspaces/project/payload/.env" ]; then
  echo "[setup] Sourcing /workspaces/project/payload/.env..."
  set -a
  source /workspaces/project/payload/.env
  set +a
else
  echo "[setup] WARNING: /workspaces/project/payload/.env not found."
fi

# 3. Check required env vars
if [ -z "$MCP_DISCORD_REPO_URL" ]; then
  echo "[setup] ERROR: MCP_DISCORD_REPO_URL is not set."
  exit 1
fi
if [ -z "$PROJECT_REPO_URL" ]; then
  echo "[setup] ERROR: PROJECT_REPO_URL is not set."
  exit 1
fi

# 4. Clone MCP Discord repo if not present
if [ ! -d "/workspaces/project/mcp-discord" ]; then
  echo "[setup] Cloning mcp-discord repo..."
  git clone "$MCP_DISCORD_REPO_URL" /workspaces/project/mcp-discord
fi

# 5. Install mcp-discord in the container venv
cd /workspaces/project/mcp-discord
/workspaces/project/.venv/bin/python -m pip install -e .
cd /workspaces/project

# 6. Clone main project repo if not present
REPO_NAME=$(basename -s .git "$PROJECT_REPO_URL")
if [ ! -d "/workspaces/project/$REPO_NAME" ]; then
  echo "[setup] Cloning main project repo..."
  git clone "$PROJECT_REPO_URL" "/workspaces/project/$REPO_NAME"
fi

# 7. Run restore script if it exists (final step)
if [ -f "/workspaces/project/restore_payload.sh" ]; then
    echo "[setup] Running restore script..."
    bash /workspaces/project/restore_payload.sh
fi

# --- End of setup --- 