#!/usr/bin/env python3
"""
create_missing_directories.py - Create missing directories in the new directory structure

This script creates the missing config and sessions directories for each team
that was identified in the test_reorganization.py script.

Usage:
    python create_missing_directories.py
"""
import os
from pathlib import Path


def create_missing_directories():
    """Create missing config and sessions directories for each team."""
    # Get list of all team directories
    teams_dir = Path("teams")
    if not teams_dir.exists():
        print("The teams directory doesn't exist. Creating it...")
        teams_dir.mkdir()

    teams = []
    for team_dir in teams_dir.iterdir():
        if team_dir.is_dir() and not team_dir.name.startswith("_"):
            teams.append(team_dir.name)

    print(f"Found {len(teams)} teams")

    # Create missing directories for each team
    for team in teams:
        team_dir = teams_dir / team

        # Create config directory if missing
        config_dir = team_dir / "config"
        if not config_dir.exists():
            print(f"Creating missing directory: {config_dir}")
            config_dir.mkdir(exist_ok=True)

            # Create template env file if it doesn't exist
            env_template = config_dir / "env.template"
            if not env_template.exists():
                print(f"Creating empty env.template file: {env_template}")
                with open(env_template, "w") as f:
                    f.write(f"# Environment template for {team}\n")
                    f.write(f"TEAM_NAME={team}\n")
                    f.write(f"PROJECT_NAME={team}\n")

        # Create sessions directory if missing
        sessions_dir = team_dir / "sessions"
        if not sessions_dir.exists():
            print(f"Creating missing directory: {sessions_dir}")
            sessions_dir.mkdir(exist_ok=True)


def main():
    """Main function."""
    print("Creating missing directories...")
    create_missing_directories()
    print("Done.")


if __name__ == "__main__":
    main()
