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
- Created a domain-centric repository organization plan with teams as primary units
- Developed scripts to implement the reorganization (organize_repo.py, update_scaffold_team.py)
- Created a separate 'reorg' branch for testing the reorganization before implementation

## Recent Changes
- Fixed session extraction in team-cli.py to properly identify role names from environment variables
- Improved validation to skip sessions with missing required keys
- Added error handling for SSH key paths and permissions
- Updated the README.md and memory bank documentation with detailed explanation of the workflow
- Added a directory structure diagram to the README for better visualization
- Modified organize_repo.py to implement a domain-centric approach with teams/{project}/sessions/{role}
- Updated update_scaffold_team.py to handle the new directory structure
- Created git branch 'reorg' for the reorganization work to isolate changes

## Next Steps
1. **Complete Repository Reorganization**:
   - Test the reorganization scripts in dry-run mode on a copy of the repository
   - Verify all path references are updated correctly
   - Handle edge cases (missing directories, unusual file names)
   - Update any import statements or path references in the code
   - Consider creating a detailed migration guide for users

2. **Improve SSH Key Management**:
   - Add better validation for SSH key paths
   - Implement more robust error handling
   - Consider adding a backup feature for generated keys

3. **Enhance Error Handling**:
   - Add more descriptive error messages
   - Implement logging for better debugging
   - Add validation for configuration files

4. **Add Testing**:
   - Create unit tests for critical functions
   - Add integration tests for the full workflow
   - Create example test cases for different team configurations

5. **Documentation Improvements**:
   - Add more examples of team configurations
   - Create troubleshooting guide with common issues
   - Add diagrams for visualization of components and workflows

## Implementation Decisions
- **Domain-Centric Organization**: Changed from a flat structure to a domain-centric approach with teams as the primary organizational unit
- **Team Sessions Nested Under Team Config**: Moved to teams/{project}/sessions/{role} to keep all team-related content together
- **Tools Directory**: Centralized command-line tools in a single directory
- **Role Templates**: Kept roles directory separate to maintain clear separation of concerns
- **Separate Branch**: Created 'reorg' branch to isolate reorganization changes for testing

## Issues to Watch
- Path references in scaffold_team.py and team_cli.py need careful updating
- Environment variable naming conventions must remain consistent
- SSH key paths may need adjustment in the new structure
- Documentation inheritance paths will change in the new structure

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