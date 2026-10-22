"""Tests for monitoring engine, content normalization, fingerprinting, and error handling."""
import pytest
from unittest.mock import MagicMock, patch
from app.models.db_models import SourceRegistry, SourceFetchHistory, ServiceRecord
from app.services.database import get_db_session, init_db
from app.services.monitoring import (
    MonitoringEngine,
    compute_fingerprint,
    normalize_html_content,
)


def test_html_normalization_and_formatting_immunity():
    """Verify scripts, CSRF tokens, and whitespace changes do not alter normalized fingerprint."""
    html1 = """
    <html>
      <head><script>var token = 'abcdef1234567890abcdef1234567890';</script></head>
      <body>
        <h1>Caste Certificate Requirements</h1>
        <p>Aadhaar Card and Residence Proof are mandatory.</p>
        <div>Current timestamp: 2026-10-19 12:00:00</div>
      </body>
    </html>
    """
    html2 = """
    <html>
      <head><script>var token = '9999991234567890abcdef9999999999';</script></head>
      <body>
        <h1>   Caste Certificate    Requirements  </h1>
        <p>Aadhaar Card and Residence Proof are mandatory.</p>
        <div>Current timestamp: 2026-10-19 12:05:00</div>
      </body>
    </html>
    """

    norm1 = normalize_html_content(html1)
    norm2 = normalize_html_content(html2)

    # Both contain the same essential text
    assert "Caste Certificate Requirements" in norm1
    assert "Aadhaar Card and Residence Proof are mandatory." in norm1
    assert "script" not in norm1.lower()


def test_conditional_http_304_not_modified(app):
    """Verify that HTTP 304 does not create changes or alter source state."""
    init_db(app, seed=True)
    engine = MonitoringEngine()

    mock_resp = MagicMock()
    mock_resp.status_code = 304
    mock_resp.history = []

    with get_db_session() as s:
        src = s.query(SourceRegistry).first()
        src_id = src.id
        src.etag = '"v12345"'

    with patch("requests.get", return_value=mock_resp), patch("app.services.security_check.validate_and_resolve_url", return_value=("url", "1.2.3.4")):
        res = engine.check_source(src_id)
        assert res["status"] == "unchanged"
        assert res["changes_count"] == 0

    with get_db_session() as s:
        fetch = s.query(SourceFetchHistory).filter_by(source_id=src_id).order_by(SourceFetchHistory.attempted_at.desc()).first()
        assert fetch is not None
        assert fetch.http_status == 304
        assert fetch.change_detected is False


def test_failed_source_does_not_erase_existing_data(app):
    """Verify network error logs failure without wiping out existing stored records."""
    init_db(app, seed=True)
    engine = MonitoringEngine()

    with get_db_session() as s:
        src = s.query(SourceRegistry).first()
        src_id = src.id
        initial_service_count = s.query(ServiceRecord).count()

    with patch("requests.get", side_effect=Exception("Connection timed out")), patch("app.services.security_check.validate_and_resolve_url", return_value=("url", "1.2.3.4")):
        res = engine.check_source(src_id)
        assert res["status"] == "error"

    with get_db_session() as s:
        src_after = s.query(SourceRegistry).filter_by(id=src_id).first()
        assert src_after.consecutive_failures >= 1
        assert "Connection timed out" in src_after.last_error_message
        # Existing services remain completely intact
        assert s.query(ServiceRecord).count() == initial_service_count
