"""Automated official government source monitoring engine.

Executes safe HTTP/PDF fetches with SSRF protection, conditional ETag/Last-Modified requests,
content normalization, fingerprinting, change detection, and duplicate suppression.
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.models.db_models import (
    AuditEvent,
    DetectedChange,
    ServiceRecord,
    SourceDocument,
    SourceFetchHistory,
    SourceRegistry,
    utc_now,
)
from app.services.change_analyzer import compare_service_content
from app.services.database import get_db_session
from app.services.security_check import SSRFValidationError, validate_and_resolve_url

logger = logging.getLogger(__name__)

USER_AGENT = "DocumentReady-GovMonitor/1.0 (+https://documentready.gov.in/bot)"


def normalize_html_content(html_str: str) -> str:
    """Strip scripts, styles, comments, dynamic tokens, and normalize whitespace for fingerprinting."""
    if not html_str:
        return ""
    soup = BeautifulSoup(html_str, "html.parser")

    # Remove script, style, meta, iframe, noscript tags
    for tag in soup(["script", "style", "meta", "noscript", "iframe", "svg"]):
        tag.decompose()

    # Get clean text
    text = soup.get_text(separator=" ")

    # Strip dynamic timestamps, CSRF tokens, session IDs
    text = re.sub(r"\b[0-9a-fA-F]{32,64}\b", "", text)
    text = re.sub(r"\b(?:csrf|token|sessionid|timestamp|datetime)=[^& ]+", "", text, flags=re.IGNORECASE)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def compute_fingerprint(text: str) -> str:
    """Compute deterministic SHA256 content fingerprint."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class MonitoringEngine:
    """Orchestrates source fetching, change detection, and history logging."""

    def __init__(self, timeout: int = 15, max_retries: int = 2):
        self.timeout = timeout
        self.max_retries = max_retries

    def check_source(self, source_id: str, session: Optional[Session] = None, force: bool = False) -> dict:
        """Perform a monitoring check for a specific registered source.
        
        Returns a dict summary of check results:
            {'source_id': str, 'status': 'unchanged' | 'changed' | 'error', 'changes_count': int, 'message': str}
        """
        if session is not None:
            return self._execute_check(source_id, session, force)
        else:
            with get_db_session() as s:
                return self._execute_check(source_id, s, force)

    def _execute_check(self, source_id: str, session: Session, force: bool = False) -> dict:
        source = session.query(SourceRegistry).filter_by(id=source_id).first()
        if not source:
            return {"source_id": source_id, "status": "error", "message": f"Source '{source_id}' not found."}

        if not source.enabled and not force:
            return {"source_id": source_id, "status": "skipped", "message": "Source is disabled."}

        source.last_attempted_check = utc_now()
        start_time = time.time()

        try:
            # Step 1: SSRF Validation
            validate_and_resolve_url(source.monitored_url)

            # Step 2: Fetch with conditional headers
            headers = {"User-Agent": USER_AGENT}
            if source.etag and not force:
                headers["If-None-Match"] = source.etag
            if source.last_modified_header and not force:
                headers["If-Modified-Since"] = source.last_modified_header

            # Attempt HTTP request with retry backoff
            response = None
            last_req_err = None
            for attempt in range(self.max_retries + 1):
                try:
                    response = requests.get(
                        source.monitored_url,
                        headers=headers,
                        timeout=self.timeout,
                        allow_redirects=True,
                    )
                    # Re-validate redirect destination URL against SSRF
                    if response.history:
                        for resp in response.history:
                            validate_and_resolve_url(resp.url)
                        validate_and_resolve_url(response.url)
                    break
                except (requests.RequestException, SSRFValidationError) as err:
                    last_req_err = err
                    time.sleep(0.5 * (2 ** attempt))

            if response is None:
                raise last_req_err or Exception("Failed to connect to source.")

            duration_ms = int((time.time() - start_time) * 1000)
            source.last_http_status = response.status_code

            # Handle 304 Not Modified
            if response.status_code == 304:
                source.last_successful_check = utc_now()
                source.consecutive_failures = 0
                source.last_error_message = None

                fetch_log = SourceFetchHistory(
                    source_id=source.id,
                    http_status=304,
                    response_time_ms=duration_ms,
                    content_fingerprint=source.current_fingerprint,
                    change_detected=False,
                )
                session.add(fetch_log)
                session.commit()
                return {
                    "source_id": source.id,
                    "status": "unchanged",
                    "changes_count": 0,
                    "message": "Content unchanged (HTTP 304 Not Modified).",
                }

            if response.status_code >= 400:
                raise Exception(f"HTTP error {response.status_code} received from source.")

            # Step 3: Parse and compute fingerprint
            is_pdf = (source.source_type == "pdf" or "application/pdf" in response.headers.get("Content-Type", "").lower())
            if is_pdf:
                from app.services.pdf_processor import extract_pdf_data
                pdf_data = extract_pdf_data(response.content)
                normalized_text = pdf_data["text"]
            else:
                normalized_text = normalize_html_content(response.text)

            fingerprint = compute_fingerprint(normalized_text)

            # Step 4: Compare fingerprint
            if source.current_fingerprint == fingerprint and not force:
                source.last_successful_check = utc_now()
                source.consecutive_failures = 0
                source.last_error_message = None

                fetch_log = SourceFetchHistory(
                    source_id=source.id,
                    http_status=response.status_code,
                    response_time_ms=duration_ms,
                    content_fingerprint=fingerprint,
                    change_detected=False,
                )
                session.add(fetch_log)
                session.commit()
                return {
                    "source_id": source.id,
                    "status": "unchanged",
                    "changes_count": 0,
                    "message": "Fingerprint identical; no meaningful changes detected.",
                }

            # Step 5: Content changed — perform structured change analysis
            detected_changes_list = []
            associated_svc_ids = source.associated_service_ids or []
            for svc_id in associated_svc_ids:
                svc = session.query(ServiceRecord).filter_by(id=svc_id).first()
                if svc:
                    svc_dict = svc.to_dict()
                    changes = compare_service_content(source.monitored_url, normalized_text, svc_dict)
                    for chg in changes:
                        # Check duplicate suppression: avoid creating identical proposed change if already pending
                        existing_dup = (
                            session.query(DetectedChange)
                            .filter_by(
                                source_id=source.id,
                                target_id=svc.id,
                                change_type=chg.change_type,
                                status="proposed",
                            )
                            .first()
                        )
                        if existing_dup:
                            existing_dup.summary = chg.summary
                            existing_dup.evidence_quote = chg.evidence_quote
                            existing_dup.detected_at = utc_now()
                            continue

                        change_rec = DetectedChange(
                            source_id=source.id,
                            target_type="service",
                            target_id=svc.id,
                            change_type=chg.change_type,
                            summary=chg.summary,
                            previous_data_json=json.dumps(chg.previous_data),
                            proposed_data_json=json.dumps(chg.proposed_data),
                            evidence_quote=chg.evidence_quote,
                            evidence_source_url=chg.evidence_source_url,
                            evidence_section=chg.evidence_section or source.name,
                            confidence_score=chg.confidence_score,
                            status="proposed",
                            detected_at=utc_now(),
                        )
                        session.add(change_rec)
                        detected_changes_list.append(change_rec)

            # Update source state
            source.current_fingerprint = fingerprint
            source.etag = response.headers.get("ETag")
            source.last_modified_header = response.headers.get("Last-Modified")
            source.last_successful_check = utc_now()
            source.last_detected_change = utc_now()
            source.consecutive_failures = 0
            source.last_error_message = None

            # Log fetch
            fetch_log = SourceFetchHistory(
                source_id=source.id,
                http_status=response.status_code,
                response_time_ms=duration_ms,
                content_fingerprint=fingerprint,
                change_detected=True,
            )
            session.add(fetch_log)

            # Log audit event
            audit = AuditEvent(
                event_type="source_change_detected",
                actor="monitoring_engine",
                details_json=json.dumps({
                    "source_id": source.id,
                    "fingerprint": fingerprint,
                    "changes_count": len(detected_changes_list),
                }),
            )
            session.add(audit)
            session.commit()

            return {
                "source_id": source.id,
                "status": "changed",
                "changes_count": len(detected_changes_list),
                "message": f"Change detected; {len(detected_changes_list)} requirement updates proposed for review.",
            }

        except Exception as exc:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error("Error monitoring source '%s': %s", source_id, exc)
            source.consecutive_failures += 1
            source.last_error_message = str(exc)

            fetch_log = SourceFetchHistory(
                source_id=source.id,
                http_status=source.last_http_status or 500,
                response_time_ms=duration_ms,
                change_detected=False,
                error_message=str(exc),
            )
            session.add(fetch_log)
            session.commit()

            return {
                "source_id": source.id,
                "status": "error",
                "changes_count": 0,
                "message": f"Check failed: {exc}",
            }

    def check_all_sources(self, force: bool = False) -> list[dict]:
        """Check all registered and enabled sources sequentially."""
        results = []
        with get_db_session() as session:
            sources = session.query(SourceRegistry).filter_by(enabled=True).all()
            source_ids = [s.id for s in sources]

        for s_id in source_ids:
            with get_db_session() as session:
                res = self.check_source(s_id, session=session, force=force)
                results.append(res)
        return results


# Module instance
monitor_engine = MonitoringEngine()
