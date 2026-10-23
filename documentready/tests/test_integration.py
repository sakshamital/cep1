"""
Integration tests — database persistence, verification workflow, monitoring engine,
authentication, and admin panel. These tests require a running Flask app + database.
"""
import pytest
from unittest.mock import MagicMock, patch
from app.models.db_models import (
    DetectedChange,
    DocumentRecord,
    GuideRecord,
    InAppNotification,
    ServiceRecord,
    ServiceVersion,
    SourceFetchHistory,
    SourceRegistry,
    StateRecord,
    StateRuleRecord,
    SynonymRecord,
    UserAccount,
)
from app.services.auth import authenticate_user, ensure_initial_admin, generate_csrf_token, validate_csrf_token
from app.services.database import get_db_session, init_db, seed_initial_data, normalize_db_uri
from app.services.monitoring import MonitoringEngine, compute_fingerprint, normalize_html_content
from app.services.verification import approve_and_publish_change, reject_change, rollback_service_version
from config import get_database_uri


# ── Database Persistence & Seed Idempotency ───────────────────────────────────

def test_database_init_and_idempotency(app):
    init_db(app, seed=True)
    with get_db_session() as s:
        initial = {
            "services": s.query(ServiceRecord).count(),
            "docs": s.query(DocumentRecord).count(),
            "guides": s.query(GuideRecord).count(),
            "sources": s.query(SourceRegistry).count(),
            "states": s.query(StateRecord).count(),
            "rules": s.query(StateRuleRecord).count(),
            "synonyms": s.query(SynonymRecord).count(),
        }
        for k, v in initial.items():
            assert v > 0, f"{k} count should be > 0 after seed"
        assert initial["states"] == 36

        # Second seed call must be fully idempotent
        counts = seed_initial_data(s)
        for k in ["services", "documents", "guides", "sources", "states", "state_rules", "synonyms"]:
            assert counts[k] == 0, f"Duplicate seed should add 0 {k}"

        assert s.query(ServiceRecord).count() == initial["services"]
        assert s.query(DocumentRecord).count() == initial["docs"]


def test_initial_demo_records_unverified(app):
    init_db(app, seed=True)
    with get_db_session() as s:
        for doc in s.query(DocumentRecord).all():
            if not doc.verified:
                assert doc.source_note and len(doc.source_note.strip()) > 0


def test_render_postgres_url_normalization(monkeypatch):
    raw = "postgres://usr:pass@dpg-abc.render.com/db"
    assert normalize_db_uri(raw).startswith("postgresql+psycopg2://")
    monkeypatch.setenv("DATABASE_URL", raw)
    assert get_database_uri().startswith("postgresql+psycopg2://")


def test_states_api_from_database(client, app):
    init_db(app, seed=True)
    res = client.get("/api/states")
    assert res.status_code == 200
    states = res.get_json()
    assert len(states) >= 36
    mh = next((s for s in states if s["id"] == "MH"), None)
    assert mh is not None and mh["name"] == "Maharashtra"


# ── Verification Workflow ─────────────────────────────────────────────────────

def test_approve_and_publish_workflow(app):
    init_db(app, seed=True)
    with get_db_session() as s:
        svc = s.query(ServiceRecord).first()
        svc_id, initial_version = svc.id, svc.version
        chg = DetectedChange(
            source_id="src_test", target_type="service", target_id=svc_id,
            change_type="new_requirement", summary="New requirement: Electricity Bill",
            previous_data_json="{}",
            proposed_data_json='{"added_requirement": {"document_id": "electricity_bill", "necessity": "required"}}',
            evidence_quote="Electricity bill is mandatory",
            evidence_source_url="https://aaplesarkar.mahaonline.gov.in/test",
            status="proposed",
        )
        s.add(chg); s.commit()
        chg_id = chg.id

    res = approve_and_publish_change(chg_id, reviewer_username="lead_reviewer", notes="Verified with GR")
    assert res["status"] == "success"
    assert res["new_version"] == initial_version + 1

    with get_db_session() as s:
        svc_after = s.query(ServiceRecord).filter_by(id=svc_id).first()
        assert svc_after.version == initial_version + 1 and svc_after.verified is True
        notif = s.query(InAppNotification).filter_by(service_id=svc_id).first()
        assert notif is not None and "Electricity Bill" in notif.message


