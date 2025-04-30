# Active Context

## Current Work
- Improved documentation handling in team-cli:
  - Added configurable documentation inclusion in payload directory
  - Updated restore_payload.sh for proper docs restoration
  - Added documentation configuration in team env file
  - Implemented recursive directory copying for docs
  - Added command-line flags for documentation control

## Recent Changes
- Implemented proper documentation organization:
  - Global docs in payload/docs/global/
  - Project docs in payload/docs/project/
  - Role docs in payload/docs/role/
- Added documentation configuration options
- Updated restore_payload.sh for docs handling
- Added ANTHROPIC_API_KEY and PERPLEXITY_API_KEY to team env template
- Verified SSH key generation uniqueness across sessions
- Improved project-based organization for sessions
- Enhanced environment variable propagation

## Next Steps
1. Test documentation handling with different configurations
2. Verify documentation restoration in containers
3. Consider adding documentation validation
4. Consider implementing documentation templates
5. Consider adding custom SSH key naming
6. Add API key format validation
7. Consider implementing key rotation capabilities

## Current State
- All core functionality is working correctly
- Documentation handling is now properly configured and organized
- Session creation (both single and crew) is working as expected
- Environment variables and SSH keys are being handled correctly
- Project-based organization is functioning properly 