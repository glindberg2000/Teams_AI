# E2E Test Project Overview

## Project Purpose

This project is an end-to-end test of the LedgerFlow AI Team framework after repository reorganization. It validates that the new directory structure and tooling work correctly for creating and managing teams of AI agents.

## Goals

1. Verify the functionality of the restructured repository
2. Test the scaffold_team.py and team_cli.py tools
3. Ensure proper environment variable resolution
4. Validate documentation inheritance
5. Verify MCP configuration generation

## Project Scope

The scope of this project is limited to verifying that the repository reorganization was successful. It does not include developing any new features or capabilities.

## Team Structure

This project includes three AI agents with distinct roles:

- **PM Guardian**: Oversees project management and coordination
- **Python Coder**: Responsible for Python development
- **Reviewer**: Handles code reviews and quality assurance

## Timeline

This is a one-time validation test with no ongoing timeline.

## Technical Requirements

- Python 3.7+
- Docker for container orchestration
- SSH key generation capabilities
- API keys for external services (placeholders used for testing)

## Success Criteria

The test is successful if:

1. Team scaffolding is correctly generated
2. Agent sessions are properly created
3. Environment variables are correctly resolved
4. Documentation is properly inherited
5. MCP configuration is correctly generated

## Stakeholders

- Project Manager: Responsible for verifying test results
- Engineering Team: Responsible for maintaining repository structure
- AI Agent Users: Benefit from reliable infrastructure 