def test_rejection_workflow(app):
    init_db(app, seed=True)
    with get_db_session() as s:
        svc = s.query(ServiceRecord).first()
        initial_version = svc.version
        chg = DetectedChange(
            source_id="src_test", target_type="service", target_id=svc.id,
            change_type="changed_fee", summary="Fee updated to Rs 500",
            evidence_quote="Fake fee note", evidence_source_url="https://fake.gov.in",
            status="proposed",
        )
        s.add(chg); s.commit()
        chg_id, svc_id = chg.id, svc.id

    res = reject_change(chg_id, reviewer_username="lead_reviewer", reason="Spurious; non-official domain")
    assert res["status"] == "success"

    with get_db_session() as s:
        chg_after = s.query(DetectedChange).filter_by(id=chg_id).first()
        assert chg_after.status == "rejected"
        assert chg_after.review_notes == "Spurious; non-official domain"
        assert s.query(ServiceRecord).filter_by(id=svc_id).first().version == initial_version


def test_rollback_operation(app):
    init_db(app, seed=True)
    with get_db_session() as s:
        svc = s.query(ServiceRecord).first()
        svc_id, v1 = svc.id, svc.version
        chg = DetectedChange(
            source_id="src_test", target_type="service", target_id=svc_id,
            change_type="changed_fee", summary="Updated fee", previous_data_json="{}",
            proposed_data_json='{"fee_note": "Rs 100"}',
            evidence_quote="Prescribed fee Rs 100",
            evidence_source_url="https://aaplesarkar.mahaonline.gov.in/test",
            status="proposed",
        )
        s.add(chg); s.commit()
        approve_and_publish_change(chg.id, reviewer_username="admin")

    res = rollback_service_version(svc_id, target_version_number=v1, reviewer_username="admin", reason="Incorrect fee")
    assert res["status"] == "success"

    with get_db_session() as s:
        assert s.query(ServiceRecord).filter_by(id=svc_id).first().version == v1 + 2
        assert len(s.query(ServiceVersion).filter_by(service_id=svc_id).all()) >= 3


# ── Monitoring Engine ─────────────────────────────────────────────────────────

def test_html_normalization_immunity():
    html1 = """<html><head><script>var token = 'abcdef1234567890';</script></head>
      <body><h1>Caste Certificate Requirements</h1>
      <p>Aadhaar Card and Residence Proof are mandatory.</p>
      <div>timestamp: 2026-10-19 12:00:00</div></body></html>"""
    html2 = """<html><head><script>var token = '99999999999';</script></head>
      <body><h1>  Caste Certificate   Requirements  </h1>
      <p>Aadhaar Card and Residence Proof are mandatory.</p>
      <div>timestamp: 2026-10-19 12:05:00</div></body></html>"""
    norm1 = normalize_html_content(html1)
    norm2 = normalize_html_content(html2)
    assert "Caste Certificate Requirements" in norm1
    assert "Aadhaar Card and Residence Proof are mandatory." in norm1
    assert "script" not in norm1.lower()


def test_conditional_http_304_not_modified(app):
    init_db(app, seed=True)
    engine = MonitoringEngine()
    mock_resp = MagicMock()
    mock_resp.status_code = 304
    mock_resp.history = []

    with get_db_session() as s:
        src = s.query(SourceRegistry).first()
        src_id = src.id
        src.etag = '"v12345"'

    with patch("requests.get", return_value=mock_resp), \
         patch("app.services.security_check.validate_and_resolve_url", return_value=("url", "1.2.3.4")):
        res = engine.check_source(src_id)
        assert res["status"] == "unchanged" and res["changes_count"] == 0

    with get_db_session() as s:
        fetch = s.query(SourceFetchHistory).filter_by(source_id=src_id)\
            .order_by(SourceFetchHistory.attempted_at.desc()).first()
        assert fetch is not None and fetch.http_status == 304 and fetch.change_detected is False


def test_failed_source_does_not_erase_existing_data(app):
    init_db(app, seed=True)
    engine = MonitoringEngine()
    with get_db_session() as s:
        src = s.query(SourceRegistry).first()
        src_id = src.id
        initial_count = s.query(ServiceRecord).count()

    with patch("requests.get", side_effect=Exception("Connection timed out")), \
         patch("app.services.security_check.validate_and_resolve_url", return_value=("url", "1.2.3.4")):
        res = engine.check_source(src_id)
        assert res["status"] == "error"

    with get_db_session() as s:
        src_after = s.query(SourceRegistry).filter_by(id=src_id).first()
        assert src_after.consecutive_failures >= 1
        assert "Connection timed out" in src_after.last_error_message
        assert s.query(ServiceRecord).count() == initial_count


