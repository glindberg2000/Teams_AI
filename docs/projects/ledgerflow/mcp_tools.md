# MCP Tools Guide

This guide describes the Model Context Protocol (MCP) tools available to agents in this environment. Each tool provides specific capabilities and may require certain secrets to be set in your `.env` file.

---

## Available MCP Tools

### 1. Claude Task Master
- **Purpose:** Automates task management by parsing Product Requirements Documents (PRDs), generating tasks, prioritizing them, and managing dependencies.
- **Secrets Required:**
  - `ANTHROPIC_API_KEY`
  - `PERPLEXITY_API_KEY`
- **Key Commands:**
  - `parse-prd <file>`: Parses a PRD (e.g., scripts/prd.txt) to generate tasks in tasks/
  - `list`: Lists all tasks with IDs, priorities, and statuses
  - `next`: Shows the next task based on dependencies and priorities
  - `complete --id=<id>`: Marks a task as complete
  - `expand --id=<id>`: Generates subtasks for a task
  - `update --id=<id> --prompt=<prompt>`: Updates task requirements
  - `analyze-complexity`: Identifies tasks needing breakdown
  - `complexity-report`: Generates task complexity report
  - `validate-dependencies`: Checks task dependencies
- **Usage Examples:**
  - "Parse my PRD at scripts/prd.txt"
  - "Show the next task"
  - "Expand task 5 into subtasks"

### 2. GitHub
- **Purpose:** Manages GitHub repositories, issues, pull requests, and code searches.
- **Secrets Required:**
  - `GITHUB_PERSONAL_ACCESS_TOKEN`
- **Key Commands:**
  - `create-issue <title> <description>`: Creates new issue
  - `list-issues`: Lists open issues
  - `create-pull-request <branch> <title>`: Creates PR
  - `commit <message>`: Commits changes
  - `get-repo-info`: Gets repository details
  - `search-code <query>`: Searches repository code
- **Usage Examples:**
  - "Create a GitHub issue for bug #123"
  - "List open pull requests"
  - "Search code for authentication functions"

### 3. Slack
- **Purpose:** Team communication via Slack for messages, channels, and notifications.
- **Secrets Required:**
  - `SLACK_BOT_TOKEN`
  - `SLACK_TEAM_ID`
- **Key Commands:**
  - `send-message <channel> <text>`: Sends channel message
  - `list-channels`: Lists available channels
  - `post-update <channel> <milestone>`: Posts milestone update
  - `get-notifications`: Gets recent notifications
  - `create-slack-connect-invitation <channel>`: Creates invites
  - `view-emoji-reactions <channel>`: Views reactions
- **Usage Examples:**
  - "Send a Slack message to #dev-team about sprint completion"
  - "List available Slack channels"
  - "Post milestone update to #project-updates"

### 4. Context7
- **Purpose:** Documentation retrieval and summarization for APIs, frameworks, and libraries.
- **Secrets Required:** None
- **Key Commands:**
  - `search-docs <query>`: Searches documentation
  - `summarize-docs <url>`: Summarizes specific docs
  - `list-recent`: Lists recently accessed docs
- **Usage Examples:**
  - "Find documentation on GraphQL authentication"
  - "Summarize the React hooks documentation"
  - "List recently viewed documentation"

---

## Team Workflow Integration

The MCPs work together in the LedgerFlow_AI_Team workflow:

1. **Task Management Flow:**
   - Use Task Master for PRD parsing and task breakdown
   - Track progress and dependencies systematically
   - Analyze task complexity for better planning

2. **Development Flow:**
   - Use GitHub for code management and reviews
   - Create issues and PRs for tracked tasks
   - Search codebase for implementations

3. **Communication Flow:**
   - Use Slack for team updates and coordination
   - Post milestone completions and blockers
   - Maintain channel-specific communications

4. **Documentation Flow:**
   - Use Context7 for technical research
   - Reference and summarize relevant docs
   - Share findings with the team

## Notes
- Ensure all required secrets are set in your `.env` file before launching your session
- For command verification or additional details, you can ask "List available commands for [MCP name]"
- When in doubt about capabilities, ask "What MCPs are available?"
- Keep PRDs in the scripts/ directory for Task Master processing
- Follow the team's established channel structure for Slack communications 