#!/usr/bin/env bash
set -e

# Set up environment
PROJECT_ROOT=${PROJECT_ROOT:-/workspaces/project}
PAYLOAD_DIR="${PROJECT_ROOT}/payload"
DOCS_DIR="${PROJECT_ROOT}/docs"
WINDSURF_DIR="/root/.codeium/windsurf"

# Ensure directories exist
mkdir -p "${WINDSURF_DIR}"
mkdir -p "${DOCS_DIR}"

# 1) copy static docs if they exist
if [ -f "${PAYLOAD_DIR}/docs/global/global_rules.md" ]; then
    cp "${PAYLOAD_DIR}/docs/global/global_rules.md" "${WINDSURF_DIR}/global_rules.md"
fi

if [ -f "${PAYLOAD_DIR}/docs/project/project_overview.md" ]; then
    cp "${PAYLOAD_DIR}/docs/project/project_overview.md" "${WINDSURF_DIR}/project_overview.md"
fi

# 2) merge in secrets & build mcp_config.json
# Load environment variables from payload .env if it exists
if [ -f "${PAYLOAD_DIR}/.env" ]; then
    set -a
    source "${PAYLOAD_DIR}/.env"
    set +a
fi

# Generate MCP config if template exists
if [ -f "${PAYLOAD_DIR}/mcp_config.template.json" ]; then
    jq \
        --arg gh "${GITHUB_TOKEN:-}" \
        --arg sl "${SLACK_TOKEN:-}" \
        '.servers |= map(
            if .type=="github" then .token=$gh
            elif .type=="slack"  then .token=$sl
            else . end
        )' \
        "${PAYLOAD_DIR}/mcp_config.template.json" \
        > "${WINDSURF_DIR}/mcp_config.json"
fi

# 3) hand off to the default Windsurf startup
exec "$@" 