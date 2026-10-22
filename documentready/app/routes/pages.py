"""HTML page routes."""
from __future__ import annotations

import logging
from flask import Blueprint, abort, render_template

from app.services.repository import get_repo
from app.services.validators import ValidationError, validate_id

logger = logging.getLogger(__name__)
bp = Blueprint("pages", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/service/<service_id>")
def service(service_id: str):
    try:
        validate_id(service_id)
    except ValidationError:
        abort(404)
    repo = get_repo()
    svc = repo.get_service(service_id)
    if svc is None:
        abort(404)

    # Fetch version history and official source metadata from database if available
    versions = []
    official_source_url = None
    last_verified_at = None
    jurisdiction = "Maharashtra"

    try:
        from app.models.db_models import ServiceRecord, ServiceVersion
        from app.services.database import get_db_session
        with get_db_session() as s:
            rec = s.query(ServiceRecord).filter_by(id=service_id).first()
            if rec:
                official_source_url = rec.official_source_url
                last_verified_at = rec.last_verified_at
                jurisdiction = rec.jurisdiction or "Maharashtra"
                v_list = (
                    s.query(ServiceVersion)
                    .filter_by(service_id=service_id)
                    .order_by(ServiceVersion.version_number.desc())
                    .all()
                )
                versions = [
                    {
                        "version_number": v.version_number,
                        "change_summary": v.change_summary,
                        "created_by": v.created_by,
                        "created_at": v.created_at,
                    }
                    for v in v_list
                ]
    except Exception as e:
        logger.debug("Database query for service history bypassed: %s", e)

    return render_template(
        "service.html",
        service=svc,
        versions=versions,
        official_source_url=official_source_url,
        last_verified_at=last_verified_at,
        jurisdiction=jurisdiction,
    )


@bp.route("/guide/<doc_id>")
def guide(doc_id: str):
    try:
        validate_id(doc_id)
    except ValidationError:
        abort(404)
    repo = get_repo()
    doc = repo.get_document(doc_id)
    if doc is None:
        abort(404)
    guide_obj = repo.get_guide_by_document(doc_id)
    if guide_obj is None:
        abort(404)
    prereqs = []
    for pid in doc.prerequisites:
        pdoc = repo.get_document(pid)
        if pdoc:
            prereqs.append(pdoc)
    return render_template("guide.html", guide=guide_obj, document=doc, prerequisites=prereqs)


@bp.route("/documents")
def documents_list():
    repo = get_repo()
    all_docs = list(repo.get_all_documents().values())
    all_docs.sort(key=lambda d: d.name)
    return render_template("documents.html", documents=all_docs)


@bp.route("/updates")
def updates():
    notifications = []
    try:
        from app.models.db_models import InAppNotification
        from app.services.database import get_db_session
        with get_db_session() as s:
            notifications = (
                s.query(InAppNotification)
                .order_by(InAppNotification.published_at.desc())
                .limit(50)
                .all()
            )
    except Exception as e:
        logger.debug("Database query for updates bypassed: %s", e)

    return render_template("updates.html", notifications=notifications)


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.errorhandler(404)
def page_404(e):
    return render_template("404.html"), 404


@bp.errorhandler(500)
def page_500(e):
    return render_template("500.html"), 500
