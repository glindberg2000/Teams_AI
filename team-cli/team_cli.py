#!/usr/bin/env python3
"""
team_cli.py - CLI tool for LedgerFlow AI Team session management

Quickstart:
  python team-cli/team_cli.py create-session --name agent-name --role python_coder --generate-ssh-key --prompt-all
  python team-cli/team_cli.py create-session --name agent-name --role python_coder --ssh-key ~/.ssh/existing_key
  python team-cli/team_cli.py create-session --name agent-name --role python_coder --all-env GIT_USER_NAME=alex GIT_USER_EMAIL=alex@example.com ...

Key Features:
- Creates isolated agent sessions from role templates
- Handles SSH key generation/copying
- Configures environment variables and MCP servers
- Manages documentation inheritance (global -> project -> role -> session)
- Generates restore scripts for container setup

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
  sessions/<agent>/      # Per-agent isolated environments

See README.md for full documentation and setup instructions.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

SESSIONS_DIR = Path("sessions")
ROLES_DIR = Path("roles")


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
        "- Example: python team-cli/team_cli.py create-session --name pm-guardian --role python_coder --ssh-key ~/.ssh/ai-architect_gl"
    )
    print(
        "- Example: python team-cli/team_cli.py create-session --name pm-guardian --role python_coder --generate-ssh-key"
    )


def list_roles():
    if not ROLES_DIR.exists():
        print("No roles directory found.")
        return
    print("Available roles/templates:")
    for role in ROLES_DIR.iterdir():
        if role.is_dir():
            print(f"- {role.name}")


def create_session(args):
    name = args.name or input("Session name (e.g. pm-guardian): ").strip()
    list_roles()
    role = args.role or input("Role/template to use: ").strip()
    role_path = ROLES_DIR / role
    if not role_path.exists():
        print(f"Role '{role}' not found in {ROLES_DIR}.")
        sys.exit(1)
    session_path = SESSIONS_DIR / name
    if session_path.exists():
        print(f"Session '{name}' already exists at {session_path}.")
        sys.exit(1)
    # Copy role template to new session
    shutil.copytree(role_path, session_path)
    print(f"Created session '{name}' from role '{role}'.")

    # --- Project and Docs Handling ---
    docs_included = []
    session_docs = session_path / "docs"
    session_docs.mkdir(exist_ok=True)
    # Copy global docs
    global_docs_dir = Path("docs/global")
    if global_docs_dir.exists():
        for f in global_docs_dir.glob("*.md"):
            shutil.copy(f, session_docs)
            docs_included.append(f"global/{f.name}")
    # Copy project docs if --project is set
    if hasattr(args, "project") and args.project:
        project_docs_dir = Path(f"docs/projects/{args.project}")
        if project_docs_dir.exists():
            for f in project_docs_dir.glob("*.md"):
                shutil.copy(f, session_docs)
                docs_included.append(f"projects/{args.project}/{f.name}")
        else:
            print(f"[WARNING] Project docs not found: {project_docs_dir}")
    # Copy role docs
    role_docs_dir = role_path / "docs"
    if role_docs_dir.exists():
        for f in role_docs_dir.glob("*.md"):
            shutil.copy(f, session_docs)
            docs_included.append(f"role/{role}/{f.name}")
    print(
        f"Included docs in session: {', '.join(docs_included) if docs_included else 'none'}"
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

    # --- .env Handling: always generate from .env.sample ---
    env_sample_path = session_path / ".env.sample"
    env_path = session_path / "payload/.env"  # Changed to write directly to payload
    env_vars = {}
    if env_sample_path.exists():
        with open(env_sample_path, "r") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#") and "=" in line:
                    k, v = line.strip().split("=", 1)
                    env_vars[k] = v
    # Allow --all-env flag to set all env keys at once (as key=value pairs)
    if hasattr(args, "all_env") and args.all_env:
        for kv in args.all_env:
            if "=" in kv:
                k, v = kv.split("=", 1)
                env_vars[k] = v
    # Prompt for all env keys if --prompt-all is set
    if hasattr(args, "prompt_all") and args.prompt_all:
        for k in env_vars:
            # Skip GITHUB_PAT if present (legacy, not used)
            if k == "GITHUB_PAT":
                continue
            if k == "GIT_SSH_KEY_PATH":
                val = input(
                    f"Enter value for {k} (leave blank to use the generated key at /root/.ssh/id_rsa): "
                )
                if not val and updated_env:
                    env_vars[k] = "/root/.ssh/id_rsa"
                elif val:
                    env_vars[k] = val
            else:
                val = input(f"Enter value for {k} (leave blank to keep current): ")
                if val:
                    env_vars[k] = val
    # Always set GIT_SSH_KEY_PATH if we handled a key
    if updated_env:
        env_vars["GIT_SSH_KEY_PATH"] = "/root/.ssh/id_rsa"
    # Write .env to payload
    with open(env_path, "w") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")
    print(f"Generated {env_path} with all crucial variables.")

    # --- Generate MCP config ---
    import json
    import re

    # Read the template
    template_path = role_path / "mcp_config.template.json"
    if not template_path.exists():
        print(
            f"[WARNING] No MCP config template found at {template_path}, using default configuration."
        )
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
            }
        }
    else:
        with open(template_path) as f:
            template = f.read()

        # Replace all ${VAR} with values from env_vars
        def replace_var(match):
            var_name = match.group(1)
            return env_vars.get(var_name, "")

        config_str = re.sub(r"\${([^}]+)}", replace_var, template)
        mcp_config = json.loads(config_str)

    # Write to payload
    mcp_config_path = session_path / "payload/mcp_config.json"
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
    name = args.name or input("New role/template name: ").strip()
    role_path = ROLES_DIR / name
    if role_path.exists():
        print(f"Role '{name}' already exists.")
        sys.exit(1)
    os.makedirs(role_path / "docs", exist_ok=True)
    # Create sample files
    (role_path / ".env.sample").write_text(
        "# Fill in environment variables\nSLACK_BOT_TOKEN=\nSLACK_TEAM_ID=\nGIT_USER_NAME=\nGIT_USER_EMAIL=\nGITHUB_PERSONAL_ACCESS_TOKEN=\nGIT_SSH_KEY_PATH=/root/.ssh/id_rsa # Defaults to generated key if left blank\n# Add other required secrets here\nANTHROPIC_API_KEY= # Required for Taskmaster MCP\nPERPLEXITY_API_KEY= # Required for Taskmaster MCP\n"
    )
    # Build mcp_config.template.json with all default servers and taskmaster-ai
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
                    "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
                },
            },
            "slack": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-slack"],
                "env": {
                    "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
                    "SLACK_TEAM_ID": "${SLACK_TEAM_ID}",
                },
            },
            "context7": {
                "command": "npx",
                "args": ["-y", "@upstash/context7-mcp@latest"],
            },
            "taskmaster-ai": {
                "command": "npx",
                "args": ["-y", "--package=task-master-ai", "task-master-ai"],
                "env": {
                    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
                    "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}",
                    "MODEL": "claude-3-7-sonnet-20250219",
                    "PERPLEXITY_MODEL": "sonar-pro",
                    "MAX_TOKENS": "64000",
                    "TEMPERATURE": "0.2",
                    "DEFAULT_SUBTASKS": "5",
                    "DEFAULT_PRIORITY": "medium",
                },
            },
        }
    }
    import json

    (role_path / "mcp_config.template.json").write_text(
        json.dumps(mcp_config, indent=2) + "\n"
    )
    (role_path / "docs/agent_instructions.md").write_text(
        "# Agent Instructions\n\nDescribe the agent's responsibilities here.\n"
    )
    print(f"Created new role template at {role_path}.")
    print("Edit the template files as needed.")


def print_simple_help():
    print(
        """
