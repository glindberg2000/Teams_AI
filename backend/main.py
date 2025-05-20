import sys
from pathlib import Path
import os

# Ensure the project root is in sys.path so 'tools' can be imported
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from fastapi import (
    FastAPI,
    HTTPException,
    Body,
    UploadFile,
    File,
    Request,
    Path,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from pathlib import Path
import subprocess
import json
from pydantic import BaseModel
from typing import Optional, Dict, List
from fastapi.responses import JSONResponse, PlainTextResponse
import logging
from fastapi.encoders import jsonable_encoder
from tools.scaffold_team import (
    generate_env_file,
    generate_env_template,
    generate_checklist,
    copy_cline_templates_and_rules,
)
from routes.team_files import router as team_files_router
from routes.admin_sessions import router as admin_sessions_router
from routes.chat import router as chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEAM_TEMPLATES_DIR = PROJECT_ROOT / "team_templates"
TEAM_TEMPLATES_DIR.mkdir(exist_ok=True)

app.include_router(team_files_router)
app.include_router(admin_sessions_router)
app.include_router(chat_router, prefix="/api/chat")

CHAT_PORT = int(os.environ.get("TEAM_CHAT_PORT", 8787))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/team/{project}/env-template")
def get_env_template(project: str):
    template_path = Path(f"teams/{project}/config/env.template")
    if not template_path.exists():
        raise HTTPException(status_code=404, detail="env.template not found")
    with open(template_path) as f:
        lines = f.readlines()
    keys = [
        line.split("=")[0].strip()
        for line in lines
        if "=" in line and not line.strip().startswith("#")
    ]
    return {"keys": keys, "raw": lines}


@app.get("/api/team/{project}/env")
def get_env(project: str):
    env_path = Path(f"teams/{project}/config/env")
    if not env_path.exists():
        raise HTTPException(status_code=404, detail="env file not found")
    with open(env_path) as f:
        lines = f.readlines()
    env = {}
    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return {"env": env, "raw": lines}


@app.put("/api/team/{project}/env")
def update_env(project: str, env=Body(...)):
    # Accept both dict and stringified JSON for compatibility
    if isinstance(env, str):
        env = json.loads(env)
    elif hasattr(env, "decode"):
        env = json.loads(env.decode())
    env_path = Path(f"teams/{project}/config/env")
    lines = [f"{k}={v}" for k, v in env.items()]
    env_path.parent.mkdir(parents=True, exist_ok=True)
    with open(env_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return {"status": "updated", "env_path": str(env_path)}


@app.post("/api/team/{project}/generate-crew")
def generate_crew(project: str):
    env_path = Path(f"teams/{project}/config/env")
    if not env_path.exists():
        raise HTTPException(status_code=404, detail="env file not found")
    # Stub: In production, run the CLI command to generate the crew
    # Example: subprocess.run(["python", "tools/team_cli.py", "create-crew", "--env-file", str(env_path)], check=True)
    return {"status": "crew generation triggered (stub)", "env_path": str(env_path)}


def get_env_path(project: str):
    return Path(f"teams/{project}/config/env")


def read_env_file(env_path: Path):
    if not env_path.exists():
        return {}
    with open(env_path, "r") as f:
        lines = f.readlines()
    env = {}
    for line in lines:
        if line.strip() and not line.strip().startswith("#"):
            if "=" in line:
                k, v = line.strip().split("=", 1)
                env[k] = v
    return env


def write_env_file(env_path: Path, env: dict):
    env_path.parent.mkdir(parents=True, exist_ok=True)
    with open(env_path, "w") as f:
        for k, v in env.items():
            f.write(f"{k}={v}\n")


@app.post("/api/team/{project}/secret")
def add_or_update_secret(project: str, body: dict = Body(...)):
    env_path = get_env_path(project)
    env = read_env_file(env_path)
    if not isinstance(body, dict) or len(body) != 1:
        raise HTTPException(
            status_code=400, detail="Body must be a single key-value pair."
        )
    k, v = list(body.items())[0]
    env[k] = v
    write_env_file(env_path, env)
    return {"status": "updated", "key": k, "value": v}


@app.get("/api/team/{project}/secret/{key}")
def get_secret(project: str, key: str):
    env_path = get_env_path(project)
    env = read_env_file(env_path)
    if key not in env:
        raise HTTPException(status_code=404, detail="Key not found.")
    return {"key": key, "value": env[key]}


@app.delete("/api/team/{project}/secret/{key}")
def delete_secret(project: str, key: str):
    env_path = get_env_path(project)
    env = read_env_file(env_path)
    if key not in env:
        raise HTTPException(status_code=404, detail="Key not found.")
    del env[key]
    write_env_file(env_path, env)
    return {"status": "deleted", "key": key}


@app.get("/api/team/{project}/secrets")
def list_secrets(project: str):
    env_path = get_env_path(project)
    env = read_env_file(env_path)
    return env


class RoleTemplate(BaseModel):
    name: str
    description: Optional[str] = None
    prompt: Optional[str] = None
    mcp_config: Optional[Dict] = None
    docs: Optional[str] = None


def get_roles_dir(project: str):
    return Path(f"teams/{project}/config/roles")


def get_role_path(project: str, name: str):
    return get_roles_dir(project) / f"{name}.json"


@app.get("/api/team/{project}/roles")
def list_roles(project: str):
    roles_dir = get_roles_dir(project)
    if not roles_dir.exists():
        return []
    roles = []
    for file in roles_dir.glob("*.json"):
        with open(file) as f:
            try:
                data = json.load(f)
                roles.append(data)
            except Exception:
                continue
    return roles


@app.post("/api/team/{project}/role")
def create_role(project: str, role: RoleTemplate):
    roles_dir = get_roles_dir(project)
    roles_dir.mkdir(parents=True, exist_ok=True)
    role_path = get_role_path(project, role.name)
    if role_path.exists():
        raise HTTPException(status_code=400, detail="Role already exists")
    with open(role_path, "w") as f:
        json.dump(role.dict(), f, indent=2)
    return {"status": "created", "role": role.dict()}


@app.get("/api/team/{project}/role/{name}")
def get_role(project: str, name: str):
    role_path = get_role_path(project, name)
    if not role_path.exists():
        raise HTTPException(status_code=404, detail="Role not found")
    with open(role_path) as f:
        data = json.load(f)
    return data


@app.put("/api/team/{project}/role/{name}")
def update_role(project: str, name: str, role=Body(...)):
    import json

    try:
        if isinstance(role, bytes):
            role = role.decode()
        if isinstance(role, str):
            role = json.loads(role)
        if not isinstance(role, dict):
            raise ValueError(f"Role body must be a dict, got {type(role)}")
        role_obj = RoleTemplate(**role)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    role_path = get_role_path(project, name)
    if not role_path.exists():
        raise HTTPException(status_code=404, detail="Role not found")
    with open(role_path, "w") as f:
        json.dump(role_obj.dict(), f, indent=2)
    return {"status": "updated", "role": role_obj.dict()}


@app.delete("/api/team/{project}/role/{name}")
def delete_role(project: str, name: str):
    role_path = get_role_path(project, name)
    if not role_path.exists():
        raise HTTPException(status_code=404, detail="Role not found")
    role_path.unlink()
    return {"status": "deleted", "name": name}


class ProjectConfig(BaseModel):
    name: str
    keys: Optional[dict] = None
    secrets: Optional[dict] = None
    docs: Optional[str] = None
    roles: Optional[dict] = None
    metadata: Optional[dict] = None


def get_config_path(project: str):
    return Path(f"teams/{project}/config/config.json")


@app.get("/api/team/{project}/config")
def get_project_config(project: str):
    config_path = get_config_path(project)
    if not config_path.exists():
        raise HTTPException(status_code=404, detail="Config not found")
    with open(config_path) as f:
        data = json.load(f)
    return data


@app.post("/api/team/{project}/config")
def create_project_config(project: str, config: ProjectConfig):
    config_path = get_config_path(project)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if config_path.exists():
        raise HTTPException(status_code=400, detail="Config already exists")
    with open(config_path, "w") as f:
        json.dump(config.dict(), f, indent=2)
    return {"status": "created", "config": config.dict()}


@app.put("/api/team/{project}/config")
def update_project_config(project: str, config=Body(...)):
    import json

    try:
        if isinstance(config, bytes):
            config = config.decode()
        if isinstance(config, str):
            config = json.loads(config)
        if not isinstance(config, dict):
            raise ValueError(f"Config body must be a dict, got {type(config)}")
        config_obj = ProjectConfig(**config)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    config_path = get_config_path(project)
    if not config_path.exists():
        raise HTTPException(status_code=404, detail="Config not found")
    with open(config_path, "w") as f:
        json.dump(config_obj.dict(), f, indent=2)
    return {"status": "updated", "config": config_obj.dict()}


@app.delete("/api/team/{project}/config")
def delete_project_config(project: str):
    config_path = get_config_path(project)
    if not config_path.exists():
        raise HTTPException(status_code=404, detail="Config not found")
    config_path.unlink()
    return {"status": "deleted", "project": project}


@app.get("/api/teams")
def list_teams():
    # Always resolve teams dir relative to project root unless TEAMS_DIR is set
    teams_dir = Path(os.environ.get("TEAMS_DIR", str(PROJECT_ROOT / "teams")))
    abs_path = teams_dir.resolve()
    print(f"[DEBUG] /api/teams: teams_dir absolute path: {abs_path}")
    if not teams_dir.exists() or not teams_dir.is_dir():
        print(
            f"[DEBUG] /api/teams: Directory does not exist or is not a dir: {abs_path}"
        )
        return JSONResponse(content=[], status_code=200)
    entries = list(teams_dir.iterdir())
    print(f"[DEBUG] /api/teams: Directory entries: {[e.name for e in entries]}")
    teams = []
    for team_folder in entries:
        if not team_folder.is_dir() or team_folder.name.startswith("_"):
            continue
        config_env = team_folder / "config" / "env"
        name = team_folder.name
        description = ""
        if config_env.exists():
            with open(config_env) as f:
                for line in f:
                    if line.startswith("TEAM_NAME="):
                        name = line.strip().split("=", 1)[1]
                    if line.startswith("TEAM_DESCRIPTION="):
                        description = line.strip().split("=", 1)[1]
        # --- New: Determine team status ---
        sessions_dir = team_folder / "sessions"
        status = "empty"
        if sessions_dir.exists() and sessions_dir.is_dir():
            session_statuses = []
            for s in sessions_dir.iterdir():
                if s.is_dir():
                    devcontainer = s / ".devcontainer"
                    payload_env = s / "payload/.env"
                    if devcontainer.exists() and payload_env.exists():
                        session_statuses.append("generated")
                    else:
                        session_statuses.append("scaffolded")
            if session_statuses:
                if all(st == "generated" for st in session_statuses):
                    status = "ready"
                elif any(st == "scaffolded" for st in session_statuses):
                    status = "scaffolded"
        teams.append(
            {
                "id": team_folder.name,
                "name": name,
                "description": description,
                "status": status,
            }
        )
    print(f"[DEBUG] /api/teams: Returning teams: {teams}")
    return JSONResponse(content=teams)


@app.get("/api/roles")
def list_global_roles():
    # Always resolve roles dir relative to project root unless ROLES_DIR is set
    roles_dir = Path(os.environ.get("ROLES_DIR", str(PROJECT_ROOT / "roles")))
    abs_path = roles_dir.resolve()
    print(f"[DEBUG] /api/roles: roles_dir absolute path: {abs_path}")
    if not roles_dir.exists() or not roles_dir.is_dir():
        print(
            f"[DEBUG] /api/roles: Directory does not exist or is not a dir: {abs_path}"
        )
        return JSONResponse(content=[], status_code=200)
    roles = []
    for role_folder in roles_dir.iterdir():
        if not role_folder.is_dir() or role_folder.name.startswith("_"):
            continue
        name = role_folder.name
        description = ""
        overview_md = role_folder / "docs" / "role_overview.md"
        if overview_md.exists():
            try:
                with open(overview_md) as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.strip() and not line.strip().startswith("#"):
                            description = line.strip()
                            break
            except Exception as e:
                print(f"[DEBUG] /api/roles: Error reading {overview_md}: {e}")
                description = ""
        else:
            print(f"[DEBUG] /api/roles: Missing {overview_md}")
        roles.append({"id": role_folder.name, "name": name, "description": description})
    print(f"[DEBUG] /api/roles: Returning roles: {roles}")
    return JSONResponse(content=roles)


@app.get("/api/role/{role}/overview")
def get_role_overview(role: str):
    overview_path = PROJECT_ROOT / "roles" / role / "docs" / "role_overview.md"
    if not overview_path.exists():
        return PlainTextResponse("", status_code=200)
    return PlainTextResponse(overview_path.read_text())


@app.get("/api/role/{role}/env-sample")
def get_role_env_sample(role: str):
    env_sample_path = PROJECT_ROOT / "roles" / role / ".env.sample"
    if not env_sample_path.exists():
        return JSONResponse(content="", status_code=200)
    return env_sample_path.read_text()


@app.get("/api/role/{role}/mcp-config")
def get_role_mcp_config(role: str):
    mcp_config_path = PROJECT_ROOT / "roles" / role / "mcp_config.template.json"
    if not mcp_config_path.exists():
        return JSONResponse(content="", status_code=200)
    try:
        with open(mcp_config_path) as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        print(f"[DEBUG] /api/role/{{role}}/mcp-config: {e}")
        return JSONResponse(content="", status_code=200)


@app.put("/api/role/{role}/overview")
def update_role_overview(role: str, content: str = Body(...)):
    overview_path = PROJECT_ROOT / "roles" / role / "docs" / "role_overview.md"
    overview_path.parent.mkdir(parents=True, exist_ok=True)
    overview_path.write_text(content)
    return {"status": "updated"}


@app.put("/api/role/{role}/env-sample")
def update_role_env_sample(role: str, content: str = Body(...)):
    env_sample_path = PROJECT_ROOT / "roles" / role / ".env.sample"
    env_sample_path.parent.mkdir(parents=True, exist_ok=True)
    env_sample_path.write_text(content)
    return {"status": "updated"}


@app.put("/api/role/{role}/mcp-config")
def update_role_mcp_config(role: str, content: str = Body(...)):
    mcp_config_path = PROJECT_ROOT / "roles" / role / "mcp_config.template.json"
    mcp_config_path.parent.mkdir(parents=True, exist_ok=True)
    mcp_config_path.write_text(content)
    return {"status": "updated"}


@app.post("/api/role")
def create_role_template(role: str = Body(...)):
    role_dir = PROJECT_ROOT / "roles" / role
    docs_dir = role_dir / "docs"
    if role_dir.exists():
        raise HTTPException(status_code=400, detail="Role already exists")
    docs_dir.mkdir(parents=True, exist_ok=True)
    (role_dir / ".env.sample").write_text("# Fill in environment variables\n")
    (role_dir / "mcp_config.template.json").write_text("{}\n")
    (docs_dir / "role_overview.md").write_text(
        f"# {role} Role Overview\n\nDescribe the role here.\n"
    )
    return {"status": "created", "role": role}


@app.delete("/api/role/{role}")
def delete_role_template(role: str):
    import shutil

    role_dir = PROJECT_ROOT / "roles" / role
    if not role_dir.exists():
        raise HTTPException(status_code=404, detail="Role not found")
    shutil.rmtree(role_dir)
    return {"status": "deleted", "role": role}


@app.get("/api/team-templates")
def list_team_templates():
    templates = []
    for file in TEAM_TEMPLATES_DIR.glob("*.json"):
        with open(file) as f:
            try:
                data = json.load(f)
                templates.append({"name": file.stem, **data})
            except Exception:
                continue
    return JSONResponse(content=templates)


@app.get("/api/team-template/{template_name}")
def get_team_template(template_name: str):
    path = TEAM_TEMPLATES_DIR / f"{template_name}.json"
    if not path.exists():
        return JSONResponse(content="", status_code=404)
    with open(path) as f:
        data = json.load(f)
    return JSONResponse(content=data)


@app.post("/api/team-template")
def create_team_template(template=Body(...)):
    name = template.get("name")
    if not name:
        return JSONResponse(content={"error": "Missing template name"}, status_code=400)
    path = TEAM_TEMPLATES_DIR / f"{name}.json"
    if path.exists():
        return JSONResponse(
            content={"error": "Template already exists"}, status_code=400
        )
    with open(path, "w") as f:
        json.dump(template, f, indent=2)
    return {"status": "created", "template": template}


@app.put("/api/team-template/{template_name}")
def update_team_template(template_name: str, template=Body(...)):
    path = TEAM_TEMPLATES_DIR / f"{template_name}.json"
    if not path.exists():
        return JSONResponse(content={"error": "Template not found"}, status_code=404)
    with open(path, "w") as f:
        json.dump(template, f, indent=2)
    return {"status": "updated", "template": template}


@app.delete("/api/team-template/{template_name}")
def delete_team_template(template_name: str):
    path = TEAM_TEMPLATES_DIR / f"{template_name}.json"
    if not path.exists():
        return JSONResponse(content={"error": "Template not found"}, status_code=404)
    path.unlink()
    return {"status": "deleted", "template": template_name}


@app.post("/api/instantiate-team")
def instantiate_team(request: Request):
    import asyncio
    import logging

    try:
        data = request.json() if hasattr(request, "json") else None
        if asyncio.iscoroutine(data):
            data = asyncio.run(data)
        if not data:
            data = request._json
        print(f"[DEBUG] Incoming instantiate-team data: {data}")
        name = data.get("name")
        description = data.get("description", "")
        comm_type = data.get("commType", "internal")
        template_name = data.get("template")
        print(f"[DEBUG] name={name}, template_name={template_name}")
        if not name or not template_name:
            print("[DEBUG] Missing team name or template in request")
            return JSONResponse(
                content={"error": "Missing team name or template"}, status_code=400
            )
        # Load template
        template_path = TEAM_TEMPLATES_DIR / f"{template_name}.json"
        print(f"[DEBUG] Resolved template_path: {template_path}")
        if not template_path.exists():
            print(f"[DEBUG] Template not found at {template_path}")
            return JSONResponse(
                content={"error": "Template not found"}, status_code=404
            )
        with open(template_path) as f:
            template = json.load(f)
        print(f"[DEBUG] Loaded template: {template}")
        # Create team dir
        team_dir = PROJECT_ROOT / "teams" / name
        if team_dir.exists():
            print(f"[DEBUG] Team dir already exists: {team_dir}")
            return JSONResponse(
                content={"error": "Team already exists"}, status_code=400
            )
        team_dir.mkdir(parents=True, exist_ok=True)
        # Write config
        config = {
            "name": name,
            "description": description,
            "commType": comm_type,
            "roles": template.get("roles", []),
            "teamDocs": template.get("teamDocs", ""),
            "template": template_name,
        }
        with open(team_dir / "config.json", "w") as f:
            json.dump(config, f, indent=2)

        # --- NEW: Run full scaffold logic ---
        try:
            roles = config["roles"]
            prefix = data.get("prefix", "user")
            domain = data.get("domain", "example.com")
            print(
                f"[DEBUG] Scaffolding with roles={roles}, prefix={prefix}, domain={domain}"
            )
            generate_env_file(name, prefix, domain, roles, dry_run=False)
            generate_env_template(name, roles, dry_run=False)
            generate_checklist(name, roles, dry_run=False)
            copy_cline_templates_and_rules(name, roles, dry_run=False)
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(f"[DEBUG] Scaffold failed: {e}")
            return JSONResponse(
                content={"error": f"Scaffold failed: {e}"}, status_code=500
            )
        # --- END SCAFFOLD ---

        return {"status": "created", "team": config}
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"[DEBUG] Unexpected error in instantiate_team: {e}")
        return JSONResponse(
            content={"error": f"Unexpected error: {e}"}, status_code=500
        )


@app.get("/api/team/{team_id}")
def get_team(team_id: str):
    team_dir = PROJECT_ROOT / "teams" / team_id
    config_path = team_dir / "config.json"
    if not config_path.exists():
        return JSONResponse(content={"error": "Team not found"}, status_code=404)
    with open(config_path) as f:
        config = json.load(f)
    return config


@app.put("/api/team/{team_id}")
def update_team(team_id: str, data=Body(...)):
    team_dir = PROJECT_ROOT / "teams" / team_id
    config_path = team_dir / "config.json"
    if not config_path.exists():
        return JSONResponse(content={"error": "Team not found"}, status_code=404)
    with open(config_path, "w") as f:
        json.dump(data, f, indent=2)
    return {"status": "updated", "team": data}


@app.delete("/api/team/{team_id}")
def delete_team(team_id: str):
    import shutil

    team_dir = PROJECT_ROOT / "teams" / team_id
    if not team_dir.exists():
        return JSONResponse(content={"error": "Team not found"}, status_code=404)
    shutil.rmtree(team_dir)
    return {"status": "deleted", "team": team_id}


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, team_id: str, websocket: WebSocket):
        await websocket.accept()
        if team_id not in self.active_connections:
            self.active_connections[team_id] = []
        self.active_connections[team_id].append(websocket)

    def disconnect(self, team_id: str, websocket: WebSocket):
        if team_id in self.active_connections:
            self.active_connections[team_id].remove(websocket)
            if not self.active_connections[team_id]:
                del self.active_connections[team_id]

    async def broadcast(self, team_id: str, message: dict):
        if team_id in self.active_connections:
            for connection in self.active_connections[team_id]:
                await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws/{team_id}")
