#!/usr/bin/env bash
set -e

# Secure backup script for Team_AI repo
# Usage: ./backup_to_icloud.sh
#
# - Backs up sessions, docs, roles, team-cli, and key files to BACKUP_TARGET
# - Reads BACKUP_TARGET from .env if set, otherwise requires it to be set in the environment
# - Skips .git and __pycache__
# - Timestamped backup folder

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load BACKUP_TARGET from .env if present
if [ -f "$REPO_ROOT/.env" ]; then
  source "$REPO_ROOT/.env"
fi

# Require BACKUP_TARGET to be set
if [ -z "$BACKUP_TARGET" ]; then
  echo "ERROR: BACKUP_TARGET is not set. Please set it in your .env or as an environment variable."
  exit 1
fi

DATE=$(date +"%Y-%m-%d_%H-%M-%S")
TARGET="$BACKUP_TARGET/Team_AI_$DATE"

echo "Backing up Team_AI repo to: $TARGET"
mkdir -p "$TARGET"

INCLUDE=(
  "sessions"
  "docs"
  "roles"
  "team-cli"
  ".env"
  "sync-devcontainer.sh"
  "README.md"
  "CONTRIBUTING.md"
)

for item in "${INCLUDE[@]}"; do
  if [ -e "$REPO_ROOT/$item" ]; then
    echo "Copying $item..."
    rsync -a --exclude='.git' --exclude='__pycache__' "$REPO_ROOT/$item" "$TARGET/"
  fi

done

echo "Backup complete!"
echo "Your backup is at: $TARGET" 