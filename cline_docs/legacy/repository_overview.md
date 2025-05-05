# LedgerFlow AI Team Repository Overview

## Repository Structure

The repository is organized with a domain-centric approach, using teams as the primary organizational units:

- `teams/` - Contains all team configurations and sessions
  - `teams/{project}/config/` - Environment files and checklists for each team
  - `teams/{project}/sessions/{agent}/` - Individual agent environments
- `roles/` - Role templates (python_coder, pm_guardian, reviewer, etc.)
- `docs/` - Documentation organized by scope
  - `docs/global/` - Documentation relevant to all agents and teams
  - `docs/projects/` - Project-specific documentation
  - `docs/role/` - Role-specific documentation
- `tools/` - CLI tools for team management
  - `tools/scaffold_team.py` - Generate team scaffolding
  - `tools/team_cli.py` - Manage team sessions
- `templates/` - System-wide templates

## Workflow

1. Create a new team using `scaffold_team.py`
2. Edit the team's environment files in `teams/{project}/config/`
3. Create sessions for the team using `team_cli.py create-crew`
4. Launch agent containers using their devcontainer configurations

## Environment Setup

Each agent session includes:
- A `.devcontainer` configuration for VSCode/Cursor
- A `payload` directory with:
  - `.env` file with environment variables
  - `.ssh` directory with SSH keys
  - `mcp_config.json` for MCP server configuration
  - `docs` directory with inherited documentation

## Best Practices

- Always use the tools to create and manage teams and sessions
- Keep sensitive information in `teams/{project}/config/env` and never commit it
- Generate unique SSH keys for each agent
- Follow the documentation inheritance model: global → project → role → session 