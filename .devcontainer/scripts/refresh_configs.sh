#!/usr/bin/env bash
set -e
# 1. Re-generate MCP JSON from template + env vars
mkdir -p /root/.codeium/windsurf/
envsubst < /workspaces/project/.devcontainer/scripts/mcp_config.template.json \
  > /root/.codeium/windsurf/mcp_config.json

# 2. Copy global rules into /workspaces/project/docs/
GLOBAL_RULES_SRC="/workspace/sessions/${SESSION_NAME}/global_rules.md"
GLOBAL_RULES_DEST="/workspaces/project/docs/global_rules.md"
if [ -f "$GLOBAL_RULES_SRC" ]; then
  mkdir -p /workspaces/project/docs
  cp "$GLOBAL_RULES_SRC" "$GLOBAL_RULES_DEST"
fi

# 3. Inject per-session IDs (Slack handle, Git identity) into .env
SESSION_ENV="/workspace/sessions/${SESSION_NAME}/.env"
PROJECT_ENV="/workspaces/project/.env"
if [ -f "$SESSION_ENV" ]; then
  cp "$SESSION_ENV" "$PROJECT_ENV"
fi
# (Add logic here to append/inject session-specific IDs as needed) 