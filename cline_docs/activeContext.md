# Active Context

## What I'm Working On Now
- Restored `.devcontainer` and Dockerfile generation for all session containers via `team_cli.py`.
- Verified that session creation now produces correct container configs and scripts for each agent.
- Preparing to streamline the setup of `mcp-discord` inside session containers, so Discord MCP server can be run without manual path edits.

## Recent Changes
- `.devcontainer` and all scripts restored from template to project root and committed.
- Confirmed that `create-session` and `create-crew` now generate container configs as before.
- Debugged and fixed propagation of env/config fields for Slack, Discord, etc.
- Updated `templates/devcontainer/Dockerfile` to always:
  - Install Node.js 20 (LTS)
  - Upgrade npm to v9 (stable for npx usage)
  - Remove any global npx v10+ binary to prevent version drift
- Updated `templates/devcontainer/scripts/mcp_config.template.json` to use the `npx -p ... -c ...` pattern for all MCP servers, ensuring compatibility with npx 9+ and preventing argument parsing bugs.
- All role-level mcp_config.template.json files have been updated to match the master template, ensuring correct Discord and Taskmaster MCP config for all session generations.

## Next Steps
- Analyze current MCP config and local repo path handling for `mcp-discord`.
- Propose a plan to automate cloning the `mcp-discord` repo into each session container (if not present).
- Update the MCP config generator to set the correct command path for `mcp-discord` (prefer local, fallback to global if available).
- Document the streamlined workflow for Discord MCP server setup in session containers.
- Reconfigure any broken MCP servers in existing sessions to use the new config pattern.
- Rebuild containers for all teams/sessions to ensure the new Dockerfile and MCP config are in effect.

## Current State
- Discord MCP integration is fully operational using the [mcp-discord](https://github.com/netixc/mcp-discord) bridge.
- The bridge can be run manually or invoked directly by Cursor/MCP if configured with the correct command and environment variables in `.cursor/mcp.json`.
- Both sending and reading messages work in real time; human and bot messages are visible to the bridge.
- All onboarding, checklist, and troubleshooting patterns are up to date and reference the correct doc locations.

## Open Issues / TODOs
- Continue to test and automate Discord workflows as needed.
- Ensure all onboarding/checklist docs reference only the correct, cleaned-up doc locations.
- Audit and clean the docs/ directory, removing or archiving anything not needed for containers.
- Update README and checklists as needed.

## Notes
- All legacy, migration, and reorg notes have been moved to cline_docs/legacy/.
- Only current, actionable context is kept here.

# Cline Memory Bank: Shared Docs Workflow (Summary)

- Fill out `teams/{project}/cline_docs_shared/` after scaffolding, before crew creation.
- Crew creation copies the filled shared docs into each session's payload.
- See productContext.md for full workflow details. 