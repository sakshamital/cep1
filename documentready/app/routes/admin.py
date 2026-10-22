"""Administrative controller and protected management routes."""
from __future__ import annotations

import json
import logging
from datetime import datetime

from flask import (
    Blueprint,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.models.db_models import (
    AuditEvent,
    DetectedChange,
    DocumentRecord,
    GuideRecord,
    ServiceRecord,
    ServiceVersion,
    SourceFetchHistory,
    SourceRegistry,
)
from app.services.auth import (
    admin_required,
    authenticate_user,
    csrf_protect,
    generate_csrf_token,
)
from app.services.database import get_db_session, seed_initial_data
from app.services.monitoring import monitor_engine
from app.services.security_check import SSRFValidationError, validate_and_resolve_url
from app.services.verification import (
    VerificationError,
    approve_and_publish_change,
    reject_change,
    rollback_service_version,
)

logger = logging.getLogger(__name__)

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.context_processor
def inject_admin_globals():
    return {
        "csrf_token": generate_csrf_token,
        "current_user": g.get("current_user") or session.get("username"),
    }


from urllib.parse import urlparse


def _is_safe_redirect(target: str | None) -> bool:
    if not target:
        return False
    parsed = urlparse(target)
    return not parsed.scheme and not parsed.netloc and target.startswith("/") and not target.startswith("//") and not target.startswith("/\\")


# ── Authentication ────────────────────────────────────────────────────────────

@bp.route("/login", methods=["GET", "POST"])
def login_view():
    if session.get("user_id"):
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = authenticate_user(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            flash(f"Welcome back, {user['username']}!", "success")
            next_url = request.args.get("next")
            if not _is_safe_redirect(next_url):
                next_url = url_for("admin.dashboard")
            return redirect(next_url)
        else:
            flash("Invalid username or password.", "error")

    return render_template("admin/login.html")


@bp.route("/logout", methods=["POST", "GET"])
def logout_view():
    username = session.get("username", "unknown")
    session.clear()
    flash("You have been signed out safely.", "info")
    return redirect(url_for("admin.login_view"))


# ── Dashboard Overview ────────────────────────────────────────────────────────

@bp.route("/")
@admin_required
def dashboard():
    with get_db_session() as s:
        services_count = s.query(ServiceRecord).count()
        docs_count = s.query(DocumentRecord).count()
        guides_count = s.query(GuideRecord).count()
        sources = s.query(SourceRegistry).all()
        pending_changes = (
            s.query(DetectedChange)
            .filter_by(status="proposed")
            .order_by(DetectedChange.detected_at.desc())
            .limit(10)
            .all()
        )
        recent_fetches = (
            s.query(SourceFetchHistory)
            .order_by(SourceFetchHistory.attempted_at.desc())
            .limit(8)
            .all()
        )
        recent_audits = (
            s.query(AuditEvent)
            .order_by(AuditEvent.timestamp.desc())
            .limit(8)
            .all()
        )

        enabled_sources_count = sum(1 for src in sources if src.enabled)
        failed_sources_count = sum(1 for src in sources if src.consecutive_failures > 0)

        stats = {
            "services_count": services_count,
            "docs_count": docs_count,
            "guides_count": guides_count,
            "sources_total": len(sources),
            "sources_enabled": enabled_sources_count,
            "sources_failed": failed_sources_count,
            "pending_changes_count": len(pending_changes),
        }

        return render_template(
            "admin/dashboard.html",
            stats=stats,
            sources=sources,
            pending_changes=pending_changes,
            recent_fetches=recent_fetches,
            recent_audits=recent_audits,
        )


# ── Sources Management ────────────────────────────────────────────────────────

@bp.route("/sources")
@admin_required
def sources_view():
    with get_db_session() as s:
        sources = s.query(SourceRegistry).order_by(SourceRegistry.created_at.desc()).all()
        services = s.query(ServiceRecord).all()
        return render_template("admin/sources.html", sources=sources, services=services)


@bp.route("/sources/add", methods=["POST"])
@admin_required
@csrf_protect
def add_source():
    source_id = request.form.get("id", "").strip().lower()
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()
    jurisdiction = request.form.get("jurisdiction", "Maharashtra").strip()
    monitored_url = request.form.get("monitored_url", "").strip()
    base_url = request.form.get("official_base_url", "").strip() or monitored_url
    source_type = request.form.get("source_type", "html")
    adapter = request.form.get("adapter", "generic_html")
    freq_str = request.form.get("check_frequency_minutes", "720")
    try:
        frequency = max(15, int(freq_str)) if freq_str else 720
    except (ValueError, TypeError):
        frequency = 720
    selected_services = request.form.getlist("associated_service_ids")

    if not source_id or not name or not monitored_url:
        flash("Source ID, Name, and Monitored URL are required fields.", "error")
        return redirect(url_for("admin.sources_view"))

    try:
        # SSRF validation check
        validate_and_resolve_url(monitored_url)
        if base_url != monitored_url:
            validate_and_resolve_url(base_url)
    except SSRFValidationError as e:
        flash(f"Security Alert: Destination blocked by SSRF shield ({e}).", "error")
        return redirect(url_for("admin.sources_view"))

    with get_db_session() as s:
        existing = s.query(SourceRegistry).filter_by(id=source_id).first()
        if existing:
            flash(f"Source with ID '{source_id}' already exists.", "error")
            return redirect(url_for("admin.sources_view"))

        src = SourceRegistry(
            id=source_id,
            name=name,
            department=department,
            jurisdiction=jurisdiction,
            official_base_url=base_url,
            monitored_url=monitored_url,
            source_type=source_type,
            adapter=adapter,
            check_frequency_minutes=frequency,
            enabled=True,
        )
        src.associated_service_ids = selected_services
        s.add(src)
        s.commit()
        flash(f"Official source '{name}' added successfully to monitoring registry.", "success")

    return redirect(url_for("admin.sources_view"))


@bp.route("/sources/<source_id>/toggle", methods=["POST"])
@admin_required
@csrf_protect
def toggle_source(source_id: str):
    with get_db_session() as s:
        src = s.query(SourceRegistry).filter_by(id=source_id).first()
        if src:
            src.enabled = not src.enabled
            s.commit()
            state_str = "enabled" if src.enabled else "disabled"
            flash(f"Source '{src.name}' is now {state_str}.", "info")
        else:
            flash(f"Source '{source_id}' not found.", "error")
    return redirect(url_for("admin.sources_view"))


@bp.route("/sources/<source_id>/delete", methods=["POST"])
@admin_required
@csrf_protect
def delete_source(source_id: str):
    with get_db_session() as s:
        src = s.query(SourceRegistry).filter_by(id=source_id).first()
        if src:
            name = src.name
            s.delete(src)
            audit = AuditEvent(
                event_type="source_deleted",
                actor=session.get("username", "admin"),
                details_json=json.dumps({"source_id": source_id, "name": name}),
            )
            s.add(audit)
            s.commit()
            flash(f"Source '{name}' was deleted from registry.", "info")
        else:
            flash(f"Source '{source_id}' not found.", "error")
    return redirect(url_for("admin.sources_view"))


@bp.route("/sources/<source_id>/check", methods=["POST"])
@admin_required
@csrf_protect
def check_source_now(source_id: str):
    result = monitor_engine.check_source(source_id, force=True)
    if result["status"] == "error":
        flash(f"Check failed: {result['message']}", "error")
    elif result["status"] == "changed":
        flash(f"Check completed: {result['message']}", "success")
    else:
        flash(f"Check completed: {result['message']}", "info")

    return redirect(url_for("admin.sources_view"))


# ── Change Verification Queue ─────────────────────────────────────────────────

@bp.route("/changes")
@admin_required
def changes_view():
    status_filter = request.args.get("status", "proposed")
    with get_db_session() as s:
        query = s.query(DetectedChange)
        if status_filter != "all":
            query = query.filter_by(status=status_filter)
        changes = query.order_by(DetectedChange.detected_at.desc()).all()
        return render_template("admin/changes.html", changes=changes, active_status=status_filter)


@bp.route("/changes/<int:change_id>/approve", methods=["POST"])
@admin_required
@csrf_protect
def approve_change_action(change_id: int):
    notes = request.form.get("notes", "Approved by administrator")
    reviewer = session.get("username", "admin")

    try:
        res = approve_and_publish_change(change_id, reviewer_username=reviewer, notes=notes)
        flash(res["message"], "success")
    except VerificationError as err:
        flash(f"Approval error: {err}", "error")

    return redirect(url_for("admin.changes_view"))


@bp.route("/changes/<int:change_id>/reject", methods=["POST"])
@admin_required
@csrf_protect
def reject_change_action(change_id: int):
    reason = request.form.get("reason", "Rejected after verification review")
    reviewer = session.get("username", "admin")

    try:
        res = reject_change(change_id, reviewer_username=reviewer, reason=reason)
        flash(res["message"], "info")
    except VerificationError as err:
        flash(f"Rejection error: {err}", "error")

    return redirect(url_for("admin.changes_view"))


# ── Version History and Rollback ──────────────────────────────────────────────

@bp.route("/history")
@admin_required
def history_view():
    service_id = request.args.get("service_id")
    with get_db_session() as s:
        services = s.query(ServiceRecord).all()
        selected_service = None
        versions = []
        if service_id:
            selected_service = s.query(ServiceRecord).filter_by(id=service_id).first()
            if selected_service:
                versions = (
                    s.query(ServiceVersion)
                    .filter_by(service_id=service_id)
                    .order_by(ServiceVersion.version_number.desc())
                    .all()
                )

        return render_template(
            "admin/history.html",
            services=services,
            selected_service=selected_service,
            versions=versions,
        )


@bp.route("/history/rollback", methods=["POST"])
@admin_required
@csrf_protect
def rollback_action():
    service_id = request.form.get("service_id", "").strip()
    ver_str = request.form.get("target_version", "1")
    try:
        target_version = int(ver_str)
    except (ValueError, TypeError):
        flash("Invalid target version number specified.", "error")
        return redirect(url_for("admin.history_view", service_id=service_id))

    reason = request.form.get("reason", "Administrative rollback")
    reviewer = session.get("username", "admin")

    try:
        res = rollback_service_version(
            service_id=service_id,
            target_version_number=target_version,
            reviewer_username=reviewer,
            reason=reason,
        )
        flash(res["message"], "success")
    except VerificationError as err:
        flash(f"Rollback error: {err}", "error")

    return redirect(url_for("admin.history_view", service_id=service_id))


# ── Audit Trail ───────────────────────────────────────────────────────────────

@bp.route("/logs")
@admin_required
def logs_view():
    with get_db_session() as s:
        audits = s.query(AuditEvent).order_by(AuditEvent.timestamp.desc()).limit(100).all()
        fetches = (
            s.query(SourceFetchHistory)
            .order_by(SourceFetchHistory.attempted_at.desc())
            .limit(100)
            .all()
        )
        return render_template("admin/logs.html", audits=audits, fetches=fetches)


@bp.route("/sync-seed", methods=["POST"])
@admin_required
@csrf_protect
def sync_seed_data():
    with get_db_session() as s:
        counts = seed_initial_data(s)
        flash(
            f"Seed synchronization complete. Synced: {counts['services']} services, "
            f"{counts['documents']} documents, {counts['guides']} guides, {counts['sources']} sources.",
            "success",
        )
    return redirect(url_for("admin.dashboard"))
