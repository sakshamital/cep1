import pytest
import json
from app.models.entities import Service, ApplicationInfo
from app.services.repository import reset_repo_for_testing

def test_api_health(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    assert res.json["data"]["status"] == "ok"
    assert "disclaimer" in res.json["meta"]

def test_api_404(client):
    res = client.get('/api/documents/nonexistent')
    assert res.status_code == 404
    assert res.json["error"]["code"] == "NOT_FOUND"

def test_api_readiness_400(client):
    res = client.post('/api/services/S1/readiness', data="not json", content_type="application/json")
    assert res.status_code == 400

def test_api_oversize_body(client):
    svc = Service("S1", "S1", [], "scheme", "", "", [], [], ApplicationInfo("", "", [], ""), False, "", None)
    reset_repo_for_testing(services={"S1": svc})
    large_payload = {"statuses": {f"doc_{i}": "available" for i in range(1000)}}
    res = client.post('/api/services/S1/readiness', json=large_payload)
    assert res.status_code == 400 # Validation error max 200 items
