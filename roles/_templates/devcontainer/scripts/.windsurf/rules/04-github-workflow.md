---
trigger: model_decision
description: >
  Define and enforce GitHub workflows for version control, collaboration, and integration with the Memory Bank system.
---

# GitHub Workflow Integration

Use these guidelines for all GitHub-related operations to maintain code quality and ensure proper documentation of changes.

## Branch Management

- Create feature branches from the main branch with descriptive names (format: `feature/brief-description`).
- Create bugfix branches with the format `fix/brief-description`.
- Ensure each branch addresses a single concern or feature.
- Keep branches up-to-date with the main branch.

## Commit Standards

- Write clear, concise commit messages in the imperative mood.
- Begin commit messages with a verb (e.g., "Add", "Fix", "Update", "Refactor").
- Keep the first line under 50 characters.
- For complex changes, add a detailed description after the first line.
- Reference issue numbers where applicable.

## Pull Request Process

- Create descriptive PR titles that summarize the change.
- Include a detailed description of changes and their purpose.
- Link related issues in the PR description.
- Ensure all tests pass before requesting review.
- Address review comments promptly and professionally.

## Memory Bank Integration

- When committing changes that affect project understanding or direction, update Memory Bank files.
- Include Memory Bank updates in the same PR as code changes they document.
- In PR descriptions, mention which Memory Bank files were updated and why.
- After merging PRs with Memory Bank changes, notify team members via Discord.
