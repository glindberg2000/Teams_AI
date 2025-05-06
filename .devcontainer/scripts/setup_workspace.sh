#!/bin/bash
set -e

# Clone MCP Discord repo if not present
if [ -n "$MCP_DISCORD_REPO_URL" ]; then
  if [ ! -d "/workspaces/project/mcp-discord" ]; then
    echo "Cloning mcp-discord repo..."
    git clone "$MCP_DISCORD_REPO_URL" /workspaces/project/mcp-discord
  fi
  # Install mcp-discord in the container venv
  cd /workspaces/project/mcp-discord
  uv pip install -e .
  cd /workspaces/project
fi

# Clone main project repo if not present
if [ -n "$PROJECT_REPO_URL" ]; then
  # Extract repo name from URL
  REPO_NAME=$(basename -s .git "$PROJECT_REPO_URL")
  if [ ! -d "/workspaces/project/$REPO_NAME" ]; then
    echo "Cloning main project repo..."
    git clone "$PROJECT_REPO_URL" "/workspaces/project/$REPO_NAME"
  fi
fi

# Run restore script if it exists (final step)
if [ -f "/workspaces/project/restore_payload.sh" ]; then
    echo "Running restore script..."
    bash /workspaces/project/restore_payload.sh
fi 