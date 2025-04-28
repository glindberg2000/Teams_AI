# team-cli

A command-line tool to automate and standardize the creation and management of agent sessions for the LedgerFlow AI Team.

## Features
- Scaffold new agent sessions in the `sessions/` directory using role templates from `roles/`
- Prepare payloads for agent containers (docs, secrets, configs, SSH keys)
- Restore payloads inside containers
- List available roles/templates
- Add new roles/templates
- Works interactively or via command-line flags (for automation/AI use)
- Provides reminders for Slack, GitHub, SSH, and other integrations

## Folder Structure
```
LedgerFlow_AI_Team/
  sessions/
    <agent-session>/
      .devcontainer/
      docs/
      payload/
      ...
  roles/
    python_coder/
      .env.sample
      mcp_config.template.json
      docs/
        agent_instructions.md
        ...
    ...
  team-cli/
    team_cli.py
    README.md
  docs/
    global/
    projects/
```

## Usage

### Quickstart
```
python team-cli/team_cli.py create-session --name my-coder --role python_coder --generate-ssh-key --prompt-all
# Or, to include project docs:
python team-cli/team_cli.py create-session --name my-coder --role python_coder --project sample_project --generate-ssh-key --prompt-all
```

### Prepare Payload
```
python team-cli/team_cli.py prepare-payload --name my-coder
```

### Restore Payload (inside container)
```
bash /workspaces/project/payload/restore_payload.sh
```

### List Roles
```
python team-cli/team_cli.py list-roles
```

### Add Role
```
python team-cli/team_cli.py add-role --name new_role
```

## Setup
- Requires Python 3.7+
- No external dependencies for basic usage
- Place `team_cli.py` and `README.md` in `team-cli/` at the repo root
- Place role templates in `roles/`

## Docs Structure
- See the main repo README for the full documentation structure and onboarding process.
- All Slack integration uses `SLACK_BOT_TOKEN` (not `SLACK_TOKEN`).

## Security & Secret Storage
- **Never commit real secrets or private keys to this repo.**
- The `.gitignore` is configured to ignore all `.env` files, all `payload/.ssh/` directories, and all generated session folders.
- SSH keys are generated or copied into `payload/.ssh/` and are never tracked by git.
- **All generated session folders are ignored by git.**
- **Store secrets and sensitive configs in a secure location outside git, such as iCloud, 1Password, or your organization's vault.**
- When onboarding a new machine, restore secrets from your secure backup and use the CLI to generate new sessions.

## Workflow
1. Use `create-session` to scaffold a new agent session in `sessions/`
2. Prepare the payload for the session
3. Launch the container for the session
4. Run the restore script inside the container
5. Agent is ready to use with all docs, secrets, and configs in place

## Reminders
- Generate or provide a unique SSH key for each agent
- Set up GitHub PAT and Slack tokens as needed
- Review generated docs and configs before launching containers

---

**WARNING:**
- Never commit generated session folders or secrets to git.
- Always use secure storage for secrets (iCloud, 1Password, etc.).
- For more details, run:
```
python team-cli/team_cli.py --simple-help
``` 