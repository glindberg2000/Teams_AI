# Progress

## Completed
- Implemented project-based organization for sessions
- Fixed SLACK_TEAM_ID synchronization across sessions
- Added proper API key propagation (ANTHROPIC_API_KEY and PERPLEXITY_API_KEY) from team env to individual sessions
- Verified unique SSH key generation for each session in crew creation
- Added proper environment variable handling and documentation
- Implemented configurable documentation handling in payload directory
- Updated restore_payload.sh to properly restore docs
- Added documentation configuration options in team env file
- Refactored team-cli to use session name as role by default
- Added support for custom MCP config per role (mcp_config.template.json)
- Improved CLI feedback: explicit about role directory and MCP config used, warns on fallback
- Created example_role as a template for new users (with docs, env, and MCP config)
- Verified that custom docs and MCP config are included in session payloads

## In Progress
- Documenting new workflow in README
- Testing with new session/role types

## To Do
- Encourage users to create custom roles for each session type
- Add more sample docs and tools to example_role
- Add documentation validation to ensure required docs exist
- Consider adding documentation templates for new projects
- Consider adding custom SSH key naming scheme for better visibility
- Add validation for API key formats
- Consider adding key rotation capabilities

# Progress Status

- What works: All session folders and shared docs are scaffolded, agent instructions are in place, .env.sample is available, and container setup patterns are documented. Role-based docs and custom MCP config are now supported and tested. Example role is available for onboarding new users.
- What's left to build: Populate .env files with real secrets, verify session-specific configs, finalize tweaks per PM/lead feedback, and expand example_role.
- Progress status: Ready for review and secrets injection; sessions can be launched once verified. 