"""Tests for structured change analysis and grounded evidence capture."""
import pytest
from app.services.change_analyzer import compare_service_content


def test_detect_new_mandatory_requirement():
    """Verify newly introduced document is detected with exact evidence."""
    source_url = "https://aaplesarkar.mahaonline.gov.in/en/Department/Notice/99"
    official_text = (
        "GOVERNMENT RESOLUTION NO. REV-2026/89: "
        "For Caste Certificate Service, the applicant must attach self declaration form "
        "and electricity bill is mandatory for address verification."
    )
    existing_service = {
        "id": "caste_certificate",
        "requirements": [
            {"document_id": "aadhaar", "necessity": "required"},
            {"document_id": "residence_proof", "necessity": "required"},
        ],
        "application_info": {"where": "Tahsil Office", "fee_note": "Rs 20"},
    }

    changes = compare_service_content(source_url, official_text, existing_service)
    assert len(changes) >= 1

    # Should detect electricity_bill or self_declaration_form
    detected_types = [c.change_type for c in changes]
    assert "new_requirement" in detected_types

    req_change = [c for c in changes if c.change_type == "new_requirement"][0]
    assert req_change.evidence_source_url == source_url
    assert len(req_change.evidence_quote) > 0
    assert req_change.confidence_score >= 0.8


def test_detect_portal_link_and_fee_update():
    """Verify updated portal URL and fee changes are detected."""
    source_url = "https://aaplesarkar.mahaonline.gov.in/notice"
    official_text = (
        "All applications must be submitted online at https://aaplesarkar.mahaonline.gov.in/portal/apply. "
        "The prescribed fee is Rs 35 for service delivery."
    )
    existing_service = {
        "id": "income_certificate",
        "requirements": [],
        "application_info": {
            "where": "Offline Tahsil counter",
            "fee_note": "Free of cost",
        },
    }

    changes = compare_service_content(source_url, official_text, existing_service)
    types = [c.change_type for c in changes]
    assert "changed_link" in types
    assert "changed_fee" in types

    link_change = [c for c in changes if c.change_type == "changed_link"][0]
    assert "https://aaplesarkar.mahaonline.gov.in/portal/apply" in link_change.proposed_data["official_link"]
