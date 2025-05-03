#!/bin/bash
set -e

# Run restore script if it exists
if [ -f "/workspaces/project/restore_payload.sh" ]; then
    echo "Running restore script..."
    bash /workspaces/project/restore_payload.sh
fi
