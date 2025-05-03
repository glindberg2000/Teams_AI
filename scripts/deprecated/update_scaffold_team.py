#!/usr/bin/env python3
"""
update_scaffold_team.py - Script to update scaffold_team.py for the new directory structure

This script modifies scaffold_team.py to work with the new directory structure
proposed in the reorganization plan.

Usage:
    python update_scaffold_team.py --dry-run    # Show changes without modifying files
    python update_scaffold_team.py --execute    # Update the scaffold_team.py file

Changes made:
1. Update file paths to match new domain-centric structure
2. Update environment file paths to use teams/{project}/config/env
3. Update checklist path to use teams/{project}/config/checklist.md
4. Update imports and references to team_cli.py
"""
import argparse
import re
from pathlib import Path
import os


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Update scaffold_team.py for the new directory structure"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without modifying files",
    )
    group.add_argument(
        "--execute", action="store_true", help="Update the scaffold_team.py file"
    )
    return parser.parse_args()


def update_paths(dry_run=True):
    """Update file paths in scaffold_team.py."""
    # Files to update
    files_to_update = {
        "scaffold_team.py": "tools/scaffold_team.py",
        "team-cli/team_cli.py": "tools/team_cli.py",
    }

    # Path replacements to make in the code
    path_replacements = [
        # Update environment file paths
        (r"\.env\.(\w+)", r"teams/\1/config/env"),
        (r"teams/(\w+)/env\.template", r"teams/\1/config/env.template"),
        (r"teams/(\w+)/checklist\.md", r"teams/\1/config/checklist.md"),
        # Update import paths
        (r"from team-cli import team_cli", r"from tools import team_cli"),
        (r"import team-cli\.team_cli", r"import tools.team_cli"),
        # Update references to CLI
        (r"python team-cli/team_cli\.py", r"python tools/team_cli.py"),
    ]

    for file_path, new_path in files_to_update.items():
        # Skip if the file doesn't exist
        if not Path(file_path).exists():
            print(f"Warning: {file_path} not found, skipping.")
            continue

        # Read the file content
        with open(file_path, "r") as f:
            content = f.read()

        # Apply all replacements
        new_content = content
        for pattern, replacement in path_replacements:
            new_content = re.sub(pattern, replacement, new_content)

        # Handle specific updates for scaffold_team.py
        if file_path == "scaffold_team.py":
            # Update file paths in the script
            new_content = new_content.replace(
                "with open(f'.env.{self.project}', 'w') as f:",
                "os.makedirs(f'teams/{self.project}/config', exist_ok=True)\n        with open(f'teams/{self.project}/config/env', 'w') as f:",
            )

            new_content = new_content.replace(
                "with open(f'teams/{self.project}/env.template', 'w') as f:",
                "os.makedirs(f'teams/{self.project}/config', exist_ok=True)\n        with open(f'teams/{self.project}/config/env.template', 'w') as f:",
            )

            new_content = new_content.replace(
                "with open(f'teams/{self.project}/checklist.md', 'w') as f:",
                "os.makedirs(f'teams/{self.project}/config', exist_ok=True)\n        with open(f'teams/{self.project}/config/checklist.md', 'w') as f:",
            )

            # Update class docstring
            new_content = re.sub(
                r'"""Generate team configuration\.\s+This class handles.*?"""',
                '"""Generate team configuration.\n\n    This class handles the generation of team configuration files including:\n    - Environment file (teams/{project}/config/env)\n    - Environment template (teams/{project}/config/env.template)\n    - Setup checklist (teams/{project}/config/checklist.md)\n    """',
                new_content,
                flags=re.DOTALL,
            )

        # Update team_cli.py
        if file_path == "team-cli/team_cli.py":
            # Update session creation logic to use new path structure
            new_content = new_content.replace(
                "dest_dir = Path(f'sessions/{self.project}/{self.name}')",
                "dest_dir = Path(f'teams/{self.project}/sessions/{self.name}')",
            )

            # Update environment variable loading
            new_content = new_content.replace(
                "env_file = f'.env.{project}'",
                "env_file = f'teams/{project}/config/env'",
            )

        # Show the changes or write the updated file
        if dry_run:
            print(f"Would update {file_path} -> {new_path}:")
            for pattern, replacement in path_replacements:
                print(f"  {pattern} -> {replacement}")
        else:
            # Create parent directory if needed
            Path(new_path).parent.mkdir(parents=True, exist_ok=True)

            # Write the updated content
            with open(new_path, "w") as f:
                f.write(new_content)
            print(f"Updated {new_path}")


def main():
    """Main function."""
    args = parse_args()
    dry_run = args.dry_run

    if dry_run:
        print("=== DRY RUN - No changes will be made ===")
    else:
        print("=== EXECUTING - Updating files for new directory structure ===")

    update_paths(dry_run)

    if dry_run:
        print("\n=== DRY RUN COMPLETE ===")
        print("Run with --execute to make these changes.")
    else:
        print("\n=== UPDATE COMPLETE ===")
        print("Please review the changes and ensure all references are correct.")


if __name__ == "__main__":
    main()
