# Testrun Team Setup Checklist

## Required Accounts & Access

### GitHub Setup
- [ ] Create GitHub account with email: user+testrun@example.com
- [ ] Generate Personal Access Token (PAT)
  - Go to: https://github.com/settings/tokens
  - Required scopes: repo, workflow, read:org
  - Add token to .env.testrun as GITHUB_PERSONAL_ACCESS_TOKEN

### Slack Setup
- [ ] Join Slack workspace
- [ ] Create Slack app for bot integration
  - Go to: https://api.slack.com/apps
  - Create New App > From scratch
  - Name: testrun-bot
  - Add to workspace
  - Add scopes: channels:read, chat:write, reactions:write
  - Install to workspace
  - Copy Bot User OAuth Token to .env.testrun as SLACK_BOT_TOKEN
  - Copy Team ID from workspace URL to .env.testrun as SLACK_TEAM_ID and SLACK_WORKSPACE_ID

### AI Integration
- [ ] Get Anthropic API key
  - Go to: https://console.anthropic.com
  - Create API key
  - Add to .env.testrun as ANTHROPIC_API_KEY
- [ ] Get Perplexity API key
  - Go to: https://perplexity.ai
  - Create API key
  - Add to .env.testrun as PERPLEXITY_API_KEY

### SSH Setup
- [ ] Generate SSH key pair:
  ```bash
  ssh-keygen -t ed25519 -C "user+testrun@example.com" -f ~/.ssh/testrun_key
  ```
- [ ] Add to GitHub account
  - Go to: https://github.com/settings/keys
  - Add new SSH key
  - Paste contents of ~/.ssh/testrun_key.pub

### Backup Setup
- [ ] Set up secure backup location (e.g., iCloud)
- [ ] Add path to .env.testrun as BACKUP_TARGET
- [ ] Test backup script works

## Role-Specific Setup

### Python Coder
- [ ] Create email alias: `user+testrun-python_coder@example.com`
- [ ] Set up Slack user: `@testrun-python_coder`
- [ ] Create GitHub account: `testrun-python_coder`
- [ ] Generate GitHub PAT and add to .env.testrun as PYTHON_CODER_GITHUB_TOKEN
- [ ] Create Slack bot token and add to .env.testrun as PYTHON_CODER_SLACK_TOKEN
- [ ] Add to team Slack channels
- [ ] Add to GitHub organization/team
- [ ] Set up repository access

## Environment File
- [ ] Copy .env.testrun to secure storage
- [ ] Fill in all required values
- [ ] Test environment loads correctly

## Team Creation
- [ ] Run the team-cli create-crew command:
  ```bash
  python team-cli/team_cli.py create-crew --env-file .env.testrun
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
