"""Flask CLI commands for database migration, user provisioning, and monitoring."""
from __future__ import annotations

import click
from flask.cli import AppGroup

admin_cli = AppGroup("admin", help="Administrative operations.")
monitor_cli = AppGroup("monitor", help="Official source monitoring operations.")
db_cli = AppGroup("db-admin", help="Database management operations.")


@admin_cli.command("create-user")
@click.option("--username", prompt=True, help="Admin username")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Password")
@click.option("--role", default="admin", type=click.Choice(["admin", "reviewer"]), help="Role")
def create_admin_user(username, password, role):
    """Create or update an administrative user account."""
    from werkzeug.security import generate_password_hash
    from app.models.db_models import UserAccount, AuditEvent
    from app.services.database import get_db_session

    with get_db_session() as s:
        existing = s.query(UserAccount).filter_by(username=username).first()
        if existing:
            existing.password_hash = generate_password_hash(password)
            existing.role = role
            existing.is_active = True
            click.echo(f"Updated password and role for existing user '{username}'.")
        else:
            user = UserAccount(
                username=username,
                password_hash=generate_password_hash(password),
                role=role,
                is_active=True,
            )
            s.add(user)
            click.echo(f"Created new {role} user '{username}'.")

        s.add(AuditEvent(event_type="user_provisioned_cli", actor="cli", details_json=f'{{"username": "{username}", "role": "{role}"}}'))
        s.commit()


@monitor_cli.command("run-all")
@click.option("--force", is_flag=True, help="Force check even if recently checked")
def run_all_monitors(force):
    """Run monitoring check across all enabled sources."""
    from app.services.monitoring import monitor_engine
    click.echo("Starting monitoring check for all enabled government sources...")
    results = monitor_engine.check_all_sources(force=force)
    for res in results:
        status_color = "green" if res["status"] in ("unchanged", "changed") else "red"
        click.secho(f"[{res['status'].upper()}] {res['source_id']}: {res['message']}", fg=status_color)
    click.echo(f"Monitoring check complete. Processed {len(results)} sources.")


@monitor_cli.command("check")
@click.argument("source_id")
@click.option("--force", is_flag=True, help="Force check")
def check_single_source(source_id, force):
    """Run monitoring check on a single official government source."""
    from app.services.monitoring import monitor_engine
    click.echo(f"Executing check on source '{source_id}'...")
    res = monitor_engine.check_source(source_id, force=force)
    status_color = "green" if res["status"] in ("unchanged", "changed") else "red"
    click.secho(f"[{res['status'].upper()}] {res['source_id']}: {res['message']}", fg=status_color)


@db_cli.command("init")
@click.option("--seed/--no-seed", default=True, help="Seed initial data from JSON")
def init_database(seed):
    """Initialize database tables and sync initial data."""
    from app.services.database import init_db
    from app.services.auth import ensure_initial_admin
    init_db(seed=seed)
    ensure_initial_admin("admin")
    click.echo("Database initialization complete.")
