#!/usr/bin/env python3
"""
fix_env_templates.py - Fix .env file generation in team_cli.py

This script patches the team_cli.py file to fix two issues:
1. Template variables like ${TEAM_NAME} are not being resolved
2. All roles' variables are included in each session's .env file

Usage:
    python fix_env_templates.py
"""
import re
from pathlib import Path
import shutil


def fix_team_cli():
    """
    Fix the team_cli.py file to properly handle .env templates
    """
    team_cli_path = Path("tools/team_cli.py")
    backup_path = Path("tools/team_cli.py.bak")

    if not team_cli_path.exists():
        print(f"Error: {team_cli_path} not found")
        return False

    # Create backup
    shutil.copy2(team_cli_path, backup_path)
    print(f"Created backup at {backup_path}")

    # Read the file
    with open(team_cli_path, "r") as f:
        lines = f.readlines()

    # Find the start of the .env handling section
    start_line = 0
    for i, line in enumerate(lines):
        if (
            "# --- .env Handling: Look for config in the new directory structure ---"
            in line
        ):
            start_line = i
            break

    if start_line == 0:
        print("Error: Could not find the .env handling section")
        return False

    # Find where to insert the template resolution code
    insert_line = 0
    for i in range(start_line, len(lines)):
        if "# Write the .env file with consistent formatting" in lines[i]:
            insert_line = i
            break

    if insert_line == 0:
        print("Error: Could not find where to insert the template resolution code")
        return False

    # Prepare the code to insert
    resolution_code = """
    # Resolve template variables in the env_vars values
    env_vars_resolved = {}
    for k, v in env_vars.items():
        if isinstance(v, str) and "${" in v:
            # Replace template variables with their values
            resolved_value = v
            # Extract variable names inside ${...}
            var_matches = re.findall(r"\\${([^}]+)}", v)
            for var_name in var_matches:
                # Try to get the value from env_vars
                replacement = env_vars.get(var_name, "")
                resolved_value = resolved_value.replace(f"${{{var_name}}}", replacement)
            env_vars_resolved[k] = resolved_value
        else:
            env_vars_resolved[k] = v

    # Filter out variables that don't belong to this session
    # Only include Task Master vars, shared vars, and vars for this specific role
    session_specific_vars = {}
    role_upper = name.upper()
    role_prefix_match = f"{role_upper}_"
    
    # Task Master variables - always include
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
    
    # Global variables that should be included for all sessions
    global_vars = [
        "GIT_USER_NAME",
        "GIT_USER_EMAIL",
        "SLACK_BOT_TOKEN",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "SLACK_WORKSPACE_ID",
        "SLACK_TEAM_ID",
        "GIT_SSH_KEY_PATH",
        "TEAM_NAME",
        "TEAM_DESCRIPTION", 
        "PROJECT_NAME",
    ]
    
    for k, v in env_vars_resolved.items():
        # Include Task Master variables
        if k in task_master_vars:
            session_specific_vars[k] = v
        # Include global variables
        elif k in global_vars:
            session_specific_vars[k] = v
        # Include variables specific to this role
        elif k.startswith(role_prefix_match):
            session_specific_vars[k] = v
        # Skip all other role-specific variables
        elif any(k.startswith(f"{r.upper()}_") for r in ["PM_GUARDIAN", "PYTHON_CODER", "REVIEWER", "DB_GUARDIAN", "FULL_STACK_DEV"]):
            continue
        # Include other variables that aren't role-specific
        else:
            session_specific_vars[k] = v
"""

    # Insert the code
    lines.insert(insert_line, resolution_code)

    # Update the lines that write to the .env file
    for i in range(insert_line, len(lines)):
        if "for k in task_master_vars:" in lines[i]:
            lines[i] = "    for k in task_master_vars:\n"
        elif "if k in env_vars:" in lines[i]:
            lines[i] = "        if k in session_specific_vars:\n"
        elif 'f.write(f"{k}={env_vars[k]}\\n")' in lines[i]:
            lines[i] = '            f.write(f"{k}={session_specific_vars[k]}\\n")\n'
        elif "for k, v in env_vars.items():" in lines[i]:
            lines[i] = "    for k, v in session_specific_vars.items():\n"

    # Add the import for re if needed
    for i, line in enumerate(lines):
        if "import re" in line:
            break
    else:
        # Insert import
        for i, line in enumerate(lines):
            if "import json" in line:
                lines.insert(i, "import re\n")
                break

    # Update create_crew function to pass TEAM_NAME and related variables
    crew_found = False
    for i, line in enumerate(lines):
        if "all_env=[" in line and "session_args = argparse.Namespace(" in lines[i - 1]:
            crew_found = True
            # Find the end of the all_env list
            for j in range(i + 1, len(lines)):
                if "]," in lines[j]:
                    # Insert TEAM_NAME and related variables at the beginning of the list
                    team_vars = [
                        '                f"TEAM_NAME={project_name}",\n',
                        "                f\"TEAM_DESCRIPTION={team_env.get('TEAM_DESCRIPTION', project_name + ' team')}\",\n",
                        '                f"PROJECT_NAME={project_name}",\n',
                    ]
                    for idx, var in enumerate(team_vars):
                        lines.insert(i + 1 + idx, var)
                    break
            break

    if not crew_found:
        print(
            "Warning: Could not find where to insert team variables in create_crew function"
        )

    # Write the file back
    with open(team_cli_path, "w") as f:
        f.writelines(lines)

    print(f"Updated {team_cli_path} with fixes for .env template handling")
    return True


def main():
    """Main function"""
    print("Fixing team_cli.py for proper .env file generation...")
    if fix_team_cli():
        print("Fix applied successfully.")
        print("Next steps:")
        print(
            "1. Test the fix by creating a new team: python tools/team_cli.py create-crew --env-file teams/test-e2e/config/env"
        )
        print("2. Verify that the .env files are correct")
    else:
        print("Failed to apply fix.")


if __name__ == "__main__":
    main()
