#!/usr/bin/env python3
"""
update_scaffold_team.py - Script to update scaffold_team.py for the new directory structure

This script modifies scaffold_team.py to work with the new directory structure
proposed in the reorganization plan.

Usage:
    python update_scaffold_team.py --dry-run    # Show changes without modifying files
    python update_scaffold_team.py --execute    # Update the scaffold_team.py file

Changes made:
1. Update file paths to match new directory structure
2. Update environment file paths to use config/teams/active/{project}/env
3. Update checklist path to use config/teams/active/{project}/checklist.md
"""
import argparse
import re
from pathlib import Path


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Update scaffold_team.py for the new directory structure"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dry-run", action="store_true", help="Show changes without modifying files"
    )
    group.add_argument(
        "--execute", action="store_true", help="Update the scaffold_team.py file"
    )
    return parser.parse_args()


def update_scaffold_team(dry_run=True):
    """Update scaffold_team.py to work with the new directory structure."""
    # Determine the path to scaffold_team.py (either in root or tools directory)
    scaffold_path = Path("scaffold_team.py")
    if not scaffold_path.exists():
        scaffold_path = Path("tools/scaffold_team.py")
        if not scaffold_path.exists():
            print("Error: Could not find scaffold_team.py in the repository.")
            return False

    print(f"Updating {scaffold_path}...")

    with open(scaffold_path, "r") as f:
        content = f.read()

    # Update paths for environment files
    content = re.sub(
        r"env_file = f'\.env\.{project}'",
        r"env_file = f'config/teams/active/{project}/env'",
        content,
    )

    # Update paths for checklist files
    content = re.sub(
        r"checklist_path = Path\(f'teams/{project}/checklist\.md'\)",
        r"checklist_path = Path(f'config/teams/active/{project}/checklist.md')",
        content,
    )

    # Update paths for template files
    content = re.sub(
        r"template_path = Path\(f'teams/{project}/env\.template'\)",
        r"template_path = Path(f'config/teams/active/{project}/env.template')",
        content,
    )

    # Update directory creation
    content = re.sub(
        r"teams_dir = Path\('teams'\)",
        r"teams_dir = Path('config/teams/active')",
        content,
    )

    # Update template copying
    content = re.sub(
        r"template_dir = Path\('teams/_templates'\)",
        r"template_dir = Path('templates/team')",
        content,
    )

    # Update reference to team-cli
    content = re.sub(
        r"python team-cli/team_cli\.py", r"python tools/team-cli/team_cli.py", content
    )

    if dry_run:
        print("\nChanges that would be made:")
        print("----------------------------")
        print(content[:500] + "...\n")  # Print first 500 chars as preview
    else:
        with open(scaffold_path, "w") as f:
            f.write(content)
        print(f"Updated {scaffold_path}")

    return True


def update_team_cli(dry_run=True):
    """Update team_cli.py to work with the new directory structure."""
    # Determine the path to team_cli.py
    team_cli_path = Path("team-cli/team_cli.py")
    if not team_cli_path.exists():
        team_cli_path = Path("tools/team-cli/team_cli.py")
        if not team_cli_path.exists():
            print("Error: Could not find team_cli.py in the repository.")
            return False

    print(f"Updating {team_cli_path}...")

    with open(team_cli_path, "r") as f:
        content = f.read()

    # Update role paths
    content = re.sub(
        r"roles_dir = Path\('roles'\)", r"roles_dir = Path('config/roles')", content
    )

    # Update session directory paths
    content = re.sub(
        r"sessions_dir = Path\('sessions'\)",
        r"sessions_dir = Path('sessions/active')",
        content,
    )

    # Update docs paths
    content = re.sub(
        r"global_docs = Path\('docs/global'\)",
        r"global_docs = Path('docs/global')",
        content,
    )

    # Update .devcontainer template path
    content = re.sub(
        r"devcontainer_template = Path\('\.devcontainer'\)",
        r"devcontainer_template = Path('templates/.devcontainer')",
        content,
    )

    if dry_run:
        print("\nChanges that would be made to team_cli.py:")
        print("----------------------------------------")
        print(content[:500] + "...\n")  # Print first 500 chars as preview
    else:
        with open(team_cli_path, "w") as f:
            f.write(content)
        print(f"Updated {team_cli_path}")

    return True


def update_readme(dry_run=True):
    """Update README.md to reflect the new directory structure."""
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("Error: Could not find README.md in the repository.")
        return False

    print(f"Updating {readme_path}...")

    with open(readme_path, "r") as f:
        content = f.read()

    # Update directory structure references
    content = re.sub(r"\.env\.{project}", r"config/teams/active/{project}/env", content)

    content = re.sub(
        r"python scaffold_team\.py", r"python tools/scaffold_team.py", content
    )

    content = re.sub(
        r"python team-cli/team_cli\.py", r"python tools/team-cli/team_cli.py", content
    )

    if dry_run:
        print("\nChanges that would be made to README.md:")
        print("--------------------------------------")
        print(content[:500] + "...\n")  # Print first 500 chars as preview
    else:
        with open(readme_path, "w") as f:
            f.write(content)
        print(f"Updated {readme_path}")

    return True


def main():
    """Main function."""
    args = parse_args()
    dry_run = args.dry_run

    if dry_run:
        print("=== DRY RUN - No changes will be made ===")
    else:
        print("=== EXECUTING - Updating files ===")
        print("WARNING: This will modify files!")
        confirm = input("Continue? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Aborted.")
            return

    # Update files
    update_scaffold_team(dry_run)
    update_team_cli(dry_run)
    update_readme(dry_run)

    if dry_run:
        print("\n=== DRY RUN COMPLETE ===")
        print("Run with --execute to make these changes.")
    else:
        print("\n=== UPDATE COMPLETE ===")
        print("Please review the changes to ensure everything works as expected.")


if __name__ == "__main__":
    main()
