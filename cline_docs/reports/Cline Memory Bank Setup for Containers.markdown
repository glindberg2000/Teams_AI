# Cline Memory Bank Setup for Containers

This setup outlines the directory structure, files, and workflows for containers using the Cline Memory Bank with Cursor/Windsurf, GitHub MCP integration, and Discord communication. It’s designed for an e-commerce web application with roles: DB Manager, Full Stack Dev, Reviewer, and Manager Agent.

## Directory Structure
```
/project_root
├── cline_docs_shared/
│   ├── productContext.md
│   ├── techContext.md
│   ├── progress.md
│   ├── prompts.md
├── cline_docs_db_manager/
│   ├── productContext.md
│   ├── activeContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   ├── progress.md
│   ├── role_instructions.md
│   ├── prompts.md
│   ├── feature_database_migration.md
│   ├── .windsurfrules
├── cline_docs_full_stack_dev/
│   ├── [similar files as above, tailored for Full Stack Dev]
├── cline_docs_reviewer/
│   ├── [similar files, tailored for Reviewer]
├── .git/
```

## 1. `cline_docs_shared/` Directory
**Purpose**: Stores common context accessible to all containers, synced via GitHub.

### Files
- `productContext.md`: Project purpose and user experience goals.
- `techContext.md`: Shared technologies and setup.
- `progress.md`: Aggregated project status from all roles.
- `prompts.md`: Common reusable prompts for cross-role tasks.

### Sample Files
#### `cline_docs_shared/productContext.md`
```markdown
# Product Context (Shared)

## Why This Project Exists
To create a scalable e-commerce platform with user authentication, product catalog, payment processing, and admin dashboard, solving fragmented shopping experiences.

## Problems It Solves
- Inefficient product discovery.
- Slow and insecure checkout processes.
- Lack of real-time inventory updates.

## How It Should Work
- Intuitive navigation with < 3-second page loads.
- Secure payments via third-party gateway.
- Mobile-first design for 70% of users.
```

#### `cline_docs_shared/techContext.md`
```markdown
# Tech Context (Shared)

## Technologies
- Frontend: React 18, Tailwind CSS, Redux.
- Backend: Node.js, Express, Prisma ORM.
- Database: PostgreSQL 15.
- Version Control: GitHub with MCP integration.
- Testing: Jest, React Testing Library.
- Communication: Discord with MCP.

## Development Setup
- Node.js v18+, PostgreSQL 15.
- Environment variables in `/.env`.
- Windsurf with Cascade and MCP servers.

## Constraints
- No server-side rendering due to budget.
- Must support Chrome, Firefox, Safari.
```

#### `cline_docs_shared/progress.md`
```markdown
# Progress (Shared)

## Overall Status
- Product catalog: 80% complete.
- User authentication: 50% complete.
- Payment integration: Not started.

## Role Contributions
- **DB Manager**: User and product tables implemented.
- **Full Stack Dev**: Register endpoint and login UI in progress.
- **Reviewer**: Reviewed product catalog code, pending auth review.

## Known Issues
- Search performance slow for large datasets.
- Missing error handling in auth endpoints.
```

#### `cline_docs_shared/prompts.md`
```markdown
# Reusable Prompts (Shared)

## Generate Test
“Write a Jest test for [FilePath] following patterns in systemPatterns.md.”

## Create PR
“Create a GitHub PR for branch [BranchName] with changes in [FileList]. Include a description based on progress.md.”
```

## 2. `cline_docs_db_manager/` Directory
**Purpose**: Role-specific context for the DB Manager, focusing on database tasks.

### Files
- `productContext.md`: Role-specific database goals.
- `activeContext.md`: Current database tasks and next steps.
- `systemPatterns.md`: Database architecture and patterns.
- `techContext.md`: Database-specific tools and constraints.
- `progress.md`: Database task status.
- `role_instructions.md`: DB Manager responsibilities and GitHub workflows.
- `prompts.md`: Database-specific prompts.
- `feature_database_migration.md`: Feature-specific documentation.
- `.windsurfrules`: Windsurf rules for Memory Bank (see above artifact).

