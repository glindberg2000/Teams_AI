#!/usr/bin/env python3
"""
organize_repo.py - Repository reorganization script

This script helps reorganize the LedgerFlow AI Team repository according to
the proposed domain-centric directory structure.

Usage:
    python organize_repo.py --dry-run     # Show what would be done without making changes
    python organize_repo.py --execute     # Actually perform the reorganization

The script performs the following reorganization steps:
1. Move all .env.{project} files to teams/{project}/config/env
2. Move sessions to teams/{project}/sessions/{role}
3. Reorganize role templates and documentation
4. Centralize tools and templates
5. Update path references in code files

IMPORTANT: Make a backup of your repository before running with --execute!
"""
import argparse
import os
import re
import shutil
from pathlib import Path


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Reorganize the LedgerFlow AI Team repository"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    group.add_argument(
        "--execute", action="store_true", help="Actually perform the reorganization"
    )
    parser.add_argument(
        "--branch",
        action="store_true",
        help="Create a new git branch for the reorganization",
    )
    parser.add_argument(
        "--branch-name",
        default="repo-reorganization",
        help="Name of the git branch to create (default: repo-reorganization)",
    )
    return parser.parse_args()


def create_directory(path, dry_run=True):
    """Create a directory if it doesn't exist."""
    if not path.exists():
        if dry_run:
            print(f"Would create directory: {path}")
        else:
            print(f"Creating directory: {path}")
            path.mkdir(parents=True, exist_ok=True)
    return path


def move_file(src, dest, dry_run=True):
    """Move a file from src to dest."""
    if not src.exists():
        print(f"Source file does not exist: {src}")
        return False

    # Create parent directory if it doesn't exist
    create_directory(dest.parent, dry_run)

    if dry_run:
        print(f"Would move {src} to {dest}")
        return True
    else:
        print(f"Moving {src} to {dest}")
        try:
            shutil.copy2(src, dest)
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False


def create_git_branch(branch_name, dry_run=True):
    """Create a new git branch for the reorganization."""
    import subprocess

    if dry_run:
        print(f"Would create git branch: {branch_name}")
        return True

    try:
        # Check if the branch already exists
        result = subprocess.run(
            ["git", "branch", "--list", branch_name],
            capture_output=True,
            text=True,
            check=True,
        )
        if branch_name in result.stdout:
            print(f"Branch {branch_name} already exists. Using existing branch.")
            subprocess.run(["git", "checkout", branch_name], check=True)
            return True

        # Create and checkout the new branch
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        print(f"Created and checked out new branch: {branch_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating git branch: {e}")
        return False


def organize_env_files(dry_run=True):
    """Move .env.{project} files to teams/{project}/config/env."""
    root = Path(".")
    env_pattern = re.compile(r"^\.env\.(.+)$")

    # Find all .env.{project} files
    env_files = []
    for item in root.iterdir():
        if item.is_file():
            match = env_pattern.match(item.name)
            if match:
                project = match.group(1)
                env_files.append((item, project))

    # Move each .env.{project} file to teams/{project}/config/env
    for env_file, project in env_files:
        dest_path = Path(f"teams/{project}/config/env")
        move_file(env_file, dest_path, dry_run)

    # Move existing team checklists
    teams_dir = Path("teams")
    if teams_dir.exists():
        for team_dir in teams_dir.iterdir():
            if team_dir.is_dir() and team_dir.name != "_templates":
                checklist = team_dir / "checklist.md"
                env_template = team_dir / "env.template"

                if checklist.exists():
                    config_dir = Path(f"teams/{team_dir.name}/config")
                    move_file(checklist, config_dir / "checklist.md", dry_run)

                if env_template.exists():
                    config_dir = Path(f"teams/{team_dir.name}/config")
                    move_file(env_template, config_dir / "env.template", dry_run)


