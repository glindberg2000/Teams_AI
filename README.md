# LedgerFlow AI Team Workspace

A secure, isolated environment for AI agent development and collaboration, providing role-based access, documentation inheritance, and standardized configuration.

## Overview

LedgerFlow AI Team provides two primary tools for managing AI agent environments:

1. **scaffold_team.py**: Generates standardized team configuration files (teams/{project}/config/env) and setup checklists.
2. **team-cli.py**: Creates isolated agent sessions based on the configuration.

## Key Features

- **Isolated Agent Environments**: Each agent gets a separate container with its own configuration and SSH keys
- **Documentation Inheritance**: Global → Project → Role → Session hierarchy
- **Secure Secret Management**: No sensitive data in Git repository
- **Role-Based Configuration**: Role-specific templates and documentation
- **Automated Setup**: Scripted creation of team environments

## Directory Structure
## Directory Structure

```
LedgerFlow_AI_Team/
├── teams/                       # All team-related content in one place
│   ├── _templates/              # Shared templates for all teams
│   ├── _shared/                 # Shared resources across teams
│   ├── {team1}/                 # Everything for team1
│   │   ├── config/              # Team configuration
│   │   │   ├── env              # Environment file (was .env.team1)
│   │   │   ├── checklist.md     # Setup instructions
│   │   │   └── manifest.json    # Team composition details
│   │   └── sessions/            # Team sessions
│   │       ├── pm_guardian/     # Session for this role
│   │       └── python_coder/    # Session for this role
│   └── {team2}/                 # Another team's config and sessions
├── roles/                       # Role templates and documentation
│   ├── _templates/              # Shared templates for all roles
│   ├── pm_guardian/             # PM Guardian role definition
│   ├── python_coder/            # Python Coder role definition
│   └── reviewer/                # Reviewer role definition
├── docs/                        # Global documentation
│   ├── global/                  # Global docs for all teams
│   └── projects/                # Docs specific to projects
├── tools/                       # Command-line tools
│   ├── scaffold_team.py         # Team configuration generator
│   ├── team_cli.py              # Session management tool
│   └── utils/                   # Helper utilities
├── templates/                   # System-wide templates
│   ├── devcontainer/            # Base container configuration
│   └── scripts/                 # Helper scripts
├── README.md
└── pyproject.toml
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/LedgerFlow_AI_Team.git
cd LedgerFlow_AI_Team
```

### 2. Create a Team Configuration

Use `scaffold_team.py` to generate team configuration files:

```bash
# Interactive mode (recommended for first-time setup)
python tools/scaffold_team.py

# Non-interactive mode with CLI flags
python tools/scaffold_team.py --project testproject --prefix user
```

This generates:
- Environment file (teams/{project}/config/env)
- Environment template (teams/{project}/config/env.template)
- Setup checklist (teams/{project}/config/checklist.md)

### 3. Create Agent Sessions

Use `team_cli.py` to create agent sessions:

```bash
# Create a single agent session with an automatically generated SSH key
python tools/team_cli.py create-session --project testproject --name agent1 --role python_coder --generate-ssh-key

# Create a single agent session with an existing SSH key
python tools/team_cli.py create-session --project testproject --name agent2 --role pm_guardian --ssh-key ~/.ssh/existing_key

# Create all agent sessions defined in the environment file
python tools/team_cli.py create-crew --env-file .env.testproject
```

### 4. Access Agent Sessions

Each agent session is an isolated environment with its own documentation, SSH key, and configuration:

```bash
cd sessions/testproject/agent1

# Start the agent's container
./restore.sh

# Connect to the agent's container using SSH
ssh -i ~/.ssh/agent1_key agent@localhost -p 2222
```

## Environment Variable Naming Conventions

To ensure compatibility between `scaffold_team.py` and `team-cli.py`, the following naming conventions are used:

1. Role-specific variables use the format: `ROLE_UPPER_KEY_NAME`
   - Example: `PM_GUARDIAN_SLACK_TOKEN`, `PYTHON_CODER_GITHUB_TOKEN`

2. Global variables use the format: `PROJECT_KEY_NAME`
   - Example: `PROJECT_ROOT_URL`, `PROJECT_DATABASE_URL`

These conventions are critical for proper session extraction in `team-cli.py`.

## Troubleshooting

### Common Issues

1. **Session extraction fails**: 
   - Ensure environment variables follow the naming convention `ROLE_UPPER_KEY_NAME`
   - Check that required keys exist for each role (`_SLACK_TOKEN`, `_ROLE_ARN`, etc.)

2. **SSH key permission issues**:
   - Run `chmod 600 path/to/key` to set correct permissions on SSH private keys

3. **Container won't start**:
   - Check Docker is running
   - Verify port conflicts with `docker ps`

For more information, see the documentation in the `/docs` directory.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## License

This project is proprietary and confidential. All rights reserved. 