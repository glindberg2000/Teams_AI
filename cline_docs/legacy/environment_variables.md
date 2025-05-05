# Environment Variables

## Overview

Environment variables are used throughout the LedgerFlow AI Team framework to configure agent behavior, set up API credentials, and manage team relationships. All environment configuration is stored in `teams/{project}/config/env`.

## Core Environment Variables

### Team Configuration

- `TEAM_NAME` - Name of the team (e.g., "ledgerflow-team")
- `TEAM_DESCRIPTION` - Brief description of the team
- `PROJECT_NAME` - Name of the project the team is working on
- `LEDGERFLOW_EMAIL_PREFIX` - Prefix used for generated email addresses

### Documentation Configuration

- `INCLUDE_GLOBAL_DOCS` - Whether to include global documentation (true/false)
- `INCLUDE_PROJECT_DOCS` - Whether to include project documentation (true/false)
- `INCLUDE_ROLE_DOCS` - Whether to include role documentation (true/false)

### Required API Keys and Tokens

- `ANTHROPIC_API_KEY` - API key for Claude/Anthropic integration
- `PERPLEXITY_API_KEY` - API key for Perplexity research capabilities
- `GITHUB_PERSONAL_ACCESS_TOKEN` - GitHub PAT for repository access
- `SLACK_BOT_TOKEN` - Slack bot token for chat integration
- `SLACK_TEAM_ID` - Slack workspace team ID
- `SLACK_WORKSPACE_ID` - Same as SLACK_TEAM_ID

### Task Master MCP Configuration

- `MODEL` - Claude model to use (e.g., "claude-3-sonnet-20240229")
- `PERPLEXITY_MODEL` - Perplexity model to use (e.g., "sonar-medium-online")
- `MAX_TOKENS` - Maximum tokens for AI responses
- `TEMPERATURE` - Temperature for AI model responses
- `DEFAULT_SUBTASKS` - Default number of subtasks for `expand`
- `DEFAULT_PRIORITY` - Default priority for new tasks
- `DEBUG` - Enable debug logging (true/false)
- `LOG_LEVEL` - Console output level (debug, info, warn, error)

### Role-Specific Variables

For each role (e.g., PM_GUARDIAN, PYTHON_CODER, REVIEWER), the following variables are defined:

- `ROLE_EMAIL` - Email address for the role
- `ROLE_SLACK_TOKEN` - Slack bot token for this role
- `ROLE_GITHUB_TOKEN` - GitHub PAT for this role
- `ROLE_BOT` - Bot username for this role
- `ROLE_GITHUB` - GitHub username for this role
- `ROLE_DISPLAY` - Display name for this role

## Environment File Handling

When creating sessions using `team_cli.py create-crew`, the environment variables are processed as follows:

1. Load team environment from `teams/{project}/config/env`
2. Extract role-specific variables based on role name
3. Fill in the session's `.env` file with only team variables and role-specific variables
4. Resolve template variables like `${TEAM_NAME}`

If .env files need to be fixed, use the `fix_env_files.py` script:

```bash
python fix_env_files.py [project_name]
``` 