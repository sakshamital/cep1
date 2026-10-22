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


def test_api_list_documents(client, app):
    from app.services.database import init_db
    from app.services.repository import get_repo
    init_db(app, seed=True)
    get_repo().load()
    res = client.get('/api/documents')
    assert res.status_code == 200
    docs = res.json["data"]
    assert len(docs) >= 30
    pan = next((d for d in docs if d["id"] == "pan_card"), None)
    assert pan is not None
    assert pan["has_guide"] is True
    assert pan["verified"] is True
    assert pan["official_link"] is not None


def test_api_document_guide_steps(client, app):
    """Verify document guide endpoint returns detailed step-by-step procedure."""
    from app.services.database import init_db
    from app.services.repository import get_repo
    init_db(app, seed=True)
    get_repo().load()
    for doc_id in ["pan_card", "voter_id", "passport", "birth_certificate", "driving_licence", "ration_card"]:
        res = client.get(f'/api/documents/{doc_id}/guide')
        assert res.status_code == 200
        data = res.json["data"]
        assert "guide" in data
        guide = data["guide"]
        assert len(guide["procedure_steps"]) >= 4
        assert len(guide["where_how_to_apply"]) > 10
        assert guide["official_link"] is not None


def test_documents_html_directory(client, app):
    """Verify /documents page renders all documents directory."""
    from app.services.database import init_db
    from app.services.repository import get_repo
    init_db(app, seed=True)
    get_repo().load()
    res = client.get('/documents')
    assert res.status_code == 200
    assert b"Important Documents Directory" in res.data
    assert b"PAN Card" in res.data
    assert b"Indian Passport" in res.data
    assert b"Driving Licence" in res.data


def test_guide_html_page(client, app):
    """Verify /guide/<doc_id> renders how-to-obtain guide page."""
    from app.services.database import init_db
    from app.services.repository import get_repo
    init_db(app, seed=True)
    get_repo().load()
    res = client.get('/guide/pan_card')
    assert res.status_code == 200
    assert b"How to Obtain: PAN Card" in res.data
    assert b"Step-by-Step Procedure" in res.data
    assert b"Where / How to Apply" in res.data

