# Active Context

## Current Work
- Refactored team-cli to use session name as role by default
- Added support for custom MCP config per role (mcp_config.template.json)
- Improved CLI feedback: explicit about role directory and MCP config used, warns on fallback
- Created example_role as a template for new users (with docs, env, and MCP config)
- Verified that custom docs and MCP config are included in session payloads

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
1. Document new workflow in README
2. Encourage users to create custom roles for each session type
3. Add more sample docs and tools to example_role
4. Continue testing with new session/role types

## Current State
- All core functionality is working correctly
- Role-based docs and custom MCP config are now supported and tested
- Example role is available for onboarding new users
- CLI output is clear and user-friendly 