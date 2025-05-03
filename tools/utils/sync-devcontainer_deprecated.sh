#!/usr/bin/env bash
set -e
for session in sessions/*; do
  if [ -d "$session" ] && [ "$(basename $session)" != "_shared" ]; then
    rsync -a --delete .devcontainer/ "$session/.devcontainer/"
    echo "Synced .devcontainer/ to $session/.devcontainer/"
  fi
done 