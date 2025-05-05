# System Architecture & Patterns

## Core Architecture

### 1. Session Management
- Team CLI (`team_cli.py`)
  - Creates isolated agent sessions
  - Manages documentation inheritance
  - Handles environment setup
  - Validates session configurations
  - Extracts sessions from standardized environment variables
  - Creates all sessions for a team with create-crew command

### 2. Team Configuration
- Scaffold Script (`scaffold_team.py`)
  - Generates team environment files (.env.{project})
  - Creates setup checklists (teams/{project}/checklist.md)
  - Establishes standardized naming conventions with ROLE_SLACK_TOKEN pattern
  - Produces environment templates compatible with team-cli
  - Validates roles against approved list
  - Supports interactive or command-line configuration

### 3. Documentation Hierarchy
```
docs/
  global/          # Team-wide documentation
  projects/        # Project-specific docs
    {project}/     # Individual project docs
roles/
  {role}/          # Role-specific docs & configs
    docs/          # Role documentation
    .env.sample    # Environment template
sessions/
  _shared/         # Shared session resources
  {project}/       # Project-specific sessions
    {agent}/       # Individual session data
      .devcontainer/  # Container configuration
      payload/        # Agent workspace
teams/
  {project}/       # Team-specific config and checklists
    checklist.md   # Setup instructions
    env.template   # Environment template
```

### 4. DevContainer Setup
- `.devcontainer/` contains core setup scripts
- Each session has its own `.devcontainer/` copied from the template
- Environment variables managed via `.env` files in payload
- MCP configuration generated during container startup
- SSH keys managed per session

## Technical Decisions

### 1. Isolation Strategy
- Each agent gets an isolated session directory
- Documentation inherited from multiple sources in a specific order
- Secrets managed separately per session
- Container environment isolated per session
- Individual SSH keys for secure access

### 2. Configuration Management
- Base configs in `.devcontainer/`
- Session-specific overrides in `sessions/{project}/{agent}/`
- MCP configuration generated from templates for each agent
- Environment variables in payload/.env
- Standardized naming conventions for environment variables

### 3. Documentation Distribution
- Global docs available to all sessions
- Project docs distributed to sessions within that project
- Role-specific docs inherited based on agent type
- All documentation merged in payload/docs with source-specific subdirectories

### 4. Team Configuration Workflow
- Generate team config with scaffold_team.py
- Follow checklist to set up accounts and tokens
- Create sessions with team-cli create-crew command
- Launch containers with properly configured environments
- Each session runs independently but collaborates through shared services

## Architecture Patterns

### 1. Documentation Inheritance
```
Global Docs
    ↓
Project Docs
    ↓
Role Docs
    ↓
Session Docs
```

### 2. Configuration Flow
```
scaffold_team.py → .env.{project} → team-cli.py → Session Config → Container
```

### 3. Team Setup Flow
```
scaffold_team.py → Manual API Setup → team-cli create-crew → Container Launch
```

### 4. Security Patterns
- Secrets stored in session-specific `.env` files
- SSH keys managed per session in payload/.ssh
- Sensitive data never committed to repo (in .gitignore)
- Container isolation for each session
- Proper file permissions for SSH keys

### 5. Environment Variable Patterns
- Team-level variables: SLACK_BOT_TOKEN, GITHUB_PERSONAL_ACCESS_TOKEN, etc.
- Role-specific variables: ROLE_SLACK_TOKEN, ROLE_GITHUB_TOKEN, ROLE_EMAIL
- Container variables: MODEL, TEMPERATURE, DEBUG, etc.
- Secret variables: ANTHROPIC_API_KEY, PERPLEXITY_API_KEY, etc.

## Development Patterns

### 1. Session Creation
1. Initialize base structure from role template
2. Copy role-specific configs 
3. Inherit documentation from multiple sources
4. Configure environment variables
5. Generate MCP configuration
6. Set up SSH keys
7. Create restore script

### 2. Team Setup
1. Run scaffold_team.py to generate team configuration
2. Complete setup checklist (accounts, tokens, keys)
3. Run team-cli create-crew with team configuration
4. Launch containers for all team members/roles
5. Verify successful setup of all sessions

### 3. Documentation Updates
1. Update source documentation (global, project, or role)
2. Regenerate affected sessions as needed
3. Verify inheritance in session payload
4. Update container configurations if necessary

### 4. Configuration Changes
1. Modify template configs or environment files
2. Update affected sessions
3. Regenerate MCP configurations
4. Restart containers if needed

## Best Practices

### 1. Documentation
- Keep documentation DRY (Don't Repeat Yourself)
- Use markdown for consistency and readability
- Include examples in documentation
- Maintain clear hierarchy for inheritance
- Update documentation when changing implementation

### 2. Configuration
- Use templates where possible
- Document all environment variables
- Validate configurations before use
- Keep secrets separate from code
- Follow consistent naming conventions

### 3. Development
- Test changes in isolation
- Verify documentation updates
- Follow security guidelines
- Maintain session independence
- Use standardized naming patterns
- Add helpful comments for complex logic

### 4. Troubleshooting
- Check environment variable format first
- Verify SSH key permissions
- Validate role configuration
- Check documentation inheritance
- Review MCP configuration generation
- Inspect container initialization 

# Only current, actionable system patterns are kept here. All legacy, migration, and reorg notes have been moved to cline_docs/legacy/. 

# Cline Memory Bank: Shared Docs Workflow (Summary)

- Fill out `teams/{project}/cline_docs_shared/` after scaffolding, before crew creation.
- Crew creation copies the filled shared docs into each session's payload.
- See productContext.md for full workflow details. 