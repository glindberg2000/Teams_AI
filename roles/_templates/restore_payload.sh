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