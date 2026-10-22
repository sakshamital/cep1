"""JSON API routes (/api/...)."""
from __future__ import annotations

import logging

from flask import Blueprint, jsonify, request

from app.services.graph import build_tree
from app.services.readiness import evaluate
from app.services.repository import get_repo, DISCLAIMER
from app.services.requirements import resolve_requirements, RequirementsError
from app.services.search import search
from app.services.validators import (
    ValidationError,
    validate_id,
    validate_limit,
    validate_query,
    validate_statuses,
)

logger = logging.getLogger(__name__)
bp = Blueprint("api", __name__, url_prefix="/api")

API_VERSION = "1"


def _meta() -> dict:
    return {"disclaimer": DISCLAIMER, "api_version": API_VERSION}


def _ok(data: object, **extra_meta) -> tuple:
    meta = {**_meta(), **extra_meta}
    return jsonify({"data": data, "meta": meta}), 200


def _err(code: str, message: str, status: int, details: dict | None = None) -> tuple:
    body: dict = {"error": {"code": code, "message": message}}
    if details:
        body["error"]["details"] = details
    return jsonify(body), status


# ── Health ────────────────────────────────────────────────────────────────────

@bp.route("/health")
def health():
    repo = get_repo()
    return _ok({
        "status": "ok",
        "services": len(repo.get_all_services()),
        "documents": len(repo.get_all_documents()),
    })


# ── States ────────────────────────────────────────────────────────────────────

@bp.route("/states")
def list_states():
    """Return list of Indian states/UTs for the state selector."""
    from app.services.database import get_db_session
    from app.models.db_models import StateRecord
    try:
        with get_db_session() as session:
            states = [s.to_dict() for s in session.query(StateRecord).order_by(StateRecord.name).all()]
            if not states:
                from app.data.initial_data import STATES_SEED
                states = list(STATES_SEED)
            return jsonify(states), 200
    except Exception as exc:
        logger.warning("Could not fetch states from database (%s); using seeds.", exc)
        from app.data.initial_data import STATES_SEED
        return jsonify(list(STATES_SEED)), 200


# ── Search ────────────────────────────────────────────────────────────────────

@bp.route("/search")
def search_endpoint():
    try:
        q = validate_query(request.args.get("q", ""))
        type_filter = request.args.get("type")
        limit = validate_limit(request.args.get("limit"), default=8, maximum=50)
    except ValidationError as exc:
        return _err("VALIDATION_ERROR", str(exc), 400, exc.details)

    hits = search(q, type_filter=type_filter, limit=limit)
    return _ok([h.to_dict() for h in hits])


# ── Services ──────────────────────────────────────────────────────────────────

@bp.route("/services")
def list_services():
    repo = get_repo()
    state_id = request.args.get("state", "").strip() or None
    result = []
    for s in repo.get_all_services().values():
        item = {
            "id": s.id,
            "name": s.name,
            "type": s.type,
            "department": s.department,
            "verified": s.verified,
            "description": s.description[:160],
            "jurisdiction": getattr(s, "jurisdiction", "Maharashtra"),
        }
        result.append(item)
    return _ok(result)


