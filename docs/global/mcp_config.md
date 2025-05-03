# MCP Configuration Guide

## Overview

The Model Context Protocol (MCP) enables AI agents to use tools and external services. This document explains how MCP is configured within the LedgerFlow AI Team framework.

## MCP Config File

Each agent session includes an MCP configuration file at `payload/mcp_config.json`. This file defines:

1. Which MCP servers to start
2. How to start each server (command and arguments)
3. Environment variables for each server

## Standard MCP Servers

The following MCP servers are typically included:

### Puppeteer

```json
"puppeteer": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-puppeteer"],
  "env": {}
}
```

Enables web browsing capabilities for the AI agent.

### GitHub

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token-here"
  }
}
```

Provides GitHub integration for repository management, issues, and PRs.

### Slack

```json
"slack": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": {
    "SLACK_BOT_TOKEN": "your-token-here",
    "SLACK_TEAM_ID": "your-team-id"
  }
}
```

Enables Slack communication for the AI agent.

### Context7

```json
"context7": {
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp@latest"]
}
```

Provides access to library documentation.

### Taskmaster

```json
"taskmaster-ai": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-taskmaster"],
  "env": {
    "ANTHROPIC_API_KEY": "your-key-here",
    "PERPLEXITY_API_KEY": "your-key-here",
    "MODEL": "claude-3-sonnet-20240229",
    "PERPLEXITY_MODEL": "sonar-medium-online",
    "MAX_TOKENS": "64000",
    "TEMPERATURE": "0.2",
    "DEFAULT_SUBTASKS": "5",
    "DEFAULT_PRIORITY": "medium",
    "DEBUG": "false",
    "LOG_LEVEL": "info"
  }
}
```

Provides task management capabilities for project planning and tracking.

## Customizing MCP Configuration

Each role can have a custom MCP configuration template at `roles/{role}/mcp_config.template.json`. This template can include variables like `${TEAM_NAME}` that will be replaced with values from the environment file.

When creating a session, the MCP configuration is generated based on:

1. The role's template if it exists
2. A default configuration otherwise

## Environment Variable Resolution

Environment variables in the MCP configuration are automatically resolved when sessions are created. For example:

```json
"env": {
  "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
}
```

Will be replaced with the actual token value from the environment file.

## Troubleshooting

If MCP servers fail to start:

1. Check the environment variables in the session's `.env` file
2. Verify the tokens and keys are valid
3. Check for errors in the MCP server logs
4. Run `fix_env_files.py` to clean up any template variables that weren't resolved 