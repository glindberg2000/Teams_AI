# LedgerFlow Team Overview

## Core Team Roles

### Technical Director / Systems Architect
- Oversees overall technical direction and architecture
- Manages team configuration and session setup
- Handles system troubleshooting and integration
- Reviews and approves final implementations
- Sets and maintains project technical standards
- Coordinates cross-team technical decisions

### PM Guardian
- Owns project roadmap and milestone tracking
- Manages task prioritization and dependencies
- Ensures documentation stays current
- Coordinates between team members
- Reviews and approves major architectural decisions

### DB Guardian
- Owns database schema design and evolution
- Manages backup and restore procedures
- Monitors database performance
- Implements data migration strategies
- Reviews DB-related code changes

### Full-Stack Developer
- Implements backend APIs and services
- Builds frontend components and features
- Ensures code quality and test coverage
- Participates in code reviews
- Helps maintain development environment

### UI Specialist
- Designs and implements user interface
- Ensures consistent UX patterns
- Optimizes frontend performance
- Creates reusable UI components
- Implements responsive design

### Python Coder
- Focuses on backend Python development
- Implements core business logic
- Writes and maintains unit tests
- Reviews Python-related PRs
- Helps maintain code standards

### Reviewer
- Performs thorough code reviews
- Ensures adherence to standards
- Validates test coverage
- Checks documentation updates
- Verifies CI/CD pipeline health

## Communication Channels

### Primary
- **Slack**: #ledgerflow-dev
- **GitHub**: Pull Request discussions
- **Documentation**: Markdown in repos

### Emergency
- **PagerDuty**: LedgerFlow-Critical service
- **Slack**: #ledgerflow-alerts

## Development Workflow

1. **Task Assignment**
   - PM Guardian assigns tasks via Task Master
   - Dependencies and priorities clearly marked
   - Relevant team members notified

2. **Development**
   - Local development using Docker
   - Feature branches from `main`
   - Regular commits with clear messages
   - Documentation updates alongside code

3. **Review Process**
   - PR created with task reference
   - Reviewer assigned
   - CI checks must pass
   - Documentation reviewed
   - Backup/restore tests verified

4. **Deployment**
   - Merge to `main` triggers CI/CD
   - Automated tests run
   - Backup integrity verified
   - PM Guardian notified of completion

## Best Practices

### Code
- Follow Python style guide (black + isort)
- Write tests for new features
- Keep functions focused and documented
- Use type hints in Python code
- Follow React best practices

### Documentation
- Update docs with code changes
- Use clear, concise language
- Include examples where helpful
- Keep diagrams up to date
- Cross-reference related docs

### Security
- No secrets in code or docs
- Use .env files for configuration
- Regular security updates
- Access control review
- Backup encryption verified

### Data Safety
- Hourly backups to iCloud
- Daily integrity checks
- Restore testing in CI
- Size monitoring and alerts
- No external API dependencies

# LedgerFlow Windsurf Team

| Slack Handle | Windsurf Session | Role | TZ / Typical Hours |
|--------------|------------------|------|--------------------|
| @greg | **tech-director** | Technical Director & Systems Architect | PST (flexible) |
| @ledgerflow-guardian | **pm-guardian** | Release captain, safety gate | PST (08-16) |
| @ledgerflow-dev | **full-stack-dev** | Django + React implementation | EST (09-17) |
| @ledgerflow-db | **db-guardian** | PostgreSQL, backups, migrations | PST (10-18) |
| @ledgerflow-review | **reviewer** | PR audit & CI enforcement | CET (async) |
| @ledgerflow-task | **task-force** | Short-lived spikes / experiments | rotates |

## Escalation

1. **Prod down / data-loss risk** → page **@ledgerflow-guardian**  
2. **DB corruption / backup failure** → **@ledgerflow-db**  
3. **CI red on `main`** → **@ledgerflow-review** + #ledgerflow-ops

## Communication Channels

| Channel | Purpose |
|---------|---------|
| #ledgerflow-ops | Deploys, infra alerts |
| #ledgerflow-dev | Daily dev chatter |
| #ledgerflow-db | Schema / migration discussions |
| #ledgerflow-reviews | PR notifications |
| #ledgerflow-alerts | PagerDuty → Slack sink | 