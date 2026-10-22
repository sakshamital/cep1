"""Application factory and core Flask setup."""
from __future__ import annotations

import logging
from flask import Flask, render_template, jsonify

from config import config_map

logger = logging.getLogger(__name__)

DISCLAIMER = (
    "Document requirements may vary by department, location, applicant category "
    "and current government guidelines. Users should verify final requirements "
    "with the relevant official authority."
)


def create_app(config_name: str = "development") -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_map.get(config_name, config_map["development"]))

    # ── Security headers ─────────────────────────────────────────────────────
    @app.after_request
    def set_security_headers(response):
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "img-src 'self' data:; "
            "font-src 'self' https://fonts.gstatic.com; "
            "connect-src 'self'"
        )
        response.headers["Content-Security-Policy"] = csp
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    # ── Error handlers ────────────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        from flask import request
        if request.path.startswith("/api/"):
            return jsonify({"error": {"code": "NOT_FOUND", "message": "Resource not found"}}), 404
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": {"code": "METHOD_NOT_ALLOWED", "message": "Method not allowed"}}), 405

    @app.errorhandler(413)
    def request_too_large(e):
        return jsonify({"error": {"code": "REQUEST_TOO_LARGE", "message": "Request body too large (max 16 KB)"}}), 413

    @app.errorhandler(500)
    def internal_error(e):
        logger.error("Internal server error", exc_info=e)
        from flask import request
        if request.path.startswith("/api/"):
            return jsonify({"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}}), 500
        return render_template("500.html"), 500

    # ── Blueprints ────────────────────────────────────────────────────────────
    from .routes.admin import bp as admin_bp
    from .routes.api import bp as api_bp
    from .routes.pages import bp as pages_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(admin_bp)

    # ── CLI Commands ──────────────────────────────────────────────────────────
    from .cli import admin_cli, monitor_cli, db_cli
    app.cli.add_command(admin_cli)
    app.cli.add_command(monitor_cli)
    app.cli.add_command(db_cli)

    # ── Context processors ────────────────────────────────────────────────────
    @app.context_processor
    def inject_globals():
        return {"disclaimer": DISCLAIMER}

    # ── Database Initialization ───────────────────────────────────────────────
    if not app.config.get("TESTING"):
        try:
            from .services.database import init_db
            from .services.auth import ensure_initial_admin
            init_db(app, seed=True)
            ensure_initial_admin("admin")
        except Exception as exc:
            logger.warning("Could not auto-initialize database on startup: %s", exc)

    return app
