# Example Role: `example_role`

This directory demonstrates how to set up a custom role for the LedgerFlow AI Team CLI.

## Structure

- `docs/` — Role-specific documentation (markdown, guides, SOPs, etc.)
- `.env.sample` — Environment variable template for this role
- `mcp_config.template.json` — MCP server config template (custom toolset for this role)

## How to Use

1. **Customize Documentation:**
   - Add markdown files to `docs/` for onboarding, checklists, etc.
2. **Set Up Environment:**
   - Edit `.env.sample` to specify required environment variables for this role.
3. **Custom MCP Config:**
   - Edit `mcp_config.template.json` to define a custom set of MCP servers/tools for this role.
   - If this file is present, it will be used for all sessions created with this role.
   - If not present, the CLI will use the default MCP config.

## Example Files

- `docs/agent_instructions.md` — Example onboarding doc for this role
- `.env.sample` — Example environment template
- `mcp_config.template.json` — Example MCP config (see below)

## Example `mcp_config.template.json`
```json
{
  "mcpServers": {
    "custom_tool": {
      "command": "npx",
      "args": ["-y", "@custom/tool"],
      "env": {}
    },
    "taskmaster-ai": {
      "command": "npx",
      "args": ["-y", "--package=task-master-ai", "task-master-ai"],
      "env": {
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}",
        "MODEL": "claude-3-7-sonnet-20250219"
      }
    }
  }
}
```

## Notes
- To add a new role, copy this folder and rename it.
- The CLI will use the session name as the role name by default.
- If you want custom docs or tools for a session, create a matching role directory here.
