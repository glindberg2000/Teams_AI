#!/usr/bin/env python3
"""
move_env_files.py - Move .env files to new directory structure

This script moves all existing .env.{project} files to teams/{project}/config/env
as part of the repository reorganization.

Usage:
    python move_env_files.py --dry-run     # Show what would be done without making changes
    python move_env_files.py --execute     # Actually move the files
"""
import argparse
import os
import re
import shutil
from pathlib import Path


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Move .env files to new directory structure"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    group.add_argument("--execute", action="store_true", help="Actually move the files")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed information about moved files",
    )
    return parser.parse_args()


def move_env_files(dry_run=True, verbose=False):
    """Move .env.{project} files to teams/{project}/config/env."""
    root = Path(".")
    env_pattern = re.compile(r"^\.env\.(.+)$")
    files_moved = 0

    # Find all .env.{project} files
    env_files = []
    for item in root.iterdir():
        if item.is_file():
            match = env_pattern.match(item.name)
            if match:
                project = match.group(1)
                env_files.append((item, project))

    if verbose:
        print(f"Found {len(env_files)} environment files to move")

    # Move each .env.{project} file to teams/{project}/config/env
    for env_file, project in env_files:
        config_dir = Path(f"teams/{project}/config")

        if dry_run:
            print(f"Would create directory: {config_dir}")
            print(f"Would move {env_file} to {config_dir}/env")
        else:
            # Create config directory if it doesn't exist
            config_dir.mkdir(parents=True, exist_ok=True)

            # Move the file
            dest_path = config_dir / "env"

            # Create backup if the destination file already exists
            if dest_path.exists():
                backup_path = dest_path.with_suffix(".bak")
                if verbose:
                    print(f"Creating backup: {backup_path}")
                shutil.copy2(dest_path, backup_path)

            # Copy the file
            if verbose:
                print(f"Moving {env_file} to {dest_path}")
            shutil.copy2(env_file, dest_path)
            files_moved += 1

    return files_moved


def main():
    """Main function."""
    args = parse_args()
    dry_run = args.dry_run
    verbose = args.verbose

    if dry_run:
        print("=== DRY RUN - No changes will be made ===")
    else:
        print("=== EXECUTING - Moving .env files ===")

    files_moved = move_env_files(dry_run, verbose)

    if dry_run:
        print(f"\nWould move {files_moved} environment files")
        print("\n=== DRY RUN COMPLETE ===")
        print("Run with --execute to make these changes.")
    else:
        print(f"\nSuccessfully moved {files_moved} environment files")
        print("\n=== MOVE COMPLETE ===")
        print("The files have been moved to their new locations.")
        print("Original .env files still exist in the root directory.")
        print("You can remove them once you verify everything works correctly.")


if __name__ == "__main__":
    main()