# ── Authentication & Admin ────────────────────────────────────────────────────

def test_admin_provisioning_and_auth(app):
    init_db(app, seed=True)
    assert ensure_initial_admin("test_admin", "SecureAdminPass123!") is True
    assert ensure_initial_admin("test_admin", "OtherPassword") is False  # No overwrite

    user = authenticate_user("test_admin", "SecureAdminPass123!")
    assert user is not None and user["username"] == "test_admin"
    assert authenticate_user("test_admin", "WrongPassword") is None


def test_csrf_token_validation(app):
    with app.test_request_context():
        token = generate_csrf_token()
        assert len(token) == 64
        assert validate_csrf_token(token) is True
        assert validate_csrf_token("invalid_token_12345") is False
        assert validate_csrf_token(None) is False


def test_admin_routes_protected(client):
    res = client.get("/admin/")
    assert res.status_code == 302
    assert "/admin/login" in res.headers["Location"]


def test_api_admin_unauthorized(client):
    res = client.get("/api/admin/sources")
    assert res.status_code == 401
    assert res.json["error"]["code"] == "UNAUTHORIZED"


def test_admin_login_open_redirect_defense(app, client):
    init_db(app, seed=True)
    ensure_initial_admin("admin_test_sec", "AdminPass@123")

    res = client.post(
        "/admin/login?next=https://evil-phishing.com",
        data={"username": "admin_test_sec", "password": "AdminPass@123"},
    )
    assert res.status_code == 302
    assert res.headers["Location"].endswith("/admin/")
    assert "evil-phishing" not in res.headers["Location"]

    res2 = client.post(
        "/admin/login?next=//evil-phishing.com",
        data={"username": "admin_test_sec", "password": "AdminPass@123"},
    )
    assert res2.status_code == 302 and res2.headers["Location"].endswith("/admin/")


def test_admin_full_panel_lifecycle(app, client):
    init_db(app, seed=True)
    ensure_initial_admin("superadmin", "SuperPass@123")

    with get_db_session() as s:
        user_id = s.query(UserAccount).filter_by(username="superadmin").first().id

    # Before logging in, /admin/login serves 200 OK
    assert client.get("/admin/login").status_code == 200

    csrf = "valid_csrf_token_test_1234567890abcdef"
    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["username"] = "superadmin"
        sess["role"] = "admin"
        sess["_csrf_token"] = csrf

    # Once authenticated, /admin/login redirects to dashboard
    assert client.get("/admin/login").status_code == 302

    dash = client.get("/admin/")
    assert dash.status_code == 200 and b"System Overview" in dash.data

    assert client.get("/admin/sources").status_code == 200
    assert client.get("/admin/changes").status_code == 200
    assert client.get("/admin/history").status_code == 200
    assert client.get("/admin/history?service_id=caste_validity_certificate").status_code == 200
    assert client.get("/admin/logs").status_code == 200

    with patch("app.services.security_check.validate_and_resolve_url",
               return_value=("https://aaplesarkar.mahaonline.gov.in", "103.20.10.1")):
        add_res = client.post("/admin/sources/add", data={
            "csrf_token": csrf, "id": "src_test_lifecycle",
            "name": "Test Dept Portal", "department": "Revenue",
            "jurisdiction": "Maharashtra",
            "monitored_url": "https://aaplesarkar.mahaonline.gov.in/test_lc",
            "official_base_url": "https://aaplesarkar.mahaonline.gov.in",
            "source_type": "html", "adapter": "generic_html",
            "check_frequency_minutes": "360",
        })
        assert add_res.status_code == 302

    assert client.post("/admin/sources/src_test_lifecycle/toggle", data={"csrf_token": csrf}).status_code == 302
    assert client.post("/admin/sources/src_test_lifecycle/delete", data={"csrf_token": csrf}).status_code == 302
    assert client.post("/admin/sync-seed", data={"csrf_token": csrf}).status_code == 302

    logout = client.post("/admin/logout", data={"csrf_token": csrf})
    assert logout.status_code == 302 and "/admin/login" in logout.headers["Location"]
