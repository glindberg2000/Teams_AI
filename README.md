# AI Team Workspace

This repository provides automation for creating isolated, role-based AI agent sessions.

## Quick Start

1. Clone this repo
2. Install Python 3.7+
3. Create a new session:
   ```bash
   # With interactive prompts for all values:
   python team-cli/team_cli.py create-session --name pm-guardian --role python_coder --prompt-all

   # Or with all values specified:
   python team-cli/team_cli.py create-session \
     --name pm-guardian \
     --role python_coder \
     --ssh-key ~/.ssh/id_rsa \
     --all-env \
       GIT_USER_NAME="PM Guardian" \
       GIT_USER_EMAIL="pm@example.com" \
       GITHUB_PERSONAL_ACCESS_TOKEN="ghp_xxx" \
       SLACK_BOT_TOKEN="xoxb-xxx" \
       SLACK_TEAM_ID="Txxx" \
       ANTHROPIC_API_KEY="sk-xxx" \
       PERPLEXITY_API_KEY="pplx-xxx"
   ```

4. Launch the container - the restore script will automatically:
   - Set up SSH keys
   - Configure environment variables
   - Set up MCP configuration
   - Copy global rules

## Documentation Structure

- `docs/global/` - Global docs for all agents/projects
- `docs/projects/<project_name>/` - Per-project docs
- `roles/<role>/docs/` - Per-role docs
- `sessions/<agent>/docs/` - Per-session docs (copied from above)

## Security

- **IMPORTANT**: Do not commit real secrets or private keys to this repository
- Store sensitive information securely:
  - SSH keys in `sessions/<agent>/payload/.ssh/`
  - Environment variables in `sessions/<agent>/payload/.env`
  - MCP configuration in `sessions/<agent>/payload/mcp_config.json`
- Generated session folders should not be committed to git

## Key Scripts & Tools

- `team-cli/team_cli.py` - Session management CLI
  - Create new sessions from role templates
  - Configure SSH keys and environment variables
  - Set up documentation and payload
- `.devcontainer/` - DevContainer setup and configuration
  - `devcontainer.json` - Container configuration
  - `Dockerfile` - Container image definition
  - `scripts/` - Setup and utility scripts

## Environment Variables

Required environment variables (set in `payload/.env`):
- `GITHUB_PERSONAL_ACCESS_TOKEN` - GitHub access token
- `SLACK_BOT_TOKEN` - Slack bot user token
- `SLACK_TEAM_ID` - Slack workspace ID
- `GIT_USER_NAME` - Git commit author name
- `GIT_USER_EMAIL` - Git commit author email
- `GIT_SSH_KEY_PATH` - Path to SSH key in container
- `ANTHROPIC_API_KEY` - Claude API key
- `PERPLEXITY_API_KEY` - Perplexity AI key

## Adding New Roles

```bash
python team-cli/team_cli.py add-role \
  --name new-role \
  --docs docs/role-specific/*.md \
  --env-sample .env.role.example
```

See `roles/python_coder` for an example role template.

## Documentation Structure

- `docs/global/` — Global docs for all agents/projects (roles, tools, integrations, etc.)
- `docs/projects/<project_name>/` — Project-specific docs
- `roles/<role>/docs/` — Role-specific docs
- `sessions/<agent>/docs/` — Per-session docs (auto-populated from above, never tracked in git)
- `tasks/` — Generated task files and documentation
- `scripts/` — Utility scripts and PRD templates

## Security & Secret Storage

- **Never commit real secrets or private keys to this repo**
- The `.gitignore` is configured to ignore:
  - All `.env` files
  - All `payload/.ssh/` directories
  - All generated session folders
  - Task Master temporary files
- SSH keys are generated or copied into `payload/.ssh/` and are never tracked
- **Store secrets and sensitive configs securely outside git** (iCloud, 1Password, etc.)
- When onboarding a new machine, restore secrets from your secure backup
- **TIP:** If you forget to provide API keys during session creation, add them to `.env` before launching

## Task Master Integration

Task Master provides AI-driven task management through the Model Control Protocol (MCP):

- **Initialize a project:**
  ```bash
  task-master init -y
  ```

- **Generate tasks from PRD:**
  ```bash
  task-master parse-prd scripts/prd.txt
  ```

- **Common commands:**
  ```bash
  task-master list              # List all tasks
  task-master next             # Show next available task
  task-master expand --id=<id> # Break down a task
  task-master show <id>        # View task details
  ```

See [README-task-master.md](README-task-master.md) for detailed Task Master documentation.

## Key Scripts & CLI

- `team-cli/team_cli.py` — Main CLI for session and agent management
  ```bash
  python team-cli/team_cli.py --help        # Full help
  python team-cli/team_cli.py --simple-help # Quick reference
  ```
- `sync-devcontainer.sh` — Copies the root `.devcontainer/` into each session
- `.devcontainer/scripts/setup_workspace.sh` — Clones main repo into session
- `.devcontainer/scripts/refresh_configs.sh` — Renders MCP config and injects secrets

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on DevContainer sync and best practices.

---

**WARNING:**
- Never commit generated session folders or secrets to git
- Always use secure storage for secrets (iCloud, 1Password, etc.)
- Keep your API keys secure and never share them
- For quick help:
  ```bash
  python team-cli/team_cli.py --simple-help
  ```

# LedgerFlow AI Team CLI

## Role-Based Session Management

### How Roles Work
- Each session is created using a role directory: `roles/<role_name>/`
- The session name is used as the role name by default
- If the role directory does not exist, the CLI will warn and fall back to `python_coder`

### Role Directory Structure
```
roles/<role_name>/
  docs/                  # Role-specific documentation (markdown, guides, SOPs, etc.)
  .env.sample            # Environment variable template for this role
  mcp_config.template.json # MCP server config template (custom toolset for this role)
  README.md              # (Optional) Explain the role's purpose and setup
```

### Custom MCP Config
- If `mcp_config.template.json` is present in the role directory, it will be used to generate the session's `payload/mcp_config.json`
- If not, the CLI uses the default MCP config
- You can define custom tools, servers, or environment variables per role

### Example Role
- See `roles/example_role/` for a complete template
- Includes sample docs, env, and MCP config
- Copy and customize this folder to create new roles

### Creating a New Role
1. Copy `roles/example_role/` to `roles/<your_role_name>/`
2. Edit `docs/` to add onboarding, checklists, or SOPs
3. Edit `.env.sample` for required environment variables
4. Edit `mcp_config.template.json` for custom tools/servers (optional)
5. (Optional) Add a `README.md` to explain the role

### Session Creation
- When you run `create-crew` or `create-session`, the CLI:
  - Uses the session name as the role
  - Copies docs from `roles/<role>/docs/` into the session's payload
  - Uses the role's MCP config if present
  - Warns and falls back to `python_coder` if the role directory is missing

### Example CLI Output
```
Creating session: example_role
Available roles/templates:
- pm_guardian
- example_role
- python_coder
Created session 'example_role' from role 'example_role' in project 'example_project'.
Included docs in session payload: ...
Using custom MCP config template for role: roles/example_role
Generated .../payload/mcp_config.json
```

### Best Practices
- Always create a role directory for each session type you want to customize
- Use the example_role as a starting point
- Keep docs, env, and MCP config together for each role
- The CLI will always tell you which role and config are being used 