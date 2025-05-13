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

# Cline Memory Bank: Shared Docs Workflow (Summary)

- Fill out `teams/{project}/cline_docs_shared/` after scaffolding, before crew creation.
- Crew creation copies the filled shared docs into each session's payload.
- See productContext.md for full workflow details. 

# LedgerFlow AI Team Dashboard UI: Technical Design

## System Architecture
- **Frontend:** React (TypeScript, modern component library, e.g., MUI or AntD)
- **Backend:** FastAPI (Python), serving a REST/JSON API
- **Integration:**
  - Backend imports and calls functions from `team_cli.py` and `scaffold_team.py` directly (refactored for API use)
  - Optionally invokes CLI as subprocess for legacy compatibility
  - Reads/writes config files in `sessions/`, `roles/`, `teams/` directories
- **Storage:**
  - **Phase 1:** File/folder-based (as today)
  - **Phase 2:** Optional DB (SQLite/Postgres) for configs, secrets, and audit logs (see below)

## Data Flow & Process
- **Current CLI Workflow:**
  1. Run scaffold to generate templates and .env files
  2. Manually fill in required fields/secrets
  3. Run team-cli to generate sessions/containers (crew create)
  4. Launch containers, run restore scripts
- **Dashboard Workflow (Proposed):**
  1. User starts new project/crew in dashboard
  2. Dashboard runs scaffold logic, presents all required fields visually
  3. User fills in all fields/secrets in browser (with validation, hints, RBAC)
  4. Dashboard can save progress (drafts) before generating containers
  5. When ready, dashboard calls team-cli logic to generate sessions/containers
  6. User can view/edit all generated configs, download, or launch containers
  7. All changes are tracked (audit log/versioning)

- **Iteration:**
  - Dashboard allows iterative editing of configs before finalizing/creating containers
  - No need to re-run CLI for every change; dashboard can update files or DB directly

## File vs. Database Storage
- **File-based (current):**
  - Pros: Simple, transparent, easy to back up, matches current workflow
  - Cons: Harder to track changes, no audit log, no concurrent editing, limited search/filter
- **DB-backed (future/optional):**
  - Pros: Enables versioning, audit logs, RBAC, concurrent edits, search/filter, API-driven
  - Cons: Migration effort, must sync with file system for container launches
- **Migration Path:**
  - Start with file-based for MVP (read/write as today)
  - Add DB layer for configs/secrets/audit as usage grows
  - Provide sync/export to files for container compatibility

## API Endpoints (Backend)
- `POST /api/scaffold` - Start new project/crew, return required fields
- `GET /api/fields` - List all required fields for a project/crew
- `POST /api/fields` - Save/update field values (draft or final)
- `POST /api/crew` - Generate sessions/containers (calls team-cli)
- `GET /api/configs` - List/view all generated configs
- `PUT /api/configs/{id}` - Edit a config (env, MCP, etc.)
- `GET /api/status` - Get health/status of all containers/agents
- `GET /api/secrets` - List/view secrets (RBAC enforced)
- `POST /api/secrets` - Add/update secrets
- `GET /api/audit` - View audit log/version history

## Frontend Structure (React)
- **Wizard for crew/session creation** (stepper UI, validation, hints)
- **Config dashboard** (list, view, edit all configs)
- **Secrets vault** (secure, RBAC, add/rotate)
- **Status/health dashboard** (real-time, drill-down to logs/metrics)
- **Audit/versioning view**
- **Download/export/share actions**

## Security & Extensibility
- All secrets encrypted at rest (file or DB)
- RBAC for all sensitive actions (frontend and backend)
- Audit logging for all config/secret changes
- API-first design for future integrations (plugins, chat, metrics, etc.)
- Modular backend: new agent types, config formats, or workflows can be added as plugins

## Deep Thoughts & Recommendations
- **Unifying the Flow:** The dashboard can present all required fields (from scaffold/team-cli) in a single UI, allowing users to fill in everything before generating containers. This removes the need for manual file editing and multiple CLI runs.
- **Drafts & Iteration:** Users can save drafts, iterate, and only "commit" when ready to generate containers. This is a major UX improvement over the current process.
- **DB Migration:** Start with file-based for MVP, but design API and frontend to support a future DB layer (for audit, RBAC, search, etc.).
- **CLI Integration:** Refactor CLI logic to be importable and API-friendly (no sys.exit, use exceptions/returns, accept dicts not argparse.Namespace).
- **Extensibility:** Design both backend and frontend for plugins/extensions (e.g., new agent types, integrations, dashboards).

---

This design will allow the dashboard to streamline and unify the LedgerFlow AI Team workflow, while remaining compatible with existing scripts and future-proof for scale and compliance. 