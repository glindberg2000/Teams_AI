# LedgerFlow Team Setup Guide

This guide walks through the process of setting up the LedgerFlow AI team environment.

## Prerequisites

1. **System Requirements**
   - Python 3.7+
   - Node.js 14.0.0+ (for Task Master)
   - Docker and Docker Compose
   - VS Code with Remote Containers extension (recommended)

2. **Required API Keys**
   - Anthropic API key (for Claude/Task Master)
   - Perplexity API key (recommended for research capabilities)
   - GitHub Personal Access Token (for repo access)
   - Slack Bot Token (for team communication)

## Setup Process

### 1. Repository Setup
```bash
# Clone the repository
git clone [repository-url]
cd LedgerFlow_AI_Team

# Copy environment templates
cp .env.example .env
cp .env.team.example .env.team
```

### 2. Environment Configuration

1. **Core Environment (.env)**
   ```bash
   # Required:
   ANTHROPIC_API_KEY=your_key_here
   PERPLEXITY_API_KEY=your_key_here  # recommended
   
   # Optional Task Master settings:
   MODEL=claude-3-opus-20240229
   MAX_TOKENS=8192
   TEMPERATURE=0.7
   DEBUG=false
   LOG_LEVEL=info
   ```

2. **Team Environment (.env.team)**
   ```bash
   # Required:
   LEDGERFLOW_EMAIL_PREFIX=your_prefix  # for email addresses
   SLACK_BOT_TOKEN=your_token_here
   GITHUB_TOKEN=your_pat_here
   
   # Optional:
   REGISTRY_URL=your_registry  # if using private registry
   ```

### 3. Session Creation

Use the team-cli tool to create your session:

```bash
# Create a new session with SSH key generation
python team-cli/team_cli.py create-session \
  --name your-session-name \
  --role python_coder \
  --generate-ssh-key \
  --prompt-all

# Or, to include project docs:
python team-cli/team_cli.py create-session \
  --name your-session-name \
  --role python_coder \
  --project sample_project \
  --generate-ssh-key \
  --prompt-all
```

### 4. Payload Preparation

```bash
# Prepare the session payload
python team-cli/team_cli.py prepare-payload --name your-session-name
```

### 5. Container Setup

1. **Build Base Containers**
   ```bash
   docker-compose build
   ```

2. **Initialize Task Master**
   ```bash
   docker-compose run --rm ledgerflow-pm task-master init
   ```

3. **Start Core Services**
   ```bash
   docker-compose up -d ledgerflow-pm ledgerflow-db ledgerflow-review
   ```

### 6. Session Activation

1. Open your session folder in VS Code
2. When prompted, click "Reopen in Container"
3. Once inside the container, run:
   ```bash
   bash /workspaces/project/payload/restore_payload.sh
   ```

## Container Roles

| Container | Purpose | Required Secrets |
|-----------|---------|-----------------|
| ledgerflow-pm | Project management, CI/CD | All in .env.team |
| ledgerflow-dev | Full-stack development | ANTHROPIC_API_KEY, GITHUB_TOKEN |
| ledgerflow-db | Database management | ANTHROPIC_API_KEY |
| ledgerflow-review | Code review, quality | ANTHROPIC_API_KEY, GITHUB_TOKEN |
| ledgerflow-taskforce | Specialist tasks | ANTHROPIC_API_KEY |

## Environment Files

1. `.env` - Core AI and project configuration
   - AI API keys
   - Model settings
   - Project metadata

2. `.env.team` - Team and integration configuration
   - Email settings
   - Slack integration
   - GitHub access
   - Container registry

## Security Notes

- Store `.env` and `.env.team` in secure storage (1Password, etc.)
- Never commit environment files to git
- SSH keys are generated in `payload/.ssh/` and never tracked
- All generated session folders are git-ignored
- Rotate API keys and tokens regularly
- Use separate tokens for each team member

## Troubleshooting

1. **Container Access Issues**
   - Verify `.env.team` credentials
   - Check Docker network connectivity
   - Ensure registry authentication

2. **Integration Problems**
   - Validate Slack tokens
   - Check GitHub permissions
   - Verify email configuration

3. **Task Master Issues**
   - Confirm ANTHROPIC_API_KEY is valid
   - Check task file permissions
   - Verify project initialization

## Maintenance

1. **Regular Updates**
   ```bash
   # Update DevContainer configs
   ./sync-devcontainer.sh
   
   # Pull latest images
   docker-compose pull
   
   # Rebuild containers
   docker-compose build --no-cache
   ```

2. **Security Checks**
   - Audit access tokens
   - Review container permissions
   - Check secret rotation

3. **Backup Verification**
   - Test environment restoration
   - Verify secret recovery
   - Validate container state 