# End-to-End Test Project Requirements

## Overview

This project serves as an end-to-end test for the LedgerFlow AI Team repository reorganization. The goal is to validate that all components of the system work together correctly after the reorganization.

## Test Objectives

1. Verify that the scaffold_team.py tool correctly creates team configuration files in the new directory structure
2. Verify that the team_cli.py tool correctly creates agent sessions based on the scaffold
3. Ensure that environment variables are properly resolved in .env files
4. Confirm that SSH keys are generated uniquely for each agent
5. Validate that documentation is correctly inherited (global → project → role)
6. Verify that MCP configuration is correct and token values are properly inserted

## Test Process

1. **Scaffold Creation**: Generate a test team using scaffold_team.py
2. **Configuration**: Fill in the generated config files with test data
3. **Session Creation**: Create agent sessions using team_cli.py
4. **Validation**: Verify all generated files and directories
5. **Documentation**: Document the results for PM review

## Team Structure

The test team will include three roles:

1. **PM Guardian**: Project management role
2. **Python Coder**: Development role
3. **Reviewer**: Code review role

## Expected Outputs

For each role, we expect to see:

1. A properly configured .env file in the payload directory
2. Unique SSH keys in the .ssh directory
3. Properly inherited documentation
4. A valid MCP configuration with resolved token values

## Success Criteria

The test is considered successful if:

1. All tools execute without errors
2. All expected files are created in the correct locations
3. Environment variables are properly resolved (no ${VAR} placeholders)
4. SSH keys are unique for each role
5. Documentation is correctly inherited
6. MCP configuration contains the correct token values

## Documentation

All test results should be documented in a comprehensive report that includes:

1. Commands executed
2. Directory structure created
3. Sample content of generated files (with sensitive values redacted)
4. Validation checks performed
5. Any issues encountered and their resolutions 