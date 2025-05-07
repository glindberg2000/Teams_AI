#!/bin/bash
set -e

# Enable logging
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

# Move docs directory if it exists
if [ -d "/workspaces/project/payload/docs" ]; then
    log "Found docs directory, copying contents..."
    mkdir -p /workspaces/project/docs
    cp -r /workspaces/project/payload/docs/* /workspaces/project/docs/
    log "Documentation copied successfully"
else
    log "WARNING: No docs directory found at /workspaces/project/payload/docs"
fi

# Move global rules if they exist (legacy support)
if [ -f "/workspaces/project/payload/global_rules.md" ]; then
    log "Found legacy global rules, copying..."
    cp /workspaces/project/payload/global_rules.md /workspaces/project/docs/global_rules.md
    log "Legacy global rules copied successfully"
else
    log "INFO: No legacy global rules found (this is normal for new setups)"
fi

# Copy Cursor user rule for easy installation
cp /workspaces/project/.devcontainer/scripts/cursor_user_rule.txt /workspaces/project/payload/cursor_user_rule.txt

# Copy Cursor project rule for auto-application
mkdir -p /workspaces/project/payload/.cursor/rules
cp /workspaces/project/.devcontainer/scripts/.cursor/rules/memory_bank.mdc /workspaces/project/payload/.cursor/rules/memory_bank.mdc

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
[ -f "/root/.ssh/id_rsa" ] && log "✓ Found: SSH key" || log "ERROR: SSH key missing"

if [ $MISSING_FILES -eq 0 ]; then
    log "Payload restoration completed successfully!"
else
    log "WARNING: Payload restored with $MISSING_FILES missing critical files"
fi 