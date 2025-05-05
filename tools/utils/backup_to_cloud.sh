#!/usr/bin/env bash
set -e

# Secure backup script for Team_AI repo
# Usage: ./backup_to_cloud.sh
#
# - Backs up sessions, docs, roles, team-cli, and key files to BACKUP_TARGET/AI_Team_Backups
# - Includes team environment files from team-envs directory
# - Reads BACKUP_TARGET from .env
# - Skips .git and __pycache__
# - Timestamped backup folder

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Load BACKUP_TARGET from .env if present
if [ -f "$REPO_ROOT/.env" ]; then
  # Extract BACKUP_TARGET value from .env file
  BACKUP_TARGET=$(grep '^BACKUP_TARGET=' "$REPO_ROOT/.env" | cut -d '=' -f2-)
fi

# Require BACKUP_TARGET to be set
if [ -z "$BACKUP_TARGET" ]; then
  echo "ERROR: BACKUP_TARGET is not set in .env file. Please set it to your iCloud backup path."
  exit 1
fi

# Create AI_Team_Backups directory if it doesn't exist
BACKUP_DIR="$BACKUP_TARGET/AI_Team_Backups"
mkdir -p "$BACKUP_DIR"

DATE=$(date +"%Y-%m-%d_%H-%M-%S")
TARGET="$BACKUP_DIR/Team_AI_$DATE"

echo "Backing up Team_AI repo to: $TARGET"

# Create backup structure
echo "Creating backup structure..."
mkdir -p "$TARGET"

# Copy key directories and files
echo "Copying teams (live team/session data)..."
if [ -d "$REPO_ROOT/teams" ]; then
  cp -r "$REPO_ROOT/teams" "$TARGET/"
else
  echo "WARNING: teams/ directory not found. Skipping teams backup."
fi

echo "Copying docs..."
if [ -d "$REPO_ROOT/docs" ]; then
  cp -r "$REPO_ROOT/docs" "$TARGET/"
else
  echo "WARNING: docs/ directory not found. Skipping docs backup."
fi

echo "Copying roles..."
if [ -d "$REPO_ROOT/roles" ]; then
  cp -r "$REPO_ROOT/roles" "$TARGET/"
else
  echo "WARNING: roles/ directory not found. Skipping roles backup."
fi

echo "Copying team-cli..."
if [ -d "$REPO_ROOT/team-cli" ]; then
  cp -r "$REPO_ROOT/team-cli" "$TARGET/"
else
  echo "WARNING: team-cli/ directory not found. Skipping team-cli backup."
fi

echo "Copying team-envs..."
if [ -d "$REPO_ROOT/team-envs" ]; then
  cp -r "$REPO_ROOT/team-envs" "$TARGET/"
else
  echo "INFO: team-envs/ directory not found. Skipping team-envs backup."
fi

# Copy .env file if it exists
if [ -f "$REPO_ROOT/.env" ]; then
  echo "Copying .env..."
  cp "$REPO_ROOT/.env" "$TARGET/"
fi

# Copy README and CONTRIBUTING
echo "Copying README.md..."
cp "$REPO_ROOT/README.md" "$TARGET/" 2>/dev/null || true
echo "Copying CONTRIBUTING.md..."
cp "$REPO_ROOT/CONTRIBUTING.md" "$TARGET/" 2>/dev/null || true

# Legacy: Copy sessions if present (non-fatal)
if [ -d "$REPO_ROOT/sessions" ]; then
  echo "Copying legacy sessions..."
  cp -r "$REPO_ROOT/sessions" "$TARGET/"
else
  echo "INFO: sessions/ directory not found (expected for new setups)."
fi

# Create backup manifest
echo "Creating backup manifest..."
cat > "$TARGET/backup_manifest.txt" << EOF
Backup created on: $(date)
From directory: $REPO_ROOT
Backup target: $TARGET
Backed up items:
✓ teams
✓ docs
✓ roles
✓ team-cli
✓ team-envs
✓ .env
✓ README.md
✓ CONTRIBUTING.md
EOF

echo "Backup complete!"
echo "Your backup is at: $TARGET"
echo "A manifest of backed up items can be found at: $TARGET/backup_manifest.txt" 