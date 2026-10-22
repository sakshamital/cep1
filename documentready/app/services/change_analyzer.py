"""Structured change analysis engine for government source monitoring.

Compares newly retrieved official content against stored service/document records,
categorizes changes with deterministic rules, and captures grounded evidence.
"""
from __future__ import annotations

import difflib
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

# Pattern matchers for common government document clauses in India
_FEE_PATTERNS = [
    re.compile(r"(?:fee|charges?|rs\.?|inr|amount)\s*[:=-]?\s*(?:rs\.?|inr)?\s*(\d+(?:,\d+)?(?:\s*/-)?)", re.IGNORECASE),
    re.compile(r"(?:free of cost|no fee|nil fee)", re.IGNORECASE),
]

_PORTAL_PATTERNS = [
    re.compile(r"(https?://[a-zA-Z0-9.\-_/]+(?:mahaonline|gov\.in|nic\.in|uidai|mahadbt)[a-zA-Z0-9.\-_/]*)", re.IGNORECASE),
]

_DOCUMENT_KEYWORDS = {
    "aadhaar": ["aadhaar", "aadhar", "uid", "uidai"],
    "photograph": ["photograph", "passport size photo", "photo", "photographs"],
    "residence_proof": ["residence proof", "address proof", "domicile proof", "electricity bill", "ration card"],
    "caste_certificate": ["caste certificate", "jaati praman", "caste proof"],
    "income_certificate": ["income certificate", "utpannacha dakhla", "tahsildar income cert"],
    "school_leaving_certificate": ["school leaving", "transfer certificate", "tc", "bonafide"],
    "affidavit_stamp_paper": ["affidavit", "stamp paper", "notarised affidavit", "self declaration on stamp paper"],
    "ration_card": ["ration card", "rationing card"],
    "electricity_bill": ["electricity bill", "light bill", "power bill"],
    "rent_agreement": ["rent agreement", "registered lease"],
    "self_declaration_form": ["self declaration form", "swayam ghoshana patra", "declaration format"],
    "relative_validity_record": ["blood relative validity", "relative caste validity", "family validity order"],
    "admission_letter": ["admission letter", "allotment letter", "college admission receipt"],
}


class ChangeAnalysisResult:
    def __init__(
        self,
        change_type: str,
        summary: str,
        previous_data: dict,
        proposed_data: dict,
        evidence_quote: str,
        evidence_source_url: str,
        evidence_section: str = "",
        confidence_score: float = 1.0,
    ):
        self.change_type = change_type
        self.summary = summary
        self.previous_data = previous_data
        self.proposed_data = proposed_data
        self.evidence_quote = evidence_quote
        self.evidence_source_url = evidence_source_url
        self.evidence_section = evidence_section
        self.confidence_score = confidence_score

    def to_dict(self) -> dict:
        return {
            "change_type": self.change_type,
            "summary": self.summary,
            "previous_data": self.previous_data,
            "proposed_data": self.proposed_data,
            "evidence_quote": self.evidence_quote,
            "evidence_source_url": self.evidence_source_url,
            "evidence_section": self.evidence_section,
            "confidence_score": self.confidence_score,
        }


def normalize_content_text(text: str) -> str:
    """Normalize text by collapsing whitespace and standardizing casing for comparison."""
    if not text:
        return ""
    # Strip HTML tags if any remain
    clean = re.sub(r"<[^>]+>", " ", text)
    # Collapse whitespace
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def compare_service_content(
    source_url: str,
    raw_text: str,
    existing_service_dict: dict,
    section_name: str = "Official Notice",
) -> list[ChangeAnalysisResult]:
    """Analyze retrieved text from a source against an existing service record.
    
    Returns a list of ChangeAnalysisResult objects representing detected changes.
    """
    detected_changes: list[ChangeAnalysisResult] = []
    text_lower = raw_text.lower()

    # 1. Check for newly introduced document requirements
    existing_req_doc_ids = set()
    for req in existing_service_dict.get("requirements", []):
        if req.get("document_id"):
            existing_req_doc_ids.add(req["document_id"])
        for opt in req.get("options", []):
            existing_req_doc_ids.add(opt)

    for doc_id, keywords in _DOCUMENT_KEYWORDS.items():
        if doc_id not in existing_req_doc_ids:
            for kw in keywords:
                # Check for explicit requirement keywords nearby (mandatory, required, must attach, submit)
                pattern = rf"(?:mandatory|compulsory|required|must attach|submit|documents? required)[^.\n]{{0,100}}\b{re.escape(kw)}\b"
                match = re.search(pattern, text_lower)
                if not match:
                    # Alternative pattern: keyword followed by required
                    pattern = rf"\b{re.escape(kw)}\b[^.\n]{{0,60}}(?:is mandatory|is required|must be submitted)"
                    match = re.search(pattern, text_lower)

                if match:
                    # Extract surrounding context (150 chars) as evidence
                    start = max(0, match.start() - 40)
                    end = min(len(raw_text), match.end() + 60)
                    evidence_snippet = raw_text[start:end].strip()

                    detected_changes.append(
                        ChangeAnalysisResult(
                            change_type="new_requirement",
                            summary=f"Official source specifies new mandatory document requirement: {doc_id.replace('_', ' ').title()}",
                            previous_data={"requirements": existing_service_dict.get("requirements", [])},
                            proposed_data={
                                "added_requirement": {
                                    "document_id": doc_id,
                                    "necessity": "required",
                                    "note": f"Detected in official publication: '{evidence_snippet}'",
                                }
                            },
                            evidence_quote=evidence_snippet,
                            evidence_source_url=source_url,
                            evidence_section=section_name,
                            confidence_score=0.92,
                        )
                    )
                    break  # Found for this doc_id

    # 2. Check for official portal link changes
    portal_matches = []
    for pat in _PORTAL_PATTERNS:
        portal_matches.extend(pat.findall(raw_text))

    current_portal = existing_service_dict.get("application_info", {}).get("where", "")
    if portal_matches:
        discovered_link = portal_matches[0]
        if discovered_link not in current_portal and discovered_link != current_portal:
            # Context
            idx = raw_text.find(discovered_link)
            snippet = raw_text[max(0, idx - 40): min(len(raw_text), idx + len(discovered_link) + 40)].strip()
            detected_changes.append(
                ChangeAnalysisResult(
                    change_type="changed_link",
                    summary=f"Updated official application portal URL discovered: {discovered_link}",
                    previous_data={"official_link": current_portal},
                    proposed_data={"official_link": discovered_link},
                    evidence_quote=snippet,
                    evidence_source_url=source_url,
                    evidence_section=section_name,
                    confidence_score=0.95,
                )
            )

    # 3. Check for fee updates
    for pattern in _FEE_PATTERNS:
        fee_match = pattern.search(raw_text)
        if fee_match:
            fee_text = fee_match.group(0)
            current_fee = existing_service_dict.get("application_info", {}).get("fee_note", "")
            if fee_text.lower() not in current_fee.lower():
                snippet = raw_text[max(0, fee_match.start() - 30): min(len(raw_text), fee_match.end() + 30)].strip()
                detected_changes.append(
                    ChangeAnalysisResult(
                        change_type="changed_fee",
                        summary=f"Official fee update detected: {fee_text}",
                        previous_data={"fee_note": current_fee},
                        proposed_data={"fee_note": f"Official prescribed fee: {fee_text}"},
                        evidence_quote=snippet,
                        evidence_source_url=source_url,
                        evidence_section=section_name,
                        confidence_score=0.88,
                    )
                )
                break

    return detected_changes
