# System Architecture & Patterns

## Core Architecture

### 1. Session Management
- Team CLI (`team_cli.py`)
  - Creates isolated agent sessions
  - Manages documentation inheritance
  - Handles environment setup
  - Validates session configurations

### 2. Documentation Hierarchy
```
docs/
  global/          # Team-wide documentation
  projects/        # Project-specific docs
roles/
  [role_name]/     # Role-specific docs & configs
sessions/
  _shared/         # Shared session resources
  [session_name]/  # Individual session data
```

### 3. DevContainer Setup
- `.devcontainer/` contains core setup scripts
- `scripts/` holds configuration templates
- Environment variables managed via `.env` files
- MCP configuration generated during container startup

## Technical Decisions

### 1. Isolation Strategy
- Each agent gets an isolated session directory
- Documentation inherited from multiple sources
- Secrets managed separately per session
- Container environment isolated per session

### 2. Configuration Management
- Base configs in `.devcontainer/`
- Session-specific overrides in `sessions/[name]/`
- MCP config generated from templates
- Environment variables sourced from multiple files

### 3. Documentation Distribution
- Global docs available to all sessions
- Role-specific docs inherited based on agent type
- Project docs distributed as needed
- Session-specific docs for unique requirements

## Architecture Patterns

### 1. Documentation Inheritance
```
Global Docs
    ↓
Role Docs
    ↓
Project Docs
    ↓
Session Docs
```

### 2. Configuration Flow
```
Base Config → Role Config → Session Config → Runtime Config
```

### 3. Security Patterns
- Secrets stored in session-specific `.env`
- SSH keys managed per session
- Sensitive data never committed to repo
- Container isolation for each session

## Development Patterns

### 1. Session Creation
1. Initialize base structure
2. Copy role-specific configs
3. Inherit documentation
4. Configure environment
5. Generate MCP config
6. Launch container

### 2. Documentation Updates
1. Update source documentation
2. Regenerate affected sessions
3. Verify inheritance
4. Update container configs

### 3. Configuration Changes
1. Modify template configs
2. Update affected sessions
3. Regenerate MCP configs
4. Restart containers if needed

## Best Practices

### 1. Documentation
- Keep documentation DRY
- Use markdown for consistency
- Include examples in docs
- Maintain clear hierarchy

### 2. Configuration
- Use templates where possible
- Document all env variables
- Validate configs before use
- Keep secrets separate

### 3. Development
- Test changes in isolation
- Verify documentation updates
- Follow security guidelines
- Maintain session independence 