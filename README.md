# LedgerFlow AI Team Workspace

A secure, isolated environment for AI agent development and collaboration, providing role-based access, documentation inheritance, and standardized configuration.

## Overview

LedgerFlow AI Team provides two primary tools for managing AI agent environments:

1. **scaffold_team.py**: Generates standardized team configuration files (.env.{project}) and setup checklists.
2. **team-cli.py**: Creates isolated agent sessions based on the configuration.

## Key Features

- **Isolated Agent Environments**: Each agent gets a separate container with its own configuration and SSH keys
- **Documentation Inheritance**: Global → Project → Role → Session hierarchy
- **Secure Secret Management**: No sensitive data in Git repository
- **Role-Based Configuration**: Role-specific templates and documentation
- **Automated Setup**: Scripted creation of team environments

## Directory Structure

```
LedgerFlow_AI_Team/
├── .env.{project}        # Project environment variables (generated)
├── scaffold_team.py      # Team configuration generator
├── docs/                 # Documentation
│   ├── global/           # Team-wide docs
│   └── projects/         # Project-specific docs
│       └── {project}/    # Docs for a specific project
├── roles/                # Role templates
│   ├── python_coder/     # Example role
│   │   ├── docs/         # Role documentation
│   │   ├── .env.sample   # Environment template
│   │   └── mcp_config.template.json  # MCP config template
│   └── {role}/           # Other role templates
├── sessions/             # Agent environments
│   ├── _shared/          # Shared resources
│   └── {project}/        # Project-specific sessions
│       └── {agent}/      # Individual agent session
│           ├── .devcontainer/  # Container configuration
│           └── payload/   # Agent workspace
├── team-cli/             # Team management CLI
│   └── team_cli.py       # CLI implementation
└── teams/                # Team configuration files
    └── {project}/        # Project-specific config
        ├── checklist.md  # Setup instructions
        └── env.template  # Environment template
```

## Workflow: scaffold_team.py → team-cli.py

The complete workflow for setting up a new AI team involves:

1. **Generate Team Configuration** with scaffold_team.py:
   ```bash
   # Full interactive mode
   python scaffold_team.py
   
   # With command-line arguments
   python scaffold_team.py --project myteam --prefix user --domain example.com --roles pm_guardian,python_coder
   ```
   
   This creates:
   - `.env.myteam` file with environment variables (team and per-role)
   - `teams/myteam/checklist.md` with setup instructions
   - `teams/myteam/env.template` for reference

2. **Fill in Required API Keys** in the generated `.env.myteam` file:
   - Team-level: `ANTHROPIC_API_KEY`, `GITHUB_PERSONAL_ACCESS_TOKEN`, `SLACK_BOT_TOKEN`, etc.
   - Per-role tokens: `PM_GUARDIAN_SLACK_TOKEN`, `PM_GUARDIAN_GITHUB_TOKEN`, etc.

3. **Create Agent Sessions** with team-cli.py:
   ```bash
   python team-cli/team_cli.py create-crew --env-file .env.myteam
   ```
   
   This creates:
   - Agent session directories in `sessions/myteam/`
   - DevContainer configuration for each agent
   - SSH key pair for each agent
   - Documentation from global, project, and role sources

4. **Launch Agent Containers**:
   - Open each agent directory in VS Code/Cursor
   - Use "Reopen in Container" to start the agent's container
   - The container restore script configures everything automatically

## Environment Variable Naming Convention

For team-cli.py to correctly create sessions, environment variables must follow these patterns:

- `ROLE_EMAIL`: The role's email address (e.g., `PM_GUARDIAN_EMAIL`)
- `ROLE_SLACK_TOKEN`: The role's Slack bot token (e.g., `PM_GUARDIAN_SLACK_TOKEN`)
- `ROLE_GITHUB_TOKEN`: The role's GitHub token (e.g., `PM_GUARDIAN_GITHUB_TOKEN`)

Team-cli extracts session names by parsing these variables:
- `PM_GUARDIAN_SLACK_TOKEN` → `pm_guardian`
- `PYTHON_CODER_GITHUB_TOKEN` → `python_coder`

The scaffold_team.py script automatically generates variables in the correct format.

## Commands and Options

### scaffold_team.py

```bash
# Interactive mode
python scaffold_team.py

# Command-line mode
python scaffold_team.py --project myteam --prefix user --domain example.com --roles pm_guardian,python_coder

# Help
python scaffold_team.py --help
```

### team-cli.py

```bash
# Create all sessions for a project
python team-cli/team_cli.py create-crew --env-file .env.myteam

# Create a single session
python team-cli/team_cli.py create-session --name agent1 --role python_coder --generate-ssh-key

# Add a new role template
python team-cli/team_cli.py add-role new_role_name

# Help
python team-cli/team_cli.py --help
```

## Documentation Inheritance

Documentation is organized in a hierarchical structure and combined during session creation:

1. **Global Documentation** (`docs/global/`): Available to all agents
2. **Project Documentation** (`docs/projects/{project}/`): Project-specific docs
3. **Role Documentation** (`roles/{role}/docs/`): Role-specific docs

The final documentation is combined in the agent's payload directory: `sessions/{project}/{agent}/payload/docs/`.

## Troubleshooting

### Environment Configuration

- **Session Extraction Issues**: If team-cli isn't creating sessions for certain roles, check that your environment variables follow the naming pattern described above. 
- **Missing Keys**: If you see "Missing required keys" errors, ensure each role has all the tokens specified (Slack, GitHub) in the environment file.

### Role Templates

- **"Role not found" Warning**: If you see a warning about a role not found, create a directory in `roles/{role_name}/` with the appropriate structure.
- **"Falling back to python_coder"**: This is normal if you're using a role that doesn't have a custom template. You can create a custom role template if needed.

### SSH Keys

- **"No SSH private key found"**: Either generate a key with `--generate-ssh-key` or provide one with `--ssh-key`.
- **SSH Key Permission Issues**: Ensure the SSH key permissions are set to 600 (read/write for owner only).

## Security Notes

- **Never commit .env files or SSH keys to git**
- All sensitive directories are already in .gitignore
- Store secrets in secure storage (1Password, iCloud, etc.)
- Use unique SSH keys for each agent
- The restore script sets proper permissions inside containers

## Requirements

- Python 3.7+
- Docker for containers
- VS Code or Cursor with Remote Containers extension
- Git
- Node.js (for MCP servers)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

This project is proprietary and confidential. All rights reserved. 