# AI Team Workspace

This repository provides full scaffolding and automation for spinning up isolated, role-based AI agent sessions for projects, including:

- Per-session workspaces with isolated code clones
- Automated DevContainer setup and config sync
- Templated secrets and MCP config injection
- Clear separation of global, project, role, and per-session documentation
- Secure handling of secrets and SSH keys

## Quick Start

1. **Clone this repo**
2. **Install Python 3.7+** (no extra dependencies required)
3. **Create a new session:**
   ```bash
   python team-cli/team_cli.py create-session --name my-coder --role python_coder --generate-ssh-key --prompt-all
   # Or, to include project docs:
   python team-cli/team_cli.py create-session --name my-coder --role python_coder --project sample_project --generate-ssh-key --prompt-all
   ```
4. **Edit the generated `.env` and docs in your session folder as needed**
5. **Prepare the payload:**
   ```bash
   python team-cli/team_cli.py prepare-payload --name my-coder
   ```
6. **Open the session folder in VS Code or Windsurf as a Dev Container**
7. **Run the restore script inside the container:**
   ```bash
   bash /workspaces/project/payload/restore_payload.sh
   ```

## Documentation Structure

- `docs/global/` — Global docs for all agents/projects (roles, tools, integrations, etc.)
- `docs/projects/<project_name>/` — Project-specific docs
- `roles/<role>/docs/` — Role-specific docs
- `sessions/<agent>/docs/` — Per-session docs (auto-populated from above, never tracked in git)

## Security & Secret Storage
- **Never commit real secrets or private keys to this repo.**
- The `.gitignore` is configured to ignore all `.env` files, all `payload/.ssh/` directories, and all generated session folders.
- SSH keys are generated or copied into `payload/.ssh/` and are never tracked by git.
- **All generated session folders are ignored by git.**
- **Store secrets and sensitive configs in a secure location outside git, such as iCloud, 1Password, or your organization's vault.**
- When onboarding a new machine, restore secrets from your secure backup and use the CLI to generate new sessions.

## Key Scripts & CLI
- `team-cli/team_cli.py` — Main CLI for session and agent management. Run with `--help` or `--simple-help` for usage.
- `sync-devcontainer.sh` — Copies the root `.devcontainer/` into each session folder
- `.devcontainer/scripts/setup_workspace.sh` — Clones the main repo into the session workspace
- `.devcontainer/scripts/refresh_configs.sh` — Renders MCP config and injects session secrets

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for details on DevContainer sync and best practices.

---

**WARNING:**
- Never commit generated session folders or secrets to git.
- Always use secure storage for secrets (iCloud, 1Password, etc.).
- For more details, run:
```bash
python team-cli/team_cli.py --simple-help
``` 