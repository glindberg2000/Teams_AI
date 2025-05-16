from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
    Body,
    BackgroundTasks,
    Request,
)
from fastapi.responses import PlainTextResponse
from pathlib import Path
import os
import shutil
import subprocess
import tempfile

router = APIRouter()

TEAMS_ROOT = Path(__file__).parent.parent.parent / "teams"
GLOBAL_DOCS_ROOT = Path(__file__).parent.parent.parent / "docs" / "global"
TEMPLATES_ROOT = (
    Path(__file__).parent.parent.parent / "roles" / "_templates" / "cline_docs_shared"
)


@router.get("/api/team/{team}/config/env", response_class=PlainTextResponse)
def get_env_file(team: str):
    env_path = TEAMS_ROOT / team / "config" / "env"
    if not env_path.exists():
        raise HTTPException(status_code=404, detail="env file not found")
    return env_path.read_text()


@router.put("/api/team/{team}/config/env")
def update_env_file(team: str, content: str):
    env_path = TEAMS_ROOT / team / "config" / "env"
    env_path.parent.mkdir(parents=True, exist_ok=True)
    env_path.write_text(content)
    return {"status": "ok"}


@router.get("/api/team/{team}/config/env.template", response_class=PlainTextResponse)
def get_env_template(team: str):
    path = TEAMS_ROOT / team / "config" / "env.template"
    if not path.exists():
        raise HTTPException(status_code=404, detail="env.template not found")
    return path.read_text()


@router.get("/api/team/{team}/config/checklist", response_class=PlainTextResponse)
def get_checklist(team: str):
    path = TEAMS_ROOT / team / "config" / "checklist.md"
    if not path.exists():
        raise HTTPException(status_code=404, detail="checklist.md not found")
    return path.read_text()


@router.put("/api/team/{team}/config/checklist")
def update_checklist(team: str, content: str):
    path = TEAMS_ROOT / team / "config" / "checklist.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return {"status": "ok"}


@router.get("/api/team/{team}/cline_docs_shared")
def list_cline_docs_shared(team: str):
    dir_path = TEAMS_ROOT / team / "cline_docs_shared"
    if not dir_path.exists():
        return []
    return [f.name for f in dir_path.glob("*.md") if f.is_file()]


@router.get(
    "/api/team/{team}/cline_docs_shared/{filename}", response_class=PlainTextResponse
)
def get_cline_doc(team: str, filename: str):
    file_path = TEAMS_ROOT / team / "cline_docs_shared" / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="file not found")
    return file_path.read_text()


@router.put("/api/team/{team}/cline_docs_shared/{filename}")
def update_cline_doc(team: str, filename: str, content: str):
    file_path = TEAMS_ROOT / team / "cline_docs_shared" / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    return {"status": "ok"}


@router.get("/api/global-docs")
def list_global_docs():
    if not GLOBAL_DOCS_ROOT.exists():
        return []
    return [f.name for f in GLOBAL_DOCS_ROOT.glob("*.md") if f.is_file()]


@router.get("/api/global-docs/{filename}", response_class=PlainTextResponse)
def get_global_doc(filename: str):
    file_path = GLOBAL_DOCS_ROOT / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="file not found")
    return file_path.read_text()


@router.post("/api/team/{team}/cline_docs_shared/{filename}")
def create_cline_doc(team: str, filename: str, content: str = Body(...)):
    file_path = TEAMS_ROOT / team / "cline_docs_shared" / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.exists():
        raise HTTPException(status_code=400, detail="file already exists")
    file_path.write_text(content)
    return {"status": "created"}


@router.delete("/api/team/{team}/cline_docs_shared/{filename}")
def delete_cline_doc(team: str, filename: str):
    file_path = TEAMS_ROOT / team / "cline_docs_shared" / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="file not found")
    file_path.unlink()
    return {"status": "deleted"}


@router.post("/api/team/{team}/cline_docs_shared/restore-defaults")
def restore_cline_docs_defaults(team: str):
    team_shared_dir = TEAMS_ROOT / team / "cline_docs_shared"
    template_dir = TEMPLATES_ROOT
    if not template_dir.exists():
        raise HTTPException(status_code=500, detail="Template source not found")
    # Remove existing shared docs
    if team_shared_dir.exists():
        shutil.rmtree(team_shared_dir)
    shutil.copytree(template_dir, team_shared_dir)
    files = [f.name for f in team_shared_dir.glob("*.md") if f.is_file()]
    return {"status": "restored", "files": files}


@router.get("/api/cline_docs_shared/templates")
def list_cline_docs_templates():
    template_dir = TEMPLATES_ROOT
    if not template_dir.exists():
        return []
    return [f.name for f in template_dir.glob("*.md") if f.is_file()]


@router.post("/api/team/{team}/cline_docs_shared/import")
def import_cline_docs_template(team: str, data: dict = Body(...)):
    filename = data.get("filename")
    if not filename:
        raise HTTPException(status_code=400, detail="filename required")
    src = TEMPLATES_ROOT / filename
    dst = TEAMS_ROOT / team / "cline_docs_shared" / filename
    if not src.exists():
        raise HTTPException(status_code=404, detail="template doc not found")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"status": "imported"}


@router.get("/api/team/{team}/sessions")
def list_team_sessions(team: str):
    sessions_dir = TEAMS_ROOT / team / "sessions"
    if not sessions_dir.exists() or not sessions_dir.is_dir():
        return []
    return [f.name for f in sessions_dir.iterdir() if f.is_dir()]


@router.post("/api/team/{team}/generate-sessions")
async def generate_team_sessions(team: str, request: Request):
    import sys
    import traceback
    import json as pyjson

    team_dir = TEAMS_ROOT / team
    if not team_dir.exists():
        return {"error": "Team not found"}, 404
    try:
        try:
            data = await request.json()
        except Exception:
            data = {}
        overwrite = data.get("overwrite", False)
        generate_ssh_key = data.get("generate_ssh_key", True)
        env_file = team_dir / "config" / "env"
        cli_path = Path(__file__).parent.parent.parent / "tools" / "team_cli.py"
        if not cli_path.exists():
            return {"error": "team_cli.py not found"}, 500
        if not env_file.exists():
            return {"error": "env file not found for team"}, 500
        # Preprocess env: fill empty or commented values with dummy data
        cleaned_lines = []
        with open(env_file) as f:
            for line in f:
                if line.strip().startswith("#") or not line.strip():
                    cleaned_lines.append(line)
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    v = v.strip()
                    if not v or v.startswith("#"):
                        if "EMAIL" in k:
                            v = "DUMMY_EMAIL@example.com"
                        elif "TOKEN" in k:
                            v = "DUMMY_TOKEN"
                        elif "CLIENT_ID" in k:
                            v = "DUMMY_CLIENT_ID"
                        elif "GUILD_ID" in k:
                            v = "DUMMY_GUILD_ID"
                        elif "URL" in k:
                            v = "https://dummy.url"
                        else:
                            v = "DUMMY_VALUE"
                        line = f"{k}={v}\n"
                cleaned_lines.append(line)
        with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
            tmp.writelines(cleaned_lines)
            tmp.flush()
            tmp_env_path = tmp.name
        # Build CLI command exactly as in working shell
        cmd = [
            sys.executable,
            str(cli_path),
            "create-crew",
            "--env-file",
            tmp_env_path,
        ]
        if overwrite:
            cmd.append("--overwrite")
        # Always capture full stdout/stderr, and set cwd to project root
        project_root = Path(__file__).parent.parent.parent.resolve()
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "exit_code": result.returncode,
        }, (200 if result.returncode == 0 else 500)
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}, 500
