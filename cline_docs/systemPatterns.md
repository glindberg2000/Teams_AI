# System Patterns

- How the system is built: Each agent session runs in a Docker container, provisioned via DevContainer, with static docs copied at build and dynamic configs injected at startup.
- Key technical decisions: Use of shared and session-specific docs, .env-based secrets management, workspace mount for codebase, and entrypoint/postCreate/postStart hooks for extensibility.
- Architecture patterns: Modular session folders, shared doc templates, agent-specific prompts, and automated environment setup for reproducible onboarding and operation. 