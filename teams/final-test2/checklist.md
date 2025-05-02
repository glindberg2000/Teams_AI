# final-test2 Team Setup Checklist

## Core Setup

- [ ] Clone the LedgerFlow AI Team repository
- [ ] Create a `.env.final-test2` file in the root (already done - see details below)
- [ ] Fill in all required API keys in `.env.final-test2`
- [ ] Run `python team-cli/team_cli.py create-crew --env-file .env.final-test2` to create all sessions

## API Keys Required

### Team Level

- [ ] **ANTHROPIC_API_KEY**: Get from https://console.anthropic.com
- [ ] **PERPLEXITY_API_KEY**: Get from https://perplexity.ai (optional)
- [ ] **GITHUB_PERSONAL_ACCESS_TOKEN**: Create at https://github.com/settings/tokens
- [ ] **SLACK_BOT_TOKEN**: Create at https://api.slack.com/apps
- [ ] **SLACK_TEAM_ID**: Get from Slack workspace settings

### Per-Role API Keys

#### Pm Guardian

- [ ] **PM_GUARDIAN_SLACK_TOKEN**: Unique Slack bot token for this role
- [ ] **PM_GUARDIAN_GITHUB_TOKEN**: Unique GitHub PAT for this role

#### Python Coder

- [ ] **PYTHON_CODER_SLACK_TOKEN**: Unique Slack bot token for this role
- [ ] **PYTHON_CODER_GITHUB_TOKEN**: Unique GitHub PAT for this role

## Session Management

- Use `team-cli/team_cli.py create-session` to create individual sessions
- Use `team-cli/team_cli.py create-crew --env-file .env.final-test2` to create all sessions at once
- Each session will have its own isolated environment with unique SSH keys