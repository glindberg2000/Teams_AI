# Project Overview

This document provides an overview of the project scope, goals, and context to help the AI agent understand the project it's working on.

## Project Purpose

The LedgerFlow AI Team project provides a framework for creating and managing AI agent teams that collaborate on software development and other tasks. It enables the orchestration of multiple specialized AI agents, each with their own role, working together to accomplish project goals.

## Key Features

- **Team Management**: Create and manage teams of AI agents with distinct roles
- **Role Specialization**: Configure agents with specialized knowledge and capabilities
- **Environment Isolation**: Each agent runs in its own isolated environment
- **Documentation Inheritance**: Global, project, and role-specific documentation
- **Secure Key Management**: Generate and manage SSH keys and API tokens
- **MCP Integration**: Configure MCP servers for AI agent capabilities

## Agent Roles

The framework supports various roles, including:

- **PM Guardian**: Project management, task tracking, and team coordination
- **Python Coder**: Python development, code generation, and refactoring
- **Reviewer**: Code reviews, quality assurance, and feedback
- **DB Guardian**: Database schema design, query optimization, and data management
- **Full Stack Dev**: Full-stack web development across frontend and backend

## Workflow

1. Define project requirements and goals
2. Create a team scaffold with appropriate roles
3. Configure environment variables and API keys
4. Launch agent sessions in their isolated environments
5. Agents collaborate through tools like GitHub, Slack, and shared repositories

## Technologies

- Python for team management tools
- Docker for environment isolation
- VSCode/Cursor DevContainer integration
- Git/GitHub for code management
- Slack for team communication
- Anthropic Claude for AI capabilities
- Perplexity for research capabilities

## Security Considerations

- API keys and tokens are stored in environment files
- SSH keys are generated uniquely for each agent
- Sensitive information is never committed to the repository