def organize_roles(dry_run=True):
    """Reorganize role templates and documentation."""
    roles_dir = Path("roles")
    if not roles_dir.exists():
        print("Roles directory does not exist.")
        return

    # Create templates directory inside roles
    roles_templates_dir = create_directory(Path("roles/_templates"), dry_run)

    # Move shared role templates
    if Path("teams/_templates").exists():
        for template in Path("teams/_templates").iterdir():
            if template.is_file():
                move_file(template, roles_templates_dir / template.name, dry_run)


def organize_sessions(dry_run=True):
    """Move sessions to teams/{project}/sessions/{role}."""
    sessions_dir = Path("sessions")
    if not sessions_dir.exists():
        print("Sessions directory does not exist.")
        return

    # Keep track of session types to organize by team
    for project_dir in sessions_dir.iterdir():
        if project_dir.is_dir() and project_dir.name != "_shared":
            # For each project directory, create a team directory and sessions subdirectory
            team_sessions_dir = create_directory(
                Path(f"teams/{project_dir.name}/sessions"), dry_run
            )

            # Move each agent session to the team's sessions directory
            for agent_dir in project_dir.iterdir():
                if agent_dir.is_dir():
                    dest_dir = team_sessions_dir / agent_dir.name
                    if dry_run:
                        print(f"Would move session {agent_dir} to {dest_dir}")
                    else:
                        print(f"Moving session {agent_dir} to {dest_dir}")
                        if not dest_dir.exists():
                            shutil.copytree(agent_dir, dest_dir)

    # Handle _shared directory - keep it at the top level of teams
    shared_dir = sessions_dir / "_shared"
    if shared_dir.exists():
        teams_shared_dir = create_directory(Path("teams/_shared"), dry_run)
        if dry_run:
            print(f"Would move shared resources {shared_dir} to {teams_shared_dir}")
        else:
            print(f"Moving shared resources {shared_dir} to {teams_shared_dir}")
            for item in shared_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, teams_shared_dir / item.name)


def organize_tools(dry_run=True):
    """Move tools to tools/ directory."""
    tools_dir = create_directory(Path("tools"), dry_run)

    # Move scaffold_team.py
    move_file(Path("scaffold_team.py"), tools_dir / "scaffold_team.py", dry_run)

    # Move team_cli.py
    team_cli_path = Path("team-cli/team_cli.py")
    if team_cli_path.exists():
        move_file(team_cli_path, tools_dir / "team_cli.py", dry_run)

    # Create utils directory and move utility scripts
    utils_dir = create_directory(tools_dir / "utils", dry_run)
    scripts_dir = Path("scripts")
    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if script.is_file() and script.suffix == ".sh":
                move_file(script, utils_dir / script.name, dry_run)


def organize_templates(dry_run=True):
    """Create templates directory structure."""
    templates_dir = create_directory(Path("templates"), dry_run)

    # Move .devcontainer to templates/devcontainer
    devcontainer_dir = Path(".devcontainer")
    if devcontainer_dir.exists():
        dest_dir = templates_dir / "devcontainer"
        if dry_run:
            print(f"Would move .devcontainer to {dest_dir}")
        else:
            print(f"Moving .devcontainer to {dest_dir}")
            shutil.copytree(devcontainer_dir, dest_dir, dirs_exist_ok=True)

    # Create scripts directory
    scripts_dir = create_directory(templates_dir / "scripts", dry_run)


