#!/usr/bin/env python3
"""
team_cli.py - CLI tool for LedgerFlow AI Team session management

Quickstart:
  python tools/team_cli.py create-session --name agent-name --role python_coder --generate-ssh-key --prompt-all
  python tools/team_cli.py create-session --name agent-name --role python_coder --ssh-key ~/.ssh/existing_key
  python tools/team_cli.py create-crew --env-file teams/myproject/config/env

Key Features:
- Creates isolated agent sessions from role templates
- Handles SSH key generation/copying
- Configures environment variables and MCP servers
- Manages documentation inheritance (global -> project -> role -> session)
- Generates restore scripts for container setup
- Sets up devcontainer configuration for VSCode/Cursor

Environment Variable Naming Convention:
  For proper session extraction, environment variables must follow these patterns:
  - ROLE_EMAIL: For the role's email address (e.g., PM_GUARDIAN_EMAIL)
  - ROLE_SLACK_TOKEN: For the role's Slack token (e.g., PM_GUARDIAN_SLACK_TOKEN)
  - ROLE_GITHUB_TOKEN: For the role's GitHub token (e.g., PM_GUARDIAN_GITHUB_TOKEN)

  Team-cli extracts session names by taking the parts before _SLACK_TOKEN, _GITHUB_TOKEN, or _EMAIL
  and joining them with underscores in lowercase. For example:
  - PM_GUARDIAN_SLACK_TOKEN -> ["PM", "GUARDIAN"] -> "pm_guardian"
  - PYTHON_CODER_GITHUB_TOKEN -> ["PYTHON", "CODER"] -> "python_coder"

Required Environment Variables:
- GIT_USER_NAME, GIT_USER_EMAIL: Git configuration
- GITHUB_PERSONAL_ACCESS_TOKEN: For GitHub access
- SLACK_BOT_TOKEN, SLACK_TEAM_ID: For Slack integration
- ANTHROPIC_API_KEY: For Claude/Taskmaster integration
- PERPLEXITY_API_KEY: For research capabilities

Directory Structure:
  docs/global/           # Global docs for all agents/projects
  docs/projects/<name>/  # Per-project docs
  roles/<role>/docs/     # Per-role docs
  sessions/<project>/    # Project-specific agent sessions
    <agent>/             # Individual agent environment
      .devcontainer/     # Container configuration
      payload/           # Agent workspace
        docs/            # Inherited documentation
        .ssh/            # Agent's SSH keys
        .env             # Agent's environment variables

See README.md for full documentation and setup instructions.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path
import yaml
import json
from typing import Dict, Any

SESSIONS_DIR = Path("teams")
ROLES_DIR = Path("roles")
TEAM_CONFIG = Path("team/crew.yaml")
TEAM_ENV = Path("teams/default/config/env")
DEVCONTAINER_DIR = Path(".devcontainer")


# --- Utility Functions ---
def print_reminders():
    print("\n[REMINDER]")
    print("- Generate or provide a unique SSH key for each agent.")
    print("- Set up GitHub PAT and Slack tokens as needed.")
    print(
        "- Set ANTHROPIC_API_KEY and PERPLEXITY_API_KEY for Taskmaster MCP integration."
    )
    print("- Review generated docs and configs before launching containers.\n")
    print(
        "- Example: python tools/team_cli.py create-session --name pm-guardian --role python_coder --ssh-key ~/.ssh/ai-architect_gl"
    )
    print(
        "- Example: python tools/team_cli.py create-session --name pm-guardian --role python_coder --generate-ssh-key"
    )


def list_roles():
    if not ROLES_DIR.exists():
        print("No roles directory found.")
        return
    print("Available roles/templates:")
    for role in ROLES_DIR.iterdir():
        if role.is_dir():
            print(f"- {role.name}")


def setup_devcontainer(session_path: Path, project: str, name: str):
    """Set up devcontainer configuration for a session."""
    if not DEVCONTAINER_DIR.exists():
        print("[WARNING] No .devcontainer directory found in project root.")
        return

    # Copy devcontainer files
    session_devcontainer = session_path / ".devcontainer"
    shutil.copytree(DEVCONTAINER_DIR, session_devcontainer, dirs_exist_ok=True)

    # Update devcontainer.json with session-specific name
    devcontainer_json = session_devcontainer / "devcontainer.json"
    if devcontainer_json.exists():
        with open(devcontainer_json, "r") as f:
            config = json.load(f)

        # Update container name
        config["name"] = f"{project}-{name}"

        # Update runArgs to use unique container name
        if "runArgs" in config:
            for i, arg in enumerate(config["runArgs"]):
                if arg == "--name":
                    config["runArgs"][i + 1] = f"windsurf-{project}-{name}"
                    break

        # Fix mount path to use payload directory
        if "mounts" in config:
            for i, mount in enumerate(config["mounts"]):
                if "source=${localWorkspaceFolder}" in mount:
                    config["mounts"][i] = mount.replace(
                        "source=${localWorkspaceFolder}/workspace",
                        "source=${localWorkspaceFolder}/payload",
                    )

        with open(devcontainer_json, "w") as f:
            json.dump(config, f, indent=4)

        print(f"Set up devcontainer configuration in {session_devcontainer}")

    # Update Dockerfile to use simpler configuration
    dockerfile = session_devcontainer / "Dockerfile"
    if dockerfile.exists():
        dockerfile_content = """FROM node:20-bullseye