@bp.route("/services/<service_id>")
def get_service(service_id: str):
    try:
        validate_id(service_id, "service_id")
    except ValidationError as exc:
        return _err("VALIDATION_ERROR", str(exc), 400)

    repo = get_repo()
    svc = repo.get_service(service_id)
    if svc is None:
        return _err("NOT_FOUND", f"Service '{service_id}' not found", 404)

    category = request.args.get("category")
    state_id = request.args.get("state", "").strip() or None
    try:
        resolved = resolve_requirements(service_id, category or None, state_id=state_id)
    except RequirementsError as exc:
        return _err("VALIDATION_ERROR", str(exc), 400)

    # Enrich each item with document details
    enriched_items = []
    for item in resolved.items:
        if item["type"] == "document":
            doc = repo.get_document(item["document_id"])
            enriched_items.append({
                **item,
                "document": {
                    "id": doc.id,
                    "name": doc.name,
                    "kind": doc.kind,
                    "verified": doc.verified,
                    "guide_id": doc.guide_id,
                    "has_guide": doc.guide_id is not None,
                    "prerequisites": doc.prerequisites,
                } if doc else {
                    "id": item["document_id"],
                    "name": item["document_id"].replace("_", " ").title(),
                    "kind": "certificate",
                    "verified": False,
                    "guide_id": None,
                    "has_guide": False,
                    "prerequisites": [],
                },
            })
        elif item["type"] == "any_of":
            opts = []
            for opt_id in item["options"]:
                doc = repo.get_document(opt_id)
                opts.append({
                    "document_id": opt_id,
                    "name": doc.name if doc else opt_id,
                    "kind": doc.kind if doc else "other",
                    "verified": doc.verified if doc else False,
                    "guide_id": doc.guide_id if doc else None,
                    "has_guide": (doc.guide_id is not None) if doc else False,
                })
            enriched_items.append({**item, "options": opts})

    # Prepare application info, adapting for selected state if applicable
    app_info = svc.application_info.to_dict()
    if resolved.state_rule:
        sr = resolved.state_rule
        if sr.get("authority"):
            app_info["where"] = f"{sr['authority']} ({sr['state_name']})"
        if sr.get("portal_url"):
            app_info["mode"] = f"Online via {sr.get('portal_name')} ({sr.get('portal_url')}) or offline at district office"
        if sr.get("application_steps"):
            app_info["steps"] = sr["application_steps"]

    response_data = {
        "service": svc.to_dict(),
        "items": enriched_items,
        "hidden_conditional": resolved.hidden_conditional,
        "application_info": app_info,
        "state_rule": resolved.state_rule,
    }
    return _ok(response_data)


# ── Documents ─────────────────────────────────────────────────────────────────

@bp.route("/documents")
def list_documents():
    """Return all documents with guides, issuing authority, and service usage counts."""
    repo = get_repo()
    result = []
    for d in repo.get_all_documents().values():
        used_by_ids = repo.get_services_using_document(d.id)
        result.append({
            "id": d.id,
            "name": d.name,
            "kind": d.kind,
            "description": d.description,
            "issuing_authority": d.issuing_authority,
            "jurisdiction": getattr(d, "jurisdiction", "India"),
            "verified": d.verified,
            "has_guide": d.guide_id is not None,
            "guide_url": f"/guide/{d.id}" if d.guide_id else None,
            "official_link": getattr(d, "official_link", None),
            "used_by_count": len(used_by_ids),
        })
    result.sort(key=lambda x: x["name"])
    return _ok(result)


@bp.route("/documents/<doc_id>")
def get_document(doc_id: str):
    try:
        validate_id(doc_id, "doc_id")
    except ValidationError as exc:
        return _err("VALIDATION_ERROR", str(exc), 400)

    repo = get_repo()
    doc = repo.get_document(doc_id)
    if doc is None:
        return _err("NOT_FOUND", f"Document '{doc_id}' not found", 404)

    # Enrich prerequisites
    prereq_details = []
    for pid in doc.prerequisites:
        pdoc = repo.get_document(pid)
        prereq_details.append({
            "document_id": pid,
            "name": pdoc.name if pdoc else pid,
            "kind": pdoc.kind if pdoc else "other",
        })

    used_by_ids = repo.get_services_using_document(doc_id)
    used_by = []
    for sid in used_by_ids:
        s = repo.get_service(sid)
        if s:
            used_by.append({"id": s.id, "name": s.name, "type": s.type})

    return _ok({
        **doc.to_dict(),
        "prerequisites_detail": prereq_details,
        "used_by_services": used_by,
    })


