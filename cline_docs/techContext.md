# Tech Context

## Technologies Used

### Core Infrastructure
- **Docker & DevContainer**: For containerized development environments and session isolation
- **VS Code**: Primary IDE with Windsurf extension for AI agent integration
- **Bash Scripting**: For automation, environment setup, and payload management
- **jq**: JSON processing in shell scripts and configuration management
- **Git**: Version control and repository management
- **MCP Server**: Core service for AI agent tool integration
- **Task Master**: Task management and tracking system
- **Context7**: Documentation retrieval and management system

### Application Stack
- **Python**: Primary programming language
- **Django**: Backend web framework
- **PostgreSQL**: Primary database
- **React**: Frontend framework
- **TailwindCSS**: Utility-first CSS framework
- **Node.js**: JavaScript runtime for frontend development
- **Claude API**: AI model integration for agent capabilities
- **Perplexity AI**: Research and analysis capabilities

### CI/CD & Automation
- **GitHub Actions**: Continuous integration and deployment
- **pre-commit hooks**: Code quality and formatting checks
- **npm scripts**: Build and development workflow automation
- **team-cli**: Custom CLI for session management
- **Windsurf Tools**: AI agent integration and management

### Documentation & Communication
- **Markdown**: Documentation format with inheritance system
- **Slack**: Team communication and agent integration
- **GitHub Issues**: Task and bug tracking
- **MCP Tools**: Integrated documentation and communication tools

## Development Setup

### Prerequisites
- Git
- Docker Desktop
- VS Code with Remote Containers extension
- Python 3.7+ (for local CLI tools)
- Required API keys:
  - ANTHROPIC_API_KEY (for Claude)
  - PERPLEXITY_API_KEY (for research capabilities)
  - GITHUB_TOKEN (for repository management)
  - SLACK_BOT_TOKEN (for team communication)

### Initial Setup Process
1. Clone repository:
   ```bash
   git clone https://github.com/your-org/LedgerFlow_AI_Team.git
   cd LedgerFlow_AI_Team
   ```

2. Environment Configuration:
   - Copy `.env.example` to `.env`
   - Copy `.env.team.example` to `.env.team`
   - Set required environment variables
   - Never commit `.env` files
   - Store sensitive data in secure storage

3. Session Management:
   - Use `new_session.sh` to create new agent sessions
   - Sessions are isolated in separate containers
   - Each session has its own documentation and configuration
   - Payload management via `restore_payload.sh`

4. Container Workflow:
   - Launch DevContainer via VS Code
   - Container automatically sets up development environment
   - `refresh_configs.sh` handles configuration generation
   - `setup_workspace.sh` initializes development environment
   - Documentation and configuration injected automatically

### Development Workflow
1. Documentation Inheritance Pattern:
   - Global docs in `/docs/global/`
   - Project docs in `/docs/projects/`
   - Role docs in `/roles/{role}/docs/`
   - Session docs in `/sessions/{session}/docs/`
   - Inheritance order: Session → Role → Project → Global

2. Configuration Management:
   - Base configs in `.devcontainer/`
   - Session-specific overrides in `/sessions/{session}/`
   - MCP configuration generated from templates
   - Environment variables merged at container startup
   - Secrets managed via secure storage

3. Task Management:
   - Initialize project with Task Master
   - Parse PRD for initial task generation
   - Break down tasks into subtasks
   - Track progress and dependencies
   - Update task documentation regularly

4. Code Development:
   - Follow project-specific guidelines
   - Use pre-commit hooks for quality checks
   - Submit PRs for review
   - Document changes in task updates
   - Update technical documentation as needed

## Technical Constraints

### Security
- No real secrets in repository
- All `.env` files ignored by Git
- Sensitive data stored securely outside repo
- SSH keys and tokens managed via secure storage
- Session isolation enforced by containers
- API keys managed through environment variables

### Isolation
- All agent sessions must be reproducible
- Sessions isolated in separate containers
- No cross-session data sharing except via documented channels
- Each session has independent:
  - Configuration
  - Documentation
  - Environment variables
  - Workspace
  - Task tracking

### Configuration
- All docs/configs injected automatically at build/startup
- No manual configuration in containers
- Changes must be made through version-controlled files
- Environment-specific settings via `.env` files
- MCP configuration generated from templates
- Documentation inheritance handled automatically

### Performance
- Container builds optimized for speed
- Documentation inheritance minimizes duplication
- Caching used where appropriate
- Resource limits set per container
- Task analysis for optimal breakdown
- Efficient configuration generation

### Maintainability
- DRY principle in documentation and code
- Clear separation of concerns
- Automated testing and validation
- Comprehensive documentation required
- Task-driven development process
- Regular documentation updates
- Standardized naming conventions

### Compatibility
- Cross-platform support (Linux, macOS, Windows)
- VS Code Remote Containers compatibility
- Docker version requirements documented
- Minimum system requirements specified
- API version compatibility maintained
- Tool integration requirements documented 