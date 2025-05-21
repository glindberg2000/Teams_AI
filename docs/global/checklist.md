# TeamAI Quickstart Checklist

## 🚀 Quickstart (Recommended)

1. **Create a new Team** in the UI or CLI. No extra config needed for basic operation.
2. **Host GitHub SSH keys** are used by default for code access.
3. **Internal chat** is enabled out-of-the-box—no setup required.
4. **Project repo** will be cloned automatically (see .env for PROJECT_REPO_URL).
5. **Start your containers** and open the workspace in your preferred editor (e.g., VSCode, Cursor).

### Mandatory Environment Fields (in .env)
- `TEAM_NAME` (e.g., `TeamAI-Alpha`)
- `PROJECT_REPO_URL` (default: placeholder, set to your repo for code sync)
- `MCP_DISCORD_REPO_URL` (default: TeamAI fork)
- `MCP_DISCORD_REPO_BRANCH` (default: `main`)

---

## ⚙️ Optional/Advanced Configuration

- **Discord/Slack Integration:**
  - Add your tokens in `.env` to enable Discord/Slack bots.
  - Example: `DISCORD_TOKEN`, `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID`
- **Multiple GitHub Accounts:**
  - Add additional GitHub tokens in `.env` as needed.
- **Custom Docker Group/Network:**
  - These are auto-generated per team, but can be overridden in `.env` if needed.
- **Platform Integrations:**
  - See `mcp_config.json` for enabled tools. Advanced users can edit this file to enable/disable integrations.

---

## 📝 Next Steps
- For advanced scaling, see the full documentation in `docs/` or the Environment tab.
- To enable more platforms, simply add the relevant tokens and restart the container.
- For troubleshooting, check the container status and logs in the UI. 