@bp.route("/documents/<doc_id>/guide")
def get_document_guide(doc_id: str):
    try:
        validate_id(doc_id, "doc_id")
    except ValidationError as exc:
        return _err("VALIDATION_ERROR", str(exc), 400)

    repo = get_repo()
    doc = repo.get_document(doc_id)
    if doc is None:
        return _err("NOT_FOUND", f"Document '{doc_id}' not found", 404)

    guide = repo.get_guide_by_document(doc_id)
    if guide is None:
        return _err("NOT_FOUND", f"No guide found for document '{doc_id}'", 404)

    documents = repo.get_all_documents()
    dep_tree = build_tree(doc_id, documents)

    # Prerequisite links
    prereq_links = []
    for pid in doc.prerequisites:
        pdoc = repo.get_document(pid)
        if pdoc:
            prereq_links.append({
                "document_id": pid,
                "name": pdoc.name,
                "kind": pdoc.kind,
                "has_guide": pdoc.guide_id is not None,
                "guide_url": f"/api/documents/{pid}/guide" if pdoc.guide_id else None,
            })

    return _ok({
        "guide": guide.to_dict(),
        "document": doc.to_dict(),
        "prerequisite_links": prereq_links,
        "dependency_tree": dep_tree,
    })


# ── Readiness ─────────────────────────────────────────────────────────────────

@bp.route("/services/<service_id>/readiness", methods=["POST"])
def check_readiness(service_id: str):
    try:
        validate_id(service_id, "service_id")
    except ValidationError as exc:
        return _err("VALIDATION_ERROR", str(exc), 400)

    if not request.is_json:
        return _err("VALIDATION_ERROR", "Content-Type must be application/json", 400)

    try:
        body = request.get_json(force=False, silent=True)
    except Exception:
        body = None

    if body is None:
        return _err("VALIDATION_ERROR", "Invalid JSON body", 400)

    try:
        raw_statuses = body.get("statuses", {})
        statuses = validate_statuses(raw_statuses)
        category = body.get("applicant_category") or None
    except ValidationError as exc:
        return _err("VALIDATION_ERROR", str(exc), 400, exc.details)

    repo = get_repo()
    if repo.get_service(service_id) is None:
        return _err("NOT_FOUND", f"Service '{service_id}' not found", 404)

    try:
        result = evaluate(service_id, statuses, category)
    except RequirementsError as exc:
        return _err("VALIDATION_ERROR", str(exc), 400)

    response = jsonify({"data": result.to_dict(), "meta": _meta()})
    response.headers["Cache-Control"] = "no-store"
    return response, 200


# ── Notifications & History ───────────────────────────────────────────────────

@bp.route("/notifications")
def list_notifications():
    try:
        from app.models.db_models import InAppNotification
        from app.services.database import get_db_session
        with get_db_session() as s:
            notifs = (
                s.query(InAppNotification)
                .order_by(InAppNotification.published_at.desc())
                .limit(50)
                .all()
            )
            return _ok([n.to_dict() for n in notifs])
    except Exception as e:
        logger.debug("Notifications fallback: %s", e)
        return _ok([])


@bp.route("/services/<service_id>/history")
def get_service_history(service_id: str):
    try:
        validate_id(service_id, "service_id")
    except ValidationError as exc:
        return _err("VALIDATION_ERROR", str(exc), 400)

    try:
        from app.models.db_models import ServiceVersion
        from app.services.database import get_db_session
        with get_db_session() as s:
            versions = (
                s.query(ServiceVersion)
                .filter_by(service_id=service_id)
                .order_by(ServiceVersion.version_number.desc())
                .all()
            )
            return _ok([
                {
                    "version_number": v.version_number,
                    "change_summary": v.change_summary,
                    "created_by": v.created_by,
                    "created_at": v.created_at.isoformat() if v.created_at else None,
                }
                for v in versions
            ])
    except Exception as e:
        logger.debug("Service history fallback: %s", e)
        return _ok([])


# ── Secured Administrative API ────────────────────────────────────────────────

