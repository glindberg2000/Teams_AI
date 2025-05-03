# final-test Team Setup Checklist

## Core Setup

- [ ] Clone the LedgerFlow AI Team repository
- [ ] Create `teams/final-test/config/env` file (already done - see details below)
- [ ] Fill in all required API keys in `teams/final-test/config/env`
- [ ] Run `python tools/team_cli.py create-crew --env-file teams/final-test/config/env` to create all sessions

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

#### Reviewer

- [ ] **REVIEWER_SLACK_TOKEN**: Unique Slack bot token for this role
- [ ] **REVIEWER_GITHUB_TOKEN**: Unique GitHub PAT for this role

## Session Management

- Use `tools/team_cli.py create-session` to create individual sessions
- Use `tools/team_cli.py create-crew --env-file teams/final-test/config/env` to create all sessions at once
- Each session will have its own isolated environment with unique SSH keys

## Troubleshooting

- **Session Extraction Issues**: If team-cli isn't finding your sessions, check that your environment variables follow the pattern `ROLE_SLACK_TOKEN` (e.g., `PM_GUARDIAN_SLACK_TOKEN`).
- **Missing Keys**: Ensure each role has all required tokens (Slack, GitHub) in the environment file.
- **Role Directory Not Found**: The warning about falling back to python_coder is normal if you don't have a custom role directory. Create `roles/your_role_name/` for custom role configuration.