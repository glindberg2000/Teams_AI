"""
team_scaffold_shared.py

Shared logic for team, session, and container generation.
This module is the single source of truth for all team scaffolding and session/container provisioning logic.
It is designed to be imported by both the backend (FastAPI/UI) and CLI tools.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import shutil
import json


# --- Team Scaffolding ---
def scaffold_team_from_template(
    template_path: Path, team_name: str, output_dir: Path
) -> None:
    """
    Scaffold a new team directory from a template JSON file.
    Args:
        template_path: Path to the team template JSON file.
        team_name: Name for the new team.
        output_dir: Directory where the team should be created (usually teams/).
    Raises:
        FileNotFoundError: If the template file does not exist.
        ValueError: If the template is invalid.
    """
    pass


# --- Session/Container Generation ---
def generate_sessions_from_config(
    team_dir: Path, config: Dict[str, Any], env: Dict[str, str]
) -> None:
    """
    Generate all session/container directories and files for a team based on config and env.
    Args:
        team_dir: Path to the team directory (teams/<team>/).
        config: Parsed config.json for the team.
        env: Environment variables for the team/roles.
    Raises:
        ValueError: If config or env is invalid.
    """
    pass


# --- Naming/Normalization Utilities ---
def normalize_team_name(name: str) -> str:
    """
    Normalize a team name to a safe directory name (lowercase, dashes for spaces, alphanum only).
    Args:
        name: Raw team name
    Returns:
        Normalized team name string
    """
    import re

    return re.sub(r"[^a-z0-9_-]", "", name.lower().replace(" ", "-"))


def normalize_role_name(name: str) -> str:
    """
    Normalize a role name to a safe directory name.
    Args:
        name: Raw role name.
    Returns:
        Normalized role name string.
    """
    pass


# --- Additional Utilities ---
def parse_env_file(env_path: Path) -> Dict[str, str]:
    """
    Parse a .env or env.template file into a dictionary.
    Args:
        env_path: Path to the env file.
    Returns:
        Dictionary of environment variables.
    Raises:
        FileNotFoundError: If the env file does not exist.
    """
    pass


def parse_config_json(config_path: Path) -> Dict[str, Any]:
    """
    Parse a config.json file into a dictionary.
    Args:
        config_path: Path to the config.json file.
    Returns:
        Dictionary of config values.
    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If the config file is invalid JSON.
    """
    pass


# --- Utility Functions ---
def capitalize_first_letters(s: str) -> str:
    """
    Capitalize the first letter of each word in a string.
    Args:
        s: Input string, typically underscore-separated
    Returns:
        String with first letter of each word capitalized
    """
    return " ".join(word.capitalize() for word in s.split("_"))


def generate_env_file(
    project: str, prefix: str, domain: str, roles: List[str], config_dir: Path
) -> Path:
    """
    Generate the environment file (config/env) with all required configuration.
    Args:
        project: Project name
        prefix: Email prefix/username
        domain: Email domain
        roles: List of roles to configure
        config_dir: Path to the config directory (teams/<project>/config)
    Returns:
        Path to the generated environment file
    """
    content = [
        f"# Environment configuration for {project} team",
        "# WARNING: Never commit this file to git!",
        "# Store a copy in your secure storage (iCloud, 1Password, etc.)",
        "",
        "# Team Configuration",
        f"TEAM_NAME={project}",
        f"TEAM_ID={normalize_team_name(project)}",
        f"TEAM_DESCRIPTION={project} team",
        f"PROJECT_NAME={project}",
        f"EMAIL_PREFIX={prefix}",
        "",
        "# Project and Integration Repos",
        "PROJECT_REPO_URL=  # Required: Main project repo URL (e.g. https://github.com/yourorg/yourproject.git)",
        "MCP_DISCORD_REPO_URL=  # Required: Discord MCP repo URL (e.g. https://github.com/netixc/mcp-discord.git)",
        "MCP_DISCORD_REPO_BRANCH=main  # Optional: Branch to clone for Discord MCP (default: main)",
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
    for role in roles:
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
                f"{role_upper}_DISCORD_TOKEN=  # Required: Discord bot token for this role",
                f"{role_upper}_DISCORD_CLIENT_ID=  # Required: Discord client ID for this role",
                f"{role_upper}_DISCORD_GUILD_ID=  # Optional: Discord guild/server ID for this role",
                f"{role_upper}_BOT={project}_{role_id}_bot",
                f"{role_upper}_GITHUB={role_github}",
                f"{role_upper}_DISPLAY={role_display_var}",
                "",
            ]
        )
    config_dir.mkdir(parents=True, exist_ok=True)
    env_file = config_dir / "env"
    with open(env_file, "w") as f:
        f.write("\n".join(content))
    return env_file


def generate_env_template(project: str, roles: List[str], config_dir: Path) -> Path:
    """
    Generate the environment template for reference (config/env.template).
    Args:
        project: Project name
        roles: List of roles to configure
        config_dir: Path to the config directory (teams/<project>/config)
    Returns:
        Path to the generated template file
    """
    content = [
        "# Team Configuration",
        "TEAM_NAME=${TEAM_NAME}",
        "TEAM_ID=${TEAM_ID}",
        "TEAM_DESCRIPTION=${TEAM_DESCRIPTION}",
        "",
        "# Project and Integration Repos",
        "PROJECT_REPO_URL=${PROJECT_REPO_URL}",
        "MCP_DISCORD_REPO_URL=${MCP_DISCORD_REPO_URL}",
        "MCP_DISCORD_REPO_BRANCH=main  # Optional: Branch to clone for Discord MCP (default: main)",
        "",
    ]
    for role in roles:
        role_upper = role.upper()
        role_id = role.lower()
        role_display = capitalize_first_letters(role_id)
        content.extend(
            [
                f"# {role_display} Configuration",
                f"{role_upper}_EMAIL=${{EMAIL_PREFIX}}+${{TEAM_NAME}}-{role_id}@${{DOMAIN}}",
                f"{role_upper}_SLACK_TOKEN=  # Required: Bot token for this role",
                f"{role_upper}_GITHUB_TOKEN=  # Required: GitHub PAT for this role",
                f"{role_upper}_DISCORD_TOKEN=  # Required: Discord bot token for this role",
                f"{role_upper}_DISCORD_CLIENT_ID=  # Required: Discord client ID for this role",
                f"{role_upper}_DISCORD_GUILD_ID=  # Optional: Discord guild/server ID for this role",
                f"{role_upper}_BOT=${{TEAM_NAME}}_{role_id}_bot",
                f"{role_upper}_GITHUB=${{TEAM_NAME}}-{role_id}",
                f"{role_upper}_DISPLAY=${{TEAM_NAME_CAP}} {role_display}",
                "",
            ]
        )
    config_dir.mkdir(parents=True, exist_ok=True)
    env_template_file = config_dir / "env.template"
    with open(env_template_file, "w") as f:
        f.write("\n".join(content))
    return env_template_file


def generate_checklist(project: str, roles: List[str], config_dir: Path) -> Path:
    """
    Generate the setup checklist for the team (config/checklist.md).
    Args:
        project: Project name
        roles: List of roles to configure
        config_dir: Path to the config directory (teams/<project>/config)
    Returns:
        Path to the generated checklist file
    """
    content = [
        f"# {project} Team Setup Checklist",
        "",
        "## Required Repositories",
        "- [ ] **PROJECT_REPO_URL**: Main project repo URL (e.g. https://github.com/yourorg/yourproject.git)",
        "- [ ] **MCP_DISCORD_REPO_URL**: Discord MCP repo URL (e.g. https://github.com/netixc/mcp-discord.git)",
        "- [ ] **MCP_DISCORD_REPO_BRANCH**: Branch to clone for Discord MCP (default: main)",
        "",
        "## Core Setup",
        "",
        f"- [ ] Clone the LedgerFlow AI Team repository",
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
        "- [ ] **PM_GUARDIAN_DISCORD_TOKEN**: Unique Discord bot token for this role",
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
        "2. **Bot Settings**",
        "    - In the left sidebar, click **'Bot'** → **'Add Bot'**.",
        "    - Click **'Reset Token'** to generate your bot token. **Copy and store this token securely.**",
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
        "      <ROLE>_DISCORD_TOKEN=your-bot-token",
        "      <ROLE>_DISCORD_CLIENT_ID=your-client-id",
        "      <ROLE>_DISCORD_GUILD_ID=your-guild-id   # (optional)",
        "      ```",
        "    - Example for `PM_GUARDIAN`:",
        "      ```",
        "      PM_GUARDIAN_DISCORD_TOKEN=...",
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
    config_dir.mkdir(parents=True, exist_ok=True)
    checklist_file = config_dir / "checklist.md"
    with open(checklist_file, "w") as f:
        f.write("\n".join(content))
    return checklist_file


def copy_cline_templates_and_rules(
    project: str, roles: List[str], team_root: Path
) -> None:
    """
    For each role, copy Cline Memory Bank templates and .windsurfrules into the session payload directory.
    Also, copy the shared cline docs template to the team root (not into each session payload).
    Args:
        project: Project name
        roles: List of roles
        team_root: Path to the team root (teams/<project>/)
    """
    base_templates = team_root.parent.parent / "roles" / "_templates" / "cline_docs"
    shared_templates = (
        team_root.parent.parent / "roles" / "_templates" / "cline_docs_shared"
    )
    windsurfrules = team_root.parent.parent / "roles" / "_templates" / ".windsurfrules"
    windsurf_rules_src = (
        team_root.parent.parent / "roles" / "_templates" / ".windsurf" / "rules"
    )
    # Copy shared cline docs to team root
    team_shared_dir = team_root / "cline_docs_shared"
    if team_shared_dir.exists():
        shutil.rmtree(team_shared_dir)
    shutil.copytree(shared_templates, team_shared_dir)
    for role in roles:
        payload_dir = team_root / "sessions" / role / "payload"
        role_cline_dir = payload_dir / "cline_docs"
        if role_cline_dir.exists():
            shutil.rmtree(role_cline_dir)
        shutil.copytree(base_templates, role_cline_dir)
        shutil.copy2(windsurfrules, payload_dir / ".windsurfrules")
        windsurf_rules_dst = payload_dir / ".windsurf" / "rules"
        if windsurf_rules_dst.exists():
            shutil.rmtree(windsurf_rules_dst)
        shutil.copytree(windsurf_rules_src, windsurf_rules_dst)


def sync_cline_docs_shared_to_sessions(team_root: Path) -> None:
    """
    Sync all files from team_root/cline_docs_shared/ to each session's payload/cline_docs_shared/.
    Overwrites existing files as needed.
    """
    shared_dir = team_root / "cline_docs_shared"
    sessions_dir = team_root / "sessions"
    if not shared_dir.exists() or not sessions_dir.exists():
        return
    for session in sessions_dir.iterdir():
        payload_dir = session / "payload" / "cline_docs_shared"
        if not payload_dir.exists():
            payload_dir.mkdir(parents=True, exist_ok=True)
        # Remove all existing files in payload_dir
        for f in payload_dir.glob("*.md"):
            f.unlink()
        # Copy all shared docs
        for f in shared_dir.glob("*.md"):
            target = payload_dir / f.name
            target.write_text(f.read_text())
