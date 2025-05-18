# Active Context

## What I'm Working On Now
- Restored `.devcontainer` and Dockerfile generation for all session containers via `team_cli.py`.
- Verified that session creation now produces correct container configs and scripts for each agent.
- Preparing to streamline the setup of `mcp-discord` inside session containers, so Discord MCP server can be run without manual path edits.
- Roles UI: All editors (overview, env, MCP config) now use large, multi-line modals for editing.
- MCP config is pretty-printed for editing, minified for saving.
- Env and overview preserve formatting for editing.
- Backend overview endpoint returns plain text for Markdown rendering.
- UI/UX for roles is now much more comfortable and user-friendly.

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
- Finalize the Team section design: either add Team Templates or streamline the team scaffolding/generation process in the Teams UI.
- Implement the chosen approach for Teams.

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

## Playwright MCP Server Setup (Working Method)

### Problem
- Playwright MCP server failed to start using npm/npx install methods (missing `androidServerImpl`, server hang, or no tools registered).
- Multiple attempts with local and global npm installs did not resolve the issue.

### Solution (Build from Source)
1. **Clone the Playwright MCP repo:**
   ```sh
   git clone https://github.com/executeautomation/mcp-playwright.git
   cd mcp-playwright
   ```
2. **Install dependencies:**
   ```sh
   npm install
   ```
3. **Build the code:**
   ```sh
   npm run build
   npm link
   ```
4. **(Optional) You can run the server directly from the repo directory:**
   ```sh
   npx --directory /path/to/mcp-playwright run @executeautomation/playwright-mcp-server
   ```

### MCP Config (Unchanged)
The following MCP config was used and did not need to be changed:
```json
"playwright": {
  "command": "npx",
  "args": [
    "-y",
    "@smithery/cli@latest",
    "run",
    "@executeautomation/playwright-mcp-server",
    "--client",
    "cursor",
    "--key",
    "d716f5ef-5e41-4f78-b816-d599bc5293e6"
  ]
}
```

### Result
- After building from source, the MCP server started successfully.
- The MCP indicator turned green and tools are now available in Cursor.

---

**Next:** Run a test using an MCP tool call to verify functionality.

## Secrets Management Security Plan (Staged Approach)

- **Current Phase (Local Dev, File-Based):**
  - All setup files, including `.env` keys, are managed via the new web UI and stored in plain text.
  - The app is only accessible locally; there is no external attack surface.
  - `.env` and config files are included in `.gitignore` and must never be committed to version control.
  - **Warning:** Do not use real production secrets in local development.

- **Future Phase (DB Backend & External Access):**
  - When migrating to a database backend and/or exposing the site externally, implement:
    - Encryption at rest for secrets and sensitive config values.
    - Secure key management (environment variables, secrets manager, or KMS).
    - HTTPS for all web access.
    - User authentication and access controls in the web UI.
  - This staged approach allows for rapid development now, with a clear plan for robust security as the project evolves.

# Playwright MCP Tool Activation (Post-Reboot)

## Steps to Ensure Playwright MCP Tools Work in Cursor

1. **Install/Update Playwright MCP and Smithery CLI**
   ```sh
   npm install -g @smithery/cli@latest @executeautomation/playwright-mcp-server@latest
   ```
   - Ensures you have the latest versions globally.

2. **Check/Update MCP Config**
   - Ensure your `~/.cursor/mcp.json` contains:
     ```json
     {
       "mcpServers": {
         "playwright": {
           "command": "npx",
           "args": [
             "-y",
             "@smithery/cli@latest",
             "run",
             "@executeautomation/playwright-mcp-server",
             "--client",
             "cursor",
             "--key",
             "<YOUR_SMITHERY_KEY>"
           ]
         }
       }
     }
     ```
   - Replace `<YOUR_SMITHERY_KEY>` with your actual key.

3. **Start the MCP Server**
   ```sh
   npx -y @smithery/cli@latest run @executeautomation/playwright-mcp-server --client cursor --key <YOUR_SMITHERY_KEY>
   ```
   - Run this in a terminal and leave it open.

4. **Restart Cursor/IDE**
   - Fully quit and reopen Cursor after starting the MCP server.

5. **Verify Tool Availability**
   - Check Cursor's MCP tool list for Playwright tools (e.g., `playwright_navigate`).

## Troubleshooting
- Ensure Node.js is v18+ and npm is up to date.
- Check for port conflicts and resolve them.
- If tools do not appear, repeat steps 3 and 4.
- If using a local install, run from the correct directory.
- Check for errors in the MCP server terminal.

---
**Always use the Smithery CLI wrapper and correct key for Cursor integration.**

# Internal Chat MCP Server Draft Plan

## Purpose
Expose the internal team chat server as an MCP tool for Cursor and agent integration, while preserving CLI and web UI compatibility.

## Key Features
- MCP manifest endpoint for tool discovery
- Tools: send_message, get_unread_messages (with filtering)
- Filtering: by user, channel, DM, or tag (for agent-directed messages)
- No breaking changes to CLI or web UI

## Manifest Example
```json
{
  "tools": [
    {
      "name": "send_message",
      "description": "Send a message to the team chat.",
      "parameters": {
        "team_id": "string",
        "user": "string",
        "message": "string"
      }
    },
    {
      "name": "get_unread_messages",
      "description": "Get unread messages for a team with filters (user, channel, DM, etc).",
      "parameters": {
        "team_id": "string",
        "since_message_id": "string",
        "limit": "integer",
        "sender_id": "string (optional)",
        "channel": "string (optional)",
        "dm_only": "boolean (optional)",
        "mention_only": "boolean (optional)",
        "content_regex": "string (optional)"
      }
    }
  ]
}
```

## Endpoints
- `GET /mcp/manifest`
- `POST /mcp/send_message` (team_id, user, message)
- `GET /mcp/get_unread_messages` (team_id, since_message_id, limit, sender_id, channel, dm_only, mention_only, content_regex)

## Filtering/Agent Use Cases
- Agent can fetch only DMs, only messages mentioning itself, or only from certain users/channels.
- PM can send directives to the agent via chat; agent can reply or update PM as needed.
- Agents can communicate with each other or receive feature updates/feedback.

## Integration Notes
- Use FastAPI for the MCP wrapper, reusing existing ChatClient logic.
- MCP server runs as a separate process; CLI and web UI remain unchanged.
- Update `.cursor/mcp.json` to point to the new MCP server.
- Track this feature in Task Master for progress and documentation.

## [2025-05-17] MCP Tool Setup Fully Documented
- Created cline_docs/mcp_tool_setup.md with a comprehensive guide for MCP tool setup, extension, and maintenance.
- internal_chat_mcp is now correctly configured with a CLI entrypoint and is running (green dot).
- All test tools are available and functional via MCP.
- Next step: add real business logic tools as needed, following the new documentation.

## [2025-05-18] Internal Chat MCP Tools Fully Integrated
- The internal_chat_mcp MCP tools (SendMessage, GetUnreadMessages, WaitForMessage) are now fully implemented and tested.
- Successfully sent, received, and waited for messages in a real workflow with the backend chat system (team-9).
- End-to-end agent workflow is confirmed working: announce availability, wait for task, receive, and respond.
- Next: further automate or extend the workflow as needed. 