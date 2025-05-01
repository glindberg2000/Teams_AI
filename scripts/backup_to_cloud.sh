#!/usr/bin/env bash
set -e

# Secure backup script for Team_AI repo
# Usage: ./backup_to_icloud.sh
#
# - Backs up sessions, docs, roles, team-cli, and key files to BACKUP_TARGET
# - Includes team environment files from team-envs directory
# - Reads BACKUP_TARGET from .env if set, otherwise requires it to be set in the environment
# - Skips .git and __pycache__
# - Timestamped backup folder

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

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

# Core directories and files to backup
INCLUDE=(
  "sessions"
  "docs"
  "roles"
  "team-cli"
  "team-envs"
  ".env"
  "README.md"
  "CONTRIBUTING.md"
)

# Create backup structure
echo "Creating backup structure..."
for item in "${INCLUDE[@]}"; do
  if [ -e "$REPO_ROOT/$item" ]; then
    echo "Copying $item..."
    if [ -d "$REPO_ROOT/$item" ]; then
      # For directories, use rsync with exclusions
      rsync -a --exclude='.git' --exclude='__pycache__' "$REPO_ROOT/$item" "$TARGET/"
    else
      # For single files, use cp
      cp "$REPO_ROOT/$item" "$TARGET/"
    fi
  else
    echo "Warning: $item not found, skipping..."
  fi
done

# Create a manifest of what was backed up
echo "Creating backup manifest..."
(
  echo "Backup created on: $(date)"
  echo "From directory: $REPO_ROOT"
  echo "Backed up items:"
  for item in "${INCLUDE[@]}"; do
    if [ -e "$TARGET/$item" ]; then
      echo "✓ $item"
    else
      echo "✗ $item (not found)"
    fi
  done
) > "$TARGET/backup_manifest.txt"

echo "Backup complete!"
echo "Your backup is at: $TARGET"
echo "A manifest of backed up items can be found at: $TARGET/backup_manifest.txt" 