def update_readme(dry_run=True):
    """Update README.md with the new directory structure."""
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("Error: Could not find README.md")
        return False

    # Read the current README
    with open(readme_path, "r") as f:
        content = f.read()

    # Define the new directory structure to insert
    new_structure = """
## Directory Structure

```
LedgerFlow_AI_Team/
├── teams/                       # All team-related content in one place
│   ├── _templates/              # Shared templates for all teams
│   ├── _shared/                 # Shared resources across teams
│   ├── {team1}/                 # Everything for team1
│   │   ├── config/              # Team configuration
│   │   │   ├── env              # Environment file (was .env.team1)
│   │   │   ├── checklist.md     # Setup instructions
│   │   │   └── manifest.json    # Team composition details
│   │   └── sessions/            # Team sessions
│   │       ├── pm_guardian/     # Session for this role
│   │       └── python_coder/    # Session for this role
│   └── {team2}/                 # Another team's config and sessions
├── roles/                       # Role templates and documentation
│   ├── _templates/              # Shared templates for all roles
│   ├── pm_guardian/             # PM Guardian role definition
│   ├── python_coder/            # Python Coder role definition
│   └── reviewer/                # Reviewer role definition
├── docs/                        # Global documentation
│   ├── global/                  # Global docs for all teams
│   └── projects/                # Docs specific to projects
├── tools/                       # Command-line tools
│   ├── scaffold_team.py         # Team configuration generator
│   ├── team_cli.py              # Session management tool
│   └── utils/                   # Helper utilities
├── templates/                   # System-wide templates
│   ├── devcontainer/            # Base container configuration
│   └── scripts/                 # Helper scripts
├── README.md
└── pyproject.toml
```
"""

    # Find the existing structure section and replace it
    structure_pattern = re.compile(
        r"#+\s*Directory Structure\s*\n```[\s\S]*?```", re.MULTILINE
    )

    if re.search(structure_pattern, content):
        new_content = re.sub(
            structure_pattern,
            "## Directory Structure\n" + new_structure.strip(),
            content,
        )
    else:
        # If no structure section exists, add after the key features section
        features_pattern = re.compile(
            r"#+\s*Key Features\s*\n[\s\S]*?\n\n", re.MULTILINE
        )
        match = re.search(features_pattern, content)
        if match:
            insert_position = match.end()
            new_content = (
                content[:insert_position]
                + "## Directory Structure\n"
                + new_structure
                + "\n"
                + content[insert_position:]
            )
        else:
            # Fallback - add at the end
            new_content = content + "\n\n## Directory Structure\n" + new_structure

    # Update workflow section references
    new_content = (
        new_content.replace(".env.{project}", "teams/{project}/config/env")
        .replace("python scaffold_team.py", "python tools/scaffold_team.py")
        .replace("python team-cli/team_cli.py", "python tools/team_cli.py")
        .replace("teams/{project}/checklist.md", "teams/{project}/config/checklist.md")
        .replace("teams/{project}/env.template", "teams/{project}/config/env.template")
        .replace("sessions/{project}/", "teams/{project}/sessions/")
    )

    if dry_run:
        print("Would update README.md with new directory structure")
    else:
        print("Updating README.md with new directory structure")
        with open(readme_path, "w") as f:
            f.write(new_content)

    return True


def main():
    """Main function."""
    args = parse_args()
    dry_run = args.dry_run

    if dry_run:
        print("=== DRY RUN - No changes will be made ===")
    else:
        print("=== EXECUTING - Making changes to the repository ===")
        print("WARNING: This will reorganize your repository!")
        confirm = input("Continue? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Aborted.")
            return

    # Create git branch if requested
    if args.branch and not dry_run:
        if not create_git_branch(args.branch_name, dry_run):
            print("Failed to create git branch. Aborting.")
            return

    # Create base directories
    create_directory(Path("teams"), dry_run)
    create_directory(Path("roles"), dry_run)
    create_directory(Path("tools"), dry_run)
    create_directory(Path("templates"), dry_run)

    # Perform reorganization steps
    organize_env_files(dry_run)
    organize_roles(dry_run)
    organize_sessions(dry_run)
    organize_tools(dry_run)
    organize_templates(dry_run)
    update_readme(dry_run)

    # Update paths in code files
    from update_scaffold_team import update_paths

    update_paths(dry_run)

    if dry_run:
        print("\n=== DRY RUN COMPLETE ===")
        print("Run with --execute to make these changes.")
        print("Consider using --branch to create a git branch for these changes.")
    else:
        print("\n=== REORGANIZATION COMPLETE ===")
        print("Please review the changes and update any references in your code.")

        if args.branch:
            print(f"\nAll changes have been made in branch: {args.branch_name}")
            print("You can now test the changes and then merge the branch when ready.")


if __name__ == "__main__":
    main()
