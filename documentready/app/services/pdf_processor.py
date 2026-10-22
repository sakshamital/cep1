"""Government PDF and Document Processing Adapter.

Safely downloads, verifies, hashes, extracts metadata and text from government PDFs.
Handles corrupt files, oversized limits, scanned PDFs, and malformed files safely.
"""
from __future__ import annotations

import hashlib
import io
import logging
import os
import re
from datetime import datetime
from typing import Optional

import requests

logger = logging.getLogger(__name__)

MAX_PDF_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB


class PDFProcessingError(Exception):
    """Raised when PDF downloading or parsing fails."""


def safe_download_pdf(
    url: str,
    dest_dir: str,
    timeout: int = 15,
    max_bytes: int = MAX_PDF_SIZE_BYTES,
) -> tuple[bytes, str, str]:
    """Stream-download a PDF with size limits and SSRF check.
    
    Returns (raw_bytes, file_path, sha256_hash).
    """
    from app.services.security_check import validate_and_resolve_url

    validate_and_resolve_url(url)
    os.makedirs(dest_dir, exist_ok=True)

    headers = {
        "User-Agent": "DocumentReady-GovMonitor/1.0 (+https://documentready.gov.in/bot)",
        "Accept": "application/pdf, application/octet-stream, */*",
    }

    try:
        with requests.get(url, headers=headers, stream=True, timeout=timeout) as resp:
            resp.raise_for_status()

            # Check content-length header if provided
            content_length = resp.headers.get("Content-Length")
            if content_length and int(content_length) > max_bytes:
                raise PDFProcessingError(f"PDF exceeds maximum permitted size of {max_bytes} bytes.")

            buffer = io.BytesIO()
            total_read = 0
            hasher = hashlib.sha256()

            for chunk in resp.iter_content(chunk_size=16384):
                if chunk:
                    total_read += len(chunk)
                    if total_read > max_bytes:
                        raise PDFProcessingError(f"PDF download exceeded {max_bytes} bytes limit.")
                    buffer.write(chunk)
                    hasher.update(chunk)

            raw_bytes = buffer.getvalue()
            sha256_hash = hasher.hexdigest()
            file_name = f"{sha256_hash}.pdf"
            file_path = os.path.join(dest_dir, file_name)

            with open(file_path, "wb") as f:
                f.write(raw_bytes)

            return raw_bytes, file_path, sha256_hash

    except requests.RequestException as exc:
        raise PDFProcessingError(f"Failed to download PDF from {url}: {exc}") from exc


def extract_pdf_data(pdf_source: bytes | str) -> dict:
    """Extract text, page count, and metadata safely from PDF bytes or filepath.
    
    Returns dict with keys:
        'text': str,
        'metadata': dict,
        'page_count': int,
        'is_scanned': bool,
        'ocr_applied': bool,
        'title': str,
        'creation_date': str,
    """
    import pypdf

    try:
        if isinstance(pdf_source, str):
            stream = open(pdf_source, "rb")
        else:
            stream = io.BytesIO(pdf_source)

        reader = pypdf.PdfReader(stream)
        page_count = len(reader.pages)
        full_text_parts: list[str] = []

        for idx, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text() or ""
                if page_text:
                    full_text_parts.append(f"--- Page {idx + 1} ---\n{page_text}")
            except Exception as page_err:
                logger.warning("Error extracting text from page %d: %s", idx + 1, page_err)

        if isinstance(pdf_source, str):
            stream.close()

        raw_text = "\n\n".join(full_text_parts)
        # Clean text of null bytes and control chars
        cleaned_text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", " ", raw_text)
        cleaned_text = re.sub(r" +", " ", cleaned_text).strip()

        # Metadata extraction
        doc_info = reader.metadata or {}
        meta_dict = {}
        for k, v in doc_info.items():
            clean_k = str(k).lstrip("/")
            meta_dict[clean_k] = str(v) if v is not None else ""

        title = meta_dict.get("Title") or ""
        creation_date = meta_dict.get("CreationDate") or ""

        # Scanned PDF detection: if total alphabetic characters are very low (< 30) despite pages
        alpha_count = len(re.findall(r"[a-zA-Z0-9]", cleaned_text))
        is_scanned = (page_count > 0 and alpha_count < 30)

        ocr_applied = False
        # Optional OCR attempt if scanned and pytesseract available
        if is_scanned:
            try:
                import pytesseract
                from PIL import Image
                # We flag as scanned; if user has configured tesseract engine, OCR could run
                logger.info("PDF appears to be a scanned document without embedded text.")
            except ImportError:
                pass

        return {
            "text": cleaned_text,
            "metadata": meta_dict,
            "page_count": page_count,
            "is_scanned": is_scanned,
            "ocr_applied": ocr_applied,
            "title": title,
            "creation_date": creation_date,
        }

    except pypdf.errors.PdfReadError as exc:
        raise PDFProcessingError(f"Corrupt or malformed PDF: {exc}") from exc
    except Exception as exc:
        raise PDFProcessingError(f"Error parsing PDF: {exc}") from exc
