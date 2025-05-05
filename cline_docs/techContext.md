# Tech Context

## Technologies Used

### Core Infrastructure
- **Docker & DevContainer**: For containerized development environments and session isolation
- **VS Code/Cursor**: Primary IDEs with Remote Containers support for AI agent integration
- **Bash Scripting**: For automation, environment setup, and payload management
- **jq**: JSON processing in shell scripts and configuration management
- **Git**: Version control and repository management
- **MCP Server**: Core service for AI agent tool integration
- **Task Master**: Task management and tracking system
- **Context7**: Documentation retrieval and management system

### Team Management Tools
- **team-cli.py**: Core CLI for creating and managing agent sessions with role templates
  - Creates isolated agent environments
  - Handles documentation inheritance (global → project → role)
  - Manages SSH key generation/copying
  - Configures MCP servers
  - Supports individual or team-wide session creation
- **scaffold_team.py**: Team configuration generator
  - Creates standardized environment files (.env.{project})
  - Generates setup checklists
  - Enforces naming conventions for proper team-cli compatibility
  - Validates roles against approved list
  - Produces documentation and templates for team setup
- **restore_payload.sh**: Script for restoring payload within containers
- **setup_workspace.sh**: Script for container initialization

### Application Stack
- **Python**: Primary programming language
  - argparse: Command-line argument parsing
  - pathlib: Path manipulation
  - yaml: Configuration file handling
  - json: MCP config generation
- **Node.js**: JavaScript runtime for MCP servers
- **Claude API**: AI model integration
- **Perplexity API**: Research capabilities

### CI/CD & Automation
- **GitHub Actions**: Continuous integration and deployment
- **pre-commit hooks**: Code quality and formatting checks
- **npm scripts**: Build and development workflow automation

### Documentation & Communication
- **Markdown**: Documentation format with inheritance system
- **Slack**: Team communication and agent integration
- **GitHub**: Repository and issue management
- **MCP Tools**: Integrated documentation and communication tools

## Development Setup

### Prerequisites
- Git
- Docker Desktop
- VS Code or Cursor with Remote Containers extension
- Python 3.7+ (for local CLI tools)
- Required API keys:
  - ANTHROPIC_API_KEY (for Claude/Task Master)
  - PERPLEXITY_API_KEY (for research capabilities)
  - GITHUB_PERSONAL_ACCESS_TOKEN (for GitHub access)
  - SLACK_BOT_TOKEN (for Slack integration)
  - SLACK_TEAM_ID (for Slack workspace)

### Team Setup Process
1. Generate team configuration:
   ```bash
   # Interactive mode
   python scaffold_team.py
   
   # Command-line mode
   python scaffold_team.py --project <project> --prefix <user> --domain <domain.com> --roles <role1>,<role2>
   ```
   This creates:
   - `.env.<project>` with all environment variables in the correct format
   - `teams/<project>/checklist.md` with step-by-step setup instructions
   - `teams/<project>/env.template` with variable templates for reference

2. Fill in API keys in the generated environment file:
   - Team-level keys (ANTHROPIC_API_KEY, GITHUB_PERSONAL_ACCESS_TOKEN, etc.)
   - Role-specific keys (PM_GUARDIAN_SLACK_TOKEN, PM_GUARDIAN_GITHUB_TOKEN, etc.)

3. Create agent sessions:
   ```bash
   python team-cli/team_cli.py create-crew --env-file .env.<project>
   ```
   This creates:
   - Isolated session directories for each role in `sessions/<project>/`
   - SSH keys for each session
   - Properly inherited documentation
   - MCP configuration for each agent

4. Launch containers:
   - Open sessions in VS Code/Cursor
   - Use "Reopen in Container" to start the DevContainer
   - The container automatically configures the development environment

### Environment Variable Conventions
For proper integration between scaffold_team.py and team-cli.py, variables must follow these patterns:

