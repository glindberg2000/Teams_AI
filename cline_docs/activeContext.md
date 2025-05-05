# Active Context

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