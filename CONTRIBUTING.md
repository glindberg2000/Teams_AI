# Contributing to LedgerFlow AI

## DevContainer Sync

- The source-of-truth `.devcontainer/` lives at the repo root.
- Each session folder (e.g., `sessions/pm-guardian/`) should have its own copy of `.devcontainer/` for container builds.
- To update all session folders after making changes to the root `.devcontainer/`, run:

```bash
./sync-devcontainer.sh
```

This will copy the root `.devcontainer/` into each session, ensuring consistency and avoiding symlink issues.

- If you add new scripts or update hooks, always re-run the sync script before launching new sessions. 