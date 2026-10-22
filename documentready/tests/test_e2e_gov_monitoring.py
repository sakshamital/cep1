"""Complete End-to-End Monitoring, Verification, Publication, and Rollback Scenario Test.

Covers all 12 steps defined in Master Engineering Requirements Section 16:
1. Configured official test source contains known document checklist.
2. Monitor retrieves and stores the original version.
3. Test fixture introduces a meaningful requirement change.
4. Monitor detects the difference.
5. Change record with grounded evidence is created.
6. Review policy determines approval needed (human-in-the-loop review).
7. Authorized reviewer approves the change.
8. Updated requirement becomes visible through existing public service API & UI.
9. Previous version remains accessible in history.
10. Repeated check does not create a duplicate change.
11. Failed source check does not erase the last verified version.
12. Rollback restores previous published version.
"""
from unittest.mock import MagicMock, patch
import pytest

from app.models.db_models import (
    DetectedChange,
    ServiceRecord,
    ServiceVersion,
    SourceRegistry,
)
from app.services.database import get_db_session, init_db
from app.services.monitoring import MonitoringEngine
from app.services.verification import (
    approve_and_publish_change,
    rollback_service_version,
)


def test_complete_e2e_12_step_monitoring_lifecycle(app, client):
    # Initialize DB and seed
    init_db(app, seed=True)
    engine = MonitoringEngine()

    target_service_id = "caste_validity_certificate"

    # ──────────────────────────────────────────────────────────────────────────
    # Step 1: Configured official test source contains known document checklist
    # ──────────────────────────────────────────────────────────────────────────
    with get_db_session() as s:
        test_source = SourceRegistry(
            id="src_official_e2e_test",
            name="Maharashtra State Scrutiny Portal Official Test Source",
            department="Social Justice & Special Assistance",
            jurisdiction="Maharashtra",
            official_base_url="https://aaplesarkar.mahaonline.gov.in",
            monitored_url="https://aaplesarkar.mahaonline.gov.in/e2e/test_notice",
            source_type="html",
            adapter="generic_html",
            check_frequency_minutes=720,
            enabled=True,
            priority="high",
            verification_policy="manual_review",
        )
        test_source.associated_service_ids = [target_service_id]
        s.add(test_source)
        s.commit()

    # Initial HTML version from government portal
    v1_html = """
    <html>
      <body>
        <h2>Caste Validity Certificate Requirements</h2>
        <p>Aadhaar Card and Caste Certificate are required.</p>
      </body>
    </html>
    """

    mock_resp_v1 = MagicMock()
    mock_resp_v1.status_code = 200
    mock_resp_v1.text = v1_html
    mock_resp_v1.content = v1_html.encode("utf-8")
    mock_resp_v1.headers = {"ETag": '"hash-v1"', "Content-Type": "text/html"}
    mock_resp_v1.history = []

    # ──────────────────────────────────────────────────────────────────────────
    # Step 2: The monitor retrieves and stores the original version
    # ──────────────────────────────────────────────────────────────────────────
    with patch("requests.get", return_value=mock_resp_v1), patch("app.services.security_check.validate_and_resolve_url", return_value=("https://aaplesarkar.mahaonline.gov.in", "103.20.10.1")):
        res_v1 = engine.check_source("src_official_e2e_test")
        assert res_v1["status"] in ("unchanged", "changed")

    with get_db_session() as s:
        src_v1 = s.query(SourceRegistry).filter_by(id="src_official_e2e_test").first()
        assert src_v1.current_fingerprint is not None
        assert src_v1.last_successful_check is not None
        fingerprint_v1 = src_v1.current_fingerprint

    # ──────────────────────────────────────────────────────────────────────────
    # Step 3: Test fixture introduces a meaningful requirement change
    # (Government issues new resolution mandating 'self_declaration_form')
    # ──────────────────────────────────────────────────────────────────────────
    v2_html = """
    <html>
      <body>
        <h2>Caste Validity Certificate Requirements</h2>
        <p>Aadhaar Card and Caste Certificate are required.</p>
        <p>Important GR: self declaration form is mandatory for all applicants.</p>
        <p>Prescribed application fee is Rs 45.</p>
      </body>
    </html>
    """

    mock_resp_v2 = MagicMock()
    mock_resp_v2.status_code = 200
    mock_resp_v2.text = v2_html
    mock_resp_v2.content = v2_html.encode("utf-8")
    mock_resp_v2.headers = {"ETag": '"hash-v2"', "Content-Type": "text/html"}
    mock_resp_v2.history = []

    # ──────────────────────────────────────────────────────────────────────────
    # Step 4: Monitor detects the difference
    # ──────────────────────────────────────────────────────────────────────────
    with patch("requests.get", return_value=mock_resp_v2), patch("app.services.security_check.validate_and_resolve_url", return_value=("https://aaplesarkar.mahaonline.gov.in", "103.20.10.1")):
        res_v2 = engine.check_source("src_official_e2e_test")
        assert res_v2["status"] == "changed"
        assert res_v2["changes_count"] >= 1

    # ──────────────────────────────────────────────────────────────────────────
    # Step 5: A change record with evidence is created
    # ──────────────────────────────────────────────────────────────────────────
    with get_db_session() as s:
        changes = (
            s.query(DetectedChange)
            .filter_by(source_id="src_official_e2e_test", target_id=target_service_id, status="proposed")
            .all()
        )
        assert len(changes) >= 1
        req_change = [c for c in changes if c.change_type == "new_requirement"][0]
        assert "self declaration form" in req_change.evidence_quote.lower()
        assert req_change.evidence_source_url == "https://aaplesarkar.mahaonline.gov.in/e2e/test_notice"
        chg_id = req_change.id

        # ──────────────────────────────────────────────────────────────────────
        # Step 6: Review policy determines whether approval is needed
        # (Status is 'proposed', requiring authorized reviewer approval)
        # ──────────────────────────────────────────────────────────────────────
        assert req_change.status == "proposed"

    # ──────────────────────────────────────────────────────────────────────────
    # Step 7: Authorized reviewer approves the change
    # ──────────────────────────────────────────────────────────────────────────
    approve_result = approve_and_publish_change(
        change_id=chg_id,
        reviewer_username="senior_officer",
        notes="Verified against official Maharashtra Government circular.",
    )
    assert approve_result["status"] == "success"
    new_version_num = approve_result["new_version"]

    # ──────────────────────────────────────────────────────────────────────────
    # Step 8: Updated requirement becomes visible through existing public API & UI
    # ──────────────────────────────────────────────────────────────────────────
    api_res = client.get(f"/api/services/{target_service_id}")
    assert api_res.status_code == 200
    svc_data = api_res.json["data"]
    item_doc_ids = [item.get("document_id") for item in svc_data["items"] if item.get("type") == "document"]
    assert "self_declaration_form" in item_doc_ids

    ui_res = client.get(f"/service/{target_service_id}")
    assert ui_res.status_code == 200
    assert "Officially Verified" in ui_res.text

    # ──────────────────────────────────────────────────────────────────────────
    # Step 9: Previous version remains accessible in history
    # ──────────────────────────────────────────────────────────────────────────
    hist_res = client.get(f"/api/services/{target_service_id}/history")
    assert hist_res.status_code == 200
    history_versions = [v["version_number"] for v in hist_res.json["data"]]
    assert 1 in history_versions
    assert new_version_num in history_versions

    # ──────────────────────────────────────────────────────────────────────────
    # Step 10: Repeated check does not create a duplicate change
    # ──────────────────────────────────────────────────────────────────────────
    with patch("requests.get", return_value=mock_resp_v2), patch("app.services.security_check.validate_and_resolve_url", return_value=("https://aaplesarkar.mahaonline.gov.in", "103.20.10.1")):
        res_repeat = engine.check_source("src_official_e2e_test")
        # Fingerprint is already matched, returns unchanged
        assert res_repeat["status"] == "unchanged"
        assert res_repeat["changes_count"] == 0

    # ──────────────────────────────────────────────────────────────────────────
    # Step 11: Failed source check does not erase the last verified version
    # ──────────────────────────────────────────────────────────────────────────
    with patch("requests.get", side_effect=Exception("Gateway Timeout 504")), patch("app.services.security_check.validate_and_resolve_url", return_value=("https://aaplesarkar.mahaonline.gov.in", "103.20.10.1")):
        res_fail = engine.check_source("src_official_e2e_test")
        assert res_fail["status"] == "error"

    # Verify public service remains verified and active at updated version
    api_res_after_fail = client.get(f"/api/services/{target_service_id}")
    assert api_res_after_fail.status_code == 200
    assert api_res_after_fail.json["data"]["service"]["version"] == new_version_num

    # ──────────────────────────────────────────────────────────────────────────
    # Step 12: Rollback restores the previous published version
    # ──────────────────────────────────────────────────────────────────────────
    rollback_res = rollback_service_version(
        service_id=target_service_id,
        target_version_number=1,
        reviewer_username="senior_officer",
        reason="Administrative rollback to baseline version 1",
    )
    assert rollback_res["status"] == "success"

    # Verify restored state via public API
    api_res_after_rollback = client.get(f"/api/services/{target_service_id}")
    assert api_res_after_rollback.status_code == 200
    restored_items = [item.get("document_id") for item in api_res_after_rollback.json["data"]["items"] if item.get("type") == "document"]
    # In version 1, self_declaration_form was not in caste_validity_certificate requirements
    assert "self_declaration_form" not in restored_items
