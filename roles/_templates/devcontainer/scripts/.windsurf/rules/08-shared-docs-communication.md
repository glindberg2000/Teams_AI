---
description: Guidelines for sharing and syncing project documentation using git-based workflows. Ensures all team members can collaborate on markdown docs across host, container, and remote environments.
globs: teams/*/cline_docs_shared/*, roles/_templates/devcontainer/scripts/.windsurf/rules/08-shared-docs-communication.md
alwaysApply: true
---

# Shared Docs Communication Protocol

## Purpose
- Enable all team members to share, update, and reference project documentation (markdown files) using git.
- Works across host, container, and remote sessions.
- Ensures a single source of truth for shared docs.

## Adding a New Doc
1. Create your file in the appropriate `cline_docs_shared/` folder.
2. `git add <filename>`
3. `git commit -m "Add <filename>"`
4. `git push`
5. Announce in chat: "Added <filename> to shared docs!"

## Getting New Docs
- If you have no local changes: `git pull`
- If you have local changes:
  - `git add . && git commit -m "WIP"` (or `git stash`)
  - `git pull`
  - (if stashed) `git stash pop`
- To get just one file:
  - `git fetch`
  - `git checkout origin/main -- <relative/path/to/filename>`

## Referencing Docs in Chat
- Use: `@cline_docs_shared:<filename>`
- Example: "See @cline_docs_shared:productContext.md for the latest requirements."

## Best Practices
- Pull before you start editing to avoid conflicts.
- Commit and push frequently.
- Communicate in chat when you add or update important docs.
- Use clear commit messages for documentation changes.

---

This rule is always copied into session payloads for reference. See also: `prompts.md` in `cline_docs_shared/` for reusable prompts and additional protocol details. 