# system deps + jq
RUN apt-get update && \\
    apt-get install -y wget curl ca-certificates tar gzip git docker.io jq && \\
    rm -rf /var/lib/apt/lists/*

# Set up workspace
WORKDIR /workspaces/project

# Keep container running
CMD ["sleep", "infinity"]"""

        with open(dockerfile, "w") as f:
            f.write(dockerfile_content)

        print(f"Updated Dockerfile in {session_devcontainer}")

    # Ensure scripts directory exists
    scripts_dir = session_devcontainer / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    # Create setup_workspace.sh
    setup_workspace = scripts_dir / "setup_workspace.sh"
    setup_workspace_content = """#!/bin/bash
set -e

# Run restore script if it exists
if [ -f "/workspaces/project/restore_payload.sh" ]; then
    echo "Running restore script..."
    bash /workspaces/project/restore_payload.sh
fi
"""
    with open(setup_workspace, "w") as f:
        f.write(setup_workspace_content)
    os.chmod(setup_workspace, 0o755)

    # Create refresh_configs.sh
    refresh_configs = scripts_dir / "refresh_configs.sh"
    refresh_configs_content = """#!/bin/bash
set -e

# Nothing to do here - configs are handled by restore script
"""
    with open(refresh_configs, "w") as f:
        f.write(refresh_configs_content)
    os.chmod(refresh_configs, 0o755)

    print(f"Created devcontainer scripts in {scripts_dir}")


def create_session(args):
    name = args.name or input("Session name (e.g. pm-guardian): ").strip()
    list_roles()
    role = args.role or input("Role/template to use: ").strip()
    project = args.project or "default"

    role_path = ROLES_DIR / role
    if not role_path.exists():
        print(f"Role '{role}' not found in {ROLES_DIR}.")
        sys.exit(1)

    # Create project-based session directory using the new structure
    project_sessions_dir = SESSIONS_DIR / project / "sessions"
    project_sessions_dir.mkdir(parents=True, exist_ok=True)

    session_path = project_sessions_dir / name
    if session_path.exists():
        if getattr(args, "overwrite", False):
            print(f"[OVERWRITE] Removing existing session directory: {session_path}")
            shutil.rmtree(session_path)
        else:
            print(f"Session '{name}' already exists at {session_path}.")
            sys.exit(1)

    # Copy role template to new session
    shutil.copytree(role_path, session_path)
    print(f"Created session '{name}' from role '{role}' in project '{project}'.")

    # Set up devcontainer configuration
    setup_devcontainer(session_path, project, name)

    # --- Project and Docs Handling ---
    docs_included = []
    payload_docs = session_path / "payload/docs"
    payload_docs.mkdir(parents=True, exist_ok=True)

    # Copy global docs if enabled
    include_global = getattr(
        args, "include_global_docs", True
    )  # Default to True for backward compatibility
    if include_global:
        global_docs_dir = Path("docs/global")
        if global_docs_dir.exists():
            for f in global_docs_dir.glob("**/*"):
                if f.is_file():
                    relative_path = f.relative_to(global_docs_dir)
                    target_path = payload_docs / "global" / relative_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(f, target_path)
                    docs_included.append(f"global/{relative_path}")

    # Copy project docs if --project is set and enabled
    if hasattr(args, "project") and args.project:
        project_docs_dir = Path(f"docs/projects/{args.project}")
        if project_docs_dir.exists():
            for f in project_docs_dir.glob("**/*"):
                if f.is_file():
                    relative_path = f.relative_to(project_docs_dir)
                    target_path = payload_docs / "project" / relative_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(f, target_path)
                    docs_included.append(f"project/{relative_path}")
        else:
            print(f"[WARNING] Project docs not found: {project_docs_dir}")

    # Copy role docs if enabled
    include_role = getattr(
        args, "include_role_docs", True
    )  # Default to True for backward compatibility
    if include_role:
        role_docs_dir = role_path / "docs"
        if role_docs_dir.exists():
            for f in role_docs_dir.glob("**/*"):
                if f.is_file():
                    relative_path = f.relative_to(role_docs_dir)
                    target_path = payload_docs / "role" / relative_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(f, target_path)
                    docs_included.append(f"role/{relative_path}")

    print(
        f"Included docs in session payload: {', '.join(docs_included) if docs_included else 'none'}"
    )

    # --- SSH Key Handling ---
    payload_ssh_dir = session_path / "payload/.ssh"
    payload_ssh_dir.mkdir(parents=True, exist_ok=True)
    ssh_key_path = payload_ssh_dir / "id_rsa"
    ssh_pub_path = payload_ssh_dir / "id_rsa.pub"
    updated_env = False
    if args.ssh_key and args.generate_ssh_key:
        print("ERROR: --ssh-key and --generate-ssh-key are mutually exclusive.")
        sys.exit(1)
    if args.ssh_key:
        src_key = Path(args.ssh_key).expanduser()
        if not src_key.exists():
            print(f"ERROR: Provided SSH key {src_key} does not exist.")
            sys.exit(1)
        shutil.copyfile(src_key, ssh_key_path)
        os.chmod(ssh_key_path, 0o600)
        pub_key = src_key.with_suffix(".pub")
        if pub_key.exists():
            shutil.copyfile(pub_key, ssh_pub_path)
        print(f"Copied SSH key to {ssh_key_path}.")
        updated_env = True
    elif args.generate_ssh_key:
        import subprocess

        subprocess.run(
            ["ssh-keygen", "-t", "ed25519", "-N", "", "-f", str(ssh_key_path)],
            check=True,
        )
        print(
            f"Generated new ed25519 SSH keypair at {ssh_key_path} and {ssh_pub_path}."
        )
        updated_env = True
    else:
        print(
            "[REMINDER] No SSH key provided or generated. You must add one to payload/.ssh/id_rsa before launching the container."
        )

    # --- .env Handling: Look for config in the new directory structure ---
    env_sample_path = SESSIONS_DIR / project / "config" / "env.template"
    env_path = session_path / "payload/.env"  # Write directly to payload

    # First load template values
    template_vars = {}
    if env_sample_path.exists():
        with open(env_sample_path, "r") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#") and "=" in line:
                    k, v = line.strip().split("=", 1)
                    template_vars[k] = v.strip()
    else:
        print(f"[WARNING] Environment template not found at {env_sample_path}")

    # Overlay any values from --all-env
    if hasattr(args, "all_env") and args.all_env:
        for kv in args.all_env:
            if "=" in kv:
                k, v = kv.split("=", 1)
                template_vars[k] = v.strip()

    # Overlay actual env file values (filled values) into template_vars LAST
    env_file_path = getattr(args, "env_file", None) or TEAM_ENV
    print(f"[DEBUG] Reading actual env file: {env_file_path}")
    if Path(env_file_path).exists():
        with open(env_file_path, "r") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#") and "=" in line:
                    k, v = line.strip().split("=", 1)
                    if k == "SLACK_TEAM_ID":
                        print(f"[DEBUG] Raw SLACK_TEAM_ID line: {line.rstrip()}")
                        print(f"[DEBUG] SLACK_TEAM_ID value before strip: '{v}'")
                        print(f"[DEBUG] SLACK_TEAM_ID value after strip: '{v.strip()}'")
                    template_vars[k] = v.strip()
    else:
        print(f"[WARNING] Actual env file not found at {env_file_path}")

    # Debug print for SLACK_TEAM_ID and all keys
    if "SLACK_TEAM_ID" in template_vars:
        print(
            f"[DEBUG] SLACK_TEAM_ID in template_vars before mapping: '{template_vars['SLACK_TEAM_ID']}'"
        )
    else:
        print("[DEBUG] SLACK_TEAM_ID not found in template_vars before mapping")
    print(f"[DEBUG] All keys in template_vars: {list(template_vars.keys())}")

    # Initialize with default values for Task Master
    env_vars = {
        "MODEL": "claude-3-sonnet-20240229",
        "PERPLEXITY_MODEL": "sonar-medium-online",
        "MAX_TOKENS": "64000",
        "TEMPERATURE": "0.2",
        "DEFAULT_SUBTASKS": "5",
        "DEFAULT_PRIORITY": "medium",
        "DEBUG": "false",
        "LOG_LEVEL": "info",
    }

    # Map only the current role's fields to standard names
    role_upper = role.upper()
    role_prefix = role_upper
    # Allow for both FOO_BAR and FOO_BAR_BAZ (e.g., FULL_STACK_DEV)
    # Map fields for this role only
    role_fields = {
        f"{role_prefix}_EMAIL": "GIT_USER_EMAIL",
        f"{role_prefix}_SLACK_TOKEN": "SLACK_BOT_TOKEN",
        f"{role_prefix}_GITHUB_TOKEN": "GITHUB_PERSONAL_ACCESS_TOKEN",
        f"{role_prefix}_DISCORD_BOT_TOKEN": "DISCORD_BOT_TOKEN",
        f"{role_prefix}_DISCORD_CLIENT_ID": "DISCORD_CLIENT_ID",
        f"{role_prefix}_DISCORD_GUILD_ID": "DISCORD_GUILD_ID",
    }
    for src, dest in role_fields.items():
        if src in template_vars:
            env_vars[dest] = template_vars[src]

    # Add any generic fields from template_vars (e.g., ANTHROPIC_API_KEY, etc.)
    generic_keys = [
        "ANTHROPIC_API_KEY",
        "PERPLEXITY_API_KEY",
        "MODEL",
        "PERPLEXITY_MODEL",
        "MAX_TOKENS",
        "TEMPERATURE",
        "DEFAULT_SUBTASKS",
        "DEFAULT_PRIORITY",
        "DEBUG",
        "LOG_LEVEL",
        "SLACK_TEAM_ID",
        "TEAM_NAME",
        "TEAM_DESCRIPTION",
        "PROJECT_NAME",
    ]
    for k in generic_keys:
        if k in template_vars:
            env_vars[k] = template_vars[k]

    # Write the .env file with consistent formatting
    os.makedirs(os.path.dirname(env_path), exist_ok=True)
    with open(env_path, "w") as f:
        # Write Task Master variables first
        task_master_vars = [
            "ANTHROPIC_API_KEY",
            "MODEL",
            "PERPLEXITY_API_KEY",
            "PERPLEXITY_MODEL",
            "MAX_TOKENS",
            "TEMPERATURE",
            "DEFAULT_SUBTASKS",
            "DEFAULT_PRIORITY",
            "DEBUG",
            "LOG_LEVEL",
        ]
        for k in task_master_vars:
            if k in env_vars:
                f.write(f"{k}={env_vars[k]}\n")
        # Write mapped role-specific fields
        for k in [
            "GIT_USER_EMAIL",
            "SLACK_BOT_TOKEN",
            "GITHUB_PERSONAL_ACCESS_TOKEN",
            "DISCORD_BOT_TOKEN",
            "DISCORD_CLIENT_ID",
            "DISCORD_GUILD_ID",
        ]:
            if k in env_vars:
                f.write(f"{k}={env_vars[k]}\n")
        # Write any other generic fields
        for k in ["SLACK_TEAM_ID", "TEAM_NAME", "TEAM_DESCRIPTION", "PROJECT_NAME"]:
            if k in env_vars:
                f.write(f"{k}={env_vars[k]}\n")

    # --- Generate MCP config ---
    import json
    import re

    # Use role's mcp_config.template.json if it exists
    template_path = role_path / "mcp_config.template.json"
    if template_path.exists():
        print(f"Using custom MCP config template for role: {role_path}")
        with open(template_path) as f:
            template = f.read()

        # Replace all ${VAR} with values from env_vars, preserving structure
        def replace_var(match):
            var_name = match.group(1)
            value = env_vars.get(var_name, "")  # Return empty string for missing vars

            # Strip comments from value if it's a string
            if isinstance(value, str) and "#" in value:
                value = value.split("#")[0].strip()

            return value

        config_str = re.sub(r"\${([^}]+)}", replace_var, template)

        try:
            mcp_config = json.loads(config_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing MCP config template: {e}")
            mcp_config = {}
    else:
        # Generate default MCP config
        mcp_config = {
            "mcpServers": {
                "puppeteer": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
                    "env": {},
                },
                "github": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-github"],
                    "env": {
                        "GITHUB_PERSONAL_ACCESS_TOKEN": env_vars.get(
                            "GITHUB_PERSONAL_ACCESS_TOKEN", ""
                        )
                    },
                },
                "slack": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-slack"],
                    "env": {
                        "SLACK_BOT_TOKEN": env_vars.get("SLACK_BOT_TOKEN", ""),
                        "SLACK_TEAM_ID": env_vars.get("SLACK_TEAM_ID", ""),
                    },
                },
                "context7": {
                    "command": "npx",
                    "args": ["-y", "@upstash/context7-mcp@latest"],
                },
                "taskmaster-ai": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-taskmaster"],
                    "env": {
                        "ANTHROPIC_API_KEY": env_vars.get("ANTHROPIC_API_KEY", ""),
                        "PERPLEXITY_API_KEY": env_vars.get("PERPLEXITY_API_KEY", ""),
                        "MODEL": env_vars.get("MODEL", ""),
                        "PERPLEXITY_MODEL": env_vars.get("PERPLEXITY_MODEL", ""),
                        "MAX_TOKENS": env_vars.get("MAX_TOKENS", ""),
                        "TEMPERATURE": env_vars.get("TEMPERATURE", ""),
                        "DEFAULT_SUBTASKS": env_vars.get("DEFAULT_SUBTASKS", ""),
                        "DEFAULT_PRIORITY": env_vars.get("DEFAULT_PRIORITY", ""),
                        "DEBUG": env_vars.get("DEBUG", ""),
                        "LOG_LEVEL": env_vars.get("LOG_LEVEL", ""),
                    },
                },
            }
        }

    # Write the MCP config
    mcp_config_path = session_path / "payload/mcp_config.json"
    os.makedirs(os.path.dirname(mcp_config_path), exist_ok=True)
    with open(mcp_config_path, "w") as f:
        json.dump(mcp_config, f, indent=4)
    print(f"Generated {mcp_config_path}")

    # --- Copy restore script ---
    restore_script = session_path / "payload/restore_payload.sh"
    shutil.copy(SESSIONS_DIR / "_shared/restore_payload.sh", restore_script)
    os.chmod(restore_script, 0o755)
    print(f"Added restore script at {restore_script}")

    # --- Check for missing env keys ---
    required_keys = [
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "SLACK_BOT_TOKEN",
        "SLACK_TEAM_ID",
        "GIT_USER_NAME",
        "GIT_USER_EMAIL",
        "GIT_SSH_KEY_PATH",
        "ANTHROPIC_API_KEY",
        "PERPLEXITY_API_KEY",
    ]
    missing_keys = [k for k in required_keys if k not in env_vars or not env_vars[k]]
    if missing_keys:
        print("[ACTION REQUIRED] The following .env keys are missing values:")
        for k in missing_keys:
            print(f"  - {k}")
        print(
            f"Edit {env_path} to fill in these values before launching the container."
        )
    else:
        print("All .env keys are set.")

    # --- Warn if no SSH key present ---
    if not ssh_key_path.exists():
        print(
            "[SECURITY WARNING] No SSH private key found in payload/.ssh/id_rsa. You must add or generate one before using git in the container."
        )

    # --- Warn if .ssh is not in .gitignore ---
    gitignore_paths = [session_path / ".gitignore", Path(".gitignore")]
    ssh_ignored = False
    for gi_path in gitignore_paths:
        if gi_path.exists():
            with open(gi_path, "r") as f:
                for line in f:
                    if ".ssh" in line:
                        ssh_ignored = True
                        break
        if ssh_ignored:
            break
    if not ssh_ignored:
        print(
            "[SECURITY WARNING] .ssh directory is not in .gitignore! Add 'payload/.ssh/' to your .gitignore to prevent accidental commits of private keys."
        )

    # Reminders for secrets
    print_reminders()
    print(f"Next: Launch the container - the restore script will handle the rest!")


