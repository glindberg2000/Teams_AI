# LedgerFlow Team Overview

## Core Team Roles

### Technical Director / Systems Architect
- Oversees overall technical direction and architecture
- Manages team configuration and session setup
- Handles system troubleshooting and integration
- Reviews and approves final implementations
- Sets and maintains project technical standards
- Coordinates cross-team technical decisions

### PM Guardian (ledgerflow-pm)
- Owns project roadmap and milestone tracking
- Manages task prioritization and dependencies
- Ensures documentation stays current
- Coordinates between team members
- Reviews and approves major architectural decisions
- Enforces backup/wrapper rules
- Owns CI & prod roll-outs

### DB Guardian (ledgerflow-db)
- Owns database schema design and evolution
- Manages backup and restore procedures
- Monitors database performance
- Implements data migration strategies
- Reviews DB-related code changes
- Maintains Postgres schema & fixtures
- Handles backup/restore scripts and tuning

### Full-Stack Developer (ledgerflow-dev)
- Implements backend APIs and services
- Builds frontend components and features
- Ensures code quality and test coverage
- Participates in code reviews
- Helps maintain development environment
- Implements Django API and React/Tailwind UI
- Handles glue code for parsers/classifier

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

### Reviewer (ledgerflow-review)
- Performs thorough code reviews
- Ensures adherence to standards
- Validates test coverage
- Checks documentation updates
- Verifies CI/CD pipeline health
- Maintains velocity without sacrificing quality

### Taskforce (ledgerflow-taskforce)
- Handles specialist tasks (PDF/NLP/Reporting)
- Spins up only when needed for complex features
- Provides temporary focused expertise
- Integrates with core team as needed

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
| @ledgerflow-pm | **ledgerflow-pm** | PM Guardian | PST (08-16) |
| @ledgerflow-dev | **ledgerflow-dev** | Full-Stack Developer | EST (09-17) |
| @ledgerflow-db | **ledgerflow-db** | DB Guardian | PST (10-18) |
| @ledgerflow-review | **ledgerflow-review** | PR audit & CI enforcement | CET (async) |
| @ledgerflow-taskforce | **ledgerflow-taskforce** | Specialist spikes | rotates |

## Escalation

1. **Prod down / data-loss risk** → page **@ledgerflow-pm**
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