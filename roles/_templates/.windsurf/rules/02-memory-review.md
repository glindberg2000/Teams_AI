---
trigger: manual
description: >
  Run a full memory review to verify and validate the completeness of the Memory Bank. Use this when context seems incomplete or after major project changes.
---

# Memory Bank Review

When triggered, perform a comprehensive review of all Memory Bank files to ensure completeness, accuracy, and consistency.

## Review Checklist

1. **File Existence Check**:
   - Verify all required files exist (`productContext.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`, `role_instructions.md`, `prompts.md`).
   - If any are missing, create them immediately based on available documentation and user input.

2. **Content Consistency Check**:
   - Ensure `activeContext.md` reflects current tasks and recent changes.
   - Verify `systemPatterns.md` is aligned with actual codebase patterns.
   - Confirm `techContext.md` lists all current technologies and dependencies.
   - Validate `progress.md` accurately reflects project status.

3. **Status Report**:
   - Generate a summary of the Memory Bank status.
   - Identify any gaps or inconsistencies requiring attention.
   - Provide recommendations for memory updates.

4. **Context Verification**:
   - Confirm understanding of the project scope, architecture, and goals.
   - Acknowledge context with `[MEMORY BANK: ACTIVE]` indicator.
   - Summarize key points from the Memory Bank to demonstrate context awareness.
