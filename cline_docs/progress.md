# Cline Memory Bank: Shared Docs Workflow (Summary)

- Fill out `teams/{project}/cline_docs_shared/` after scaffolding, before crew creation.
- Crew creation copies the filled shared docs into each session's payload.
- See productContext.md for full workflow details.

---

# Progress

## What Works
- Discord MCP integration is fully operational (send/read tested)
- Team scaffolding, session creation, and onboarding workflows are robust and up to date
- Documentation inheritance for containers is working as intended

## What's Left to Build
- Ongoing: Audit and clean docs/ to ensure only global, role, and project docs are inherited by containers
- Continue to improve onboarding and checklist docs as needed

## Status
- All legacy, migration, and reorg notes have been moved to cline_docs/legacy/.
- Only current, actionable progress is kept here.

- [ ] Plan for internal chat MCP server documented in activeContext.md
- [ ] MCP server will expose send_message and get_unread_messages with advanced filtering (user, channel, DM, etc)
- [ ] CLI and web UI will remain unchanged
- [ ] Task Master will be updated with this new feature for tracking
- [ ] Next: commit current state, then implement MCP server and update Task Master 