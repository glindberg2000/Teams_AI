# LedgerFlow AI Team Workspace

A secure, isolated environment for AI agent development and collaboration, providing role-based access, documentation inheritance, and standardized configuration.

## Overview

LedgerFlow AI Team provides a robust, reproducible workflow for creating, configuring, and managing teams of AI agents. The system is designed for both human and AI users, with a focus on security, modularity, and documentation.

## Key Features

- **Isolated Agent Environments**: Each agent gets a separate container with its own configuration and SSH keys
- **Documentation Inheritance**: Global → Project → Role → Session hierarchy
- **Secure Secret Management**: No sensitive data in Git repository
- **Role-Based Configuration**: Role-specific templates and documentation
- **Automated Setup**: Scripted creation of team environments
- **Task Master Integration**: Advanced task management for AI-driven workflows (see cline_docs/README-task-master.md)

## Directory Structure

```
LedgerFlow_AI_Team/
├── cline_docs/                # Project-level docs, migration guides, reports, advanced usage
│   ├── MIGRATION_GUIDE.md
│   ├── README-task-master.md
│   └── reports/
├── docs/                      # Generated/inherited agent docs (for containers/sessions)
│   ├── global/
│   ├── projects/
│   └── role/
├── roles/                     # Role templates and docs
│   ├── _templates/
│   ├── pm_guardian/
│   ├── python_coder/
│   └── reviewer/
├── teams/                     # User-generated team configs and sessions (gitignored)
├── templates/                 # System-wide templates (devcontainer, scripts)
├── tools/                     # Official CLI tools
│   ├── scaffold_team.py
│   ├── team_cli.py
│   └── utils/
├── scripts/                   # Deprecated/legacy scripts (in scripts/deprecated/)
├── .cursor/                   # Cursor AI config/rules
├── .gitignore
├── README.md                  # Main entrypoint for all users
└── ... (other config files)
```

> **Note:** `cline_docs/` is *never* inherited or copied into agent containers or sessions. Only `docs/` and `roles/` are used for agent/session documentation. See the now-archived [Documentation Organization Proposal](cline_docs/reports/DOCUMENTATION_ORGANIZATION_PROPOSAL.md) for historical context and verification of this separation.

