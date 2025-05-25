---
trigger: model_decision
description: >
  Define specialized workflows and responsibilities for different project roles to ensure efficient collaboration and task management.
---

# Role-Based Workflows

Each role in the project has specific responsibilities and workflows to follow. These guidelines ensure consistent work quality and effective collaboration.

## Developer Role

- Focus on implementing features and fixing bugs according to specifications.
- Maintain `cline_docs_developer/` with up-to-date technical details.
- Document all implementation decisions in code comments and Memory Bank.
- Run tests locally before submitting code for review.
- Update `activeContext.md` when implementation details deviate from original plan.

## Reviewer Role

- Review PRs thoroughly for code quality, correctness, and adherence to standards.
- Provide specific, actionable feedback using GitHub's review tools.
- Verify Memory Bank updates accurately reflect code changes.
- Ensure tests cover new functionality adequately.
- Document review decisions in `cline_docs_reviewer/` for future reference.

## Architect Role

- Guide overall system design and technical direction.
- Maintain `systemPatterns.md` as the canonical source for architectural decisions.
- Review and approve major design changes before implementation.
- Document architecture decision records (ADRs) for significant choices.
- Ensure consistent patterns across the codebase.

## Manager Role

- Coordinate cross-team collaboration and task prioritization.
- Maintain project roadmap and milestone tracking.
- Facilitate resolution of blockers and dependencies.
- Sync shared `cline_docs_shared/` based on team updates.
- Communicate project status to stakeholders.

## Documentation Role

- Ensure comprehensive documentation for features and APIs.
- Maintain user-facing documentation for features.
- Review and improve developer documentation for clarity.
- Update `techContext.md` with changes to technologies or configurations.
- Create and maintain how-to guides for common development tasks.