### Sample Files
#### `cline_docs_db_manager/productContext.md`
```markdown
# Product Context (DB Manager)

## Role-Specific Context
- Design and optimize database schemas for user accounts, products, and transactions.
- Ensure data integrity and performance for high-concurrency queries.

## Role-Specific Goals
- Support 10,000 concurrent users with < 100ms query response times.
- Implement ACID-compliant transactions for payments.
```

#### `cline_docs_db_manager/activeContext.md`
```markdown
# Active Context (DB Manager)

## Current Work Focus
Designing transaction table in `/prisma/schema.prisma`.

## Recent Changes
- Added indexes to `products` table.
- Created migration for `users` table.

## Next Steps
- Optimize product search queries.
- Test transaction rollbacks.

## Active Decisions
- Use UUIDs for primary keys.
- Normalize tables to 3NF.
```

#### `cline_docs_db_manager/systemPatterns.md`
```markdown
# System Patterns (DB Manager)

## Database Architecture
- Relational model with PostgreSQL.
- Normalized schema with indexes on queried columns.
- Transaction management for payments.

## Design Patterns
- Repository pattern for data access.
- Foreign key constraints for integrity.

## Key Decisions
- Prisma ORM for migrations.
- Logical replication for scalability.
```

#### `cline_docs_db_manager/techContext.md`
```markdown
# Tech Context (DB Manager)

## Technologies
- PostgreSQL 15, Prisma ORM.
- pgAdmin for schema management.
- Jest for integration tests.

## Development Setup
- Local PostgreSQL: `postgresql://user:pass@localhost:5432/db`.
- Prisma CLI: `npx prisma migrate dev`.

## Constraints
- No NoSQL due to transaction needs.
- High-concurrency query support.
```

#### `cline_docs_db_manager/progress.md`
```markdown
# Progress (DB Manager)

## What Works
- User and product tables with CRUD operations.
- Initial migrations tested.

## What’s Left
- Transaction table schema.
- Search query optimization.

## Known Issues
- Index tuning needed for large datasets.
```

#### `cline_docs_db_manager/role_instructions.md`
```markdown
# Role Instructions (DB Manager)

## Responsibilities
- Design/maintain database schemas.
- Optimize queries for performance.
- Ensure data integrity/security.
- Create/test migrations.

## Best Practices
- Follow 3NF for schemas.
- Use indexes judiciously.
- Document migrations in `progress.md`.

## Tool Usage
- Prisma CLI: `npx prisma migrate dev`.
- pgAdmin: Schema visualization.
- Cursor/Windsurf: Query generation with “init memory”.
- GitHub MCP: Commit migrations to `db-manager` branch, create PRs.

## GitHub Workflow
- Branch: `db-manager/[feature]`.
- Commit: `cline_docs_db_manager/` and `/prisma/` changes.
- PR: Create PR to `main`, notify `#db-manager` on Discord.
- Merge: Manager Agent approves/merges.
```

#### `cline_docs_db_manager/prompts.md`
```markdown
# Reusable Prompts (DB Manager)

## Generate Schema
“Generate a Prisma schema for [TableName] with fields [FieldList]. Follow 3NF per systemPatterns.md.”

## Optimize Query
“Optimize SQL query: [Query]. Suggest indexes and explain improvements.”
```

#### `cline_docs_db_manager/feature_database_migration.md`
```markdown
# Feature: Database Migration for Transactions

## Objective
Add a transaction table to support payment processing.

## Requirements
- Fields: `id` (UUID), `userId` (UUID), `amount` (DECIMAL), `status` (ENUM).
- ACID compliance for payments.

## Implementation Steps
1. Update `/prisma/schema.prisma` with transaction model.
2. Run `npx prisma migrate dev`.
3. Test rollback in Jest.

