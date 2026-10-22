"""Requirements resolver: determines which requirements apply for a service + applicant category + state."""
from __future__ import annotations

import json
import os
from typing import Optional

from app.models.entities import ResolvedRequirements, Service
from app.services.repository import get_repo

import logging

logger = logging.getLogger(__name__)

_state_rules_cache: Optional[dict] = None
_states_cache: Optional[list] = None


def clear_state_cache() -> None:
    """Clear memory cache for state rules and states."""
    global _state_rules_cache, _states_cache
    _state_rules_cache = None
    _states_cache = None


def _load_state_data() -> tuple[dict, list]:
    global _state_rules_cache, _states_cache
    if _state_rules_cache is None or _states_cache is None:
        try:
            from app.services.database import get_db_session, get_engine, seed_initial_data
            from app.models.db_models import Base, StateRecord, StateRuleRecord

            engine = get_engine()
            Base.metadata.create_all(engine)

            with get_db_session() as session:
                states_db = session.query(StateRecord).order_by(StateRecord.id).all()
                if not states_db:
                    seed_initial_data(session)
                    states_db = session.query(StateRecord).order_by(StateRecord.id).all()

                _states_cache = [s.to_dict() for s in states_db]

                rules_list = session.query(StateRuleRecord).all()
                rules_map: dict = {}
                for r in rules_list:
                    rules_map.setdefault(r.service_id, {})[r.state_id] = r.to_dict()
                _state_rules_cache = rules_map
        except Exception as exc:
            logger.warning("Could not load state data from database (%s); using initial seeds.", exc)
            from app.data.initial_data import STATES_SEED, STATE_RULES_SEED
            _states_cache = list(STATES_SEED)
            _state_rules_cache = dict(STATE_RULES_SEED)
    return _state_rules_cache, _states_cache


class RequirementsError(Exception):
    """Raised for invalid requirement resolution inputs."""


def get_state_rule(service_id: str, state_id: str | None) -> Optional[dict]:
    """Retrieve or generate the state-specific rule and guidelines for a service."""
    if not state_id:
        return None

    state_rules, states = _load_state_data()
    state_info = next((s for s in states if s["id"] == state_id), None)
    state_name = state_info["name"] if state_info else state_id

    # Check curated rules
    svc_rules = state_rules.get(service_id, {})
    if state_id in svc_rules:
        rule = dict(svc_rules[state_id])
        rule["state_name"] = state_name
        return rule

    # Fallback rule for any state/UT without custom rule
    return {
        "state_id": state_id,
        "state_name": state_name,
        "authority": f"Revenue Department / District Authority of {state_name}",
        "portal_name": f"{state_name} Citizen Services Portal",
        "portal_url": None,
        "statutory_rule": (
            f"Requirements and scrutiny are governed under the state rules of {state_name}. "
            f"Applicants must provide valid residence or domicile proof of {state_name} "
            f"along with category certifications attested by the competent district authority."
        ),
        "additional_requirements": [
            {
                "document_id": "domicile_certificate",
                "necessity": "required",
                "note": f"Proof of residence or domicile in {state_name}",
            }
        ],
        "application_steps": [
            f"Visit the official {state_name} citizen service portal or district Tehsil / SDM office",
            "Fill the state-prescribed application format",
            "Attach attested copies of all checklist documents and identity proofs",
            "Submit the application and collect the acknowledgment receipt",
            "Complete local inquiry/verification with the area revenue authority if notified",
            "Receive digitally signed certificate once sanctioned",
        ],
    }


def resolve_requirements(
    service_id: str,
    applicant_category: str | None = None,
    state_id: str | None = None,
) -> ResolvedRequirements:
    """Resolve which requirements apply for a service, optional category, and state.

    Conditional items are included only if the category matches; they are promoted to 'required'.
    State-specific requirements and rules are merged if a state_id is provided.
    """
    repo = get_repo()
    service = repo.get_service(service_id)
    if service is None:
        raise RequirementsError(f"Unknown service id: {service_id!r}")

    # Validate category
    if applicant_category is not None and service.applicant_categories:
        if applicant_category not in service.applicant_categories:
            raise RequirementsError(
                f"Invalid applicant_category {applicant_category!r} for service {service_id!r}. "
                f"Allowed: {service.applicant_categories}"
            )

    items: list[dict] = []
    hidden_conditional: list[str] = []
    existing_doc_ids: set[str] = set()

    for req in service.requirements:
        if req.necessity == "conditional":
            when_cats = (req.when or {}).get("applicant_category", [])
            if applicant_category and applicant_category in when_cats:
                items.append({
                    "type": "document",
                    "document_id": req.document_id,
                    "necessity": "required",  # Promote to required
                    "note": req.note,
                    "is_state_specific": False,
                })
                if req.document_id:
                    existing_doc_ids.add(req.document_id)
            else:
                if req.document_id:
                    hidden_conditional.append(req.document_id)

        elif req.necessity == "any_of":
            items.append({
                "type": "any_of",
                "group": req.group,
                "options": req.options,
                "necessity": "required",
                "note": req.note,
                "is_state_specific": False,
            })
            for opt in req.options:
                existing_doc_ids.add(opt)

        else:
            # required or optional
            items.append({
                "type": "document",
                "document_id": req.document_id,
                "necessity": req.necessity,
                "note": req.note,
                "is_state_specific": False,
            })
            if req.document_id:
                existing_doc_ids.add(req.document_id)

    # ── State-specific requirements injection ─────────────────────────────────
    state_rule = get_state_rule(service_id, state_id)
    if state_rule:
        for extra in state_rule.get("additional_requirements", []):
            doc_id = extra.get("document_id")
            if not doc_id:
                continue
            if doc_id in existing_doc_ids:
                # Mark existing item as emphasized for this state
                for itm in items:
                    if itm.get("document_id") == doc_id:
                        itm["is_state_specific"] = True
                        itm["state_id"] = state_id
                        itm["state_name"] = state_rule["state_name"]
                        if extra.get("note"):
                            itm["note"] = extra["note"]
            else:
                items.append({
                    "type": "document",
                    "document_id": doc_id,
                    "necessity": extra.get("necessity", "required"),
                    "note": extra.get("note"),
                    "is_state_specific": True,
                    "state_id": state_id,
                    "state_name": state_rule["state_name"],
                })
                existing_doc_ids.add(doc_id)

    return ResolvedRequirements(
        service=service.to_dict(),
        items=items,
        hidden_conditional=hidden_conditional,
        state_rule=state_rule,
    )
