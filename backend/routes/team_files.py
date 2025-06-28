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
import re
import logging
import json
from backend.services.team_scaffold_shared import sync_cline_docs_shared_to_sessions

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
async def update_env_file(team: str, request: Request):
    env_path = TEAMS_ROOT / team / "config" / "env"
    env_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        # Try to parse as JSON with 'content' field
        data = await request.json()
        content = data.get("content", None)
        if content is not None:
            env_path.write_text(content)
            return {"status": "ok"}
    except Exception:
        pass  # Not JSON, fall through to raw body
    # Fallback: treat as raw text
    body = await request.body()
    # Try to decode as utf-8, fallback to bytes if not possible
    try:
        text = body.decode("utf-8")
        env_path.write_text(text)
    except Exception:
        env_path.write_bytes(body)
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


def parse_extra_propagate_paths(env_path):
    if not env_path.exists():
        return []
    paths = []
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("EXTRA_PROPAGATE_PATHS="):
            value = line.split("=", 1)[1].strip()
            if value:
                paths = [p.strip() for p in value.split(",") if p.strip()]
            break
    return paths


@router.post("/api/team/{team}/cline_docs_shared/propagate")
def propagate_cline_docs_shared(team: str, body: dict = Body(default=None)):
    print(f"[DEBUG] propagate_cline_docs_shared called for team: {team}")
    team_root = TEAMS_ROOT / team
    if not team_root.exists():
        raise HTTPException(status_code=404, detail="Team not found")
    sync_cline_docs_shared_to_sessions(team_root)
    # Propagate to extra host paths if set
    env_path = team_root / "config" / "env"
    extra_paths = parse_extra_propagate_paths(env_path)
    print(f"[DEBUG] EXTRA_PROPAGATE_PATHS: {extra_paths}")
    shared_dir = team_root / "cline_docs_shared"
    propagated_host_paths = []
    if extra_paths and shared_dir.exists():
        for host_path in extra_paths:
            print(f"[DEBUG] Propagating to host path: {host_path}")
            host_path_obj = Path(host_path)
            host_path_obj.mkdir(parents=True, exist_ok=True)
            for f in shared_dir.glob("*.md"):
                print(f"[DEBUG] Copying {f} to {host_path_obj / f.name}")
                shutil.copy2(f, host_path_obj / f.name)
            propagated_host_paths.append(str(host_path_obj))
    # List updated sessions
    sessions_dir = team_root / "sessions"
    updated_sessions = [s.name for s in sessions_dir.iterdir() if s.is_dir()]
    return {
        "status": "propagated",
        "sessions": updated_sessions,
        "host_paths": propagated_host_paths,
    }


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
    sessions = []
    for f in sessions_dir.iterdir():
        if f.is_dir():
            # Check for .devcontainer and payload/.env to determine status
            devcontainer = f / ".devcontainer"
            payload_env = f / "payload/.env"
            if devcontainer.exists() and payload_env.exists():
                status = "generated"
            else:
                status = "scaffolded"
            sessions.append({"name": f.name, "status": status})
    return sessions


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
        # Clean up empty/incomplete session directories before running CLI
        sessions_dir = team_dir / "sessions"
        if sessions_dir.exists():
            for session_dir in sessions_dir.iterdir():
                if session_dir.is_dir():
                    devcontainer_dir = session_dir / ".devcontainer"
                    # If .devcontainer is missing or empty, remove the session dir
                    if not devcontainer_dir.exists() or not any(
                        devcontainer_dir.iterdir()
                    ):
                        import shutil

                        shutil.rmtree(session_dir)
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
        # Log the contents of the temp env file
        with open(tmp_env_path) as f:
            env_contents = f.read()
        print(f"[DEBUG] Temp env file path: {tmp_env_path}")
        print(f"[DEBUG] Temp env file contents:\n{env_contents}")
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
        print(f"[DEBUG] Running CLI command: {' '.join(cmd)}")
        print(f"[DEBUG] Working directory: {project_root}")
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=project_root
            )
        except Exception as e:
            print(f"[ERROR] Exception running subprocess: {e}")
            traceback.print_exc()
            return {"error": f"Exception running subprocess: {e}"}, 500
        print(f"[DEBUG] CLI stdout:\n{result.stdout}")
        print(f"[DEBUG] CLI stderr:\n{result.stderr}")
        print(f"[DEBUG] CLI exit code: {result.returncode}")
        created = re.findall(r"Created session: ([^\n]+)", result.stdout)
        skipped = re.findall(r"Skipped session: ([^\n]+)", result.stdout)
        errors = re.findall(r"Error: ([^\n]+)", result.stderr + result.stdout)
        # After CLI runs, check for devcontainer in each session
        sessions_dir = team_dir / "sessions"
        missing_devcontainers = []
        empty_devcontainers = []
        if sessions_dir.exists():
            for session_dir in sessions_dir.iterdir():
                if session_dir.is_dir():
                    devcontainer_dir = session_dir / ".devcontainer"
                    if not devcontainer_dir.exists():
                        missing_devcontainers.append(str(devcontainer_dir))
                    elif not any(devcontainer_dir.iterdir()):
                        empty_devcontainers.append(str(devcontainer_dir))
        # Parse CLI stdout for warnings about missing devcontainer templates
        devcontainer_warning = False
        if (
            "No .devcontainer directory found" in result.stdout
            or "No .devcontainer directory found" in result.stderr
        ):
            devcontainer_warning = True
        if missing_devcontainers or empty_devcontainers or devcontainer_warning:
            return {
                "status": "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "missing_devcontainers": missing_devcontainers,
                "empty_devcontainers": empty_devcontainers,
                "devcontainer_warning": devcontainer_warning,
                "command": " ".join(cmd),
                "exit_code": result.returncode,
                "env_file": tmp_env_path,
                "env_contents": env_contents,
                "error": "One or more .devcontainer directories were not created or are empty. Check that templates/devcontainer exists and is populated.",
            }, 500
        return {
            "status": "ok" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "exit_code": result.returncode,
            "created": created,
            "skipped": skipped,
            "errors": errors,
            "env_file": tmp_env_path,
            "env_contents": env_contents,
        }, (200 if result.returncode == 0 else 500)
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}, 500


