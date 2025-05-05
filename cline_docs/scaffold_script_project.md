# Team Scaffold Script Project

## Overview
A meta-driven scaffolding system that automates team setup using a single source of truth. The script generates standardized account names, configurations, and directory structures based on project metadata.

## Core Components

### 1. Input Collection (CLI Interface)
- Interactive questionnaire using `questionary`
- Collects:
  - Project name
  - Project description
  - Roles needed
  - Tools per role (LLM-suggested or user-overridden)
  - Email domain
  - Project prefix

### 2. Naming Convention Generator
Standardized naming patterns for all accounts:
- Emails: `{prefix}+{project}-{role}@{domain}`
- Slack handles: `@{project}-{role}`
- Bot names: `{project}_{role}_bot`
- Display names: `{Project} {Role}`
- GitHub accounts: `{project}-{role}`

### 3. Configuration Generation
Generates two key files:
- `crew.{teamname}.yaml`: Setup checklist and metadata
  ```yaml
  project:
    name: {project_name}
    description: {description}
    prefix: {prefix}
    domain: {domain}
  
  roles:
    - name: {role}
      tools:
        - {tool1}
        - {tool2}
      accounts:
        email: {generated_email}
        slack: {generated_handle}
        github: {generated_github}
        bot: {generated_bot}
      display_name: {generated_display}
  ```
- `.env.{teamname}`: Environment configuration
  ```env
  PROJECT_NAME={project_name}
  PROJECT_DESCRIPTION={description}
  ROLE_ACCOUNTS=...
  ```

### 4. Directory Structure
```
team-envs/
  ├── crew.{teamname}.yaml    # Setup checklist & metadata
  └── .env.{teamname}         # Environment configuration
```

## Workflow

1. **Initial Input**
   ```python
   project_info = questionary.prompt([
       Text("project_name", "Project name:"),
       Text("description", "Project description:"),
       Text("prefix", "Account prefix:"),
       Text("domain", "Email domain:"),
       Checkbox("roles", "Select roles:", choices=[
           "pm_guardian",
           "full_stack_dev",
           "db_guardian",
           "reviewer"
       ])
   ])
   ```

2. **Tool Suggestion**
   - LLM suggests appropriate tools per role
   - User can override/modify suggestions

3. **Name Generation**
   - Apply naming conventions
   - Generate all account names
   - Present for user review

4. **File Generation**
   - Create crew.{teamname}.yaml
   - Create .env.{teamname}
   - Generate any missing role directories/docs

5. **Output**
   - Display generated names and configurations
   - Show checklist for manual account creation
   - Provide next steps for team-cli usage

## Usage Example

```bash
# Run the scaffold script
python scaffold_team.py

# Follow interactive prompts
Project name: ledgerflow
Description: LedgerFlow AI Team
Prefix: greglindberg
Domain: gmail.com
Roles: [pm_guardian, full_stack_dev, db_guardian, reviewer]

# Review generated names
PM Guardian:
  - Email: greglindberg+ledgerflow-pm@gmail.com
  - Slack: @ledgerflow-pm
  - Bot: ledgerflow_pm_bot
  ...

# Confirm and generate files
Generated:
  - team-envs/crew.ledgerflow.yaml
  - team-envs/.env.ledgerflow
  ...
```

## Integration with Existing Tools

- Works alongside team-cli
- Focuses on initial setup and configuration
- Generates files needed by team-cli
- Provides clear handoff between setup and deployment

## Next Steps

1. Implement basic CLI interface
2. Build name generation system
3. Create YAML/env file generators
4. Add LLM tool suggestions
5. Integrate with team-cli
6. Add validation and error handling

# Only current, actionable scaffold script project documentation is kept here. All legacy, migration, and reorg notes have been moved to cline_docs/legacy/. 