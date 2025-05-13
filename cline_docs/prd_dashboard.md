# Product Requirements Document (PRD): LedgerFlow AI Team Dashboard UI

## Overview & Goals
The LedgerFlow AI Team Dashboard UI will provide a modern, visual interface for configuring, managing, and monitoring all aspects of the LedgerFlow AI Team platform. It will make agent/crew creation, environment setup, and config management accessible to both technical and non-technical users, while integrating tightly with existing CLI and automation tools.

## User Personas
- **Project Manager:** Wants to onboard new projects and agents without using the CLI.
- **Developer:** Needs to review, edit, and debug session/container configs quickly.
- **Security Lead:** Audits secrets, keys, and compliance in one place.
- **Operator:** Monitors health/status of all containers and agents.

## Core Features & Requirements
- **Visual Crew/Session Creation:**
  - Wizard for creating new agent sessions, teams, and roles
  - Form-based input for all required parameters (names, roles, repo URLs, tokens, etc.)
  - Option to generate/upload SSH keys and secrets securely
- **Config Management:**
  - Dashboard view of all generated configs (env, SSH, MCP, .windsurfrules, etc.)
  - Inline editing with validation and version history
  - Download/export and secure sharing options
- **Container/Agent Status:**
  - Real-time status/health view for all containers and agents
  - Visual indicators for errors, missing configs, or unhealthy agents
  - Quick links to logs, metrics, and troubleshooting tools
- **Secrets & Key Management:**
  - Secure vault for managing sensitive values (API keys, tokens, SSH keys)
  - Role-based access control for secret visibility and editing
- **Integration & Extensibility:**
  - Hooks into existing CLI and automation scripts (team-cli, setup_workspace.sh, etc.)
  - API for future integrations (logs, chat, metrics, etc.)
  - Modular design for adding new agent types or workflows

## User Flows
- **Crew/Session Creation:**
  1. User clicks "Create Crew/Session"
  2. Fills out form (names, roles, env vars, secrets, etc.)
  3. Optionally uploads or generates SSH keys
  4. Selects container type for each session (or applies to all)
  5. Submits; backend calls CLI logic to scaffold session(s)
  6. User sees confirmation and can view/edit generated configs
- **Config Editing:**
  1. User selects a session/container
  2. Views all configs (env, MCP, SSH, etc.)
  3. Edits inline with validation; changes are saved and versioned
- **Status Monitoring:**
  1. Dashboard shows all containers/agents with health/status
  2. User can drill down to logs, metrics, or troubleshooting tools
- **Secrets Management:**
  1. User accesses secure vault
  2. Views, adds, or rotates secrets/keys with RBAC controls

## Integration Points
- Directly import and call functions from `team_cli.py` (refactor as needed for API use)
- Optionally invoke CLI as subprocess for legacy compatibility
- Read/write all config files in `sessions/`, `roles/`, and `teams/` directories
- Trigger setup scripts (e.g., `setup_workspace.sh`) via backend API

## Security & Compliance
- All secrets encrypted at rest
- Role-based access control for sensitive actions
- Audit logging for config/secret changes
- Never expose secrets in logs or UI

## Milestones & MVP Definition
- **MVP:**
  - Visual crew/session creation wizard
  - Config dashboard with inline editing
  - Status/health view for containers/agents
  - Secure secrets/key management (basic vault)
  - CLI integration for session/crew creation
- **Future:**
  - Advanced metrics/logs
  - Chat/agent interaction
  - Plugin system for new agent types
  - Automated troubleshooting

## Open Questions/Risks
- How much refactoring is needed for CLI logic to be API-friendly?
- What is the best approach for secure secret storage (local vault, cloud KMS, etc.)?
- How to handle concurrent edits/versioning of configs?
- What are the requirements for multi-user/RBAC support?
- How to ensure compatibility with future CLI/tooling changes?

## Expanded Requirements: Team & Role Management Flow

### Role Management (CRUD)
- Dashboard provides full CRUD (Create, Read, Update, Delete) for roles/templates
- Each role includes:
  - Name, description, and display name
  - Prompt/instructions for the agent
  - MCP tools config (template for mcp_config.json)
  - Default environment variables (env.sample)
  - Associated docs (editable markdown)
- Roles can be added, edited, or removed at any time
- Roles are versioned; changes tracked in audit log

### Team/Project Configuration
- Team/project entity includes:
  - Name, description, and metadata
  - Project-level docs (included in all sessions)
  - Team-wide keys/secrets (SSH, Git, Discord, etc.)
  - List of roles/templates to include in the team
  - Mapping of roles to team members (assignments)
- All keys/secrets are managed securely (vault, RBAC)
- Project config can be edited before finalizing session output

### Documentation Inclusion
- Project-level docs: included in all sessions
- Role-level docs: included for sessions with that role
- Session/member-level docs: can be added/edited per session
- Docs are editable in the dashboard (markdown editor)
- Docs inheritance follows: Project → Role → Session

### Final Session Output
- When ready, dashboard generates the full session directory structure using templates and filled configs
- Output includes:
  - `.devcontainer/` config
  - `payload/` with .env, .ssh, docs, mcp_config.json, restore script
  - All inherited docs and configs
- Output is viewable and editable in the dashboard before download/export
- Users can make last-minute edits to any config or doc before "committing" the session
- All changes are tracked (audit/versioning)

### Additional Requirements/Improvements
- Allow preview of generated configs and directory structure before finalization
- Support for bulk editing of team member/session configs
- Option to clone/copy existing roles or sessions as templates
- Integration with external secret stores (optional, future)
- API endpoints for all CRUD operations (roles, team, sessions, docs)
- UI should guide user through required/optional fields with validation and tooltips

### Container Type Selection
- Users can select the type of container to generate for each session or team:
  - Windsurf (current default)
  - Cursor
  - Claude Code
  - Codex
  - Cline
  - (Extensible: add new container types as needed)
- Container type determines the generated `.devcontainer/` config, startup scripts, and any IDE-specific files
- Dashboard UI provides a dropdown or selection wizard for container type during session/team creation
- All config templates and scripts are modular to support multiple container types
- Users can preview and edit the generated container config before finalizing

#### User Flow Update
- During crew/session creation, user selects container type for each session (or applies to all)
- Dashboard generates the appropriate config and scripts for the selected type
- User can review/edit before committing

### Team Communication System Selection
- Users can select the communication system for the team/project:
  - Discord (via mcp-discord)
  - Slack (via mcp-slack)
  - Internal chat (simple built-in room chat, optional future)
- Communication system selection determines:
  - Which MCP server/tools are configured for each session
  - What keys/tokens are required (Discord bot token, Slack token, etc.)
  - Which docs/instructions are included for onboarding
- Dashboard UI provides a selection wizard for communication system during team/project setup
- All config templates/scripts are modular to support multiple comms systems
- Users can preview and edit the generated comms config before finalizing

#### User Flow Update
- During team/project setup, user selects communication system
- Dashboard prompts for required keys/tokens and docs for the selected system
- Generated session configs and docs reflect the chosen comms system

---

This expanded flow ensures the dashboard supports the full lifecycle: role/template management, team/project config, doc inclusion, and final session output—fully viewable, editable, and auditable before deployment. 