# Active Context

## Current Work
- Successfully debugged and improved scaffold_team.py to generate team-cli compatible .env files
- Fixed variable naming patterns to match team-cli's session extraction logic (ROLE_UPPER_SLACK_TOKEN format)
- Added robustness to team-cli.py by validating required keys before attempting to create sessions
- Added comprehensive documentation to both scripts, including:
  - Improved docstrings with parameter types and return values
  - Detailed documentation of variable naming conventions
  - Better error messages and troubleshooting guidance
- Updated README.md with clear workflow descriptions and directory structure

## Recent Changes
- Completely refactored scaffold_team.py for better organization and maintainability
- Fixed session extraction in team-cli.py to properly handle role names with underscores
- Added troubleshooting information to help users debug common issues
- Created comprehensive README with documentation of project workflow
- Added validation of role names against a predefined list of valid roles
- Added helpful inline comments for complex parsing logic

## Next Steps
- Reorganize the project structure for better clarity and organization:
  - Move test/temporary .env files into the teams directory
  - Consider structuring sessions by project/team for better organization
  - Add cleanup options to remove temporary or unused sessions
- Add more robust validation of team-cli configuration
- Add support for more role types
- Create a test suite to verify end-to-end workflow
- Add documentation for how to debug common issues in the team creation process

## Current Understanding
- scaffold_team.py generates .env.{project} files with required configuration
- The .env files follow a specific naming convention: ROLE_UPPER_SLACK_TOKEN
- team-cli.py extracts session names by parsing these variables (e.g., PM_GUARDIAN_SLACK_TOKEN → pm_guardian)
- team-cli.py creates isolated agent sessions in sessions/{project}/{agent}/
- Documentation is inherited through a hierarchical structure (global → project → role)
- Each agent gets its own SSH key, documentation, and environment vars
- The typical workflow is:
  1. Generate configuration with scaffold_team.py
  2. Fill in API keys in .env.{project}
  3. Create sessions with team-cli.py create-crew
  4. Launch containers for each agent 