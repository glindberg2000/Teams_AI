# Repository Reorganization: Migration Guide

This document explains the reorganization of the LedgerFlow AI Team workspace structure and provides guidance for migrating existing work.

## Overview of Changes

We're reorganizing the repository to follow a domain-centric approach with teams as the primary organizational unit. This provides better organization, clearer separation of concerns, and improved scalability for multiple teams.

### Key Changes:

1. **Team-Centric Structure**: All team-related content is unified under the `teams/` directory
2. **Centralized Tools**: All command-line tools are moved to `tools/` directory
3. **Domain-Specific Layouts**: Configuration, sessions, and templates have clear, logical locations
4. **Consistent Naming**: Standardized naming conventions throughout

## Directory Structure: Before vs After

### Before:
```
LedgerFlow_AI_Team/
├── .env.{project}                # Environment files in root
├── scaffold_team.py              # Tools in root
├── team-cli/team_cli.py          # CLI in separate directory
├── teams/{project}/              # Team config files only
│   ├── checklist.md              # Setup instructions
│   └── env.template              # Environment template
├── sessions/{project}/{agent}/   # Flat session structure
└── roles/{role}/                 # Role definitions
```

### After:
```
LedgerFlow_AI_Team/
├── teams/                        # All team-related content
│   ├── _templates/               # Shared templates
│   ├── _shared/                  # Shared resources
│   └── {project}/                # Project-specific content
│       ├── config/               # Team configuration
│       │   ├── env               # Environment file (was .env.{project})
│       │   ├── checklist.md      # Setup instructions
│       │   └── env.template      # Environment template
│       └── sessions/             # Team sessions
│           └── {role}/           # Session for specific role
├── roles/                        # Role templates
├── tools/                        # Command-line tools
│   ├── scaffold_team.py          # Team configuration generator
│   ├── team_cli.py               # Session management tool
│   └── utils/                    # Helper utilities
└── templates/                    # System-wide templates
    ├── devcontainer/             # Base container configuration
    └── scripts/                  # Helper scripts
```

## Migration Steps

The reorganization will be performed automatically by the `organize_repo.py` script, but here's what's happening:

1. **Environment Files**: `.env.{project}` → `teams/{project}/config/env`
2. **Team Config**: `teams/{project}/checklist.md` → `teams/{project}/config/checklist.md`
3. **Sessions**: `sessions/{project}/{agent}` → `teams/{project}/sessions/{agent}`
4. **Tools**: 
   - `scaffold_team.py` → `tools/scaffold_team.py`
   - `team-cli/team_cli.py` → `tools/team_cli.py`
5. **Templates**: `.devcontainer` → `templates/devcontainer`

## How to Migrate Your Workflow

### Command Changes

Update your commands as follows:

| Old Command | New Command |
|-------------|-------------|
| `python scaffold_team.py --project test` | `python tools/scaffold_team.py --project test` |
| `python team-cli/team_cli.py create-crew --env-file .env.test` | `python tools/team_cli.py create-crew --env-file teams/test/config/env` |

### File Locations

| Old Path | New Path |
|----------|----------|
| `.env.{project}` | `teams/{project}/config/env` |
| `sessions/{project}/{agent}` | `teams/{project}/sessions/{agent}` |
| `teams/{project}/checklist.md` | `teams/{project}/config/checklist.md` |

## Running the Migration

1. **Create a backup** of your repository before proceeding
2. **Test with dry-run mode**:
   ```bash
   python organize_repo.py --dry-run
   ```
3. **Execute the reorganization** (creates a separate branch):
   ```bash
   python organize_repo.py --execute --branch
   ```
4. **Test everything works** in the new structure
5. **Merge the branch** when you're satisfied

## Troubleshooting

### Common Issues

1. **Missing files after migration**:
   - Check if the files were moved to their new locations
   - Look for any error messages during migration

2. **Path references in scripts**:
   - Some hard-coded paths in scripts might need manual updating
   - Check logs if scripts fail to run

3. **SSH key paths**:
   - Update any references to SSH keys in your scripts or documentation

4. **Command not found errors**:
   - Remember to use the new paths for commands (tools/script_name.py)

## Reverting the Migration

If you need to revert the changes:

1. If you used the `--branch` flag, simply switch back to the main branch:
   ```bash
   git checkout main
   ```

2. If you made the changes directly on main, restore from your backup.

## Getting Help

If you encounter issues during migration:

1. Check the execution log for any error messages
2. Review this migration guide for path changes
3. Open an issue in the repository with specific details about the problem

---

Happy migrating! The new structure should make the repository more organized, intuitive, and easier to maintain as it grows. 