def add_role(args):
    import shutil

    name = args.name or input("New role/template name: ").strip()
    role_path = ROLES_DIR / name
    if role_path.exists():
        print(f"Role '{name}' already exists.")
        sys.exit(1)
    # Copy from example_role as a full-featured template
    example_role_path = ROLES_DIR / "example_role"
    if not example_role_path.exists():
        print(
            "Error: example_role template not found. Please ensure roles/example_role exists."
        )
        sys.exit(1)
    shutil.copytree(example_role_path, role_path)
    print(
        f"Created new role template at {role_path} (copied from example_role). Edit the template files as needed."
    )


def print_simple_help():
    print(
        """
LedgerFlow Team CLI - Quickstart

To create a new python-coder session for the current project and generate SSH keys:

  python tools/team_cli.py create-session --name my-coder --role python_coder --generate-ssh-key --prompt-all

To create a session and provide an existing SSH key:

  python tools/team_cli.py create-session --name my-coder --role python_coder --ssh-key ~/.ssh/your_key

To include project-specific docs (if you have a project called 'myproject'):

  python tools/team_cli.py create-session --name my-coder --role python_coder --project myproject --generate-ssh-key --prompt-all

For more options, run:
  python tools/team_cli.py --help
    """
    )


def load_crew_config(config_path: Path = None) -> Dict[str, Any]:
    """Load and validate the crew configuration.

    Args:
        config_path: Optional path to crew config. Defaults to team/crew.yaml
    """
    config_file = config_path or TEAM_CONFIG

    if not config_file.exists():
        print(f"Error: Crew configuration not found at {config_file}")
        sys.exit(1)

    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error parsing crew configuration: {e}")
        sys.exit(1)

    if not isinstance(config, dict) or "crew" not in config:
        print(f"Error: Invalid crew configuration format in {config_file}")
        print("Expected format: {'crew': {...}}")
        sys.exit(1)

    # Validate crew member configs
    required_fields = ["role", "bot_id", "container", "slack_handle", "email"]
    for member_id, member in config["crew"].items():
        missing = [f for f in required_fields if f not in member]
        if missing:
            print(
                f"Error: Member '{member_id}' missing required fields: {', '.join(missing)}"
            )
            sys.exit(1)

    return config


