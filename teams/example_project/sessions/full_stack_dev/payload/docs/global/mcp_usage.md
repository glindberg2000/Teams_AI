# MCP Usage (Global)

## What is MCP?
- MCP (Model Context Protocol) is used for context sharing, automation, and agent orchestration.

## Setup
- Each agent/session has an MCP config generated from a template.
- Key environment variables are set in the .env file (e.g., GITHUB_PERSONAL_ACCESS_TOKEN, SLACK_BOT_TOKEN, SLACK_TEAM_ID).

## Best Practices
- Keep MCP config templates up to date with all required variables.
- Use environment variable substitution for secrets.
- Review generated configs before launching containers. 