---
trigger: always_on
description: >
  Enforce consistent code quality standards across the project, with specific guidelines for different file types and programming languages.
---

# Code Quality Standards

Follow these standards for all code modifications, generation, and reviews:

## General Standards

- Write self-documenting code with clear variable/function names.
- Include meaningful comments for complex logic.
- Keep functions focused on a single responsibility.
- Avoid deep nesting (>3 levels) when possible.
- Maintain consistent indentation and formatting.
- Limit line length to 100 characters when practical.

## Language-Specific Standards

### JavaScript/TypeScript
- Use camelCase for variables and functions.
- Use PascalCase for classes and component names.
- Prefer const over let, avoid var.
- Use async/await over direct Promise handling when possible.
- Add JSDoc comments for all functions and classes.

### Python
- Follow PEP 8 style guidelines.
- Use snake_case for variables and functions.
- Use PascalCase for class names.
- Include docstrings for all functions, classes, and modules.
- Use type hints where appropriate.

### CSS/SCSS
- Use kebab-case for class names and IDs.
- Group related properties.
- Use variables for repeated values.
- Maintain a logical structure (layout → box model → typography → visual).

## Documentation Standards

- Maintain up-to-date README.md files in all major directories.
- Document API endpoints with examples.
- Include setup instructions in the root README.md.
- Document architectural decisions in `systemPatterns.md`.
- Keep `techContext.md` updated with all dependencies and versions.
