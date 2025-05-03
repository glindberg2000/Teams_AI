#!/usr/bin/env python3
"""
update_shell_scripts.py - Update path references in shell scripts

This script scans shell scripts in the repository and updates path references
to match the new directory structure after reorganization.

Usage:
    python update_shell_scripts.py --dry-run    # Show changes without making them
    python update_shell_scripts.py --execute    # Update the shell scripts

Changes made:
1. Update 'sessions/{project}' references to 'teams/{project}/sessions'
2. Update '.env.{project}' references to 'teams/{project}/config/env'
3. Update 'teams/{project}/checklist.md' references to 'teams/{project}/config/checklist.md'
4. Update script paths (scaffold_team.py, team_cli.py)
"""
import argparse
import os
import re
from pathlib import Path


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Update path references in shell scripts"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without modifying files",
    )
    group.add_argument(
        "--execute", action="store_true", help="Update the shell scripts"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed information about changes",
    )
    parser.add_argument(
        "--file",
        help="Process a specific file instead of searching for all shell scripts",
    )
    return parser.parse_args()


def find_shell_scripts():
    """Find all shell scripts in the repository."""
    result = []
    for root, _, files in os.walk("."):
        if ".venv" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(".sh") or file == "restore.sh":
                path = os.path.join(root, file)
                result.append(path)
    return result


def update_script(script_path, dry_run=True, verbose=False):
    """Update path references in a shell script."""
    try:
        with open(script_path, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {script_path}: {e}")
        return False

    original_content = content

    # Define replacements to make - using more specific regex patterns
    replacements = [
        # Session paths with common shell commands
        (
            r"(cd|cp|mkdir|rm|source|mv|find|ls)(\s+)sessions/([a-zA-Z0-9_-]+)",
            r"\1\2teams/\3/sessions",
        ),
        # Session paths with variable assignments
        (
            r'(=|"|\'|\s+)sessions/([a-zA-Z0-9_-]+)(/|\s|"|\'|$)',
            r"\1teams/\2/sessions\3",
        ),
        # Session paths in quotes with absolute paths
        (
            r'(=|\s+)"(/workspace/|/home/\w+/)sessions/([a-zA-Z0-9_-]+)',
            r'\1"\2teams/\3/sessions',
        ),
        (
            r"(=|\s+)\'(/workspace/|/home/\w+/)sessions/([a-zA-Z0-9_-]+)",
            r"\1\'\2teams/\3/sessions",
        ),
        # Session paths with variables in path
        (
            r"(/workspace/|/home/\w+/)sessions/(\$\{?[A-Za-z0-9_]+\}?)",
            r"\1teams/\2/sessions",
        ),
        # Environment files with common shell commands
        (r"(source|cat|cp|mv)(\s+)\.env\.([a-zA-Z0-9_-]+)", r"\1\2teams/\3/config/env"),
        # Environment files with variable assignments
        (r'(=|"|\'|\s+)\.env\.([a-zA-Z0-9_-]+)(\s|"|\'|$)', r"\1teams/\2/config/env\3"),
        # Environment files with CLI arguments
        (r"--env-file(\s+)\.env\.([a-zA-Z0-9_-]+)", r"--env-file\1teams/\2/config/env"),
        # Environment files with variables
        (r"\.env\.\$\{?([A-Za-z0-9_]+)\}?", r"teams/\$\1/config/env"),
        # Team files with common shell commands
        (
            r"(cd|cp|mkdir|rm|source|mv|find|ls)(\s+)teams/([a-zA-Z0-9_-]+)/checklist\.md",
            r"\1\2teams/\3/config/checklist.md",
        ),
        (
            r"(cd|cp|mkdir|rm|source|mv|find|ls)(\s+)teams/([a-zA-Z0-9_-]+)/env\.template",
            r"\1\2teams/\3/config/env.template",
        ),
        # Team files with variable assignments
        (
            r'(=|"|\'|\s+)teams/([a-zA-Z0-9_-]+)/checklist\.md(\s|"|\'|$)',
            r"\1teams/\2/config/checklist.md\3",
        ),
        (
            r'(=|"|\'|\s+)teams/([a-zA-Z0-9_-]+)/env\.template(\s|"|\'|$)',
            r"\1teams/\2/config/env.template\3",
        ),
        # Tool paths with common execution patterns
        (r"python(\s+)scaffold_team\.py", r"python\1tools/scaffold_team.py"),
        (r"python(\s+)team-cli/team_cli\.py", r"python\1tools/team_cli.py"),
        (r"./scaffold_team\.py", r"./tools/scaffold_team.py"),
        (r"./team-cli/team_cli\.py", r"./tools/team_cli.py"),
        # Legacy team-cli command structures
        (r"team-cli\.py", r"tools/team_cli.py"),
        # Restore scripts with project variable
        (r"sessions/\$\{?([A-Za-z0-9_]+)\}?/", r"teams/\$\1/sessions/"),
    ]

    # Apply replacements and track changes
    changes_made = []
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            changes_made.append((pattern, replacement))
            content = new_content

    # Check if content changed
    if content == original_content:
        if verbose:
            print(f"No changes needed for {script_path}")
        return False

    if dry_run:
        print(f"Would update {script_path}")
        if verbose:
            for pattern, replacement in changes_made:
                print(f"  Pattern: {pattern}")
                print(f"  Replacement: {replacement}")
                print()

            # Show a diff of changes
            print("Changes:")
            from difflib import unified_diff

            diff = unified_diff(
                original_content.splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile=f"{script_path} (original)",
                tofile=f"{script_path} (updated)",
            )
            print("".join(diff))
    else:
        try:
            # Create backup of original file
            backup_path = f"{script_path}.bak"
            with open(backup_path, "w") as f:
                f.write(original_content)

            # Write updated content
            with open(script_path, "w") as f:
                f.write(content)
            print(f"Updated {script_path} (backup at {backup_path})")
        except Exception as e:
            print(f"Error updating {script_path}: {e}")
            return False

    return True


def main():
    """Main function."""
    args = parse_args()
    dry_run = args.dry_run
    verbose = args.verbose

    if dry_run:
        print("=== DRY RUN - No changes will be made ===")
    else:
        print("=== EXECUTING - Updating shell scripts ===")

    if args.file:
        scripts = [args.file]
        print(f"Processing single file: {args.file}")
    else:
        scripts = find_shell_scripts()
        print(f"Found {len(scripts)} shell scripts")

    updated = 0
    for script in scripts:
        if update_script(script, dry_run, verbose):
            updated += 1

    print(
        f"\n{updated} scripts would be updated"
        if dry_run
        else f"\n{updated} scripts updated"
    )

    if dry_run:
        print("\n=== DRY RUN COMPLETE ===")
        print("Run with --execute to make these changes.")
    else:
        print("\n=== UPDATE COMPLETE ===")
        print("Please review the changes and check if scripts work correctly.")
        print("Backups of original files were created with .bak extension.")


if __name__ == "__main__":
    main()
