#!/usr/bin/env python3
"""
scaffold_team.py - Team Configuration Generator

This script generates standardized team configuration for a LedgerFlow AI project, including:
- Environment file (.env.{project}) with all required API keys and settings
- Environment template (teams/{project}/env.template) for reference
- Comprehensive setup checklist (teams/{project}/checklist.md)
- Standard naming conventions for consistent team-cli.py integration

Usage:
    python scaffold_team.py                     # Interactive mode
    python scaffold_team.py --project test      # CLI mode with flags
    python scaffold_team.py -f crew.yaml        # Use YAML file
    python scaffold_team.py --help              # Show help

Examples:
    # Create a new project with specific settings
    python scaffold_team.py --project testproj --prefix user --domain example.com --roles pm_guardian,python_coder

    # Generate files without creating directories (for testing)
    python scaffold_team.py --project testdry --dry-run --roles pm_guardian

Required Environment Variables (in .env.{project}):
- Team tokens:
  - ANTHROPIC_API_KEY: Claude/Taskmaster integration
  - GITHUB_PERSONAL_ACCESS_TOKEN: For GitHub access
  - SLACK_BOT_TOKEN, SLACK_TEAM_ID: For Slack integration
  - PERPLEXITY_API_KEY: For research capabilities
- Per-role tokens:
  - ROLE_SLACK_TOKEN: Slack bot token for the role
  - ROLE_GITHUB_TOKEN: GitHub personal access token for the role
  - ROLE_EMAIL: Email address for the role

Notes:
- Never commit .env files to git
- Store sensitive data in secure storage (iCloud, 1Password, etc.)
- Follow the checklist completely before starting development
"""
import argparse
import os
import sys
from pathlib import Path
import yaml
import datetime
import json
import shutil

# Constants
DEFAULT_ROLES = ["pm_guardian", "python_coder", "reviewer"]
ROLES_DIR = Path("roles")


def capitalize_first_letters(s):
    """
    Capitalize the first letter of each word in a string.

    Args:
        s (str): Input string, typically underscore-separated

    Returns:
        str: String with first letter of each word capitalized
    """
    return " ".join(word.capitalize() for word in s.split("_"))


