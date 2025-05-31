# Reusable Prompts (Shared)

- [Prompt 1: Describe a common cross-role task.]
- [Prompt 2: Another reusable prompt for all roles.]

# How to Upload and Propagate Shared Docs

## Upload a Shared Doc (API)
- **Endpoint:** `POST /api/team/<team>/cline_docs_shared/<filename>`
- **Body:** Raw file content (text/plain)
- **Who:** Any agent or user with API access
- **Effect:** Uploads or updates `<filename>` in the team's canonical shared folder.

## Propagate a Shared Doc (API)
- **Endpoint (single file):** `POST /api/team/<team>/cline_docs_shared/propagate/<filename>`
- **Endpoint (all files):** `POST /api/team/<team>/cline_docs_shared/propagate`
- **Who:** Any agent or user with API access
- **Effect:** Copies the file(s) from the canonical shared folder to all session payloads and extra host paths.

## Recommended Workflow
1. Upload or update your doc using the upload endpoint.
2. Trigger propagation (single file or all files) to sync with all sessions/containers/hosts.
3. Use the UI or API for both steps.

**Note:** Propagation is explicit to prevent accidental overwrites. Only propagate when you want to sync the latest version to all destinations. 