def load_team_env(env_path: Path = None) -> Dict[str, str]:
    """Load the team environment variables.

    Args:
        env_path: Optional path to team env file. Defaults to teams/default/config/env
    """
    env_file = env_path or TEAM_ENV

    if not env_file.exists():
        print(f"Error: Team environment file not found at {env_file}")
        print(
            "Copy teams/default/config/env.template to teams/default/config/env and fill in values."
        )
        sys.exit(1)

    env_vars = {}
    try:
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()
    except Exception as e:
        print(f"Error reading team environment file: {e}")
        sys.exit(1)

    # Validate required env vars
    required_vars = ["LEDGERFLOW_EMAIL_PREFIX", "SLACK_BOT_TOKEN", "SLACK_TEAM_ID"]
    missing = [v for v in required_vars if not env_vars.get(v)]
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)

    return env_vars


def create_crew(args):
    """Create multiple sessions based on a team environment file."""
    env_file = Path(args.env_file) if args.env_file else TEAM_ENV
    if not env_file.exists():
        print(f"Error: Team environment file not found at {env_file}")
        sys.exit(1)

    # Load team environment
    team_env = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                team_env[key.strip()] = value.strip()

    # Extract project info and docs config
    project_name = team_env.get("PROJECT_NAME", "default")
    repo_url = team_env.get("REPO_URL", "")
    include_global_docs = team_env.get("INCLUDE_GLOBAL_DOCS", "true").lower() == "true"
    include_project_docs = (
        team_env.get("INCLUDE_PROJECT_DOCS", "true").lower() == "true"
    )
    include_role_docs = team_env.get("INCLUDE_ROLE_DOCS", "true").lower() == "true"

    # Create project directory with the new structure
    project_dir = SESSIONS_DIR / project_name / "sessions"
    project_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nCreating sessions for project: {project_name}")
    print(f"Documentation settings:")
    print(f"- Include global docs: {include_global_docs}")
    print(f"- Include project docs: {include_project_docs}")
    print(f"- Include role docs: {include_role_docs}")

    # Shared tokens
    shared_tokens = {
        "SLACK_WORKSPACE_ID": team_env.get("SLACK_WORKSPACE_ID", ""),
        "GITHUB_ORG": team_env.get("GITHUB_ORG", ""),
        "GITHUB_REPO": team_env.get("GITHUB_REPO", ""),
    }

    # Group environment variables by session
    sessions = {}
    for key, value in team_env.items():
        # Skip shared/project config
        if key in ["PROJECT_NAME", "REPO_URL"] or key in shared_tokens:
            continue

        # Parse session name from key (e.g., PM_GUARDIAN_EMAIL -> pm_guardian)
        parts = key.lower().split("_")
        if len(parts) < 2:
            continue

        # Extract session name and variable
        if key.endswith("_EMAIL"):
            session_name = "_".join(parts[:-1])
            sessions.setdefault(session_name, {})["email"] = value
        elif key.endswith("_SLACK_TOKEN"):
            session_name = "_".join(parts[:-2])
            sessions.setdefault(session_name, {})["slack_token"] = value
        elif key.endswith("_GITHUB_TOKEN"):
            session_name = "_".join(parts[:-2])
            sessions.setdefault(session_name, {})["github_token"] = value

    # If no sessions found, print error and exit
    if not sessions:
        print("\nError: No valid sessions found in environment file.")
        print(
            "Make sure you have variables named like PM_GUARDIAN_EMAIL, PM_GUARDIAN_SLACK_TOKEN, etc."
        )
        sys.exit(1)

    # Create each session
    for session_name, config in sessions.items():
        print(f"\nCreating session: {session_name}")

        # Check if all required keys are present
        required_keys = ["email", "slack_token", "github_token"]
        missing_keys = [k for k in required_keys if k not in config]
        if missing_keys:
            print(
                f"Error: Missing required keys for session {session_name}: {', '.join(missing_keys)}"
            )
            print(f"Available keys: {', '.join(config.keys())}")
            print(f"Skipping session {session_name}")
            continue

        # Use session name as role, fallback to python_coder with warning
        role_dir = ROLES_DIR / session_name
        if role_dir.exists():
            role = session_name
        else:
            print(
                f"[WARNING] Role directory 'roles/{session_name}/' not found. Falling back to 'python_coder'. Please create 'roles/{session_name}/' for custom docs and templates."
            )
            role = "python_coder"

        # Prepare session arguments
        session_args = argparse.Namespace(
            name=session_name,
            role=role,
            generate_ssh_key=True,
            ssh_key=None,
            project=project_name if include_project_docs else None,
            include_global_docs=include_global_docs,
            include_role_docs=include_role_docs,
            prompt_all=False,
            all_env=[
                # Add team-level variables first
                f"TEAM_NAME={team_env.get('TEAM_NAME', project_name)}",
                f"TEAM_DESCRIPTION={team_env.get('TEAM_DESCRIPTION', project_name + ' team')}",
                f"PROJECT_NAME={project_name}",
                # Session-specific variables
                f"GIT_USER_NAME={session_name}",
                f"GIT_USER_EMAIL={config['email']}",
                f"SLACK_BOT_TOKEN={config['slack_token']}",
                f"GITHUB_PERSONAL_ACCESS_TOKEN={config['github_token']}",
                f"SLACK_WORKSPACE_ID={shared_tokens['SLACK_WORKSPACE_ID']}",
                f"SLACK_TEAM_ID={shared_tokens['SLACK_WORKSPACE_ID']}",  # Add SLACK_TEAM_ID
                # Add base configuration with actual values from team env
                f"ANTHROPIC_API_KEY={team_env.get('ANTHROPIC_API_KEY', '')}",
                f"PERPLEXITY_API_KEY={team_env.get('PERPLEXITY_API_KEY', '')}",
                f"MODEL={team_env.get('MODEL', 'claude-3-sonnet-20240229')}",
                f"PERPLEXITY_MODEL={team_env.get('PERPLEXITY_MODEL', 'sonar-medium-online')}",
                f"MAX_TOKENS={team_env.get('MAX_TOKENS', '64000')}",
                f"TEMPERATURE={team_env.get('TEMPERATURE', '0.2')}",
                f"DEFAULT_SUBTASKS={team_env.get('DEFAULT_SUBTASKS', '5')}",
                f"DEFAULT_PRIORITY={team_env.get('DEFAULT_PRIORITY', 'medium')}",
                f"DEBUG={team_env.get('DEBUG', 'false')}",
                f"LOG_LEVEL={team_env.get('LOG_LEVEL', 'info')}",
                # Include any role-specific variables that are in the team env
                *[
                    f"{k}={v}"
                    for k, v in team_env.items()
                    if k.startswith(session_name.upper())
                    or any(
                        k.startswith(part.upper() + "_")
                        for part in session_name.upper().split("_")
                    )
                ],
            ],
            overwrite=getattr(args, "overwrite", False),
        )
        # Ensure the correct env file is always used
        session_args.env_file = str(env_file)

        try:
            create_session(session_args)
            print(f"Successfully created session: {session_name}")
        except Exception as e:
            print(f"Error creating session {session_name}: {str(e)}")
            continue

    # After all session payloads are created
    propagate_cline_docs_shared(project_name, [role for role in sessions.keys()])
    print("[INFO] All session payloads have received the finalized cline_docs_shared.")

    print(f"\nTeam creation complete! All sessions created in {project_dir}")
    print("\nAction Required:")
    print("1. Set ANTHROPIC_API_KEY in each session's .env file")
    print("2. Set PERPLEXITY_API_KEY in each session's .env file (optional)")
    print_reminders()


