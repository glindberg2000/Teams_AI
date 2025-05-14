from fastapi import FastAPI, HTTPException, Body, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from pathlib import Path
import subprocess
import os
import json
from pydantic import BaseModel
from typing import Optional, Dict
from fastapi.responses import JSONResponse, PlainTextResponse
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = Path(__file__).parent.parent.resolve()


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
        teams.append({"id": team_folder.name, "name": name, "description": description})
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
