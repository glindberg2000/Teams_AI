#!/usr/bin/env bash
set -e
REPO=${REPO_URL:-https://github.com/YourOrg/YourRepo.git}
if [ ! -d /workspaces/project/.git ]; then
  git clone "$REPO" /workspaces/project
fi 