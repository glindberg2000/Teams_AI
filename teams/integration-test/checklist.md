# Integration-test Team Setup Checklist

## Required Accounts & Access

### GitHub Setup
- [ ] Create GitHub account with email: test-user+integration-test@example.com
- [ ] Generate Personal Access Token (PAT)
  - Go to: https://github.com/settings/tokens
  - Required scopes: repo, workflow, read:org
  - Add token to .env.integration-test as GITHUB_PERSONAL_ACCESS_TOKEN

### Slack Setup
- [ ] Join Slack workspace
- [ ] Create Slack app for bot integration
  - Go to: https://api.slack.com/apps
  - Create New App > From scratch
  - Name: integration-test-bot
  - Add to workspace
  - Add scopes: channels:read, chat:write, reactions:write
  - Install to workspace
  - Copy Bot User OAuth Token to .env.integration-test as SLACK_BOT_TOKEN
  - Copy Team ID from workspace URL to .env.integration-test as SLACK_TEAM_ID and SLACK_WORKSPACE_ID

### AI Integration
- [ ] Get Anthropic API key
  - Go to: https://console.anthropic.com
  - Create API key
  - Add to .env.integration-test as ANTHROPIC_API_KEY
- [ ] Get Perplexity API key
  - Go to: https://perplexity.ai
  - Create API key
  - Add to .env.integration-test as PERPLEXITY_API_KEY

### SSH Setup
- [ ] Generate SSH key pair:
  ```bash
  ssh-keygen -t ed25519 -C "test-user+integration-test@example.com" -f ~/.ssh/integration-test_key
  ```
- [ ] Add to GitHub account
  - Go to: https://github.com/settings/keys
  - Add new SSH key
  - Paste contents of ~/.ssh/integration-test_key.pub

### Backup Setup
- [ ] Set up secure backup location (e.g., iCloud)
- [ ] Add path to .env.integration-test as BACKUP_TARGET
- [ ] Test backup script works

## Role-Specific Setup

### Pm Guardian
- [ ] Create email alias: `test-user+integration-test-pm_guardian@example.com`
- [ ] Set up Slack user: `@integration-test-pm_guardian`
- [ ] Create GitHub account: `integration-test-pm_guardian`
- [ ] Generate GitHub PAT and add to .env.integration-test as PM_GUARDIAN_GITHUB_TOKEN
- [ ] Create Slack bot token and add to .env.integration-test as PM_GUARDIAN_SLACK_TOKEN
- [ ] Add to team Slack channels
- [ ] Add to GitHub organization/team
- [ ] Set up repository access

### Python Coder
- [ ] Create email alias: `test-user+integration-test-python_coder@example.com`
- [ ] Set up Slack user: `@integration-test-python_coder`
- [ ] Create GitHub account: `integration-test-python_coder`
- [ ] Generate GitHub PAT and add to .env.integration-test as PYTHON_CODER_GITHUB_TOKEN
- [ ] Create Slack bot token and add to .env.integration-test as PYTHON_CODER_SLACK_TOKEN
- [ ] Add to team Slack channels
- [ ] Add to GitHub organization/team
- [ ] Set up repository access

## Environment File
- [ ] Copy .env.integration-test to secure storage
- [ ] Fill in all required values
- [ ] Test environment loads correctly

## Team Creation
- [ ] Run the team-cli create-crew command:
  ```bash
  python team-cli/team_cli.py create-crew --env-file .env.integration-test
  ```

## Container Setup
- [ ] Install Docker Desktop
- [ ] Install VS Code with Remote Containers extension
- [ ] Open each session folder in VS Code and launch DevContainer
- [ ] Verify all tools work inside container

## Final Checks
- [ ] All environment variables set
- [ ] SSH key works with GitHub
- [ ] Slack bot responds
- [ ] Backup location accessible
- [ ] Containers build successfully
