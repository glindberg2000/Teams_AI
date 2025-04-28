# Tech Context

- Technologies used: Docker, DevContainer, Bash scripting, VS Code (with Windsurf extension), jq, Python (for app), Django, React, TailwindCSS, GitHub Actions.
- Development setup: Clone repo, use provided .devcontainer config, launch sessions via new_session.sh, manage secrets via .env files, and mount or clone codebase as needed.
- Technical constraints: No real secrets in repo, .env files ignored by Git, all agent sessions must be reproducible and isolated, and docs/configs must be injected automatically at build/startup. 