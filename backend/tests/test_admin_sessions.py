import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure backend is importable
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import app

client = TestClient(app)

TEAM = "Test 10"
SESSION = "python_coder"


@pytest.mark.order(1)
def test_list_all_sessions():
    resp = client.get("/api/admin/sessions")
    assert resp.status_code == 200
    sessions = resp.json()
    assert any(s["team"] == TEAM and s["session_id"] == SESSION for s in sessions)


@pytest.mark.order(2)
def test_get_session_metadata():
    resp = client.get(f"/api/admin/sessions/{TEAM}/{SESSION}")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "mcpServers" in data or ("team" in data and data["team"] == TEAM)


@pytest.mark.order(3)
def test_get_session_filesystem():
    resp = client.get(f"/api/admin/sessions/{TEAM}/{SESSION}/filesystem")
    assert resp.status_code == 200
    tree = resp.json()
    assert tree["type"] == "directory"
    assert tree["name"] == "payload"


@pytest.mark.order(4)
def test_get_session_config():
    resp = client.get(f"/api/admin/sessions/{TEAM}/{SESSION}/config")
    assert resp.status_code == 200
    config = resp.json()
    assert isinstance(config, dict)
    assert "tools" in config or len(config) > 0


@pytest.mark.order(5)
def test_get_session_health():
    resp = client.get(f"/api/admin/sessions/{TEAM}/{SESSION}/health")
    assert resp.status_code == 200
    health = resp.json()
    assert "env_present" in health
    assert "mcp_config_present" in health