- **Team-level variables**:
  - `TEAM_NAME`: Name of the team/project
  - `SLACK_BOT_TOKEN`: Main Slack bot token
  - `GITHUB_PERSONAL_ACCESS_TOKEN`: GitHub access token
  - `ANTHROPIC_API_KEY`: Claude API key
  - `PERPLEXITY_API_KEY`: Perplexity API key

- **Role-specific variables**:
  - `ROLE_EMAIL`: Email address for the role (e.g., `PM_GUARDIAN_EMAIL`)
  - `ROLE_SLACK_TOKEN`: Slack token for the role (e.g., `PM_GUARDIAN_SLACK_TOKEN`)
  - `ROLE_GITHUB_TOKEN`: GitHub token for the role (e.g., `PM_GUARDIAN_GITHUB_TOKEN`)
  - `ROLE_BOT`: Bot name for the role (e.g., `PM_GUARDIAN_BOT`)
  - `ROLE_GITHUB`: GitHub username for the role (e.g., `PM_GUARDIAN_GITHUB`)
  - `ROLE_DISPLAY`: Display name for the role (e.g., `PM_GUARDIAN_DISPLAY`)

- **MCP configuration variables**:
  - `MODEL`: Claude model to use
  - `PERPLEXITY_MODEL`: Perplexity model
  - `MAX_TOKENS`: Maximum tokens for AI responses
  - `TEMPERATURE`: Temperature setting
  - `DEFAULT_SUBTASKS`: Default number of subtasks
  - `DEFAULT_PRIORITY`: Default priority level
  - `DEBUG`: Debug mode flag
  - `LOG_LEVEL`: Logging level

### Documentation Inheritance Pattern
1. Documentation Inheritance:
   - Global docs in `/docs/global/`
   - Project docs in `/docs/projects/{project}/`
   - Role docs in `/roles/{role}/docs/`
   - Inheritance order: Global → Project → Role

2. Configuration Flow:
   - Team config: `.env.{project}` (from scaffold_team.py)
   - Session config: `sessions/{project}/{agent}/payload/.env` (from team-cli.py)
   - MCP config: `sessions/{project}/{agent}/payload/mcp_config.json` (from team-cli.py)
   - Container config: `.devcontainer/` directory (from team-cli.py)

3. Session Directory Structure:
   ```
   sessions/
     {project}/
       {agent}/
         .devcontainer/         # Container configuration
           Dockerfile           # Container definition
           devcontainer.json    # VS Code/Cursor config
           scripts/             # Setup scripts
         payload/               # Agent workspace
           .env                 # Environment variables
           .ssh/                # SSH keys
           docs/                # Inherited documentation
           mcp_config.json      # MCP configuration
           restore_payload.sh   # Payload setup script
   ```

## Technical Constraints

### Security
- No real secrets in repository
- All `.env` files in .gitignore
- SSH keys and tokens managed securely
- Session isolation enforced by containers
- API keys passed through environment variables

### Isolation
- All agent sessions must be reproducible
- Sessions isolated in separate containers
- Each session has independent:
  - Configuration
  - Documentation
  - Environment variables
  - SSH keys
  - Workspace

### Configuration
- All docs/configs injected automatically at build/startup
- No manual configuration in containers
- Environment-specific settings via `.env` files
- MCP configuration generated from templates
- Documentation inheritance handled automatically

### Variable Naming
- Role-specific variables must follow the pattern `ROLE_VARIABLE` (e.g., `PM_GUARDIAN_SLACK_TOKEN`)
- Session names extracted from variable names by team-cli.py
- Ensure consistent naming conventions across all environment files
- scaffold_team.py ensures these conventions are followed

### Portability
- Cross-platform support (Linux, macOS, Windows)
- VS Code/Cursor Remote Containers compatibility
- Docker version requirements documented
- Minimum system requirements specified
- API version compatibility maintained 

# Only current, actionable technical context is kept here. All legacy, migration, and reorg notes have been moved to cline_docs/legacy/. 