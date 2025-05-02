# Teams Directory

This directory contains team configurations and related files organized by project/team.

## Directory Structure

```
teams/
├── _templates/           # Template files for new teams
│   ├── env.template     # Environment file template
│   └── checklist.md     # Checklist template
│
├── ledgerflow/          # LedgerFlow team
│   ├── .env            # Team environment configuration
│   └── checklist.md    # Team setup checklist
│
└── README.md           # This file
```

## File Naming Convention

Each team directory contains:
- `.env` - Environment configuration for the team
- `checklist.md` - Account and access setup checklist
- Additional team-specific files as needed

## Usage

1. New teams are created using the scaffold script:
   ```bash
   python scaffold_team.py
   ```

2. Files are automatically placed in a team-specific directory
3. Follow the checklist in the team directory for setup
4. Use the team's .env file with the team CLI 