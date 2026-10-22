"""Readiness engine: evaluates whether a user is ready to apply for a service."""
from __future__ import annotations

from app.models.entities import ReadinessResult
from app.services.graph import prerequisite_closure, topological_order
from app.services.repository import get_repo
from app.services.requirements import resolve_requirements

DISCLAIMER = (
    "Document requirements may vary by department, location, applicant category "
    "and current government guidelines. Users should verify final requirements "
    "with the relevant official authority."
)

VALID_STATUSES = {"available", "missing"}


def evaluate(
    service_id: str,
    statuses: dict[str, str],
    applicant_category: str | None = None,
) -> ReadinessResult:
    """Evaluate readiness for a service given the user's document statuses.

    Args:
        service_id: The service to evaluate.
        statuses: Mapping of document_id -> "available" | "missing".
                  Unknown keys are ignored (returned as ignored_ids).
                  Missing keys are treated as "unmarked".
        applicant_category: Optional applicant category.

    Returns:
        ReadinessResult with ready flag, blockers, unverified, obtain_plan, etc.
    """
    repo = get_repo()
    documents = repo.get_all_documents()

    # Track unknown / ignored IDs
    known_ids = set(documents.keys())
    ignored_ids = [doc_id for doc_id in statuses if doc_id not in known_ids]
    clean_statuses: dict[str, str] = {k: v for k, v in statuses.items() if k in known_ids}

    resolved = resolve_requirements(service_id, applicant_category)
    items = resolved.items

    blockers: list[dict] = []
    unverified: list[dict] = []
    group_results: list[dict] = []

    total_required = 0
    satisfied_required = 0

    for item in items:
        if item["type"] == "document":
            necessity = item["necessity"]
            doc_id = item["document_id"]
            doc = documents.get(doc_id)
            doc_name = doc.name if doc else doc_id

            if necessity == "optional":
                continue  # Never affects readiness

            # Required item
            total_required += 1
            status = clean_statuses.get(doc_id, "unmarked")

            if status == "available":
                satisfied_required += 1
            elif status == "missing":
                obtain_first = _compute_obtain_first(doc_id, clean_statuses, documents)
                blockers.append({
                    "document_id": doc_id,
                    "name": doc_name,
                    "status": "missing",
                    "obtain_first": obtain_first,
                })
            else:  # unmarked
                unverified.append({"document_id": doc_id, "name": doc_name})

        elif item["type"] == "any_of":
            group_id = item["group"]
            options = item["options"]
            total_required += 1

            available_options = [opt for opt in options if clean_statuses.get(opt) == "available"]
            missing_options = [opt for opt in options if clean_statuses.get(opt) == "missing"]
            unmarked_options = [opt for opt in options if clean_statuses.get(opt, "unmarked") == "unmarked"]

            group_satisfied = len(available_options) > 0

            option_details = []
            for opt in options:
                d = documents.get(opt)
                option_details.append({
                    "document_id": opt,
                    "name": d.name if d else opt,
                    "status": clean_statuses.get(opt, "unmarked"),
                })

            group_results.append({
                "group": group_id,
                "satisfied": group_satisfied,
                "options": option_details,
                "note": item.get("note"),
            })

            if group_satisfied:
                satisfied_required += 1
            elif missing_options and not unmarked_options:
                # All explicitly missing — pick the one with fewest missing prerequisites as "easiest"
                easiest = _pick_easiest(options, clean_statuses, documents)
                obtain_first = _compute_obtain_first(easiest, clean_statuses, documents)
                blockers.append({
                    "document_id": None,
                    "group": group_id,
                    "name": f"Any one of: {', '.join(documents[o].name if o in documents else o for o in options)}",
                    "status": "missing",
                    "obtain_first": obtain_first,
                    "options": option_details,
                })
            else:
                # Some unmarked — treat group as unverified
                unverified.append({
                    "document_id": None,
                    "group": group_id,
                    "name": f"Address proof group ({group_id}): select any one",
                })

    # Build ordered obtain plan (de-duplicated, topologically sorted)
    all_blocker_ids: list[str] = []
    for b in blockers:
        if b.get("document_id"):
            all_blocker_ids.append(b["document_id"])
        elif b.get("options"):
            # Add the easiest option
            for opt in b.get("options", []):
                if opt not in all_blocker_ids:
                    all_blocker_ids.append(opt["document_id"])
                    break

    # Collect all prerequisite chains for blockers
    plan_ids: set[str] = set()
    for bid in all_blocker_ids:
        plan_ids.add(bid)
        closure = prerequisite_closure(bid, documents)
        # Filter out prerequisites already available
        closure = {c for c in closure if clean_statuses.get(c) != "available"}
        plan_ids |= closure

    obtain_plan = topological_order(list(plan_ids), documents) if plan_ids else []

    # Readiness
    ready = (len(blockers) == 0 and len(unverified) == 0)
    percent = round(100 * satisfied_required / total_required) if total_required > 0 else 100

    if ready:
        message = "You're Ready to Apply."
    else:
        parts = []
        if blockers:
            parts.append(f"{len(blockers)} missing")
        if unverified:
            parts.append(f"{len(unverified)} not yet checked")
        message = (
            f"{satisfied_required} of {total_required} required items ready. "
            + ", ".join(parts) + "."
        )

    return ReadinessResult(
        ready=ready,
        message=message,
        progress={
            "satisfied": satisfied_required,
            "total": total_required,
            "percent": percent,
        },
        blockers=blockers,
        unverified=unverified,
        groups=group_results,
        obtain_plan=obtain_plan,
        ignored_ids=ignored_ids,
    )


def _compute_obtain_first(
    doc_id: str,
    statuses: dict[str, str],
    documents: dict,
) -> list[dict]:
    """Return prerequisite documents needed before obtaining doc_id, excluding already-available ones."""
    closure = prerequisite_closure(doc_id, documents)
    # Remove anything already available
    needed = {c for c in closure if statuses.get(c) != "available"}
    ordered = topological_order(list(needed), documents) if needed else []
    result = []
    for pid in ordered:
        doc = documents.get(pid)
        result.append({"document_id": pid, "name": doc.name if doc else pid})
    return result


def _pick_easiest(
    options: list[str],
    statuses: dict[str, str],
    documents: dict,
) -> str:
    """Pick the option with the fewest missing prerequisites (simplest to obtain)."""
    def missing_prereqs(opt: str) -> int:
        closure = prerequisite_closure(opt, documents)
        return sum(1 for c in closure if statuses.get(c) != "available")

    return min(options, key=missing_prereqs)
