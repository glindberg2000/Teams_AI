#!/bin/bash
set -e

# Move SSH key to root
if [ -d "/workspaces/project/payload/.ssh" ]; then
  mkdir -p /root/.ssh
  cp -r /workspaces/project/payload/.ssh/* /root/.ssh/
  chmod 600 /root/.ssh/id_rsa
fi

# Move environment file
if [ -f "/workspaces/project/payload/.env" ]; then
  cp /workspaces/project/payload/.env /workspaces/project/.env
fi

# Move MCP config
if [ -f "/workspaces/project/payload/mcp_config.json" ]; then
  mkdir -p /root/.codeium/windsurf
  cp /workspaces/project/payload/mcp_config.json /root/.codeium/windsurf/mcp_config.json
fi

# Move docs directory if it exists
if [ -d "/workspaces/project/payload/docs" ]; then
  mkdir -p /workspaces/project/docs
  cp -r /workspaces/project/payload/docs/* /workspaces/project/docs/
fi

# Move global rules if they exist (legacy support)
if [ -f "/workspaces/project/payload/global_rules.md" ]; then
  cp /workspaces/project/payload/global_rules.md /workspaces/project/docs/global_rules.md
fi

echo "Payload restored successfully" 