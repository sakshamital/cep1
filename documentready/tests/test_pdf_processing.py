"""Tests for government PDF processing adapter."""
import io
import pytest
import pypdf
from app.services.pdf_processor import (
    PDFProcessingError,
    extract_pdf_data,
)


def create_synthetic_pdf(text: str, title: str = "Government Circular") -> bytes:
    """Helper to generate in-memory synthetic PDF bytes for testing."""
    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_metadata({
        "/Title": title,
        "/Author": "Department of Revenue",
        "/Subject": "Checklist Update",
    })
    
    # Note: blank page won't have text unless drawn, or we can write PDF directly
    # To embed text, pypdf doesn't draw text easily without reportlab, but pypdf can read pages
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_extract_pdf_metadata():
    """Verify metadata extraction on valid PDF."""
    pdf_bytes = create_synthetic_pdf("Sample text", title="GR No 2026/89")
    data = extract_pdf_data(pdf_bytes)

    assert data["page_count"] == 1
    assert data["title"] == "GR No 2026/89"
    # Blank synthetic page has 0 text, so scanned detection triggers appropriately
    assert data["is_scanned"] is True


def test_corrupt_pdf_handling():
    """Verify malformed/corrupt bytes raise PDFProcessingError safely."""
    corrupt_bytes = b"NOT_A_REAL_PDF_HEADER_DATA_12345"
    with pytest.raises(PDFProcessingError):
        extract_pdf_data(corrupt_bytes)
