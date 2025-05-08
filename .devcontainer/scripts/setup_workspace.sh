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
  if [ -z "$MCP_DISCORD_REPO_BRANCH" ]; then
    git clone "$MCP_DISCORD_REPO_URL" /workspaces/project/mcp-discord
  else
    git clone -b "$MCP_DISCORD_REPO_BRANCH" "$MCP_DISCORD_REPO_URL" /workspaces/project/mcp-discord
  fi
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

# --- Restore all payload files directly (incorporated from canonical restore_payload.sh) ---
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting payload restoration..."

# Move SSH key to root
if [ -d "/workspaces/project/payload/.ssh" ]; then
    log "Found SSH directory, copying keys..."
    mkdir -p /root/.ssh
    cp -r /workspaces/project/payload/.ssh/* /root/.ssh/
    chmod 600 /root/.ssh/id_rsa
    log "SSH keys copied and permissions set"
else
    log "WARNING: No SSH directory found at /workspaces/project/payload/.ssh"
fi

# Move environment file
if [ -f "/workspaces/project/payload/.env" ]; then
    log "Found .env file, copying..."
    cp /workspaces/project/payload/.env /workspaces/project/.env
    log ".env file copied successfully"
else
    log "WARNING: No .env file found at /workspaces/project/payload/.env"
fi

# Move MCP config
if [ -f "/workspaces/project/payload/mcp_config.json" ]; then
    log "Found MCP config, copying..."
    mkdir -p /root/.codeium/windsurf
    cp /workspaces/project/payload/mcp_config.json /root/.codeium/windsurf/mcp_config.json
    log "MCP config copied successfully"
else
    log "WARNING: No MCP config found at /workspaces/project/payload/mcp_config.json"
fi

# Restore .windsurfrules
if [ -f "/workspaces/project/payload/.windsurfrules" ]; then
    log "Found .windsurfrules, copying..."
    cp /workspaces/project/payload/.windsurfrules /workspaces/project/.windsurfrules
    log ".windsurfrules copied successfully"
else
    log "WARNING: No .windsurfrules found at /workspaces/project/payload/.windsurfrules"
fi

# Restore cline_docs
if [ -d "/workspaces/project/payload/cline_docs" ]; then
    log "Found cline_docs, restoring..."
    rm -rf /workspaces/project/cline_docs
    cp -r /workspaces/project/payload/cline_docs /workspaces/project/cline_docs
    log "cline_docs restored successfully"
else
    log "WARNING: No cline_docs directory found at /workspaces/project/payload/cline_docs"
fi

# Restore cline_docs_shared
if [ -d "/workspaces/project/payload/cline_docs_shared" ]; then
    log "Found cline_docs_shared, restoring..."
    rm -rf /workspaces/project/cline_docs_shared
    cp -r /workspaces/project/payload/cline_docs_shared /workspaces/project/cline_docs_shared
    log "cline_docs_shared restored successfully"
else
    log "WARNING: No cline_docs_shared directory found at /workspaces/project/payload/cline_docs_shared"
fi

# Restore .windsurf/rules
if [ -d "/workspaces/project/payload/.windsurf/rules" ]; then
    log "Found .windsurf/rules, restoring..."
    mkdir -p /workspaces/project/.windsurf
    rm -rf /workspaces/project/.windsurf/rules
    cp -r /workspaces/project/payload/.windsurf/rules /workspaces/project/.windsurf/rules
    log ".windsurf/rules restored successfully"
else
    log "WARNING: No .windsurf/rules directory found at /workspaces/project/payload/.windsurf/rules"
fi

# Verify critical files
log "Verifying critical files..."
MISSING_FILES=0

check_file() {
    if [ ! -f "$1" ]; then
        log "ERROR: Critical file missing: $1"
        MISSING_FILES=$((MISSING_FILES + 1))
    else
        log "✓ Found: $1"
    fi
}

check_file "/workspaces/project/.env"
check_file "/root/.codeium/windsurf/mcp_config.json"
check_file "/workspaces/project/.windsurfrules"
[ -f "/root/.ssh/id_rsa" ] && log "✓ Found: SSH key" || log "ERROR: SSH key missing"

if [ $MISSING_FILES -eq 0 ]; then
    log "Payload restoration completed successfully!"
else
    log "WARNING: Payload restored with $MISSING_FILES missing critical files"
fi

# --- End of setup --- 