async def websocket_endpoint(websocket: WebSocket, team_id: str):
    await manager.connect(team_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Expecting {"user": ..., "message": ...}
            store_message(team_id, data.get("user"), data.get("message"), channel=None)
            await manager.broadcast(team_id, data)
    except WebSocketDisconnect:
        manager.disconnect(team_id, websocket)


# --- BEGIN: In-memory message store for chat history (prototype) ---
from threading import Lock
from datetime import datetime
import re

MESSAGE_STORE = {}  # team_id -> list of messages
MESSAGE_ID_COUNTER = {}  # team_id -> int
MESSAGE_STORE_LOCK = Lock()
# NEW: Per-user, per-team last read message id
LAST_READ_MESSAGE_ID = {}  # (team_id, user) -> int

# Message format: {"id": int, "user": str, "message": str, "timestamp": str, "channel": str or None}


def store_message(team_id, user, message, channel=None):
    with MESSAGE_STORE_LOCK:
        if team_id not in MESSAGE_STORE:
            MESSAGE_STORE[team_id] = []
            MESSAGE_ID_COUNTER[team_id] = 1
        msg_id = MESSAGE_ID_COUNTER[team_id]
        msg = {
            "id": msg_id,
            "user": user,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "channel": channel,
        }
        MESSAGE_STORE[team_id].append(msg)
        MESSAGE_ID_COUNTER[team_id] += 1
        return msg


def get_messages(
    team_id,
    since_message_id=None,
    sender=None,
    limit=20,
    mention_only=False,
    dm_only=False,
    content_regex=None,
):
    with MESSAGE_STORE_LOCK:
        msgs = MESSAGE_STORE.get(team_id, [])
        # Filter by since_message_id
        if since_message_id is not None:
            msgs = [m for m in msgs if m["id"] > int(since_message_id)]
        # Filter by sender
        if sender:
            msgs = [m for m in msgs if m["user"] == sender]
        # Filter by mention_only (if implemented)
        # For now, just a placeholder: if mention_only, only messages containing '@' (simulate mention)
        if mention_only:
            msgs = [m for m in msgs if "@" in m["message"]]
        # Filter by dm_only (not implemented, placeholder)
        # If dm_only, only messages with channel == None
        if dm_only:
            msgs = [m for m in msgs if not m.get("channel")]
        # Filter by content_regex
        if content_regex:
            msgs = [m for m in msgs if re.search(content_regex, m["message"])]
        # Sort by id ascending (oldest to newest)
        msgs = sorted(msgs, key=lambda m: m["id"])
        # Apply limit
        return msgs[:limit]


# --- END: In-memory message store ---


@app.get("/api/team/{team_id}/messages")
def get_team_messages(
    team_id: str,
    user: str,  # REQUIRED for unread tracking
    limit: int = 20,
    mention_only: bool = False,
    dm_only: bool = False,
    content_regex: str = None,
    request: Request = None,
):
    """
    Retrieve unread messages for a user in a team.
    - user: required, the user requesting messages
    - limit: max number of messages (default 20)
    """
    print(
        f"[DEBUG] GET /api/team/{team_id}/messages: method={request.method if request else 'GET'}, path={request.url if request else ''}, query={request.query_params if request else ''}"
    )
    # Get last read message id for this user/team
    last_read_id = LAST_READ_MESSAGE_ID.get((team_id, user), 0)
    # Get all messages with id > last_read_id
    msgs = get_messages(
        team_id,
        since_message_id=last_read_id,
        limit=limit,
        mention_only=mention_only,
        dm_only=dm_only,
        content_regex=content_regex,
    )
    # Update last read id if any messages returned
    if msgs:
        LAST_READ_MESSAGE_ID[(team_id, user)] = msgs[-1]["id"]
    return {"messages": msgs}


# --- MessageFilter model for advanced filtering ---
class MessageFilter(BaseModel):
    user: Optional[str] = None  # For unread tracking
    channels: Optional[List[str]] = None  # If None, default to ["general"]
    dm_only: Optional[bool] = None
    mention_only: Optional[bool] = None
    content_regex: Optional[str] = None
    from_user: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None
    sort: Optional[str] = "asc"
    limit: Optional[int] = 20


# --- Helper: filter messages using MessageFilter ---
def filter_messages(team_id, filter: MessageFilter, since_message_id=None):
    with MESSAGE_STORE_LOCK:
        msgs = MESSAGE_STORE.get(team_id, [])
        # Filter by since_message_id (for unread tracking)
        if since_message_id is not None:
            msgs = [m for m in msgs if m["id"] > int(since_message_id)]
        # Filter by user (from_user = sender, user = recipient)
        if filter.from_user:
            msgs = [m for m in msgs if m["user"] == filter.from_user]
        # Filter by channels
        if filter.channels:
            msgs = [m for m in msgs if m.get("channel", "general") in filter.channels]
        # Filter by mention_only
        if filter.mention_only:
            msgs = [m for m in msgs if "@" in m["message"]]
        # Filter by dm_only
        if filter.dm_only:
            msgs = [m for m in msgs if not m.get("channel")]
        # Filter by content_regex
        if filter.content_regex:
            import re

            msgs = [m for m in msgs if re.search(filter.content_regex, m["message"])]
        # Filter by before/after timestamp
        if filter.before:
            msgs = [m for m in msgs if m["timestamp"] < filter.before]
        if filter.after:
            msgs = [m for m in msgs if m["timestamp"] > filter.after]
        # Sort
        reverse = filter.sort == "desc"
        msgs = sorted(msgs, key=lambda m: m["id"], reverse=reverse)
        # Apply limit
        return msgs[: (filter.limit or 20)]


# --- New: POST endpoint for advanced message queries ---
@app.post("/api/team/{team_id}/messages/query")
def query_team_messages(
    team_id: str, filter: MessageFilter = Body(...), request: Request = None
):
    print(
        f"[DEBUG] POST /api/team/{team_id}/messages/query: method={request.method if request else 'POST'}, path={request.url if request else ''}, body={filter.dict() if filter else ''}"
    )
    # Sensible defaults
    if not filter.channels:
        filter.channels = ["general"]
    if not filter.limit:
        filter.limit = 20
    # For unread tracking, use last_read_id if user is specified
    since_message_id = None
    if filter.user:
        since_message_id = LAST_READ_MESSAGE_ID.get((team_id, filter.user), 0)
    msgs = filter_messages(team_id, filter, since_message_id=since_message_id)
    # Update last read id if any messages returned and user is specified
    if msgs and filter.user:
        LAST_READ_MESSAGE_ID[(team_id, filter.user)] = msgs[-1]["id"]
    return {"messages": msgs}


# Add a global exception handler for 422 errors
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request as StarletteRequest


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: StarletteRequest, exc: RequestValidationError
):
    print(
        f"[ERROR] 422 Unprocessable Content: {exc.errors()} | body={await request.body()}"
    )
    return JSONResponse(
        status_code=422,
        content={
            "detail": "422 Unprocessable Content: Check that you are using the correct endpoint and request format. For GET /messages, use query parameters only. For POST /messages/query, use a JSON body matching the MessageFilter model.",
            "errors": exc.errors(),
        },
    )
