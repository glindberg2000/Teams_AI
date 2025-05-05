# Team Overview

This document provides information about how teams are structured and managed within the LedgerFlow AI Team framework.

## Team Structure

A team consists of:

1. **Configuration** - Stored in `teams/{project}/config/`
   - Environment variables (`env`)
   - Environment template (`env.template`)
   - Project checklist (`checklist.md`)
   
2. **Sessions** - Stored in `teams/{project}/sessions/`
   - One directory per agent role (e.g., `pm_guardian`, `python_coder`)
   - Each session has:
     - `.devcontainer/` - Container configuration
     - `payload/` - Agent workspace
       - `.env` - Environment variables
       - `.ssh/` - SSH keys
       - `docs/` - Inherited documentation
       - `mcp_config.json` - MCP server configuration

## Team Members

Teams typically include the following roles:

- **PM Guardian** - Project manager role
- **Python Coder** - Python development role
- **Reviewer** - Code review role
- **DB Guardian** - Database specialist role (optional)
- **Full Stack Dev** - Full-stack development role (optional)

## Team Creation

Teams are created using the scaffold_team.py tool:

```bash
python tools/scaffold_team.py --project [project-name] --prefix [email-prefix] --domain [email-domain]
```

This creates:
- Team configuration directory
- Environment template
- Project checklist

After updating the environment file with appropriate values, sessions can be created using:

```bash
python tools/team_cli.py create-crew --env-file teams/[project-name]/config/env
```

## Team Communication

Team members communicate through:

1. **Slack** - Each agent has a Slack bot token
2. **GitHub** - Each agent has a GitHub PAT
3. **Shared Repository** - Agents work on the same codebase
4. **Documentation** - Shared documentation in the payload directory

## Environment Variables

Teams share common environment variables while each agent has role-specific variables:

- Common: `ANTHROPIC_API_KEY`, `SLACK_WORKSPACE_ID`, etc.
- Role-specific: `PM_GUARDIAN_EMAIL`, `PYTHON_CODER_SLACK_TOKEN`, etc.

## Best Practices

- Use descriptive team and project names
- Set up all required API keys before creating sessions
- Ensure environment variables are properly configured
- Use unique SSH keys for each agent
- Document project requirements and specifications 