LedgerFlow Team CLI - Quickstart

To create a new python-coder session for the current project and generate SSH keys:

  python team-cli/team_cli.py create-session --name my-coder --role python_coder --generate-ssh-key --prompt-all

To create a session and provide an existing SSH key:

  python team-cli/team_cli.py create-session --name my-coder --role python_coder --ssh-key ~/.ssh/your_key

To include project-specific docs (if you have a project called 'myproject'):

  python team-cli/team_cli.py create-session --name my-coder --role python_coder --project myproject --generate-ssh-key --prompt-all

For more options, run:
  python team-cli/team_cli.py --help
    """
    )


def main():
    parser = argparse.ArgumentParser(
        description="LedgerFlow AI Team session management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    # create-session command
    create_parser = subparsers.add_parser(
        "create-session", help="Create a new agent session from a role template"
    )
    create_parser.add_argument("--name", help="Session name (e.g. pm-guardian)")
    create_parser.add_argument("--role", help="Role/template to use")
    create_parser.add_argument(
        "--project", help="Project name to include project-specific docs"
    )
    create_parser.add_argument(
        "--ssh-key", help="Path to SSH private key to copy into payload"
    )
    create_parser.add_argument(
        "--generate-ssh-key",
        action="store_true",
        help="Generate a new SSH keypair in payload",
    )
    create_parser.add_argument(
        "--prompt-all",
        action="store_true",
        help="Prompt for all .env keys interactively",
    )
    create_parser.add_argument(
        "--all-env",
        nargs="+",
        help="Set all .env keys at once (key=value pairs)",
    )
    create_parser.add_argument(
        "--github-pat", help="GitHub Personal Access Token (reminder only)"
    )
    create_parser.add_argument(
        "--slack-token", help="Slack Bot/User Token (reminder only)"
    )

    # add-role command
    add_role_parser = subparsers.add_parser("add-role", help="Add a new role template")
    add_role_parser.add_argument("--name", help="Role name (e.g. python_coder)")
    add_role_parser.add_argument("--docs", nargs="+", help="Paths to docs to include")
    add_role_parser.add_argument("--env-sample", help="Path to .env.sample to include")

    args = parser.parse_args()

    if not args.command:
        print_simple_help()
        sys.exit(1)

    if args.command == "create-session":
        create_session(args)
    elif args.command == "add-role":
        add_role(args)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
