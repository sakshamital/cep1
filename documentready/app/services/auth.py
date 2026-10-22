"""Authentication, session security, CSRF protection, and role authorization."""
from __future__ import annotations

import functools
import hmac
import logging
import os
import secrets
from datetime import datetime
from typing import Callable, Optional

from flask import abort, g, has_request_context, jsonify, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.db_models import AuditEvent, UserAccount, utc_now
from app.services.database import get_db_session

logger = logging.getLogger(__name__)


def generate_csrf_token() -> str:
    """Generate or retrieve a cryptographically secure CSRF token in the session."""
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(32)
    return session["_csrf_token"]


def validate_csrf_token(token: Optional[str]) -> bool:
    """Constant-time comparison of submitted CSRF token against session token."""
    session_token = session.get("_csrf_token")
    if not session_token or not token:
        return False
    return hmac.compare_digest(str(session_token), str(token))


def csrf_protect(fn: Callable) -> Callable:
    """Decorator to require valid CSRF token on state-changing HTTP methods."""
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            token = (
                request.headers.get("X-CSRFToken")
                or request.headers.get("X-CSRF-Token")
                or request.form.get("csrf_token")
            )
            # If JSON body has csrf_token
            if not token and request.is_json:
                body = request.get_json(silent=True) or {}
                token = body.get("csrf_token")

            if not validate_csrf_token(token):
                if request.path.startswith("/api/"):
                    return jsonify({"error": {"code": "CSRF_ERROR", "message": "Invalid or missing CSRF token."}}), 403
                abort(403, description="CSRF validation failed.")
        return fn(*args, **kwargs)
    return decorated


def admin_required(fn: Callable) -> Callable:
    """Decorator requiring an authenticated admin/reviewer user in session."""
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            if request.path.startswith("/api/"):
                return jsonify({"error": {"code": "UNAUTHORIZED", "message": "Authentication required."}}), 401
            return redirect(url_for("admin.login_view", next=request.path))

        with get_db_session() as s:
            user = s.query(UserAccount).filter_by(id=user_id, is_active=True).first()
            if not user:
                session.clear()
                if request.path.startswith("/api/"):
                    return jsonify({"error": {"code": "UNAUTHORIZED", "message": "User session expired or invalid."}}), 401
                return redirect(url_for("admin.login_view"))

            g.current_user = {
                "id": user.id,
                "username": user.username,
                "role": user.role,
            }
        return fn(*args, **kwargs)
    return decorated


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Verify username and password against persistent UserAccount records."""
    if not username or not password:
        return None

    with get_db_session() as s:
        user = s.query(UserAccount).filter_by(username=username.strip(), is_active=True).first()
        if user and check_password_hash(user.password_hash, password):
            user.last_login_at = utc_now()
            client_ip = request.remote_addr if has_request_context() else "127.0.0.1"
            audit = AuditEvent(
                event_type="user_login_success",
                actor=user.username,
                ip_address=client_ip,
            )
            s.add(audit)
            s.commit()
            return {"id": user.id, "username": user.username, "role": user.role}

    return None


def ensure_initial_admin(username: str = "admin", password: Optional[str] = None) -> bool:
    """Provision initial administrator if none exists. Never overwrites existing credentials."""
    with get_db_session() as s:
        existing = s.query(UserAccount).filter_by(username=username).first()
        if existing:
            return False  # Already exists

        default_pw = password or os.environ.get("INITIAL_ADMIN_PASSWORD") or "Admin@DocReady2026"
        hashed = generate_password_hash(default_pw)
        admin_user = UserAccount(
            username=username,
            password_hash=hashed,
            role="admin",
            is_active=True,
        )
        s.add(admin_user)
        audit = AuditEvent(
            event_type="admin_provisioned",
            actor="system",
            details_json=f'{{"username": "{username}"}}',
        )
        s.add(audit)
        s.commit()
        logger.info("Initial administrator '%s' provisioned.", username)
        return True
