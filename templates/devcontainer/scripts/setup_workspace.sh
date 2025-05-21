#!/bin/bash
set -e

# Enable logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "[setup] Starting payload restoration and environment setup..."

# --- PAYLOAD RESTORATION ---
# 1. SSH keys
if [ -d "/workspaces/project/payload/.ssh" ]; then
    log "Found SSH directory, copying keys..."
    mkdir -p /root/.ssh
    cp -r /workspaces/project/payload/.ssh/* /root/.ssh/
    chmod 600 /root/.ssh/id_rsa
    log "SSH keys copied and permissions set"
else
    log "WARNING: No SSH directory found at /workspaces/project/payload/.ssh"
fi

# 2. .env file
if [ -f "/workspaces/project/payload/.env" ]; then
    log "Found .env file, copying..."
    cp /workspaces/project/payload/.env /workspaces/project/.env
    log ".env file copied successfully"
else
    log "WARNING: No .env file found at /workspaces/project/payload/.env"
fi

# 3. MCP config
if [ -f "/workspaces/project/payload/mcp_config.json" ]; then
    log "Found MCP config, copying..."
    mkdir -p /root/.codeium/windsurf
    cp /workspaces/project/payload/mcp_config.json /root/.codeium/windsurf/mcp_config.json
    log "MCP config copied successfully"
else
    log "WARNING: No MCP config found at /workspaces/project/payload/mcp_config.json"
fi

# 4. Docs directory
if [ -d "/workspaces/project/payload/docs" ]; then
    log "Moving all docs from payload/docs/ to /workspaces/project/docs/..."
    mkdir -p /workspaces/project/docs
    shopt -s nullglob dotglob
    DOC_ITEMS=(/workspaces/project/payload/docs/*)
    if [ ${#DOC_ITEMS[@]} -eq 0 ]; then
        log "INFO: No files found in /workspaces/project/payload/docs to move."
    else
        for item in "${DOC_ITEMS[@]}"; do
            name=$(basename "$item")
            if [ -e "/workspaces/project/docs/$name" ]; then
                rm -rf "/workspaces/project/docs/$name"
            fi
            mv "$item" /workspaces/project/docs/
            log "Moved $name to /workspaces/project/docs/"
        done
        log "All documentation moved. /workspaces/project/docs/ is now the source of truth."
    fi
else
    log "WARNING: No docs directory found at /workspaces/project/payload/docs"
fi

# 5. Global rules (legacy)
if [ -f "/workspaces/project/payload/global_rules.md" ]; then
    log "Found legacy global rules, copying..."
    cp /workspaces/project/payload/global_rules.md /workspaces/project/docs/global_rules.md
    log "Legacy global rules copied successfully"
else
    log "INFO: No legacy global rules found (this is normal for new setups)"
fi

# 6. Cursor user rule and memory bank
cp /workspaces/project/.devcontainer/scripts/cursor_user_rule.txt /workspaces/project/payload/cursor_user_rule.txt
mkdir -p /workspaces/project/payload/.cursor/rules
cp /workspaces/project/.devcontainer/scripts/.cursor/rules/memory_bank.mdc /workspaces/project/payload/.cursor/rules/memory_bank.mdc

# --- ENVIRONMENT SETUP ---
# 1. Ensure .venv exists (use uv if available, fallback to python)
if [ ! -d "/workspaces/project/.venv" ]; then
  log "Creating Python venv in /workspaces/project/.venv..."
  if command -v uv &> /dev/null; then
    uv venv /workspaces/project/.venv
  else
    python3 -m venv /workspaces/project/.venv
  fi
fi

# 1b. Ensure 'ws' package is installed for MCP server compatibility
log "Ensuring 'ws' package is installed in the container venv..."
/workspaces/project/.venv/bin/python -m pip install ws || log "WARNING: Failed to install 'ws' package, continuing..."

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

# 3. Check required env vars
if [ -z "$MCP_DISCORD_REPO_URL" ]; then
  log "ERROR: MCP_DISCORD_REPO_URL is not set."
  exit 1
fi
if [ -z "$PROJECT_REPO_URL" ]; then
  log "ERROR: PROJECT_REPO_URL is not set."
  exit 1
fi

# 4. Clone MCP Discord repo if not present
if [ ! -d "/workspaces/project/mcp-discord" ]; then
  if [ -n "$MCP_DISCORD_REPO_URL" ]; then
    log "Cloning mcp-discord repo..."
    if ! git clone "$MCP_DISCORD_REPO_URL" /workspaces/project/mcp-discord; then
      log "WARNING: Failed to clone mcp-discord repo from $MCP_DISCORD_REPO_URL, continuing..."
    fi
  else
    log "WARNING: MCP_DISCORD_REPO_URL is not set, skipping mcp-discord clone."
  fi
fi

# 5. Install mcp-discord in the container venv
if [ -d "/workspaces/project/mcp-discord" ]; then
  cd /workspaces/project/mcp-discord
  /workspaces/project/.venv/bin/python -m pip install -e . || /workspaces/project/.venv/bin/python -m pip install . || log "WARNING: Failed to install mcp-discord, continuing..."
  cd /workspaces/project
else
  log "INFO: mcp-discord repo not found, skipping install."
fi

# 6. Install internal_chat_mcp tool in the container venv if present
if [ -d "/workspaces/project/tools/internal_chat_mcp" ]; then
  log "Installing internal_chat_mcp tool in the container venv..."
  cd /workspaces/project/tools/internal_chat_mcp
  /workspaces/project/.venv/bin/python -m pip install -e . || log "WARNING: Failed to install internal_chat_mcp, continuing..."
  cd /workspaces/project
else
  log "INFO: internal_chat_mcp tool not found in tools/. Checking for standalone repo..."
  if [ ! -d "/workspaces/project/internal_chat_mcp" ]; then
    log "Cloning internal_chat_mcp standalone repo..."
    if ! git clone https://github.com/glindberg2000/internal_chat_mcp.git /workspaces/project/internal_chat_mcp; then
      log "WARNING: Failed to clone internal_chat_mcp from GitHub, continuing..."
    fi
  fi
  if [ -d "/workspaces/project/internal_chat_mcp" ]; then
    log "Installing internal_chat_mcp standalone tool in the container venv..."
    cd /workspaces/project/internal_chat_mcp
    /workspaces/project/.venv/bin/python -m pip install -e . || log "WARNING: Failed to install internal_chat_mcp standalone, continuing..."
    cd /workspaces/project
  else
    log "INFO: internal_chat_mcp standalone repo not found, skipping install."
  fi
fi

# 7. Clone main project repo if not present and not a placeholder
REPO_NAME=$(basename -s .git "$PROJECT_REPO_URL")
if [[ "$PROJECT_REPO_URL" == *"your-org/your-project.git"* || -z "$PROJECT_REPO_URL" ]]; then
  log "Skipping main project repo clone (placeholder or not set)."
else
  if [ ! -d "/workspaces/project/$REPO_NAME" ]; then
    log "Cloning main project repo..."
    if ! git clone "$PROJECT_REPO_URL" "/workspaces/project/$REPO_NAME"; then
      log "WARNING: Failed to clone main project repo from $PROJECT_REPO_URL, continuing..."
    fi
  fi
fi

# --- CRITICAL FILE VERIFICATION ---
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
[ -f "/root/.ssh/id_rsa" ] && log "✓ Found: SSH key" || log "ERROR: SSH key missing"

if [ $MISSING_FILES -eq 0 ]; then
    log "Payload restoration and setup completed successfully!"
else
    log "WARNING: Payload restored with $MISSING_FILES missing critical files"
    exit 2
fi

# --- End of setup ---

# --- PORTS & CONNECTIVITY ---
# Note: The MCP server may bind to a port (default 8000 for SSE mode). If you want to access it from outside the container, ensure the port is exposed in your devcontainer.json or Docker config.
# For outbound-only MCP clients, no port exposure is needed. For inbound HTTP/SSE, expose the port (e.g., 8000). 