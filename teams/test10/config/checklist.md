# Test10 Team Setup Checklist

## Required Accounts & Access

### GitHub Setup
- [ ] Create GitHub account with email: gpl+test10@gmail.com
- [ ] Generate Personal Access Token (PAT)
  - Go to: https://github.com/settings/tokens
  - Required scopes: repo, workflow, read:org
  - Add token to .env.test10 as GITHUB_PERSONAL_ACCESS_TOKEN

### Slack Setup
- [ ] Join Slack workspace
- [ ] Create Slack app for bot integration
  - Go to: https://api.slack.com/apps
  - Create New App > From scratch
  - Name: test10-bot
  - Add to workspace
  - Add scopes: channels:read, chat:write, reactions:write
  - Install to workspace
  - Copy Bot User OAuth Token to .env.test10 as SLACK_BOT_TOKEN
  - Copy Team ID from workspace URL to .env.test10 as SLACK_TEAM_ID

### AI Integration
- [ ] Get Anthropic API key
  - Go to: https://console.anthropic.com
  - Create API key
  - Add to .env.test10 as ANTHROPIC_API_KEY
- [ ] Get Perplexity API key
  - Go to: https://perplexity.ai
  - Create API key
  - Add to .env.test10 as PERPLEXITY_API_KEY

### SSH Setup
- [ ] Generate SSH key pair:
  ```bash
  ssh-keygen -t ed25519 -C "gpl+test10@gmail.com" -f ~/.ssh/test10_key
  ```
- [ ] Add to GitHub account
  - Go to: https://github.com/settings/keys
  - Add new SSH key
  - Paste contents of ~/.ssh/test10_key.pub

### Backup Setup
- [ ] Set up secure backup location (e.g., iCloud)
- [ ] Add path to .env.test10 as BACKUP_TARGET
- [ ] Test backup script works

## Role-Specific Setup

### Pm Guardian
- [ ] Create email alias: `gpl+test10-pm_guardian@gmail.com`
- [ ] Set up Slack user: `@test10-pm_guardian`
- [ ] Create GitHub account: `test10-pm_guardian`
- [ ] Add to team Slack channels
- [ ] Add to GitHub organization/team
- [ ] Set up repository access

### Python Coder
- [ ] Create email alias: `gpl+test10-python_coder@gmail.com`
- [ ] Set up Slack user: `@test10-python_coder`
- [ ] Create GitHub account: `test10-python_coder`
- [ ] Add to team Slack channels
- [ ] Add to GitHub organization/team
- [ ] Set up repository access

## Environment File
- [ ] Copy .env.test10 to secure storage
- [ ] Fill in all required values
- [ ] Test environment loads correctly

## Container Setup
- [ ] Install Docker Desktop
- [ ] Install VS Code with Remote Containers extension
- [ ] Test container builds and runs
- [ ] Verify all tools work inside container

## Final Checks
- [ ] All environment variables set
- [ ] SSH key works with GitHub
- [ ] Slack bot responds
- [ ] Backup location accessible
- [ ] Container builds successfully
