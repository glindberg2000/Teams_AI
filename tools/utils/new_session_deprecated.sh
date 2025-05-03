#!/usr/bin/env bash
# Usage: ./new_session.sh teamA

if [ -z "$1" ]; then
  echo "Usage: $0 <session-name>"
  exit 1
fi

export SESSION_NAME="$1"
# copy your real secrets into sessions/$1/.env (or edit env.sample → .env)
if [ ! -f "sessions/$1/mcp_servers.json" ]; then
  echo "No session named '$1'."
  exit 1
fi

# Launch Windsurf devcontainer (or VS Code devcontainer)
# In Windsurf: use "Open Folder in Container" on this repo root.
# In VS Code: code .
# The devcontainer.json's remoteEnv will pick up SESSION_NAME.
windsurf devcontainer open .  # or in VS Code: code . 