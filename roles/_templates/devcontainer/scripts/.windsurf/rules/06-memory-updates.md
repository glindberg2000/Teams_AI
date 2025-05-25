---
trigger: always_on
description: >
  Guidelines for when and how to update Memory Bank files throughout the development process.
---

# Memory Bank Update Protocol

Follow these guidelines to ensure that Memory Bank files are updated consistently and thoroughly, maintaining perfect context across development cycles.

## When to Update

- After completing a significant feature or component.
- When making architectural or design pattern decisions.
- Upon discovering new technical constraints or requirements.
- After resolving complex bugs that impact understanding of the system.
- When onboarding new technologies or dependencies.
- At the end of each sprint or major milestone.
- When prompted with "update memory" by a user.

## Update Process

1. **activeContext.md**:
   - Update current task status.
   - Document recent changes and their impact.
   - Clarify next steps and priorities.
   - Note any blockers or dependencies.

2. **progress.md**:
   - Record completed work with dates.
   - Update overall project completion status.
   - Identify what's working and what needs attention.
   - Revise upcoming milestones if necessary.

3. **systemPatterns.md**:
   - Document any new patterns or architectural decisions.
   - Update diagrams or flow explanations if needed.
   - Explain rationale behind pattern changes.

4. **techContext.md**:
   - Add new technologies, libraries, or tools.
   - Update version information.
   - Document integration details and configuration.

## After Updates

1. Commit changes to GitHub with a descriptive message.
2. Post an update to the appropriate Discord channel.
3. Include the tag `[MEMORY BANK: UPDATED]` in your communication.
4. Summarize the key changes made to the Memory Bank.

## Update Quality

- Be concise but thorough in your documentation.
- Focus on information that future developers (or AI) would need to understand context.
- Use clear, consistent formatting for readability.
- Cross-reference related information between Memory Bank files when relevant.
