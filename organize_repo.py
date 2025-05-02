#!/usr/bin/env python3
"""
organize_repo.py - Repository reorganization script

This script helps reorganize the LedgerFlow AI Team repository according to
the proposed directory structure.

Usage:
    python organize_repo.py --dry-run     # Show what would be done without making changes
    python organize_repo.py --execute     # Actually perform the reorganization

The script performs the following reorganization steps:
1. Move all .env.{project} files to teams/{project}/env
2. Move role templates to config/roles/
3. Create a more organized session structure
4. Centralize documentation
5. Move tools to tools/ directory

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


def organize_env_files(dry_run=True):
    """Move .env.{project} files to teams/{project}/env."""
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

    # Move each .env.{project} file to teams/{project}/env
    for env_file, project in env_files:
        dest_path = Path(f"teams/{project}/env")
        move_file(env_file, dest_path, dry_run)


def organize_roles(dry_run=True):
    """Move role templates to config/roles/."""
    roles_dir = Path("roles")
    if not roles_dir.exists():
        print("Roles directory does not exist.")
        return

    config_roles_dir = create_directory(Path("config/roles"), dry_run)

    # Move each role to config/roles/
    for role_dir in roles_dir.iterdir():
        if role_dir.is_dir():
            dest_dir = config_roles_dir / role_dir.name
            if dry_run:
                print(f"Would move role {role_dir} to {dest_dir}")
            else:
                print(f"Moving role {role_dir} to {dest_dir}")
                shutil.copytree(role_dir, dest_dir, dirs_exist_ok=True)


def organize_sessions(dry_run=True):
    """Create a more organized session structure."""
    sessions_dir = Path("sessions")
    if not sessions_dir.exists():
        print("Sessions directory does not exist.")
        return

    # Create active and archive directories
    active_dir = create_directory(sessions_dir / "active", dry_run)
    archive_dir = create_directory(sessions_dir / "archive", dry_run)

    # Move project sessions to active directory
    for item in sessions_dir.iterdir():
        if (
            item.is_dir()
            and item.name != "_shared"
            and item.name != "active"
            and item.name != "archive"
        ):
            dest_dir = active_dir / item.name
            if dry_run:
                print(f"Would move session project {item} to {dest_dir}")
            else:
                print(f"Moving session project {item} to {dest_dir}")
                shutil.copytree(item, dest_dir, dirs_exist_ok=True)


def centralize_docs(dry_run=True):
    """Centralize documentation."""
    # Move role docs to docs/roles/
    roles_docs_dir = create_directory(Path("docs/roles"), dry_run)
    roles_dir = Path("roles")

    if roles_dir.exists():
        for role_dir in roles_dir.iterdir():
            if role_dir.is_dir():
                role_docs_dir = role_dir / "docs"
                if role_docs_dir.exists():
                    dest_dir = roles_docs_dir / role_dir.name
                    if dry_run:
                        print(f"Would move role docs {role_docs_dir} to {dest_dir}")
                    else:
                        print(f"Moving role docs {role_docs_dir} to {dest_dir}")
                        shutil.copytree(role_docs_dir, dest_dir, dirs_exist_ok=True)


def organize_tools(dry_run=True):
    """Move tools to tools/ directory."""
    tools_dir = create_directory(Path("tools"), dry_run)

    # Move scaffold_team.py
    move_file(Path("scaffold_team.py"), tools_dir / "scaffold_team.py", dry_run)

    # Create team-cli directory and move team_cli.py
    team_cli_dir = create_directory(tools_dir / "team-cli", dry_run)
    move_file(Path("team-cli/team_cli.py"), team_cli_dir / "team_cli.py", dry_run)

    # Move utility scripts
    utils_dir = create_directory(tools_dir / "utils", dry_run)
    scripts_dir = Path("scripts")
    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if script.is_file() and script.suffix == ".sh":
                move_file(script, utils_dir / script.name, dry_run)


def create_templates(dry_run=True):
    """Create template directories."""
    templates_dir = create_directory(Path("templates"), dry_run)

    # Move .devcontainer to templates
    devcontainer_dir = Path(".devcontainer")
    if devcontainer_dir.exists():
        dest_dir = templates_dir / ".devcontainer"
        if dry_run:
            print(f"Would copy .devcontainer to {dest_dir}")
        else:
            print(f"Copying .devcontainer to {dest_dir}")
            shutil.copytree(devcontainer_dir, dest_dir, dirs_exist_ok=True)

    # Create scripts directory
    scripts_dir = create_directory(templates_dir / "scripts", dry_run)


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

    # Create base directories
    create_directory(Path("config"), dry_run)
    create_directory(Path("tools"), dry_run)
    create_directory(Path("templates"), dry_run)

    # Perform reorganization steps
    organize_env_files(dry_run)
    organize_roles(dry_run)
    organize_sessions(dry_run)
    centralize_docs(dry_run)
    organize_tools(dry_run)
    create_templates(dry_run)

    if dry_run:
        print("\n=== DRY RUN COMPLETE ===")
        print("Run with --execute to make these changes.")
    else:
        print("\n=== REORGANIZATION COMPLETE ===")
        print("Please review the changes and update any references in your code.")


if __name__ == "__main__":
    main()
