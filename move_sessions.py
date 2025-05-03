#!/usr/bin/env python3
"""
move_sessions.py - Move session directories to new directory structure

This script moves all existing sessions/{project}/{agent} directories to
teams/{project}/sessions/{agent} as part of the repository reorganization.

Usage:
    python move_sessions.py --dry-run     # Show what would be done without making changes
    python move_sessions.py --execute     # Actually move the directories
"""
import argparse
import os
import shutil
from pathlib import Path


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Move session directories to new directory structure"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    group.add_argument(
        "--execute", action="store_true", help="Actually move the directories"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed information about moved directories",
    )
    return parser.parse_args()


def move_sessions(dry_run=True, verbose=False):
    """Move sessions/{project}/{agent} directories to teams/{project}/sessions/{agent}."""
    sessions_dir = Path("sessions")
    if not sessions_dir.exists():
        print("No sessions directory found. Nothing to move.")
        return 0

    projects_moved = 0
    sessions_moved = 0

    # Iterate through all project directories in sessions/
    for project_dir in sessions_dir.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith("_"):
            # Skip files and special directories like _shared
            continue

        project_name = project_dir.name
        target_sessions_dir = Path(f"teams/{project_name}/sessions")

        if verbose:
            print(f"Processing project: {project_name}")
            print(f"Target directory: {target_sessions_dir}")

        # Create target directory if it doesn't exist
        if dry_run:
            print(f"Would create directory: {target_sessions_dir}")
        else:
            target_sessions_dir.mkdir(parents=True, exist_ok=True)

        # Move each agent session directory
        for agent_dir in project_dir.iterdir():
            if not agent_dir.is_dir():
                # Skip files
                continue

            agent_name = agent_dir.name
            target_agent_dir = target_sessions_dir / agent_name

            if dry_run:
                print(f"Would move {agent_dir} to {target_agent_dir}")
            else:
                # Create backup if the destination already exists
                if target_agent_dir.exists():
                    backup_dir = Path(f"{target_agent_dir}.bak")
                    if verbose:
                        print(f"Creating backup: {backup_dir}")
                    if backup_dir.exists():
                        shutil.rmtree(backup_dir)
                    shutil.copytree(target_agent_dir, backup_dir)
                    shutil.rmtree(target_agent_dir)

                # Copy the directory
                if verbose:
                    print(f"Moving {agent_dir} to {target_agent_dir}")
                shutil.copytree(agent_dir, target_agent_dir)
                sessions_moved += 1

        projects_moved += 1

    # Handle _shared directory if it exists
    shared_dir = sessions_dir / "_shared"
    if shared_dir.exists() and shared_dir.is_dir():
        target_shared_dir = Path("teams/_shared")

        if dry_run:
            print(f"Would create directory: {target_shared_dir}")
            print(f"Would move {shared_dir} to {target_shared_dir}")
        else:
            # Create target directory
            target_shared_dir.mkdir(parents=True, exist_ok=True)

            # Copy shared resources
            for item in shared_dir.iterdir():
                target_item = target_shared_dir / item.name
                if item.is_file():
                    if verbose:
                        print(f"Copying {item} to {target_item}")
                    shutil.copy2(item, target_item)
                elif item.is_dir():
                    if verbose:
                        print(f"Copying directory {item} to {target_item}")
                    shutil.copytree(item, target_item, dirs_exist_ok=True)

    return projects_moved, sessions_moved


def main():
    """Main function."""
    args = parse_args()
    dry_run = args.dry_run
    verbose = args.verbose

    if dry_run:
        print("=== DRY RUN - No changes will be made ===")
    else:
        print("=== EXECUTING - Moving session directories ===")

    projects_moved, sessions_moved = move_sessions(dry_run, verbose)

    if dry_run:
        print(
            f"\nWould move {sessions_moved} session directories across {projects_moved} projects"
        )
        print("\n=== DRY RUN COMPLETE ===")
        print("Run with --execute to make these changes.")
    else:
        print(
            f"\nSuccessfully moved {sessions_moved} session directories across {projects_moved} projects"
        )
        print("\n=== MOVE COMPLETE ===")
        print("The directories have been moved to their new locations.")
        print("Original directories still exist in the sessions/ directory.")
        print("You can remove them once you verify everything works correctly.")


if __name__ == "__main__":
    main()