def propagate_cline_docs_shared(project, roles):
    """
    Copy the filled cline_docs_shared from the team root into each session payload.
    """
    team_shared_dir = Path(f"teams/{project}/cline_docs_shared")
    for role in roles:
        payload_dir = Path(f"teams/{project}/sessions/{role}/payload")
        target_shared_dir = payload_dir / "cline_docs_shared"
        if target_shared_dir.exists():
            shutil.rmtree(target_shared_dir)
        shutil.copytree(team_shared_dir, target_shared_dir)
        print(f"[INFO] Propagated cline_docs_shared to {target_shared_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="LedgerFlow AI Team CLI", usage="%(prog)s <command> [options]"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Create Session Command
    create_parser = subparsers.add_parser(
        "create-session", help="Create a new agent session"
    )
    create_parser.add_argument("--name", help="Session name")
    create_parser.add_argument("--role", help="Role/template to use")
    create_parser.add_argument("--project", help="Project name for docs")
    create_parser.add_argument("--ssh-key", help="Path to existing SSH key to use")
    create_parser.add_argument(
        "--generate-ssh-key", action="store_true", help="Generate new SSH key"
    )
    create_parser.add_argument(
        "--prompt-all", action="store_true", help="Prompt for all env values"
    )
    create_parser.add_argument(
        "--all-env", nargs="+", help="Set all env values at once (key=value pairs)"
    )
    create_parser.add_argument(
        "--no-global-docs",
        action="store_false",
        dest="include_global_docs",
        help="Skip including global documentation",
    )
    create_parser.add_argument(
        "--no-role-docs",
        action="store_false",
        dest="include_role_docs",
        help="Skip including role-specific documentation",
    )
    create_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing session directory and regenerate all payload files",
    )

    # Create Crew Command
    crew_parser = subparsers.add_parser(
        "create-crew", help="Create multiple sessions from team config"
    )
    crew_parser.add_argument("--env-file", help="Path to team environment file")
    crew_parser.add_argument("--template", help="Path to team template YAML file")
    crew_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing session directories and regenerate all payload files",
    )

    # Add Role Command
    add_role_parser = subparsers.add_parser("add-role", help="Add a new role template")
    add_role_parser.add_argument("name", help="Name of the new role")
    add_role_parser.add_argument("--copy-from", help="Existing role to copy from")

    args = parser.parse_args()

    if not args.command:
        print_simple_help()
        sys.exit(1)

    if args.command == "create-session":
        create_session(args)
    elif args.command == "add-role":
        add_role(args)
    elif args.command == "create-crew":
        create_crew(args)
    else:
        print(f"Unknown command: {args.command}")
        print_simple_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