@bp.route("/admin/sources")
def api_admin_sources():
    from app.services.auth import admin_required
    @admin_required
    def _handler():
        from app.models.db_models import SourceRegistry
        from app.services.database import get_db_session
        with get_db_session() as s:
            sources = s.query(SourceRegistry).all()
            return _ok([src.to_dict() for src in sources])
    return _handler()


@bp.route("/admin/sources/<source_id>/check", methods=["POST"])
def api_admin_check_source(source_id: str):
    from app.services.auth import admin_required, csrf_protect
    @admin_required
    @csrf_protect
    def _handler():
        from app.services.monitoring import monitor_engine
        res = monitor_engine.check_source(source_id, force=True)
        if res.get("status") == "error":
            return _err("MONITOR_ERROR", res["message"], 500, res)
        return _ok(res)
    return _handler()


@bp.route("/admin/changes")
def api_admin_changes():
    from app.services.auth import admin_required
    @admin_required
    def _handler():
        from app.models.db_models import DetectedChange
        from app.services.database import get_db_session
        status_filter = request.args.get("status", "proposed")
        with get_db_session() as s:
            q = s.query(DetectedChange)
            if status_filter != "all":
                q = q.filter_by(status=status_filter)
            changes = q.order_by(DetectedChange.detected_at.desc()).all()
            return _ok([c.to_dict() for c in changes])
    return _handler()


@bp.route("/admin/changes/<int:change_id>/approve", methods=["POST"])
def api_admin_approve_change(change_id: int):
    from app.services.auth import admin_required, csrf_protect
    @admin_required
    @csrf_protect
    def _handler():
        from flask import session
        from app.services.verification import approve_and_publish_change, VerificationError
        data = request.get_json(silent=True) or {}
        notes = data.get("notes", "Approved via API")
        reviewer = session.get("username", "admin_api")
        try:
            res = approve_and_publish_change(change_id, reviewer_username=reviewer, notes=notes)
            return _ok(res)
        except VerificationError as err:
            return _err("VERIFICATION_ERROR", str(err), 400)
    return _handler()


@bp.route("/admin/changes/<int:change_id>/reject", methods=["POST"])
def api_admin_reject_change(change_id: int):
    from app.services.auth import admin_required, csrf_protect
    @admin_required
    @csrf_protect
    def _handler():
        from flask import session
        from app.services.verification import reject_change, VerificationError
        data = request.get_json(silent=True) or {}
        reason = data.get("reason", "Rejected via API")
        reviewer = session.get("username", "admin_api")
        try:
            res = reject_change(change_id, reviewer_username=reviewer, reason=reason)
            return _ok(res)
        except VerificationError as err:
            return _err("VERIFICATION_ERROR", str(err), 400)
    return _handler()


@bp.route("/admin/rollback", methods=["POST"])
def api_admin_rollback():
    from app.services.auth import admin_required, csrf_protect
    @admin_required
    @csrf_protect
    def _handler():
        from flask import session
        from app.services.verification import rollback_service_version, VerificationError
        data = request.get_json(silent=True) or {}
        service_id = data.get("service_id")
        target_version = data.get("target_version")
        reason = data.get("reason", "API rollback")
        if not service_id or target_version is None:
            return _err("VALIDATION_ERROR", "service_id and target_version are required", 400)
        try:
            target_version_int = int(target_version)
        except (ValueError, TypeError):
            return _err("VALIDATION_ERROR", "target_version must be an integer", 400)
        reviewer = session.get("username", "admin_api")
        try:
            res = rollback_service_version(service_id, target_version_int, reviewer_username=reviewer, reason=reason)
            return _ok(res)
        except VerificationError as err:
            return _err("ROLLBACK_ERROR", str(err), 400)
    return _handler()


# ── Error handlers ────────────────────────────────────────────────────────────

@bp.errorhandler(ValidationError)
def handle_validation_error(exc: ValidationError):
    return _err("VALIDATION_ERROR", str(exc), 400, exc.details)

