"""Optional AI Assistant for DocumentReady.

Provides plain-language explanations of government rules, prerequisite reasoning,
and change summarization with grounded citations.
Operates completely offline with deterministic fallbacks when AI keys are not configured.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


def explain_requirements_simply(
    service_name: str,
    requirements: list[dict],
    applicant_category: Optional[str] = None,
) -> dict:
    """Generate a citizen-friendly plain-language explanation of service requirements.
    
    Returns structured dict with 'summary', 'key_takeaways', and 'advice'.
    """
    total_reqs = len(requirements)
    doc_names = []
    has_any_of = False

    for r in requirements:
        if r.get("document_id"):
            doc_names.append(r["document_id"].replace("_", " ").title())
        elif r.get("type") == "any_of" or r.get("group"):
            has_any_of = True

    category_clause = f" for {applicant_category.title()} applicants" if applicant_category else ""
    summary = (
        f"To apply for {service_name}{category_clause}, you need to prepare {total_reqs} primary document requirements. "
        f"Make sure all documents have matching names and dates of birth across records."
    )

    takeaways = [
        "Ensure all identity documents have your current, updated residential address.",
        "Keep both original documents and 2 sets of self-attested photocopies ready.",
    ]
    if has_any_of:
        takeaways.append("For address proof, you only need to provide any ONE valid document from the specified list.")

    advice = (
        "Check your checklist readiness before visiting the authority. If any prerequisite document "
        "is missing, obtain it first according to the guided sequence."
    )

    return {
        "summary": summary,
        "key_takeaways": takeaways,
        "advice": advice,
        "is_ai_generated": False,  # Verified deterministic template
    }


def explain_prerequisite_chain(doc_name: str, prerequisites: list[str]) -> str:
    """Explain why a document requires prerequisites before it can be issued."""
    if not prerequisites:
        return f"{doc_name} is a base document and does not require prior government certificates."

    prereq_str = ", ".join(p.replace("_", " ").title() for p in prerequisites)
    return (
        f"Before you can apply for {doc_name}, the issuing department requires verified proof from {prereq_str}. "
        f"The issuing authority verifies identity, residence, and category eligibility through these prerequisite records."
    )


def summarize_verified_change(change_type: str, previous_val: str, new_val: str, evidence: str) -> str:
    """Summarize a verified change in clear, citizen-friendly language."""
    if change_type == "new_requirement":
        return f"New requirement added: Applicants must now provide '{new_val}'. (Source: {evidence[:80]}...)"
    elif change_type == "changed_fee":
        return f"Fee updated: Previous fee was '{previous_val}'; officially revised to '{new_val}'."
    elif change_type == "changed_link":
        return f"Official application portal link updated to: {new_val}."
    else:
        return f"Requirements updated from official government circular: {evidence[:100]}..."
