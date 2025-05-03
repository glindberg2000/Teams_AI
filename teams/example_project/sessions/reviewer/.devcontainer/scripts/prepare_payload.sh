#!/usr/bin/env bash
set -e

# Usage: prepare_payload.sh <session-name>
# This script prepares the payload directory for a session by copying:
# - Docs into payload/docs/
# - SSH keys into payload/.ssh/
# - .env into payload/
# - MCP configs into payload/mcp/
# - Generating restore_payload.sh

if [ -z "$1" ]; then
  echo "Usage: $0 <session-name>"
  exit 1
fi

SESSION_NAME="$1"
SESSIONS_DIR="sessions"
SESSION_PATH="$SESSIONS_DIR/$SESSION_NAME"
PAYLOAD_DIR="$SESSION_PATH/payload"

# Ensure payload directories exist
mkdir -p "$PAYLOAD_DIR/docs"
mkdir -p "$PAYLOAD_DIR/mcp"

# 1. Copy docs
echo "Copying docs..."
cp -r "$SESSION_PATH/docs/"* "$PAYLOAD_DIR/docs/"

# 2. Copy SSH keys (if they exist)
if [ -d "$SESSION_PATH/payload/.ssh" ]; then
  echo "Copying SSH keys..."
  mkdir -p "$PAYLOAD_DIR/.ssh"
  cp -r "$SESSION_PATH/payload/.ssh/"* "$PAYLOAD_DIR/.ssh/"
  chmod 600 "$PAYLOAD_DIR/.ssh/"*
fi

# 3. Copy .env (if it exists)
if [ -f "$SESSION_PATH/.env" ]; then
  echo "Copying .env..."
  cp "$SESSION_PATH/.env" "$PAYLOAD_DIR/.env"
fi

# 4. Process MCP configs
echo "Processing MCP configs..."
if [ -f "$SESSION_PATH/mcp_config.template.json" ]; then
  # Use envsubst to process the template with current environment variables
  envsubst < "$SESSION_PATH/mcp_config.template.json" > "$PAYLOAD_DIR/mcp/mcp_config.json"
fi
if [ -f "$SESSION_PATH/mcp_servers.json" ]; then
  cp "$SESSION_PATH/mcp_servers.json" "$PAYLOAD_DIR/mcp/"
fi

# 5. Generate restore_payload.sh
cat > "$PAYLOAD_DIR/restore_payload.sh" << 'EOF'
#!/usr/bin/env bash
set -e

# This script restores the payload inside the container
echo "Restoring payload..."

# 1. Copy docs
echo "Copying docs..."
mkdir -p /workspaces/project/docs
cp -r /workspaces/project/payload/docs/* /workspaces/project/docs/

# 2. Copy SSH keys
if [ -d /workspaces/project/payload/.ssh ]; then
  echo "Copying SSH keys..."
  mkdir -p /root/.ssh
  cp -r /workspaces/project/payload/.ssh/* /root/.ssh/
  chmod 600 /root/.ssh/*
fi

# 3. Copy .env
if [ -f /workspaces/project/payload/.env ]; then
  echo "Copying .env..."
  cp /workspaces/project/payload/.env /workspaces/project/.env
fi

# 4. Set up MCP configs
echo "Setting up MCP configs..."
# For Windsurf
mkdir -p /root/.codeium/windsurf/
if [ -f /workspaces/project/payload/mcp/mcp_config.json ]; then
  cp /workspaces/project/payload/mcp/mcp_config.json /root/.codeium/windsurf/
fi
if [ -f /workspaces/project/payload/mcp/mcp_servers.json ]; then
  cp /workspaces/project/payload/mcp/mcp_servers.json /root/.codeium/windsurf/
fi

# For Cursor
mkdir -p /root/.cursor/
if [ -f /workspaces/project/payload/mcp/mcp_config.json ]; then
  cp /workspaces/project/payload/mcp/mcp_config.json /root/.cursor/
fi
if [ -f /workspaces/project/payload/mcp/mcp_servers.json ]; then
  cp /workspaces/project/payload/mcp/mcp_servers.json /root/.cursor/
fi

echo "Payload restored successfully!"
EOF

chmod +x "$PAYLOAD_DIR/restore_payload.sh"

echo "Payload prepared successfully in $PAYLOAD_DIR"
echo "Next: Launch the container and run restore_payload.sh" 