def parse_args():
    """
    Parse command-line arguments for scaffold_team.py.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate team configuration and checklist"
    )
    parser.add_argument("--project", help="Project name")
    parser.add_argument("--prefix", help="Email prefix (username)")
    parser.add_argument("--domain", help="Email domain")
    parser.add_argument("--roles", help="Comma-separated list of roles")
    parser.add_argument(
        "--dry-run", action="store_true", help="Don't create directories"
    )
    parser.add_argument("-f", "--file", help="YAML configuration file")
    parser.add_argument(
        "--add-role",
        help="Append a new role's config block to the env file (does not overwrite others)",
    )
    return parser.parse_args()


def interactive_input():
    """
    Get user input interactively for project configuration.

    Returns:
        tuple: (project, prefix, domain, roles) configuration values
    """
    print("Team Configuration Generator")
    print("----------------------------")

    project = input("Project name: ").strip().lower()
    prefix = input("Email prefix (username): ").strip()
    domain = input("Email domain: ").strip()

    roles_input = input(
        f"Roles (comma-separated, default: {','.join(DEFAULT_ROLES)}): "
    ).strip()
    roles = (
        [r.strip() for r in roles_input.split(",")] if roles_input else DEFAULT_ROLES
    )

    return project, prefix, domain, roles


def get_valid_roles():
    """
    Dynamically list valid roles by reading the roles directory, excluding _templates and example_role.
    Returns:
        list: List of valid role names
    """
    if not ROLES_DIR.exists():
        return []
    return [
        d.name
        for d in ROLES_DIR.iterdir()
        if d.is_dir() and d.name not in ["_templates", "example_role"]
    ]


def validate_roles(roles):
    """
    Validate roles against the list of valid roles (from roles directory).

    Args:
        roles (list): List of role names to validate

    Returns:
        bool: True if all roles are valid, False otherwise
    """
    valid_roles = get_valid_roles()
    invalid_roles = [r for r in roles if r not in valid_roles]
    if invalid_roles:
        print(f"Warning: Invalid roles: {', '.join(invalid_roles)}")
        print(f"Valid roles are: {', '.join(valid_roles)}")
        return False
    return True


def generate_env_file(project, prefix, domain, roles, dry_run=False):
    """
    Generate the environment file (teams/{project}/config/env) with all required configuration.

    This creates a complete environment file that is compatible with team-cli.py.

    Args:
        project (str): Project name
        prefix (str): Email prefix/username
        domain (str): Email domain
        roles (list): List of roles to configure
        dry_run (bool): If True, don't actually write file

    Returns:
        str: Path to the generated environment file
    """
    content = [
        f"# Environment configuration for {project} team",
        "# WARNING: Never commit this file to git!",
        "# Store a copy in your secure storage (iCloud, 1Password, etc.)",
        "",
        "# Team Configuration",
        f"TEAM_NAME={project}",
        f"TEAM_DESCRIPTION={project} team",
        f"PROJECT_NAME={project}",
        f"EMAIL_PREFIX={prefix}",
        "",
        "# Documentation Configuration",
        "INCLUDE_GLOBAL_DOCS=true",
        "INCLUDE_PROJECT_DOCS=true",
        "INCLUDE_ROLE_DOCS=true",
        "",
        "# Required API Keys and Tokens",
        "ANTHROPIC_API_KEY=  # Required: Get from https://console.anthropic.com",
        "PERPLEXITY_API_KEY=  # Optional: Get from https://perplexity.ai",
        "SLACK_TEAM_ID=  # Required: Get from Slack workspace settings",
        "",
        "# Task Master MCP Configuration",
        "MODEL=claude-3-sonnet-20240229",
        "PERPLEXITY_MODEL=sonar-medium-online",
        "MAX_TOKENS=64000",
        "TEMPERATURE=0.2",
        "DEFAULT_SUBTASKS=5",
        "DEFAULT_PRIORITY=medium",
        "DEBUG=false",
        "LOG_LEVEL=info",
        "",
        "# Docker Configuration",
        "DOCKER_GROUP=1000  # Default group ID for Docker",
        "DOCKER_NETWORK=ledgerflow  # Docker network name",
        "",
        "# Backup Configuration",
        "BACKUP_TARGET=/path/to/backup  # Where to store backups",
        "",
        "# SSH Configuration",
        "SSH_KEY_PATH=/root/.ssh/id_rsa  # Default SSH key path in container",
        "GIT_SSH_KEY_PATH=/root/.ssh/id_rsa  # Default SSH key path for Git",
        "",
    ]

    # Add role-specific configurations
    for role in roles:
        # CRITICAL: For team-cli parsing, we must follow a specific format:
        # It extracts session names by looking at environment variables like:
        # PM_GUARDIAN_SLACK_TOKEN -> ["PM", "GUARDIAN", "SLACK_TOKEN"]
        # Then it takes parts[:-2] (["PM", "GUARDIAN"]) and joins with "_" to get "pm_guardian"

        # Convert role to uppercase for environment variables
        role_upper = role.upper()
        role_id = role.lower()
        role_display = capitalize_first_letters(role_id)
        project_display = capitalize_first_letters(project)
        role_github = f"{project}-{role_id.replace('_', '-')}"
        role_display_var = f"{project_display} {' '.join([part.upper() for part in role_id.split('_')])}"

        content.extend(
            [
                f"# {role_display} Configuration",
                f"{role_upper}_EMAIL={prefix}+{project}-{role_id}@{domain}",
                f"{role_upper}_SLACK_TOKEN=  # Required: Bot token for this role",
                f"{role_upper}_GITHUB_TOKEN=  # Required: GitHub PAT for this role",
                f"{role_upper}_DISCORD_BOT_TOKEN=  # Required: Discord bot token for this role",
                f"{role_upper}_DISCORD_CLIENT_ID=  # Required: Discord client ID for this role",
                f"{role_upper}_DISCORD_GUILD_ID=  # Optional: Discord guild/server ID for this role",
                f"{role_upper}_BOT={project}_{role_id}_bot",
                f"{role_upper}_GITHUB={role_github}",
                f"{role_upper}_DISPLAY={role_display_var}",
                "",
            ]
        )

    # Use new directory structure
    config_dir = Path(f"teams/{project}/config")
    env_file = config_dir / "env"

    if not dry_run:
        # Create directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)

        with open(env_file, "w") as f:
            f.write("\n".join(content))
        print(f"Created {env_file}")

    return env_file


def generate_env_template(project, roles, dry_run=False):
    """
    Generate the environment template for reference.

    This creates a template file that shows the variable structure without
    actual values, stored in teams/{project}/config/env.template.

    Args:
        project (str): Project name
        roles (list): List of roles to configure
        dry_run (bool): If True, don't actually write file

    Returns:
        Path or None: Path to the generated template file, or None if dry_run
    """
    content = [
        "# Team Configuration",
        "TEAM_NAME=${TEAM_NAME}",
        "TEAM_DESCRIPTION=${TEAM_DESCRIPTION}",
        "",
    ]

    # Add role-specific configurations
    for role in roles:
        # Follow the same pattern as in generate_env_file for consistency
        role_upper = role.upper()
        role_id = role.lower()
        role_display = capitalize_first_letters(role_id)

        content.extend(
            [
                f"# {role_display} Configuration",
                f"{role_upper}_EMAIL=${{EMAIL_PREFIX}}+${{TEAM_NAME}}-{role_id}@${{DOMAIN}}",
                f"{role_upper}_SLACK_TOKEN=  # Required: Bot token for this role",
                f"{role_upper}_GITHUB_TOKEN=  # Required: GitHub PAT for this role",
                f"{role_upper}_DISCORD_BOT_TOKEN=  # Required: Discord bot token for this role",
                f"{role_upper}_DISCORD_CLIENT_ID=  # Required: Discord client ID for this role",
                f"{role_upper}_DISCORD_GUILD_ID=  # Optional: Discord guild/server ID for this role",
                f"{role_upper}_BOT=${{TEAM_NAME}}_{role_id}_bot",
                f"{role_upper}_GITHUB=${{TEAM_NAME}}-{role_id}",
                f"{role_upper}_DISPLAY=${{TEAM_NAME_CAP}} {role_display}",
                "",
            ]
        )

    if dry_run:
        return None

    # Create config directory structure
    config_dir = Path(f"teams/{project}/config")
    config_dir.mkdir(parents=True, exist_ok=True)

    env_template_file = config_dir / "env.template"

    with open(env_template_file, "w") as f:
        f.write("\n".join(content))

    print(f"Created {env_template_file} with team-cli compatible template")
    return env_template_file


def generate_checklist(project, roles, dry_run=False):
    """
    Generate the setup checklist for the team.

    Creates a markdown file with setup instructions in teams/{project}/config/checklist.md.

    Args:
        project (str): Project name
        roles (list): List of roles to configure
        dry_run (bool): If True, don't actually write file

    Returns:
        Path or None: Path to the generated checklist file, or None if dry_run
    """
    content = [
        f"# {project} Team Setup Checklist",
        "",
        "## Core Setup",
        "",
        "- [ ] Clone the LedgerFlow AI Team repository",
        f"- [ ] Create `teams/{project}/config/env` file (already done - see details below)",
        f"- [ ] Fill in all required API keys in `teams/{project}/config/env`",
        f"- [ ] Run `python tools/team_cli.py create-crew --env-file teams/{project}/config/env` to create all sessions",
        "",
        "## API Keys Required",
        "",
        "### Team Level",
        "",
        "- [ ] **ANTHROPIC_API_KEY**: Get from https://console.anthropic.com",
        "- [ ] **PERPLEXITY_API_KEY**: Get from https://perplexity.ai (optional)",
        "- [ ] **GITHUB_PERSONAL_ACCESS_TOKEN**: Create at https://github.com/settings/tokens",
        "- [ ] **SLACK_BOT_TOKEN**: Create at https://api.slack.com/apps",
        "- [ ] **SLACK_TEAM_ID**: Get from Slack workspace settings",
        "",
        "### Per-Role API Keys",
        "",
        "- [ ] **For each role, you must create a separate Discord bot (application) and obtain its credentials.**",
        "- [ ] **Each role needs its own Discord bot token, client ID, and (optionally) guild/server ID.**",
        "",
        "#### Example for PM_GUARDIAN:",
        "- [ ] **PM_GUARDIAN_SLACK_TOKEN**: Unique Slack bot token for this role",
        "- [ ] **PM_GUARDIAN_GITHUB_TOKEN**: Unique GitHub PAT for this role",
        "- [ ] **PM_GUARDIAN_DISCORD_BOT_TOKEN**: Unique Discord bot token for this role",
        "- [ ] **PM_GUARDIAN_DISCORD_CLIENT_ID**: Discord client ID for this role",
        "- [ ] **PM_GUARDIAN_DISCORD_GUILD_ID**: (Optional) Discord guild/server ID for this role",
        "",
        "(Repeat for each role: PYTHON_CODER, REVIEWER, DB_GUARDIAN, FULL_STACK_DEV, etc.)",
        "",
        "## Discord Bot Setup (Repeat for Each Role)",
        "",
        "1. **Create a Discord Application & Bot**",
        "    - Go to the [Discord Developer Portal](https://discord.com/developers/applications).",
        "    - Click **'New Application'**. Name it for the role (e.g., `Ledgerflow PM Guardian`).",
        "    - **Set an app icon**: Upload a square image (preferably 512x512px PNG) that represents the role.",
        "    - **Set a banner image**: (optional, for branding) Recommended size: 960x540px PNG or JPG.",
        "    - In the left sidebar, click **'Bot'** → **'Add Bot'**.",
        "    - Click **'Reset Token'** to generate your bot token. **Copy and store this token securely.**",
        "2. **Bot Settings**",
        "    - **PUBLIC BOT**: Enable if you want others to add the bot to their servers. For most use cases, leave this checked.",
        "    - **REQUIRES OAUTH2 CODE GRANT**: Leave unchecked unless you need advanced OAuth2 flows.",
        "3. **Privileged Gateway Intents** (Bot tab)",
        "    - **PRESENCE INTENT**: Enable if your bot needs to see user presence (recommended: ON).",
        "    - **SERVER MEMBERS INTENT**: Enable if your bot needs to see member join/leave events (recommended: ON).",
        "    - **MESSAGE CONTENT INTENT**: Enable if your bot needs to read message content (recommended: ON).",
        "    - **Note**: If your bot is in 100+ servers, you may need to apply for verification for these intents.",
        "4. **Get Your Client ID**",
        "    - On the application's main page, copy the **Application (client) ID**.",
        "5. **(Optional) Get Your Guild (Server) ID**",
        "    - In Discord, enable **Developer Mode** (User Settings → Advanced).",
        "    - Right-click your server icon → **Copy Server ID**.",
        "6. **Invite the Bot to Your Server**",
        "    - Go to **OAuth2 → URL Generator** in the Developer Portal.",
        "    - Select scopes: `bot` and `applications.commands`.",
        "    - Select permissions your bot needs (e.g., `Send Messages`, `Read Messages`, etc.).",
        "    - Use the permissions calculator if needed: [Discord Permissions Calculator](https://discordapi.com/permissions.html)",
        "    - Copy the generated URL, open it in your browser, and invite the bot to your server.",
        "7. **Fill in Your Env File**",
        "    - For each role, add:",
        "      ```",
        "      <ROLE>_DISCORD_BOT_TOKEN=your-bot-token",
        "      <ROLE>_DISCORD_CLIENT_ID=your-client-id",
        "      <ROLE>_DISCORD_GUILD_ID=your-guild-id   # (optional)",
        "      ```",
        "    - Example for `PM_GUARDIAN`:",
        "      ```",
        "      PM_GUARDIAN_DISCORD_BOT_TOKEN=...",
        "      PM_GUARDIAN_DISCORD_CLIENT_ID=...",
        "      PM_GUARDIAN_DISCORD_GUILD_ID=...",
        "      ```",
        "",
        "## Session Management",
        "",
        "- Use `tools/team_cli.py create-session` to create individual sessions",
        "- Use `tools/team_cli.py create-crew --env-file teams/{project}/config/env` to create all sessions at once",
        "- Each session will have its own isolated environment with unique SSH keys",
        "",
        "## Troubleshooting",
        "",
        "- **Session Extraction Issues**: If team-cli isn't finding your sessions, check that your environment variables follow the pattern `ROLE_SLACK_TOKEN` (e.g., `PM_GUARDIAN_SLACK_TOKEN`).",
        "- **Missing Keys**: Ensure each role has all required tokens (Slack, GitHub, Discord) in the environment file.",
        "- **Role Directory Not Found**: The warning about falling back to python_coder is normal if you don't have a custom role directory. Create `roles/your_role_name/` for custom role configuration.",
        "",
        "For each role, create and configure a Discord bot as described above. This ensures every AI persona has its own Discord identity and can operate independently in your Discord server.",
    ]

    if dry_run:
        return None

    # Create config directory structure
    config_dir = Path(f"teams/{project}/config")
    config_dir.mkdir(parents=True, exist_ok=True)

    checklist_file = config_dir / "checklist.md"

    with open(checklist_file, "w") as f:
        f.write("\n".join(content))

    print(f"Created {checklist_file}")
    return checklist_file


def generate_slackbot_manifest(display_name):
    """
    Generate a Slackbot manifest JSON for the given role, using the correct Slack schema (features.bot_user).
    """
    return {
        "display_information": {"name": display_name},
        "settings": {
            "org_deploy_enabled": False,
            "socket_mode_enabled": False,
            "is_hosted": False,
            "token_rotation_enabled": False,
        },
        "features": {"bot_user": {"display_name": display_name, "always_online": True}},
        "oauth_config": {
            "scopes": {
                "bot": [
                    "app_mentions:read",
                    "channels:history",
                    "channels:join",
                    "channels:manage",
                    "channels:read",
                    "chat:write",
                    "groups:history",
                    "groups:read",
                    "im:history",
                    "im:read",
                    "im:write",
                    "mpim:history",
                    "mpim:read",
                    "users:read",
                    "users:read.email",
                    "users:write",
                    "files:read",
                    "files:write",
                ]
            }
        },
    }


def copy_cline_templates_and_rules(project, roles, dry_run=False):
    """
    For each role, copy Cline Memory Bank templates and .windsurfrules into the session payload directory.
    Also, copy the shared cline docs template to the team root (not into each session payload).
    """
    base_templates = Path("roles/_templates/cline_docs")
    shared_templates = Path("roles/_templates/cline_docs_shared")
    windsurfrules = Path("roles/_templates/.windsurfrules")
    restore_script = Path("roles/_templates/restore_payload.sh")

    # Copy shared cline docs to team root if not already present
    team_shared_dir = Path(f"teams/{project}/cline_docs_shared")
    if team_shared_dir.exists():
        shutil.rmtree(team_shared_dir)
    shutil.copytree(shared_templates, team_shared_dir)
    print(
        f"[INFO] Copied shared Cline docs template to {team_shared_dir}. Fill these out before running crew creation."
    )

    for role in roles:
        payload_dir = Path(f"teams/{project}/sessions/{role}/payload")
        # Copy per-role cline_docs
        role_cline_dir = payload_dir / "cline_docs"
        if role_cline_dir.exists():
            shutil.rmtree(role_cline_dir)
        shutil.copytree(base_templates, role_cline_dir)
        # Copy .windsurfrules and restore script
        shutil.copy2(windsurfrules, payload_dir / ".windsurfrules")
        shutil.copy2(restore_script, payload_dir / "restore_payload.sh")
        print(
            f"Populated {payload_dir} with Cline Memory Bank templates, .windsurfrules, and restore_payload.sh"
        )


def main():
    """
    Main function to run the scaffold_team.py script.

    The workflow is:
    1. Get configuration (from args, file, or interactive)
    2. Validate roles
    3. Generate env file, template, and checklist
    """
    args = parse_args()

    # Add support for --add-role flag
    add_role = None
    for i, arg in enumerate(sys.argv):
        if arg == "--add-role" and i + 1 < len(sys.argv):
            add_role = sys.argv[i + 1]
            break

    # Load from YAML file if provided
    if args.file:
        try:
            with open(args.file) as f:
                config = yaml.safe_load(f)

            project = config.get("project")
            prefix = config.get("prefix")
            domain = config.get("domain")
            roles = config.get("roles", DEFAULT_ROLES)
        except Exception as e:
            print(f"Error loading config file: {e}")
            sys.exit(1)

    # Interactive input if no args and no file
    elif not args.project and not args.prefix and not args.domain:
        project, prefix, domain, roles = interactive_input()

    # Use command-line args
    else:
        if not args.project or not args.prefix or not args.domain:
            print("Error: --project, --prefix, and --domain are required")
            sys.exit(1)

        project = args.project
        prefix = args.prefix
        domain = args.domain
        roles = args.roles.split(",") if args.roles else DEFAULT_ROLES

    config_dir = Path(f"teams/{project}/config")
    env_file = config_dir / "env"

    # --- Add Role Mode ---
    if add_role:
        # Only append the new role's config block
        valid_roles = get_valid_roles()
        if add_role not in valid_roles:
            print(
                f"Error: Role '{add_role}' not found in roles/. Valid roles: {', '.join(valid_roles)}"
            )
            sys.exit(1)
        if not env_file.exists():
            print(
                f"Error: {env_file} does not exist. Run scaffold_team.py normally first."
            )
            sys.exit(1)
        # Generate the config block for the new role
        role_upper = add_role.upper()
        role_id = add_role.lower()
        role_display = capitalize_first_letters(role_id)
        project_display = capitalize_first_letters(project)
        block = [
            f"# {role_display} Configuration",
            f"{role_upper}_EMAIL={prefix}+{project}-{role_id}@{domain}",
            f"{role_upper}_SLACK_TOKEN=  # Required: Bot token for this role",
            f"{role_upper}_GITHUB_TOKEN=  # Required: GitHub PAT for this role",
            f"{role_upper}_DISCORD_BOT_TOKEN=  # Required: Discord bot token for this role",
            f"{role_upper}_DISCORD_CLIENT_ID=  # Required: Discord client ID for this role",
            f"{role_upper}_DISCORD_GUILD_ID=  # Optional: Discord guild/server ID for this role",
            f"{role_upper}_BOT={project}_{role_id}_bot",
            f"{role_upper}_GITHUB={project}-{role_id}",
            f"{role_upper}_DISPLAY={project_display} {role_display}",
            "",
        ]
        with open(env_file, "a") as f:
            f.write("\n" + "\n".join(block))
        print(f"Appended config block for role '{add_role}' to {env_file}")
        return

    # --- Normal Mode ---
    # Warn if env file exists
    if env_file.exists():
        confirm = (
            input(f"Warning: {env_file} already exists. Overwrite? (y/n): ")
            .strip()
            .lower()
        )
        if confirm != "y":
            print("Aborted.")
            sys.exit(1)

    # Generate files
    try:
        env_file = generate_env_file(project, prefix, domain, roles, args.dry_run)
        env_template = generate_env_template(project, roles, args.dry_run)
        checklist = generate_checklist(project, roles, args.dry_run)

        # --- Cline Memory Bank and Windsurfrules propagation ---
        copy_cline_templates_and_rules(project, roles, args.dry_run)

        print("\nTeam configuration generated successfully!")
        print(f"Next steps:")
        print(f"1. Fill in API keys in {env_file}")
        print(f"2. Run 'python tools/team_cli.py create-crew --env-file {env_file}'")
        print(
            f"3. Follow the checklist at {checklist if not args.dry_run else 'teams/' + project + '/config/checklist.md'}"
        )

        # For each role, generate the Slackbot manifest in the config directory
        for role in roles:
            display_name = capitalize_first_letters(role)
            slackbot_manifest = generate_slackbot_manifest(display_name)
            with open(config_dir / f"slackbot_manifest_{role}.json", "w") as f:
                json.dump(slackbot_manifest, f, indent=2)

    except Exception as e:
        print(f"Error creating files: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