## Testing Plan
- Unit tests: Schema validation.
- Integration tests: Transaction CRUD.
```

## 3. `cline_docs_full_stack_dev/` Directory
**Purpose**: Context for Full Stack Dev, focusing on API and frontend tasks.

### Files (Summary)
- Similar to DB Manager but tailored:
  - `productContext.md`: Focus on API and UI goals.
  - `activeContext.md`: Tracks API routes and React components.
  - `systemPatterns.md`: REST API and component patterns.
  - `techContext.md`: Node.js, React, and testing tools.
  - `progress.md`: API/UI task status.
  - `role_instructions.md`: API/UI development and GitHub PRs.
  - `prompts.md`: Prompts for routes and components.
  - `feature_authentication.md`: Authentication feature details.
  - `.windsurfrules`: Same as above.

### Sample File (Excerpt)
#### `cline_docs_full_stack_dev/role_instructions.md`
```markdown
# Role Instructions (Full Stack Dev)

## Responsibilities
- Develop REST API routes and React components.
- Implement business logic and UI.
- Write unit/integration tests.

## Best Practices
- Follow Airbnb JavaScript style guide.
- Use functional React components.
- Validate inputs with Joi.

## Tool Usage
- Windsurf: Code generation with “init memory”.
- Jest: `npm test` for tests.
- GitHub MCP: Commit to `full-stack/[feature]` branch, create PRs.

## GitHub Workflow
- Branch: `full-stack/[feature]`.
- Commit: `cline_docs_full_stack_dev/`, `/backend/`, `/frontend/`.
- PR: Create PR to `main`, notify `#full-stack-dev` on Discord.
- Merge: Manager Agent approves/merges.
```

## 4. `cline_docs_reviewer/` Directory
**Purpose**: Context for Reviewer, focusing on code quality and PR reviews.

### Files (Summary)
- Tailored for review tasks:
  - `productContext.md`: Focus on quality and compliance.
  - `activeContext.md`: Tracks PRs under review.
  - `systemPatterns.md`: Code review standards.
  - `techContext.md`: Review tools and constraints.
  - `progress.md`: Review status.
  - `role_instructions.md`: Review process and GitHub comments.
  - `prompts.md`: Prompts for PR comments.
  - `.windsurfrules`: Same as above.

### Sample File (Excerpt)
#### `cline_docs_reviewer/role_instructions.md`
```markdown
# Role Instructions (Reviewer)

## Responsibilities
- Review PRs for code quality, adherence to patterns.
- Provide feedback via GitHub comments.
- Approve/reject PRs.

## Best Practices
- Check against `systemPatterns.md`.
- Ensure tests pass.
- Flag security/performance issues.

## Tool Usage
- Windsurf: Review code with “init memory”.
- GitHub MCP: Post comments, approve PRs.
- Discord: Notify `#reviewer` of PR status.

