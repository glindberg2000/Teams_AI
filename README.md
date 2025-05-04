# LedgerFlow AI Team Workspace

A secure, isolated environment for AI agent development and collaboration, providing role-based access, documentation inheritance, and standardized configuration.

## Overview

LedgerFlow AI Team provides a robust, reproducible workflow for creating, configuring, and managing teams of AI agents. The system is designed for both human and AI users, with a focus on security, modularity, and documentation.

## Key Features

- **Isolated Agent Environments**: Each agent gets a separate container with its own configuration and SSH keys
- **Documentation Inheritance**: Global → Project → Role → Session hierarchy
- **Secure Secret Management**: No sensitive data in Git repository
- **Role-Based Configuration**: Role-specific templates and documentation
- **Automated Setup**: Scripted creation of team environments
- **Task Master Integration**: Advanced task management for AI-driven workflows (see cline_docs/README-task-master.md)

## Directory Structure

```
LedgerFlow_AI_Team/
├── cline_docs/                # Project-level docs, migration guides, reports, advanced usage
│   ├── MIGRATION_GUIDE.md
│   ├── README-task-master.md
│   └── reports/
├── docs/                      # Generated/inherited agent docs (for containers/sessions)
│   ├── global/
│   ├── projects/
│   └── role/
├── roles/                     # Role templates and docs
│   ├── _templates/
│   ├── pm_guardian/
│   ├── python_coder/
│   └── reviewer/
├── teams/                     # User-generated team configs and sessions (gitignored)
├── templates/                 # System-wide templates (devcontainer, scripts)
├── tools/                     # Official CLI tools
│   ├── scaffold_team.py
│   ├── team_cli.py
│   └── utils/
├── scripts/                   # Deprecated/legacy scripts (in scripts/deprecated/)
├── .cursor/                   # Cursor AI config/rules
├── .gitignore
├── README.md                  # Main entrypoint for all users
└── ... (other config files)
```

> **Note:** `cline_docs/` is *never* inherited or copied into agent containers or sessions. Only `docs/` and `roles/` are used for agent/session documentation. See the now-archived [Documentation Organization Proposal](cline_docs/reports/DOCUMENTATION_ORGANIZATION_PROPOSAL.md) for historical context and verification of this separation.

## Quickstart: Official Workflow

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/LedgerFlow_AI_Team.git
cd LedgerFlow_AI_Team
```

### 2. Scaffold a New Team

```bash
python tools/scaffold_team.py --project myteam --prefix user --domain example.com
```
- This creates `teams/myteam/config/env`, `env.template`, and `checklist.md`.

### 3. Fill in Environment File
- Edit `teams/myteam/config/env` with your API keys, tokens, and team details.
- **Never commit secrets!** The `teams/` directory is gitignored by default.

### 4. Generate Agent Sessions

```bash
python tools/team_cli.py create-crew --env-file teams/myteam/config/env
```
- This creates session folders for each agent role, with:
  - `.env` file (role-specific)
  - Unique SSH keypair
  - Inherited documentation
  - Devcontainer config and restore script

### 5. Launch and Use Sessions
- Each session is ready for containerized development or AI agent operation.
- See the generated `checklist.md` for next steps.

## Documentation
- **Project/Framework Docs:** See `cline_docs/` for migration guides, advanced usage, and verification reports. *These are never inherited by agent containers.*
- **Task Master:** See `cline_docs/README-task-master.md` for advanced AI-driven task management.
- **Generated Agent Docs:** See `docs/` for global, project, and role documentation inherited by agent containers.

## Security & Best Practices
- **No secrets in git:** All sensitive data is in `teams/` (gitignored).
- **Unique SSH keys:** Each agent/session gets a unique keypair.
- **Documentation inheritance:** All sessions inherit up-to-date docs from `docs/`.
- **Legacy scripts:** Deprecated scripts are in `scripts/deprecated/` for reference only.

## Task Master Integration (Optional)
- For advanced, AI-driven project management, use the Task Master tool.
- See `cline_docs/README-task-master.md` for setup and usage.

## Migration & History
- See `cline_docs/MIGRATION_GUIDE.md` for details on the repository reorganization and migration steps.

## Contributing
- Please see the main README and `cline_docs/` for up-to-date contribution guidelines.

## License
This project is proprietary and confidential. All rights reserved. 