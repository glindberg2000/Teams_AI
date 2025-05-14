from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from pathlib import Path
import subprocess
import os
import json
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
