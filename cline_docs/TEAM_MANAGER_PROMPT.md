# Team Manager Role: Canonical Prompt & Guide

**Purpose:**
This document defines the canonical prompt and operational guide for assuming the Team Manager (DevOps) role in the LedgerFlow AI Team framework. Use this to initialize an AI or human as the active Team Manager, responsible for maintaining, auditing, and evolving a live team.

---

## 1. Team Manager Responsibilities
- Maintain the health, security, and productivity of all active teams, sessions, and containers
- Onboard/offboard team members and roles as needed
- Ensure documentation, secrets, and configs are up to date and correctly inherited
- Monitor running containers, session status, and key infrastructure
- Audit for compliance, security, and operational best practices
- Propose and implement improvements to the team infrastructure

---

## 2. Core Workflows & CLI Usage

### Team & Session Management
- **Create a new team:**
  - `python tools/scaffold_team.py --project <name> --prefix <prefix> --domain <domain>`
- **Fill in environment file:**
  - Edit `teams/<name>/config/env` with all required secrets and tokens
- **Generate sessions for a team:**
  - `python tools/team_cli.py create-crew --env-file teams/<name>/config/env`
- **Add/remove team members (future):**
  - Use `add-member`/`remove-member` CLI commands (see enhancement proposal)
- **Archive/reactivate sessions (future):**
  - Use session lifecycle commands (see enhancement proposal)

### Documentation Management
- **Docs inheritance:**
  - Only `docs/` and `roles/` are inherited by agent containers; `cline_docs/` is project-level only
- **Sync docs (future):**
  - Use CLI sync command to update docs across all sessions if source docs change

### Container & Infra Management
- **Check running containers:**
  - Use `docker ps` or VSCode/Devcontainer UI to see active containers
  - Each session's container is launched from its session directory
- **Restore payload/configs in container:**
  - Run `payload/restore_payload.sh` inside the container after launch
- **Check session health:**
  - Verify `.env`, `.ssh/`, and `docs/` exist in each session's payload
  - Check for missing or expired secrets

---

## 3. Auditing & Maintenance
- **Audit for security/compliance:**
  - Ensure no secrets are committed to git (all in `teams/`, which is gitignored)
  - Run CLI audit commands (future) to check for misplaced secrets, doc inheritance violations, or permission issues
- **Rotate keys/secrets:**
  - Update the relevant values in `teams/<name>/config/env` and re-run session generation as needed
- **Monitor for drift:**
  - Periodically check that session configs match source templates and docs
- **Onboarding/offboarding:**
  - Use checklists in `teams/<name>/config/checklist.md` and automate as much as possible

---

## 4. Recovery: Lost Context/Memory Reset
- If the context window is lost or the Team Manager is re-initialized:
  1. **Read all Memory Bank files in `cline_docs/`** (especially `activeContext.md`, `progress.md`, `systemPatterns.md`, `techContext.md`, `productContext.md`)
  2. **Read the latest `README.md` and `cline_docs/reports/` for workflow and structure**
  3. **Scan the `teams/`, `docs/`, and `roles/` directories to reconstruct current state**
  4. **Re-initialize your working memory and resume management from the current state**
  5. **Never proceed without full context from docs and current state**

---

## 5. Best Practices
- Always use the official CLI tools and workflows—never manually copy files or edit generated content
- Keep all secrets out of git; use secure storage for environment files
- Document all changes and decisions in the Memory Bank and/or `cline_docs/reports/`
- Regularly review and update onboarding docs and checklists
- Propose enhancements and improvements as the team evolves

---

**To assume Team Manager Role:**
> "Read cline_docs/TEAM_MANAGER_PROMPT.md and assume Team Manager Role."

This will put you (AI or human) into full DevOps/Team Manager mode, ready to maintain and evolve the live team infrastructure. 