# LedgerFlow AI Team Workspace

## Purpose
- Provides a secure, isolated environment for AI agent development and collaboration
- Enables role-based access and configuration for different agent types
- Streamlines agent onboarding with automated documentation and setup
- Standardizes team configuration and setup with scaffolding tools

## Problems Solved
1. Agent Isolation & Security
   - Each agent gets an isolated environment with its own SSH keys and secrets
   - Sensitive data is never committed to the repository
   - Role-based access control through documentation inheritance

2. Configuration Management
   - Automated MCP server setup with environment-specific configuration
   - Standardized environment variable handling with consistent naming conventions
   - SSH key management (generation or existing key usage)
   - Team-wide configuration scaffolding with proper validation

3. Documentation Organization
   - Hierarchical documentation structure (global → project → role → session)
   - Automatic documentation inheritance during session creation
   - Centralized shared resources in _shared directory

4. Team Workflow
   - Integrated task management through Taskmaster MCP
   - GitHub and Slack integration for collaboration
   - Standardized development environment through DevContainers
   - Streamlined team setup process with scaffolding and checklists

## Core Components
1. Team CLI (team_cli.py)
   - Session creation and management
   - Role template handling
   - Documentation distribution
   - Environment configuration
   - Multi-session creation via create-crew command
   - Consistent session name extraction from environment variables

2. Team Scaffold (scaffold_team.py)
   - Team configuration generation (.env.{project} files)
   - Environment templates in teams/{project}/ directory
   - Setup checklist creation with detailed instructions
   - Standardized naming conventions (ROLE_SLACK_TOKEN format)
   - Project directory structure

3. MCP Integration
   - Taskmaster for task management
   - GitHub for code management
   - Slack for communication
   - Context7 for documentation access
   - Puppeteer for web automation

4. DevContainer Setup
   - Consistent development environment
   - Automated restore scripts
   - Configuration regeneration

## Discord MCP Integration

- Discord is now a first-class communication and automation channel for all roles and teams.
- Integration is provided by the [mcp-discord](https://github.com/netixc/mcp-discord) bridge, which must be installed and configured.
- Each role/team must create a Discord bot application, invite it to the server with the correct permissions, and provide the bot token, client ID, and (optionally) guild/server and channel IDs.
- The integration supports sending and reading messages, reactions, and more, via MCP tools.
- All setup steps are included in onboarding and checklist docs.

## Success Criteria
- Agents can be created with minimal manual configuration
- All sensitive data is properly secured
- Documentation is automatically distributed based on role/project
- MCP servers are configured correctly for each agent
- Team collaboration tools (GitHub, Slack) are properly integrated
- Teams can be configured with standardized naming and setup process

## Technical Requirements
- Python 3.7+ for CLI tools
- Docker for containerization
- Node.js for MCP servers
- Git for version control
- SSH key management capability
- Questionary for interactive prompts
- YAML for configuration file handling

## Current Status
- Session creation and management fully implemented
- Documentation inheritance system working properly
- MCP server configuration automated
- SSH key handling implemented
- Environment variable management working with consistent naming
- Team scaffolding tool working correctly with team-cli integration
- End-to-end workflow tested successfully

## Next Steps
- Improve project structure organization
  - Move temporary .env files to teams directory
  - Organize sessions by project/team
- Add cleanup and archival functionality
- Enhance role validation and support
- Develop test suite for automated verification
- Add session state monitoring and healthchecks
- Create detailed troubleshooting documentation
- Support for more complex team structures
- Add monitoring and metrics for container health

# Cline Memory Bank: Shared Docs Workflow (Summary)

- After scaffolding a team, fill out `teams/{project}/cline_docs_shared/` with all required shared context (product, system, tech, progress) before running crew creation.
- During crew creation, the filled `cline_docs_shared/` is copied into each session's payload for all roles.
- Each role then fills out their own `cline_docs/` as they work.
- Never edit the templates in `roles/_templates/` directly; always use the team-level shared docs as the source of truth before crew creation. 