#!/bin/bash
set -e

# 0. Run restore script first to ensure SSH keys are in place
if [ -f "/workspaces/project/.devcontainer/scripts/restore_payload.sh" ]; then
    echo "[setup] Running restore script from .devcontainer/scripts (pre-clone)..."
    bash /workspaces/project/.devcontainer/scripts/restore_payload.sh
fi

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

# 2. Robustly export env vars from .env (skip invalid lines)
if [ -f "/workspaces/project/payload/.env" ]; then
  echo "[setup] Exporting env vars from /workspaces/project/payload/.env..."
  while IFS='=' read -r key value; do
    # Skip comments and empty lines
    if [[ "$key" =~ ^#.*$ ]] || [[ -z "$key" ]]; then
      continue
    fi
    export "$key"="$value"
  done < /workspaces/project/payload/.env
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
# Try editable install, fall back to standard if not supported
/workspaces/project/.venv/bin/python -m pip install -e . || /workspaces/project/.venv/bin/python -m pip install .
cd /workspaces/project

# 6. Clone main project repo if not present
REPO_NAME=$(basename -s .git "$PROJECT_REPO_URL")
if [ ! -d "/workspaces/project/$REPO_NAME" ]; then
  echo "[setup] Cloning main project repo..."
  git clone "$PROJECT_REPO_URL" "/workspaces/project/$REPO_NAME"
fi

# 7. Run restore script from scripts directory if it exists (final step)
if [ -f "/workspaces/project/.devcontainer/scripts/restore_payload.sh" ]; then
    echo "[setup] Running restore script from .devcontainer/scripts..."
    bash /workspaces/project/.devcontainer/scripts/restore_payload.sh
fi

# Remove any root-level docs directory if it exists (cleanup from old runs)
if [ -d "../docs" ]; then
  echo "[CLEANUP] Removing root-level docs directory (../docs) from previous runs."
  rm -rf ../docs
fi

# Ensure payload/docs exists
if [ ! -d "./docs" ]; then
  echo "[INFO] Creating payload/docs directory."
  mkdir -p ./docs
fi

# Only operate on payload/docs, payload/cline_docs, payload/cline_docs_shared
# (Add any setup logic here as needed)

# Example: Print structure for verification
ls -l ./docs
ls -l ./cline_docs
ls -l ./cline_docs_shared

# --- End of setup --- 