## Quickstart: Official Workflow

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/LedgerFlow_AI_Team.git
cd LedgerFlow_AI_Team
```

### 2. Scaffold a New Team

```bash
python tools/scaffold_team.py --project myteam --prefix user --domain example.com
```
- This creates `teams/myteam/config/env`, `env.template`, and `checklist.md`.

### 3. Fill in Environment File
- Edit `teams/myteam/config/env` with your API keys, tokens, and team details.
- **Never commit secrets!** The `teams/` directory is gitignored by default.

### 4. Generate Agent Sessions

```bash
python tools/team_cli.py create-crew --env-file teams/myteam/config/env
```
- This creates session folders for each agent role, with:
  - `.env` file (role-specific)
  - Unique SSH keypair
  - Inherited documentation
  - Devcontainer config and restore script

### 5. Launch and Use Sessions
- Each session is ready for containerized development or AI agent operation.
- See the generated `checklist.md` for next steps.

## Documentation
- **Project/Framework Docs:** See `cline_docs/` for migration guides, advanced usage, and verification reports. *These are never inherited by agent containers.*
- **Task Master:** See `cline_docs/README-task-master.md` for advanced AI-driven task management.
- **Generated Agent Docs:** See `docs/` for global, project, and role documentation inherited by agent containers.
- **Team Manager Role:** See [`cline_docs/TEAM_MANAGER_PROMPT.md`](cline_docs/TEAM_MANAGER_PROMPT.md) for the canonical Team Manager (DevOps) prompt and guide. **Any AI or human can use this to assume full team management and DevOps responsibilities, even after a memory reset.**

> Only up-to-date reports in `cline_docs/reports/` are relevant. Outdated or legacy reports have been removed to avoid confusion.

## Security & Best Practices
- **No secrets in git:** All sensitive data is in `teams/` (gitignored).
- **Unique SSH keys:** Each agent/session gets a unique keypair.
- **Documentation inheritance:** All sessions inherit up-to-date docs from `docs/`.
- **Legacy scripts:** Deprecated scripts are in `scripts/deprecated/` for reference only.

## Task Master Integration (Optional)
- For advanced, AI-driven project management, use the Task Master tool.
- See `cline_docs/README-task-master.md` for setup and usage.

## Migration & History
- See `cline_docs/MIGRATION_GUIDE.md` for details on the repository reorganization and migration steps.

## Contributing
- Please see the main README and `cline_docs/` for up-to-date contribution guidelines.

## License
This project is proprietary and confidential. All rights reserved.

## Team Configuration & Role Management

### Adding a New Role to an Existing Team (Safe Mode)

- To add a new role to an existing team **without overwriting other roles or team members**:

  ```sh
  python tools/scaffold_team.py --project <project> --prefix <prefix> --domain <domain> --add-role <role>
  ```
  - This will **append** the new role's config block to `teams/<project>/config/env`.
  - No other roles or team members will be touched.
  - Live sessions and agent data are never overwritten by default.

### Overwrite Safeguards

- If you run the scaffolder for an existing project (normal mode), you will be **warned and prompted for confirmation** before any config file is overwritten.
- Example:
  ```sh
  python tools/scaffold_team.py --project <project> --prefix <prefix> --domain <domain> --roles pm_guardian,python_coder
  ```
  - If `teams/<project>/config/env` exists, you must confirm before it is overwritten.

### Best Practices
- All operations are strictly within `teams/<project>/` (never the legacy top-level `sessions/` directory).
- To update or add a role, use the `--add-role` flag for safety.
- To regenerate the entire team config, use the normal scaffold command, but be aware of the overwrite prompt.

## Discord MCP Integration (Permanent)

### Overview
- Discord is fully supported for all roles and teams via the [mcp-discord](https://github.com/netixc/mcp-discord) bridge.
- This enables AI agents and workflows to send/read messages, react, and automate Discord tasks.

### Setup Steps
1. **Create a Discord Bot Application**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Create a new application and add a bot.
   - Save the bot token and client ID.
2. **Set Permissions and Invite the Bot**
   - Use the OAuth2 URL Generator to select `bot` and `applications.commands` scopes.
   - Grant at least `Send Messages` and `View Channels` permissions.
   - Invite the bot to your server using the generated link.
3. **Get Channel and Guild IDs**
   - Enable Developer Mode in Discord.
   - Right-click your server and channels to copy their IDs.
4. **Install and Run the MCP Discord Bridge**
   - Clone [mcp-discord](https://github.com/netixc/mcp-discord).
   - Install with `pip install -e .` in a Python 3.10+ venv.
   - Run with `mcp-discord` or configure your MCP/agent to launch it directly.
5. **Configure MCP**
   - In `.cursor/mcp.json`, set the `discord` server to use the absolute path to `mcp-discord` and provide the required environment variables.

### Troubleshooting
- If the bot cannot send/read messages, check permissions and re-invite with the correct scopes.
- If the MCP cannot find the CLI, use the absolute path.
- See onboarding checklist for detailed, step-by-step instructions.

### See Also
- [Onboarding Checklist](teams/ledgerflow/config/checklist.md)
- [mcp-discord GitHub](https://github.com/netixc/mcp-discord)

## Cline Memory Bank: Shared Docs Workflow

1. **Scaffold your team** using the provided script. This will create a `cline_docs_shared/` folder at the team level.
2. **Before creating the crew**, fill out all files in `teams/{project}/cline_docs_shared/` with your project's product, system, and tech context.
3. **Run crew creation**. The system will copy your filled-out shared docs into each role's session payload, ensuring every role has the same context.
4. **Each role** can then fill out their own `cline_docs/` as they work.

**Never edit the templates in `roles/_templates/` directly.**  
Always fill out the shared docs at the team level before crew creation.

## Session Environment File Generation (Updated)

Each session's `.env` file is now generated to include **only the fields for that role**, mapped to standard names. This ensures clean, minimal, and secure environment files for each agent.

### What is included in each session `.env`:
- Generic/global fields (e.g., `MODEL`, `ANTHROPIC_API_KEY`, etc.)
- The following fields for the current role, mapped as follows:
  - `<ROLE>_EMAIL` → `GIT_USER_EMAIL`
  - `<ROLE>_SLACK_TOKEN` → `SLACK_BOT_TOKEN`
  - `<ROLE>_GITHUB_TOKEN` → `GITHUB_PERSONAL_ACCESS_TOKEN`
  - `<ROLE>_DISCORD_TOKEN` → `DISCORD_TOKEN`
  - `<ROLE>_DISCORD_CLIENT_ID` → `DISCORD_CLIENT_ID`
  - `<ROLE>_DISCORD_GUILD_ID` → `DISCORD_GUILD_ID`
- No other roles' fields will be present in the session `.env`.

### Discord Integration

To enable Discord integration for each agent:
- In your high-level team env file (e.g., `teams/<project>/config/env`), provide the following for each role:
  - `<ROLE>_DISCORD_TOKEN` (required)
  - `<ROLE>_DISCORD_CLIENT_ID` (required)
  - `<ROLE>_DISCORD_GUILD_ID` (optional, for server-specific features)
- These will be mapped to `DISCORD_TOKEN`, `DISCORD_CLIENT_ID`, and `DISCORD_GUILD_ID` in the session `.env`.
- The MCP config for each agent will automatically use these values.

#### Example (for pm_guardian):
```
PM_GUARDIAN_DISCORD_TOKEN=your-bot-token
PM_GUARDIAN_DISCORD_CLIENT_ID=your-client-id
PM_GUARDIAN_DISCORD_GUILD_ID=your-guild-id
```

#### Where to get these values:
- Create a Discord Application and Bot for each role at https://discord.com/developers/applications
- Copy the Bot Token and Client ID from the application page
- (Optional) Get your server's Guild ID by enabling Developer Mode in Discord and right-clicking your server

For more details, see the Discord section in `tools/scaffold_team.py` or the project documentation.

## Devcontainer SSH Key & GitHub Access Flow

### How it Works
- The team CLI generates a unique SSH keypair for each session/agent on the host machine.
- The public key is located at: `teams/<project>/sessions/<role>/payload/.ssh/id_ed25519.pub` (or `id_rsa.pub`)
- The private key is also in the same directory.
- When you launch a devcontainer, the `restore_payload.sh` script copies the keypair into `/root/.ssh/` inside the container.
- This allows the container to use SSH for git operations (clone, push, pull, PRs) as the agent.

### How to Enable GitHub Access
1. **Copy the public key** from the payload directory (see above).
2. **Add it to your GitHub account:**
   - Go to GitHub → Settings → SSH and GPG keys → New SSH key
   - Paste the public key, give it a descriptive title (e.g., "LedgerFlow Devcontainer Key"), and save.
3. **Ensure the GitHub user is a collaborator or org member** with access to the repo.
4. **Launch the container.** The restore script will ensure the key is in place for SSH authentication.
5. **Test with:**
   ```
   ssh -T git@github.com
   ```
   You should see a success message.

### Notes
- The key does NOT have to be generated inside the container; it just needs to be present and match the public key on GitHub.
- The restore script also copies `.env`, `mcp_config.json`, and docs as needed.
- This flow enables seamless SSH-based git operations and PR creation from inside the devcontainer. 