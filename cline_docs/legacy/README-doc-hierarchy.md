# Documentation Hierarchy & Inheritance (Legacy Reference)

This file is kept for reference in cline_docs/legacy/. See cline_docs/ for current Memory Bank and doc system.

## Doc Locations

- **cline_docs/**: Memory Bank for AI agent context only. Never inherited by containers.
- **docs/global/**: Global docs inherited by all containers (MCP, onboarding, security, tools, etc.).
- **docs/projects/{project}/**: Project-specific docs (requirements, architecture, team setup, etc.).
- **roles/{role}/docs/**: Role-specific docs (instructions, best practices, checklists for each agent type).

## Inheritance Order

```
global → project → role → session
```

- **Global docs** are always included in every session/container.
- **Project docs** are included for sessions belonging to that project.
- **Role docs** are included for sessions of that role.
- **Session docs** (payload/docs/) are the final, merged set for each agent.

## What Goes Where?

- **Global:** Anything all agents/roles need (MCP, Slack, security, onboarding, tools overview, etc.)
- **Project:** Project-specific requirements, architecture, team setup, workflows, etc.
- **Role:** What a Reviewer, DB Guardian, etc. should do; role-specific checklists and best practices.
- **cline_docs:** Only for AI agent memory/context. Not inherited by containers.

## Best Practices

- Never put repo-specific or AI_Team-only docs in global/project/role docs.
- Prune outdated or irrelevant docs regularly.
- Use stubs in roles/_templates/ for new role docs.
- Document any changes to this hierarchy in this README. 