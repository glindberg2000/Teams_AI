#!/usr/bin/env python3
"""
fix_env_files.py - Fix existing .env files in session payloads

This script finds and fixes .env files in all sessions to:
1. Resolve template variables like ${TEAM_NAME}
2. Remove variables that don't belong to the specific role

Usage:
    python fix_env_files.py [project]

Arguments:
    project - Optional project name. If not specified, all projects are processed.
"""
import os
import re
import sys
from pathlib import Path
import json


def fix_env_files(project=None):
    """Fix .env files in session payloads"""
    teams_dir = Path("teams")
    if not teams_dir.exists():
        print(f"Error: {teams_dir} not found")
        return False

    processed = 0
    errors = 0

    # Process all projects or just the specified one
    projects = (
        [project] if project else [p.name for p in teams_dir.iterdir() if p.is_dir()]
    )

    for project_name in projects:
        project_dir = teams_dir / project_name
        if not project_dir.exists():
            print(f"Error: Project {project_name} not found")
            continue

        # Load the main env file for the project
        env_file = project_dir / "config" / "env"
        if not env_file.exists():
            print(f"Warning: No env file found for project {project_name}")
            continue

        # Parse the main env file to get all variables
        all_vars = {}
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.strip().startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    all_vars[key.strip()] = value.strip()

        # Process each session
        sessions_dir = project_dir / "sessions"
        if not sessions_dir.exists():
            print(f"Warning: No sessions directory for project {project_name}")
            continue

        for session in sessions_dir.iterdir():
            if not session.is_dir():
                continue

            # Get the role name
            role = session.name.upper()

            # Find .env file in payload
            env_path = session / "payload" / ".env"
            if not env_path.exists():
                print(f"Warning: No .env file found for session {session.name}")
                continue

            try:
                # Read the current .env file
                with open(env_path, "r") as f:
                    env_content = f.read()

                # Resolve template variables
                for var_name, var_value in all_vars.items():
                    placeholder = f"${{{var_name}}}"
                    if placeholder in env_content:
                        env_content = env_content.replace(placeholder, var_value)

                # Handle special variables that may not be in all_vars
                if "${DOMAIN}" in env_content:
                    domain = all_vars.get("DOMAIN", "example.com")
                    env_content = env_content.replace("${DOMAIN}", domain)

                if "${TEAM_NAME_CAP}" in env_content:
                    team_name = all_vars.get("TEAM_NAME", "")
                    team_name_cap = team_name.replace("-", " ").title()
                    env_content = env_content.replace("${TEAM_NAME_CAP}", team_name_cap)

                if "${LEDGERFLOW_EMAIL_PREFIX}" in env_content:
                    email_prefix = all_vars.get("LEDGERFLOW_EMAIL_PREFIX", "test")
                    env_content = env_content.replace(
                        "${LEDGERFLOW_EMAIL_PREFIX}", email_prefix
                    )

                # Parse the fixed content into lines
                lines = []
                for line in env_content.splitlines():
                    if not line.strip() or line.strip().startswith("#"):
                        lines.append(line)
                        continue

                    if "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()

                        # Skip variables specific to other roles
                        known_roles = [
                            "PM_GUARDIAN",
                            "PYTHON_CODER",
                            "REVIEWER",
                            "DB_GUARDIAN",
                            "FULL_STACK_DEV",
                        ]
                        if any(
                            key.startswith(f"{r}_") for r in known_roles if r != role
                        ):
                            continue

                        lines.append(line)

                # Write the fixed .env file
                with open(env_path, "w") as f:
                    f.write("\n".join(lines))

                # Fix MCP config file if it exists
                mcp_config_path = session / "payload" / "mcp_config.json"
                if mcp_config_path.exists():
                    try:
                        with open(mcp_config_path, "r") as f:
                            mcp_config = json.load(f)

                        # Clean up token values by removing comments
                        for server_name, server_config in mcp_config.get(
                            "mcpServers", {}
                        ).items():
                            if "env" in server_config:
                                for key, value in server_config["env"].items():
                                    if isinstance(value, str) and "#" in value:
                                        # Remove comments from token values
                                        server_config["env"][key] = value.split("#")[
                                            0
                                        ].strip()

                        # Write the fixed MCP config
                        with open(mcp_config_path, "w") as f:
                            json.dump(mcp_config, f, indent=2)

                        print(f"Fixed MCP config for {project_name}/{session.name}")
                    except Exception as e:
                        print(
                            f"Error fixing MCP config for {project_name}/{session.name}: {e}"
                        )
                        errors += 1

                print(f"Fixed .env file for {project_name}/{session.name}")
                processed += 1
            except Exception as e:
                print(f"Error fixing .env file for {project_name}/{session.name}: {e}")
                errors += 1

    print(f"\nProcessed {processed} .env files, encountered {errors} errors")
    return errors == 0


def main():
    """Main function"""
    project = sys.argv[1] if len(sys.argv) > 1 else None

    print(
        f"Fixing .env files in {'all projects' if project is None else f'project {project}'}"
    )
    success = fix_env_files(project)

    if success:
        print("All .env files processed successfully.")
    else:
        print("Errors encountered during processing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
