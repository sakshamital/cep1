"""
Service-layer unit tests — PDF processing, government change analysis,
and SSRF / security URL validation.
"""
import io
import pytest
import pypdf
from unittest.mock import MagicMock, patch
from app.services.pdf_processor import PDFProcessingError, extract_pdf_data
from app.services.change_analyzer import compare_service_content
from app.services.security_check import SSRFValidationError, is_ip_blocked, validate_and_resolve_url


# ── PDF Processing ────────────────────────────────────────────────────────────

def _make_pdf(text: str = "", title: str = "Government Circular") -> bytes:
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_metadata({"/Title": title, "/Author": "Department of Revenue", "/Subject": "Checklist Update"})
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def test_extract_pdf_metadata():
    data = extract_pdf_data(_make_pdf(title="GR No 2026/89"))
    assert data["page_count"] == 1
    assert data["title"] == "GR No 2026/89"
    assert data["is_scanned"] is True  # Blank page triggers scanned detection


def test_corrupt_pdf_handling():
    with pytest.raises(PDFProcessingError):
        extract_pdf_data(b"NOT_A_REAL_PDF_HEADER_DATA_12345")


# ── Change Analysis ───────────────────────────────────────────────────────────

def test_detect_new_mandatory_requirement():
    source_url = "https://aaplesarkar.mahaonline.gov.in/en/Department/Notice/99"
    official_text = (
        "GOVERNMENT RESOLUTION NO. REV-2026/89: "
        "For Caste Certificate Service, the applicant must attach self declaration form "
        "and electricity bill is mandatory for address verification."
    )
    existing = {
        "id": "caste_certificate",
        "requirements": [
            {"document_id": "aadhaar", "necessity": "required"},
            {"document_id": "residence_proof", "necessity": "required"},
        ],
        "application_info": {"where": "Tahsil Office", "fee_note": "Rs 20"},
    }
    changes = compare_service_content(source_url, official_text, existing)
    assert len(changes) >= 1
    types = [c.change_type for c in changes]
    assert "new_requirement" in types
    req = next(c for c in changes if c.change_type == "new_requirement")
    assert req.evidence_source_url == source_url
    assert len(req.evidence_quote) > 0
    assert req.confidence_score >= 0.8


def test_detect_portal_link_and_fee_update():
    source_url = "https://aaplesarkar.mahaonline.gov.in/notice"
    official_text = (
        "All applications must be submitted online at https://aaplesarkar.mahaonline.gov.in/portal/apply. "
        "The prescribed fee is Rs 35 for service delivery."
    )
    existing = {
        "id": "income_certificate",
        "requirements": [],
        "application_info": {"where": "Offline Tahsil counter", "fee_note": "Free of cost"},
    }
    changes = compare_service_content(source_url, official_text, existing)
    types = [c.change_type for c in changes]
    assert "changed_link" in types
    assert "changed_fee" in types
    link_chg = next(c for c in changes if c.change_type == "changed_link")
    assert "https://aaplesarkar.mahaonline.gov.in/portal/apply" in link_chg.proposed_data["official_link"]


# ── Security / SSRF ───────────────────────────────────────────────────────────

def test_blocked_ip_ranges():
    for ip in ["127.0.0.1", "127.0.1.5", "10.0.0.1", "192.168.1.100",
               "172.16.5.10", "169.254.169.254", "::1", "0.0.0.0"]:
        assert is_ip_blocked(ip) is True, f"{ip} should be blocked"
    for ip in ["8.8.8.8", "1.1.1.1"]:
        assert is_ip_blocked(ip) is False, f"{ip} should be allowed"


def test_validate_url_schemes():
    for url in ["file:///etc/passwd", "ftp://ftp.example.gov.in/data", "gopher://127.0.0.1:70"]:
        with pytest.raises(SSRFValidationError, match="scheme"):
            validate_and_resolve_url(url)


def test_validate_prohibited_hostnames():
    for url in [
        "http://localhost/admin",
        "http://127.0.0.1:5000/api",
        "http://169.254.169.254/latest/meta-data/",
        "http://internal.service.local/status",
    ]:
        with pytest.raises(SSRFValidationError):
            validate_and_resolve_url(url)


def test_validate_public_url():
    url, ip = validate_and_resolve_url("https://aaplesarkar.mahaonline.gov.in")
    assert url.startswith("https://")
    assert ip != ""
