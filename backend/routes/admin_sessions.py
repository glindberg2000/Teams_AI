from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter()

# Use the root teams directory (not backend/teams)
TEAMS_ROOT = Path(__file__).parent.parent.parent / "teams"


# 1. List all sessions across all teams
@router.get("/api/admin/sessions")
def list_all_sessions():
    sessions = []
    for team_dir in TEAMS_ROOT.iterdir():
        if not team_dir.is_dir():
            continue
        team = team_dir.name
        sessions_dir = team_dir / "sessions"
        if not sessions_dir.exists() or not sessions_dir.is_dir():
            continue
        for session_dir in sessions_dir.iterdir():
            if session_dir.is_dir():
                session_id = session_dir.name  # e.g., 'python_coder'
                meta = {"team": team, "session_id": session_id}
                # Optionally load more metadata here
                sessions.append(meta)
    return sessions


# 2. Get session metadata/payload
@router.get("/api/admin/sessions/{team}/{session_id}")
def get_session_metadata(team: str, session_id: str):
    payload_dir = TEAMS_ROOT / team / "sessions" / session_id / "payload"
    if not payload_dir.exists():
        raise HTTPException(status_code=404, detail="Session payload not found")
    mcp_file = payload_dir / "mcp_config.json"
    if mcp_file.exists():
        try:
            return json.loads(mcp_file.read_text())
        except Exception:
            pass
    return {"team": team, "session_id": session_id}


# 3. Get session filesystem tree (start from payload/)
@router.get("/api/admin/sessions/{team}/{session_id}/filesystem")
def get_session_filesystem(team: str, session_id: str):
    payload_dir = TEAMS_ROOT / team / "sessions" / session_id / "payload"
    if not payload_dir.exists():
        raise HTTPException(status_code=404, detail="Session payload not found")

    def build_tree(path):
        if path.is_file():
            return {"name": path.name, "type": "file"}
        return {
            "name": path.name,
            "type": "directory",
            "children": [build_tree(child) for child in path.iterdir()],
        }

    return build_tree(payload_dir)


# 4. Get session config (payload/mcp_config.json)
@router.get("/api/admin/sessions/{team}/{session_id}/config")
def get_session_config(team: str, session_id: str):
    payload_dir = TEAMS_ROOT / team / "sessions" / session_id / "payload"
    mcp_file = payload_dir / "mcp_config.json"
    if not mcp_file.exists():
        raise HTTPException(status_code=404, detail="mcp_config.json not found")
    try:
        return json.loads(mcp_file.read_text())
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error parsing mcp_config.json: {e}"
        )


# 5. Get session health/status (check for .env, mcp_config.json, etc.)
@router.get("/api/admin/sessions/{team}/{session_id}/health")
def get_session_health(team: str, session_id: str):
    payload_dir = TEAMS_ROOT / team / "sessions" / session_id / "payload"
    if not payload_dir.exists():
        raise HTTPException(status_code=404, detail="Session payload not found")
    env_present = (payload_dir / ".env").exists()
    mcp_present = (payload_dir / "mcp_config.json").exists()
    # Add more health checks as needed (e.g., SSH keys, chat connection, etc.)
    return {
        "env_present": env_present,
        "mcp_config_present": mcp_present,
        # Add more fields as needed
    }


# TODO: Add authentication/authorization for admin endpoints
