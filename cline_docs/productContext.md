# LedgerFlow AI Team Workspace

## Purpose
- Provides a secure, isolated environment for AI agent development and collaboration
- Enables role-based access and configuration for different agent types
- Streamlines agent onboarding with automated documentation and setup

## Problems Solved
1. Agent Isolation & Security
   - Each agent gets an isolated environment with its own SSH keys and secrets
   - Sensitive data is never committed to the repository
   - Role-based access control through documentation inheritance

2. Configuration Management
   - Automated MCP server setup with environment-specific configuration
   - Standardized environment variable handling
   - SSH key management (generation or existing key usage)

3. Documentation Organization
   - Hierarchical documentation structure (global -> project -> role -> session)
   - Automatic documentation inheritance during session creation
   - Centralized shared resources in _shared directory

4. Team Workflow
   - Integrated task management through Taskmaster MCP
   - GitHub and Slack integration for collaboration
   - Standardized development environment through DevContainers

## Core Components
1. Team CLI (team_cli.py)
   - Session creation and management
   - Role template handling
   - Documentation distribution
   - Environment configuration

2. MCP Integration
   - Taskmaster for task management
   - GitHub for code management
   - Slack for communication
   - Context7 for documentation access
   - Puppeteer for web automation

3. DevContainer Setup
   - Consistent development environment
   - Automated restore scripts
   - Configuration regeneration

## Success Criteria
- Agents can be created with minimal manual configuration
- All sensitive data is properly secured
- Documentation is automatically distributed based on role/project
- MCP servers are configured correctly for each agent
- Team collaboration tools (GitHub, Slack) are properly integrated

## Technical Requirements
- Python 3.7+ for CLI tools
- Docker for containerization
- Node.js for MCP servers
- Git for version control
- SSH key management capability

## Current Status
- Basic session creation and management implemented
- Documentation inheritance system working
- MCP server configuration automated
- SSH key handling implemented
- Environment variable management working

## Next Steps
- Implement team-wide session creation
- Add session cleanup/archival functionality
- Enhance documentation templates
- Add role validation and testing
- Implement session state monitoring 