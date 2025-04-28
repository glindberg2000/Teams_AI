# Team_AI Product Context

## Project Purpose
Team_AI is designed to automate the onboarding, management, and workflow orchestration of AI-powered developer agents for software teams. Its goal is to streamline the creation, configuration, and operation of role-based AI agents ("coders," "reviewers," "PMs," etc.) that can collaborate on software projects, generate and maintain documentation, and integrate with existing developer tools and workflows. All agents and their environments are containerized using Docker for consistency, security, and portability, and orchestrated by Windsurf and Cursor sessions.

## Key Features
- Automated generation of role-based Markdown documentation (for agents, projects, and global/team standards)
- Session and workspace setup for each staff member/agent, including secure payload and SSH key management
- Integration with Task Master for task planning, breakdown, and workflow automation
- Support for onboarding new staff/agents with a single command
- Automated backup and restore of session data to cloud storage (e.g., iCloud, S3)
- Integration with external services (GitHub, Slack, etc.) for seamless team collaboration
- Enforcement of best practices and coding standards via documentation and rule generation
- Secure management of secrets and environment variables (never stored in git)
- Scalable to support multiple teams, projects, and agent roles
- Containerization of all agents and workspaces using Docker, orchestrated by Windsurf and Cursor sessions

## Technical Stack
- Python (core automation scripts, agent logic)
- Bash (shell scripting and automation)
- Docker (containerization of agents and workspaces)
- Task Master (Node.js-based, for task management and workflow control)
- GitHub (source control, integration)
- Slack (team communication and notifications)
- Cloud storage (iCloud, S3, etc. for backups)
- Markdown for documentation
- Environment variable management for secrets
- Windsurf and Cursor (for orchestrating agent sessions and containers)

## Constraints or Requirements
- No hardcoded paths; all scripts and tools must work across different environments
- Must support multiple cloud providers for backup/restore
- All automation must be scriptable and non-interactive (for CI/CD and agent use)
- Secrets and sensitive data must never be stored in git or public repos
- Documentation and rules must be kept up to date and versioned
- Must integrate with Task Master for all task and workflow management
- Should be extensible to support new agent roles and integrations
- All agent environments must be containerized using Docker and orchestrated by Windsurf and Cursor

## Success Criteria
- New staff/agents can be onboarded with a single command, with all required docs, keys, and workspaces generated
- All documentation (role, project, global) is generated, versioned, and accessible
- Task Master can control and track all major flows (onboarding, coding, review, etc.)
- Backups and restores work seamlessly across supported cloud providers
- No secrets or sensitive data are ever committed to git
- The system is used successfully by multiple teams and projects, with positive feedback from users 