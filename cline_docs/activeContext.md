# Active Context

## What I'm working on now
- Completed a full end-to-end test and verification of the team scaffolding and session generation workflow
- Updated README.md for clear onboarding and usage (for both humans and AI)
- Updated cline_docs/README-task-master.md and MIGRATION_GUIDE.md with context and references
- All legacy, deprecated, and backup files removed
- All changes committed and pushed to main branch
- Directory structure and documentation are now clean, discoverable, and ready for onboarding

## Recent changes
- Merged reorg branch into main after full verification
- Cleaned up .devcontainer, contrib, and backup files
- Moved advanced and historical docs to cline_docs/
- Updated .gitignore to ensure no secrets or generated content are committed
- Discord MCP integration is now fully operational using the [mcp-discord](https://github.com/netixc/mcp-discord) bridge.
- The bridge can be run manually (for local testing) or invoked directly by Cursor/MCP if configured with the correct command and environment variables in `.cursor/mcp.json`.
- Confirmed: Both sending and reading messages work in real time.
- Human and bot messages are visible to the bridge.
- Troubleshooting included: fixing config structure, using absolute CLI path, ensuring correct bot permissions, and re-inviting the bot with the right scopes.

## Next steps
- Propose/document a better long-term documentation and directory organization (see below)
- Review and update any script references to doc locations if needed
- Continue onboarding, optimization, and rule improvements as needed
- Keep Discord setup instructions in all onboarding/checklist docs.
- Ensure the README and Memory Bank reflect Discord as a first-class integration.
- Continue to test and automate Discord workflows as needed.

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
- Developed comprehensive reorganization tools and documentation:
  - Created organize_repo.py for handling file moves and directory structure changes
  - Developed update_scaffold_team.py to update path references in Python code
  - Created update_shell_scripts.py to fix path references in shell scripts
  - Added detailed MIGRATION_GUIDE.md for users
- Created a separate 'reorg' branch for testing the reorganization before implementation

## Recent Changes
- Fixed session extraction in team-cli.py to properly identify role names from environment variables
- Improved validation to skip sessions with missing required keys
- Added error handling for SSH key paths and permissions
- Updated the README.md and memory bank documentation with detailed explanation of the workflow
- Added a directory structure diagram to the README for better visualization
- Modified organize_repo.py to implement a domain-centric approach with teams/{project}/sessions/{role}
- Updated update_scaffold_team.py to handle the new directory structure
- Created specialized update_shell_scripts.py with improved regex patterns for handling shell script path updates
- Added diffing capabilities to show precise changes being made to files
- Created a comprehensive migration guide with before/after directory structure comparisons
- Added backup capabilities to all update scripts to ensure no data loss

## Next Steps
1. **Final Testing of Reorganization**:
   - Test all reorganization scripts in dry-run mode on a copy of the repository
   - Verify path updates in Python and shell scripts
   - Create a test environment to validate the new structure with real usage

2. **Implementation of Reorganization**:
   - Once fully tested, run the reorganization on the reorg branch
   - Test the reorganized structure thoroughly (create teams, sessions, etc.)
   - Fix any remaining path issues or edge cases
   - Merge the reorg branch to main when validated

3. **Documentation Updates**:
   - Update project documentation to reflect the new structure
   - Provide examples using the new paths
   - Create a quick-reference guide for common commands with new paths
   - Add troubleshooting section for common migration issues

4. **Cleanup of Old Structure**:
   - Remove deprecated scripts and directories
   - Clean up any leftover configuration files
   - Handle remaining test environments

## Implementation Decisions
- **Domain-Centric Organization**: Changed from a flat structure to a domain-centric approach with teams as the primary organizational unit
- **Team Sessions Nested Under Team Config**: Moved to teams/{project}/sessions/{role} to keep all team-related content together
- **Tools Directory**: Centralized command-line tools in a single directory
- **Role Templates**: Kept roles directory separate to maintain clear separation of concerns
- **Separate Branch**: Created 'reorg' branch to isolate reorganization changes for testing
- **Comprehensive Migration Tools**: Created specialized tools for each aspect of the migration:
  - organize_repo.py: Handles directory restructuring
  - update_scaffold_team.py: Updates Python code paths
  - update_shell_scripts.py: Updates shell script paths
- **Automatic Backups**: All update tools create backups of modified files for safety
- **Verbose Logging**: Added detailed logging options to all scripts for transparency

## Issues to Watch
- Path references in shell scripts that use variables (e.g., ${SESSION_NAME})
- Environment variable naming conventions must remain consistent
- SSH key paths may need adjustment in the new structure
- Documentation inheritance paths will change in the new structure
- Container configuration that references specific paths

## Current Understanding
- The repository would benefit from a more organized structure with teams as the primary unit
- Current flat session structure makes it hard to manage multiple teams
- The new structure provides better separation of concerns:
  - teams/ contains all team-specific content (config, sessions)
  - tools/ contains all command-line tools
  - roles/ contains role templates and documentation
  - templates/ contains system-wide templates
- The reorganization can be implemented with specialized scripts without manual file copying
- The reorganization should be done in a separate branch and tested thoroughly before merging to main
- Shell scripts require careful path updates using regex patterns to handle various script styles 