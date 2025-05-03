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

# Constants
DEFAULT_ROLES = ["pm_guardian", "python_coder", "reviewer"]
VALID_ROLES = [
    "pm_guardian",
    "python_coder",
    "full_stack_dev",
    "db_guardian",
    "reviewer",
]


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


def validate_roles(roles):
    """
    Validate roles against the list of valid roles.

    Args:
        roles (list): List of role names to validate

    Returns:
        bool: True if all roles are valid, False otherwise
    """
    invalid_roles = [r for r in roles if r not in VALID_ROLES]
    if invalid_roles:
        print(f"Warning: Invalid roles: {', '.join(invalid_roles)}")
        print(f"Valid roles are: {', '.join(VALID_ROLES)}")
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
        f"LEDGERFLOW_EMAIL_PREFIX={prefix}",
        "",
        "# Documentation Configuration",
        "INCLUDE_GLOBAL_DOCS=true",
        "INCLUDE_PROJECT_DOCS=true",
        "INCLUDE_ROLE_DOCS=true",
        "",
        "# Required API Keys and Tokens",
        "ANTHROPIC_API_KEY=  # Required: Get from https://console.anthropic.com",
        "PERPLEXITY_API_KEY=  # Optional: Get from https://perplexity.ai",
        "GITHUB_PERSONAL_ACCESS_TOKEN=  # Required: Create at https://github.com/settings/tokens",
        "SLACK_BOT_TOKEN=  # Required: Create at https://api.slack.com/apps",
        "SLACK_TEAM_ID=  # Required: Get from Slack workspace settings",
        "SLACK_WORKSPACE_ID=  # Same as SLACK_TEAM_ID",
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
        "# Git Configuration",
        f'GIT_USER_NAME="{prefix}"',
        f'GIT_USER_EMAIL="{prefix}+{project}@{domain}"',
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

        content.extend(
            [
                f"# {role_display} Configuration",
                f"{role_upper}_EMAIL={prefix}+{project}-{role_id}@{domain}",
                f"{role_upper}_SLACK_TOKEN=  # Required: Bot token for this role",
                f"{role_upper}_GITHUB_TOKEN=  # Required: GitHub PAT for this role",
                f"{role_upper}_BOT={project}_{role_id}_bot",
                f"{role_upper}_GITHUB={project}-{role_id}",
                f"{role_upper}_DISPLAY={project_display} {role_display}",
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
                f"{role_upper}_EMAIL=${{LEDGERFLOW_EMAIL_PREFIX}}+${{TEAM_NAME}}-{role_id}@${{DOMAIN}}",
                f"{role_upper}_SLACK_TOKEN=  # Required: Bot token for this role",
                f"{role_upper}_GITHUB_TOKEN=  # Required: GitHub PAT for this role",
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
    ]

    for role in roles:
        role_upper = role.upper()
        role_id = role.lower()
        role_display = capitalize_first_letters(role_id)

        content.extend(
            [
                f"#### {role_display}",
                "",
                f"- [ ] **{role_upper}_SLACK_TOKEN**: Unique Slack bot token for this role",
                f"- [ ] **{role_upper}_GITHUB_TOKEN**: Unique GitHub PAT for this role",
                "",
            ]
        )

    content.extend(
        [
            "## Session Management",
            "",
            "- Use `tools/team_cli.py create-session` to create individual sessions",
            f"- Use `tools/team_cli.py create-crew --env-file teams/{project}/config/env` to create all sessions at once",
            "- Each session will have its own isolated environment with unique SSH keys",
            "",
            "## Troubleshooting",
            "",
            "- **Session Extraction Issues**: If team-cli isn't finding your sessions, check that your environment variables follow the pattern `ROLE_SLACK_TOKEN` (e.g., `PM_GUARDIAN_SLACK_TOKEN`).",
            "- **Missing Keys**: Ensure each role has all required tokens (Slack, GitHub) in the environment file.",
            "- **Role Directory Not Found**: The warning about falling back to python_coder is normal if you don't have a custom role directory. Create `roles/your_role_name/` for custom role configuration.",
        ]
    )

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


def main():
    """
    Main function to run the scaffold_team.py script.

    The workflow is:
    1. Get configuration (from args, file, or interactive)
    2. Validate roles
    3. Generate env file, template, and checklist
    """
    args = parse_args()

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

    # Validate roles
    if not validate_roles(roles):
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != "y":
            sys.exit(1)

    try:
        # Generate files
        env_file = generate_env_file(project, prefix, domain, roles, args.dry_run)
        env_template = generate_env_template(project, roles, args.dry_run)
        checklist = generate_checklist(project, roles, args.dry_run)

        print("\nTeam configuration generated successfully!")
        print(f"Next steps:")
        print(f"1. Fill in API keys in {env_file}")
        print(f"2. Run 'python tools/team_cli.py create-crew --env-file {env_file}'")
        print(
            f"3. Follow the checklist at {checklist if not args.dry_run else 'teams/' + project + '/config/checklist.md'}"
        )

    except Exception as e:
        print(f"Error creating files: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
