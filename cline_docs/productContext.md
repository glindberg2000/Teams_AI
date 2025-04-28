# Product Context

- Why this project exists: To provide a self-hosted, safety-first bookkeeping platform for ingesting PDFs & CSVs, classifying payees, and producing tax-ready reports, with robust backup/restore and agent-driven workflows.
- What problems it solves: Eliminates manual bookkeeping errors, automates classification and reporting, ensures data safety with automated backups, and supports team-based, auditable operations.
- How it should work: Runs in Docker containers, supports multiple agent sessions (PM, Dev, DB, Reviewer, Taskforce), injects static/dynamic docs and secrets at startup, and integrates with codebase and external services via configurable endpoints and secrets management. 