#!/usr/bin/env bash
set -e

# 1) copy static docs
SESS_DIR="/workspaces/sessions/${SESSION_NAME}"
mkdir -p "/root/.codeium/windsurf/"

cp "$SESS_DIR/global_rules.md"    "/root/.codeium/windsurf/global_rules.md"
cp "$SESS_DIR/project_overview.md" "/root/.codeium/windsurf/project_overview.md"

# 2) merge in secrets & build mcp_config.json
#    you can load a .env in sessions/<name>/env.sample (copy to sessions/<name>/.env)
if [ -f "$SESS_DIR/.env" ]; then
  export $(grep -v '^#' "$SESS_DIR/.env" | xargs)
fi

jq \
  --arg gh "$GITHUB_TOKEN" \
  --arg sl "$SLACK_TOKEN" \
  '.servers |= map(
      if .type=="github" then .token=$gh
      elif .type=="slack"  then .token=$sl
      else . end
    )' \
  "$SESS_DIR/mcp_servers.json" \
  > "/root/.codeium/windsurf/mcp_config.json"

# 3) hand off to the default Windsurf startup
exec "$@" 