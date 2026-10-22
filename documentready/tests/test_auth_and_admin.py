"""Tests for authentication, authorization, session management, and CSRF protection."""
import pytest
from app.services.auth import (
    authenticate_user,
    ensure_initial_admin,
    generate_csrf_token,
    validate_csrf_token,
)
from app.services.database import init_db


def test_admin_provisioning_and_auth(app):
    """Verify administrator account can be provisioned and authenticated securely."""
    init_db(app, seed=True)
    created = ensure_initial_admin("test_admin", "SecureAdminPass123!")
    assert created is True

    # Duplicate provisioning does not overwrite
    created_again = ensure_initial_admin("test_admin", "OtherPassword")
    assert created_again is False

    # Valid auth
    user = authenticate_user("test_admin", "SecureAdminPass123!")
    assert user is not None
    assert user["username"] == "test_admin"

    # Invalid auth
    bad_user = authenticate_user("test_admin", "WrongPassword")
    assert bad_user is None


def test_csrf_token_validation(app):
    """Verify CSRF token generation and validation."""
    with app.test_request_context():
        token = generate_csrf_token()
        assert len(token) == 64
        assert validate_csrf_token(token) is True
        assert validate_csrf_token("invalid_token_12345") is False
        assert validate_csrf_token(None) is False


def test_admin_routes_protected(client):
    """Verify unauthenticated requests to admin dashboard redirect to login."""
    res = client.get("/admin/")
    assert res.status_code == 302
    assert "/admin/login" in res.headers["Location"]


def test_api_admin_unauthorized(client):
    """Verify unauthenticated requests to /api/admin/* return 401."""
    res = client.get("/api/admin/sources")
    assert res.status_code == 401
    assert res.json["error"]["code"] == "UNAUTHORIZED"


def test_admin_login_open_redirect_defense(app, client):
    """Verify open redirect attacks are mitigated on login."""
    init_db(app, seed=True)
    ensure_initial_admin("admin_test_sec", "AdminPass@123")

    # Attempt malicious external redirect
    res = client.post(
        "/admin/login?next=https://evil-phishing.com",
        data={"username": "admin_test_sec", "password": "AdminPass@123"},
    )
    assert res.status_code == 302
    assert res.headers["Location"].endswith("/admin/")
    assert "evil-phishing" not in res.headers["Location"]

    # Protocol-relative redirect defense
    res2 = client.post(
        "/admin/login?next=//evil-phishing.com",
        data={"username": "admin_test_sec", "password": "AdminPass@123"},
    )
    assert res2.status_code == 302
    assert res2.headers["Location"].endswith("/admin/")


def test_admin_full_panel_lifecycle(app, client):
    """Verify end-to-end admin panel pages, templates, and actions."""
    from unittest.mock import patch
    from app.models.db_models import UserAccount
    from app.services.database import get_db_session

    init_db(app, seed=True)
    ensure_initial_admin("superadmin", "SuperPass@123")

    with get_db_session() as s:
        user = s.query(UserAccount).filter_by(username="superadmin").first()
        user_id = user.id

    # 1. Login view
    login_page = client.get("/admin/login")
    assert login_page.status_code == 200
    assert b"Admin Sign In" in login_page.data

    # Log in user via session
    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["username"] = "superadmin"
        sess["role"] = "admin"
        sess["_csrf_token"] = "valid_csrf_token_test_1234567890abcdef"

    csrf = "valid_csrf_token_test_1234567890abcdef"

    # 2. Overview / Dashboard view
    dash_res = client.get("/admin/")
    assert dash_res.status_code == 200
    assert b"System Overview" in dash_res.data
    assert b"Monitored Sources" in dash_res.data

    # 3. Sources view
    sources_res = client.get("/admin/sources")
    assert sources_res.status_code == 200
    assert b"Official Source Registry" in sources_res.data

    # 4. Add new source
    with patch("app.services.security_check.validate_and_resolve_url", return_value=("https://aaplesarkar.mahaonline.gov.in", "103.20.10.1")):
        add_res = client.post(
            "/admin/sources/add",
            data={
                "csrf_token": csrf,
                "id": "src_test_new_gov",
                "name": "New Test Dept Portal",
                "department": "Revenue Dept",
                "jurisdiction": "Maharashtra",
                "monitored_url": "https://aaplesarkar.mahaonline.gov.in/test_src",
                "official_base_url": "https://aaplesarkar.mahaonline.gov.in",
                "source_type": "html",
                "adapter": "generic_html",
                "check_frequency_minutes": "360",
            },
        )
        assert add_res.status_code == 302

    # 5. Toggle source
    toggle_res = client.post("/admin/sources/src_test_new_gov/toggle", data={"csrf_token": csrf})
    assert toggle_res.status_code == 302

    # 6. Delete source
    del_res = client.post("/admin/sources/src_test_new_gov/delete", data={"csrf_token": csrf})
    assert del_res.status_code == 302

    # 7. Changes view
    changes_res = client.get("/admin/changes")
    assert changes_res.status_code == 200
    assert b"Verification &amp; Approval Queue" in changes_res.data

    # 8. History view
    hist_res = client.get("/admin/history")
    assert hist_res.status_code == 200
    assert b"Version History &amp; Rollback Controls" in hist_res.data

    hist_svc = client.get("/admin/history?service_id=caste_validity_certificate")
    assert hist_svc.status_code == 200
    assert b"Active Version" in hist_svc.data

    # 9. Audit Logs view
    logs_res = client.get("/admin/logs")
    assert logs_res.status_code == 200
    assert b"Audit Trail &amp; Job History" in logs_res.data

    # 10. Sync Seed Data
    sync_res = client.post("/admin/sync-seed", data={"csrf_token": csrf})
    assert sync_res.status_code == 302

    # 11. Logout
    logout_res = client.post("/admin/logout", data={"csrf_token": csrf})
    assert logout_res.status_code == 302
    assert "/admin/login" in logout_res.headers["Location"]