def detect_container_name(team, session):
    session_path = TEAMS_ROOT / team / "sessions" / session
    devcontainer_json = session_path / ".devcontainer" / "devcontainer.json"
    container_name = None
    # 1. Try to read name from devcontainer.json
    if devcontainer_json.exists():
        try:
            with open(devcontainer_json) as f:
                config = json.load(f)
            if "name" in config and config["name"]:
                container_name = config["name"]
        except Exception:
            pass
    # 2. If not, search for containers with session name in their name
    if not container_name:
        try:
            result = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{.Names}}|{{.CreatedAt}}"],
                capture_output=True,
                text=True,
            )
            lines = result.stdout.strip().split("\n")
            matches = [l.split("|")[0] for l in lines if session in l.split("|")[0]]
            if matches:
                # If multiple, pick the most recently created
                # Sort by CreatedAt descending
                matches_with_time = [
                    tuple(l.split("|")) for l in lines if session in l.split("|")[0]
                ]
                matches_with_time.sort(key=lambda x: x[1], reverse=True)
                container_name = matches_with_time[0][0]
        except Exception:
            pass
    return container_name


@router.get("/api/team/{team}/session/{session}/container-status")
def container_status(team: str, session: str):
    import subprocess

    name = detect_container_name(team, session)
    if not name:
        return {"status": "none", "container_name": None}
    try:
        result = subprocess.run(
            [
                "docker",
                "ps",
                "-a",
                "--filter",
                f"name=^{name}$",
                "--format",
                "{{.Status}}",
            ],
            capture_output=True,
            text=True,
        )
        status = result.stdout.strip()
        if not status:
            return {"status": "none", "container_name": name}
        if status.startswith("Up"):
            return {"status": "running", "container_name": name}
        if status.startswith("Exited"):
            return {"status": "stopped", "container_name": name}
        return {"status": status, "container_name": name}
    except Exception as e:
        return {"status": "error", "error": str(e), "container_name": name}


@router.post("/api/team/{team}/session/{session}/start-container")
def start_container(team: str, session: str):
    import subprocess

    name = detect_container_name(team, session)
    if not name:
        return {"status": "error", "error": "No container found for this session."}
    try:
        result = subprocess.run(
            ["docker", "start", name], capture_output=True, text=True
        )
        if result.returncode == 0:
            return {"status": "started", "container_name": name}
        return {
            "status": "error",
            "error": result.stderr.strip(),
            "container_name": name,
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "container_name": name}


@router.post("/api/team/{team}/session/{session}/stop-container")
def stop_container(team: str, session: str):
    import subprocess

    name = detect_container_name(team, session)
    if not name:
        return {"status": "error", "error": "No container found for this session."}
    try:
        result = subprocess.run(
            ["docker", "stop", name], capture_output=True, text=True
        )
        if result.returncode == 0:
            return {"status": "stopped", "container_name": name}
        return {
            "status": "error",
            "error": result.stderr.strip(),
            "container_name": name,
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "container_name": name}


@router.post("/api/team/{team}/session/{session}/remove-container")
def remove_container(team: str, session: str):
    import subprocess

    name = detect_container_name(team, session)
    if not name:
        return {"status": "error", "error": "No container found for this session."}
    try:
        result = subprocess.run(["docker", "rm", name], capture_output=True, text=True)
        if result.returncode == 0:
            return {"status": "removed", "container_name": name}
        return {
            "status": "error",
            "error": result.stderr.strip(),
            "container_name": name,
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "container_name": name}


@router.post("/api/team/{team}/cline_docs_shared/propagate/{filename}")
def propagate_single_cline_doc(team: str, filename: str):
    print(
        f"[DEBUG] propagate_single_cline_doc called for team: {team}, file: {filename}"
    )
    team_root = TEAMS_ROOT / team
    if not team_root.exists():
        raise HTTPException(status_code=404, detail="Team not found")
    shared_dir = team_root / "cline_docs_shared"
    file_path = shared_dir / filename
    if not file_path.exists():
        raise HTTPException(
            status_code=404, detail="File not found in cline_docs_shared"
        )
    # Propagate to session payloads
    sessions_dir = team_root / "sessions"
    updated_sessions = []
    for session in sessions_dir.iterdir():
        if session.is_dir():
            payload_dir = session / "payload"
            payload_dir.mkdir(parents=True, exist_ok=True)
            dest = payload_dir / filename
            shutil.copy2(file_path, dest)
            updated_sessions.append(session.name)
    # Propagate to extra host paths if set
    env_path = team_root / "config" / "env"
    extra_paths = parse_extra_propagate_paths(env_path)
    print(f"[DEBUG] EXTRA_PROPAGATE_PATHS: {extra_paths}")
    propagated_host_paths = []
    if extra_paths:
        for host_path in extra_paths:
            print(f"[DEBUG] Propagating single file to host path: {host_path}")
            host_path_obj = Path(host_path)
            host_path_obj.mkdir(parents=True, exist_ok=True)
            dest = host_path_obj / filename
            shutil.copy2(file_path, dest)
            propagated_host_paths.append(str(dest))
    return {
        "status": "propagated_single_file",
        "file": filename,
        "sessions": updated_sessions,
        "host_paths": propagated_host_paths,
    }
