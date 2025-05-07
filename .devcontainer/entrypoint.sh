#!/usr/bin/env bash
set -e

echo "[entrypoint] Starting entrypoint.sh"

# Set up environment
PROJECT_ROOT=${PROJECT_ROOT:-/workspaces/project}
PAYLOAD_DIR="${PROJECT_ROOT}/payload"
DOCS_DIR="${PROJECT_ROOT}/docs"
WINDSURF_DIR="/root/.codeium/windsurf"

echo "[entrypoint] Ensuring directories exist..."
mkdir -p "${WINDSURF_DIR}"
mkdir -p "${DOCS_DIR}"

echo "[entrypoint] Copying static docs if they exist..."
if [ -f "${PAYLOAD_DIR}/docs/global/global_rules.md" ]; then
    cp "${PAYLOAD_DIR}/docs/global/global_rules.md" "${WINDSURF_DIR}/global_rules.md"
fi

if [ -f "${PAYLOAD_DIR}/docs/project/project_overview.md" ]; then
    cp "${PAYLOAD_DIR}/docs/project/project_overview.md" "${WINDSURF_DIR}/project_overview.md"
fi

echo "[entrypoint] Loading env vars from payload/.env if present..."
# Robustly export env vars from .env (skip invalid lines)
if [ -f "${PAYLOAD_DIR}/.env" ]; then
  while IFS='=' read -r key value; do
    # Skip comments and empty lines
    if [[ "$key" =~ ^#.*$ ]] || [[ -z "$key" ]]; then
      continue
    fi
    export "$key"="$value"
  done < "${PAYLOAD_DIR}/.env"
else
  echo "[entrypoint] WARNING: ${PAYLOAD_DIR}/.env not found."
fi

echo "[entrypoint] Generating MCP config if template exists..."
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

echo "[entrypoint] Handing off to CMD: $@"
exec "$@" 