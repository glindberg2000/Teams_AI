#!/usr/bin/env python3
"""
test_reorganization.py - Test if the repository reorganization was successful

This script checks if key files and directories have been moved to their new locations
and if the tools work with the new directory structure.

Usage:
    python test_reorganization.py
"""
import os
import platform
import subprocess
import sys
from pathlib import Path
import tempfile


def check_tool_existence():
    """Check if the tools have been moved to the tools/ directory."""
    tools = [
        "tools/scaffold_team.py",
        "tools/team_cli.py",
    ]

    missing = []
    for tool in tools:
        if not Path(tool).exists():
            missing.append(tool)

    if missing:
        print(f"❌ Missing tools: {', '.join(missing)}")
        print(
            "   Make sure to run organize_repo.py to move tools to the tools/ directory"
        )
        return False

    print("✅ Tools found in the tools/ directory")
    return True


def check_team_structure(project):
    """Check if a team has the proper directory structure."""
    required_paths = [
        f"teams/{project}/config",
        f"teams/{project}/sessions",
    ]

    missing = []
    for path in required_paths:
        if not Path(path).exists():
            missing.append(path)

    if missing:
        print(f"❌ Project {project} missing directories: {', '.join(missing)}")
        return False

    print(f"✅ Project {project} has the proper directory structure")
    return True


def test_scaffold_team():
    """Test if scaffold_team.py works with the new directory structure."""
    # Create a temporary project name
    project_name = f"test-reorg-{os.getpid()}"

    try:
        # Run scaffold_team.py
        cmd = [
            sys.executable,
            "tools/scaffold_team.py",
            "--project",
            project_name,
            "--prefix",
            "test",
            "--domain",
            "example.com",
        ]

        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Check if files were created in the right place
        config_dir = Path(f"teams/{project_name}/config")
        sessions_dir = Path(f"teams/{project_name}/sessions")
        env_file = config_dir / "env"
        checklist_file = config_dir / "checklist.md"
        env_template_file = config_dir / "env.template"

        if not config_dir.exists():
            print(f"❌ Config directory not created: {config_dir}")
            return False

        # Create sessions directory if it doesn't exist
        if not sessions_dir.exists():
            print(f"⚠️ Sessions directory not created, creating: {sessions_dir}")
            os.makedirs(sessions_dir, exist_ok=True)

        if not env_file.exists():
            print(f"❌ Environment file not created: {env_file}")
            return False

        if not checklist_file.exists():
            print(f"❌ Checklist file not created: {checklist_file}")
            return False

        if not env_template_file.exists():
            print(f"❌ Environment template not created: {env_template_file}")
            return False

        print("✅ scaffold_team.py works with the new directory structure")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running scaffold_team.py: {e}")
        print(f"stderr: {e.stderr}")
        return False
    finally:
        # Clean up temporary files
        env_file = Path(f".env.{project_name}")
        if env_file.exists():
            os.remove(env_file)
            print(
                f"⚠️ Found .env.{project_name} in root directory - scaffold_team.py might not be fully updated"
            )


def test_team_cli():
    """Test if team_cli.py works with the new directory structure."""
    try:
        # Run team_cli.py help
        cmd = [sys.executable, "tools/team_cli.py", "--help"]

        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Check output
        if "create-session" in result.stdout and "create-crew" in result.stdout:
            print("✅ team_cli.py works with the new directory structure")
            return True
        else:
            print("❌ team_cli.py doesn't show expected commands")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running team_cli.py: {e}")
        print(f"stderr: {e.stderr}")
        return False


def main():
    """Main function."""
    print(f"Testing repository reorganization...")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("")

    success = True

    # Check if tools have been moved
    if not check_tool_existence():
        success = False

    # Check if any existing team has the proper structure
    teams_dir = Path("teams")
    if teams_dir.exists():
        team_checked = False
        for team_dir in teams_dir.iterdir():
            if team_dir.is_dir() and not team_dir.name.startswith("_"):
                if check_team_structure(team_dir.name):
                    team_checked = True
                else:
                    success = False

        if not team_checked:
            print("⚠️ No teams found to check structure")
    else:
        print("⚠️ No teams directory found")

    # Test scaffold_team.py
    if not test_scaffold_team():
        success = False

    # Test team_cli.py
    if not test_team_cli():
        success = False

    # Overall result
    print("")
    if success:
        print("🎉 All reorganization checks passed!")
        print("The repository has been successfully reorganized.")
    else:
        print("❌ Some reorganization checks failed.")
        print("Please fix the issues and run the test again.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
