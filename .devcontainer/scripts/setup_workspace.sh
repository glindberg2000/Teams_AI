#!/bin/bash
set -e

# --- Robust DevContainer Setup Script ---

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 1. Ensure .venv exists (use uv if available, fallback to python)
if [ ! -d "/workspaces/project/.venv" ]; then
  log "Creating Python venv in /workspaces/project/.venv..."
  if command -v uv &> /dev/null; then
    uv venv /workspaces/project/.venv
  else
    python3 -m venv /workspaces/project/.venv
  fi
fi

# 2. Export env vars from .env (skip invalid lines)
if [ -f "/workspaces/project/payload/.env" ]; then
  log "Exporting env vars from /workspaces/project/payload/.env..."
  while IFS='=' read -r key value; do
    if [[ "$key" =~ ^#.*$ ]] || [[ -z "$key" ]]; then
      continue
    fi
    export "$key"="$value"
  done < /workspaces/project/payload/.env
else
  log "WARNING: /workspaces/project/payload/.env not found."
fi

# 3. Check required env vars (warn, don't exit)
if [ -z "$MCP_DISCORD_REPO_URL" ]; then
  log "WARNING: MCP_DISCORD_REPO_URL is not set. Skipping Discord MCP setup."
fi
if [ -z "$PROJECT_REPO_URL" ]; then
  log "WARNING: PROJECT_REPO_URL is not set. Skipping main project clone."
fi

# 4. Clone MCP Discord repo if not present
if [ -n "$MCP_DISCORD_REPO_URL" ] && [ ! -d "/workspaces/project/mcp-discord" ]; then
  log "Cloning mcp-discord repo..."
  if [ -z "$MCP_DISCORD_REPO_BRANCH" ]; then
    git clone "$MCP_DISCORD_REPO_URL" /workspaces/project/mcp-discord
  else
    git clone -b "$MCP_DISCORD_REPO_BRANCH" "$MCP_DISCORD_REPO_URL" /workspaces/project/mcp-discord
  fi
fi

# 5. Install mcp-discord in the container venv
if [ -d "/workspaces/project/mcp-discord" ]; then
  cd /workspaces/project/mcp-discord
  /workspaces/project/.venv/bin/python -m pip install -e . || /workspaces/project/.venv/bin/python -m pip install .
  cd /workspaces/project
fi

# 6. Clone main project repo if not present
if [ -n "$PROJECT_REPO_URL" ]; then
  REPO_NAME=$(basename -s .git "$PROJECT_REPO_URL")
  if [ ! -d "/workspaces/project/$REPO_NAME" ]; then
    log "Cloning main project repo..."
    git clone "$PROJECT_REPO_URL" "/workspaces/project/$REPO_NAME"
  fi
fi

# 7. Restore .windsurfrules from payload
if [ -f "/workspaces/project/payload/.windsurfrules" ]; then
  log "Restoring .windsurfrules to project root..."
  cp /workspaces/project/payload/.windsurfrules /workspaces/project/.windsurfrules
else
  log "WARNING: No .windsurfrules found in payload."
fi

# 8. Generate .cursor directory and rules
CURSOR_TEMPLATE_DIR="/workspaces/project/.devcontainer/scripts/.cursor"
CURSOR_TARGET_DIR="/workspaces/project/.cursor"
if [ ! -d "$CURSOR_TARGET_DIR" ]; then
  log "Creating .cursor directory in project root..."
  mkdir -p "$CURSOR_TARGET_DIR"
fi
if [ -d "$CURSOR_TEMPLATE_DIR/rules" ]; then
  log "Copying .cursor rules from template..."
  mkdir -p "$CURSOR_TARGET_DIR/rules"
  cp -r $CURSOR_TEMPLATE_DIR/rules/* $CURSOR_TARGET_DIR/rules/
else
  log "WARNING: .cursor rules template not found at $CURSOR_TEMPLATE_DIR/rules."
fi
if [ -f "/workspaces/project/.devcontainer/scripts/mcp_config.template.json" ]; then
  log "Generating .cursor/mcp.json from template..."
  envsubst < /workspaces/project/.devcontainer/scripts/mcp_config.template.json > $CURSOR_TARGET_DIR/mcp.json
else
  log "WARNING: mcp_config.template.json not found."
fi

# 9. Setup internal chat MCP server
if [ ! -d "/workspaces/project/tools/internal_chat_mcp" ]; then
  log "Copying internal_chat_mcp..."
  cp -r /workspaces/project/tools/internal_chat_mcp /workspaces/project/tools/internal_chat_mcp
fi
if [ -d "/workspaces/project/tools/internal_chat_mcp" ]; then
  cd /workspaces/project/tools/internal_chat_mcp
  /workspaces/project/.venv/bin/python -m pip install -e .
  cd /workspaces/project
else
  log "WARNING: internal_chat_mcp directory not found."
fi

# 10. Install Task Master globally
if ! command -v task-master &> /dev/null; then
  log "Installing task-master-ai globally..."
  npm install -g task-master-ai || log "WARNING: Failed to install task-master-ai."
fi

# 11. Comment out refresh_configs.sh in devcontainer.json (manual step)
log "NOTE: If present, comment out refresh_configs.sh in devcontainer.json postStartCommand."

log "Setup complete." 