## GitHub Workflow
- Review PRs in `main` from other roles.
- Comment via GitHub MCP.
- Approve/reject, notify Manager Agent via Discord.
```

## Setup Instructions
1. **Team Creator Initialization**:
   - Run the automation script to deploy containers (DB Manager, Full Stack Dev, Reviewer, Manager Agent).
   - Payload includes:
     - `cline_docs_shared/` in the GitHub repo.
     - `cline_docs_[role]/` for each container, with role-specific files.
     - `.windsurfrules` in each `cline_docs_[role]/`.
     - GitHub repo URL and Discord channel IDs.
     - MCP configurations for GitHub and Discord (see below).

2. **Container Configuration**:
   - Install Windsurf/Cursor with GitHub MCP server (`@github-mcp`) and Discord MCP server (if available).[](https://www.firecrawl.dev/blog/best-mcp-servers-for-cursor)[](https://cline.bot/mcp-marketplace)
   - Place `cline_docs_[role]/` and link to `cline_docs_shared/` (e.g., via repo clone).
   - Configure `.windsurfrules` in each container’s workspace.

3. **GitHub MCP Setup**:
   - Add GitHub MCP server to Windsurf:
     ```json
     {
       "mcpServers": {
         "@github-mcp": {
           "command": "node",
           "args": ["/path/to/github-mcp/index.js"],
           "env": { "GITHUB_TOKEN": "your-token" }
         }
       }
     }
     ```
     Location: `~/.codeium/windsurf/mcp_config.json` or `.vscode/mcp.json`.[](https://sebastian-petrus.medium.com/mcp-servers-in-windsurf-ai-f339df968705)
   - Tools: List repos, create branches, commit, create PRs, post comments.[](https://cline.bot/mcp-marketplace)
   - Workflow:
     - Commit: `cline_docs_[role]/` to `role/[feature]` branch.
     - PR: Create PR to `main` via `@github-mcp create_pr`.
     - Review: Reviewer uses `@github-mcp comment_pr` to post feedback.
     - Merge: Manager Agent uses `@github-mcp merge_pr`.

4. **Discord MCP Setup** (Optional):
   - If available, add Discord MCP server to post updates automatically:
     ```json
     {
       "mcpServers": {
         "@discord-mcp": {
           "command": "node",
           "args": ["/path/to/discord-mcp/index.js"],
           "env": { "DISCORD_TOKEN": "your-token" }
         }
       }
     }
     ```
   - Tools: Post messages, fetch channel updates.[](https://cline.bot/mcp-marketplace)
   - Fallback: Manually post `activeContext.md` snippets to Discord.

5. **Initialize Memory**:
   - In each container, prompt “init memory” to load `cline_docs_[role]/` and `cline_docs_shared/`.
   - Verify `[MEMORY BANK: ACTIVE]` in Cascade output.

6. **Task Execution**:
   - Manager Agent assigns tasks via Discord (e.g., `#db-manager: Design transaction table`).
   - Containers execute tasks, update `activeContext.md`/`progress.md`, commit via GitHub MCP.
   - Post updates to role-specific Discord channels.

7. **Sync Workflow**:
   - **Push**: Containers commit `progress.md` to `role/[feature]`, create PR to `main`.
   - **Pull**: Containers pull `cline_docs_shared/` from `main` daily.
   - **Manager Agent**: Reviews/merges PRs, updates shared `progress.md`.
   - **Discord**: Notify PR creation (`#role-channel`) and shared updates (`#shared-progress`).

8. **Validation**:
   - Containers run role-specific tests (e.g., Jest for DB Manager).
   - Reviewer validates PRs against `systemPatterns.md`.
   - Manager Agent ensures shared `progress.md` accuracy.

## Notes
- **GitHub MCP**: Ensure each container has a unique GitHub token with repo access. Restrict permissions (e.g., DB Manager: write to `/prisma/`, Full Stack Dev: write to `/backend/`, `/frontend/`).[](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- **Discord**: Create channels (`#db-manager`, `#full-stack-dev`, `#reviewer`, `#shared-progress`). Use bots for MCP-driven posts if available.[](https://neon.tech/guides/windsurf-mcp-neon)
- **Sync Automation**: Write a manager agent script to pull role-specific `progress.md`, merge into shared `progress.md`, and push to `main`. Run daily or after PR merges.
- **Security**: Add `.codeiumignore` to exclude sensitive files (e.g., `/.env`) from Windsurf indexing.[](https://codeparrot.ai/blogs/a-guide-to-using-windsurfai)
- **Scalability**: Add new roles by duplicating `cline_docs_[role]/` and updating the team creator.
- **Prompt Optimization**: Expand `prompts.md` for common tasks (e.g., PR creation, test generation).

This setup ensures role-specific focus, seamless GitHub integration, and efficient collaboration via Discord, leveraging the Cline Memory Bank for context persistence.