"""Tests for database persistence and idempotent seed migration."""
import pytest
from app.models.db_models import (
    DocumentRecord,
    GuideRecord,
    ServiceRecord,
    SourceRegistry,
    StateRecord,
    StateRuleRecord,
    SynonymRecord,
)
from app.services.database import get_db_session, init_db, seed_initial_data, normalize_db_uri
from config import get_database_uri


def test_database_init_and_idempotency(app):
    """Test that database initializes and subsequent seed calls do not duplicate records."""
    init_db(app, seed=True)

    with get_db_session() as session:
        initial_services = session.query(ServiceRecord).count()
        initial_docs = session.query(DocumentRecord).count()
        initial_guides = session.query(GuideRecord).count()
        initial_sources = session.query(SourceRegistry).count()
        initial_states = session.query(StateRecord).count()
        initial_rules = session.query(StateRuleRecord).count()
        initial_synonyms = session.query(SynonymRecord).count()

        assert initial_services > 0
        assert initial_docs > 0
        assert initial_guides > 0
        assert initial_sources > 0
        assert initial_states == 36
        assert initial_rules > 0
        assert initial_synonyms > 0

        # Run seed again (idempotent test)
        counts = seed_initial_data(session)
        assert counts["services"] == 0
        assert counts["documents"] == 0
        assert counts["guides"] == 0
        assert counts["sources"] == 0
        assert counts["states"] == 0
        assert counts["state_rules"] == 0
        assert counts["synonyms"] == 0

        # Verify counts remain identical
        assert session.query(ServiceRecord).count() == initial_services
        assert session.query(DocumentRecord).count() == initial_docs
        assert session.query(GuideRecord).count() == initial_guides
        assert session.query(SourceRegistry).count() == initial_sources
        assert session.query(StateRecord).count() == initial_states
        assert session.query(StateRuleRecord).count() == initial_rules
        assert session.query(SynonymRecord).count() == initial_synonyms


def test_initial_demo_records_unverified(app):
    """Verify demo seed records are explicitly unverified with source notes."""
    init_db(app, seed=True)

    with get_db_session() as session:
        docs = session.query(DocumentRecord).all()
        for doc in docs:
            if not doc.verified:
                assert doc.source_note is not None
                assert len(doc.source_note.strip()) > 0


def test_render_postgres_url_normalization(monkeypatch):
    """Verify postgres:// is converted to postgresql+psycopg2:// for SQLAlchemy compatibility on Render."""
    render_raw_url = "postgres://usr_123:secretpass@dpg-abc-a.oregon-postgres.render.com/docready_db"
    normalized = normalize_db_uri(render_raw_url)
    assert normalized.startswith("postgresql+psycopg2://")
    assert "usr_123:secretpass" in normalized

    # Also test config.py get_database_uri
    monkeypatch.setenv("DATABASE_URL", render_raw_url)
    assert get_database_uri().startswith("postgresql+psycopg2://")


def test_states_api_from_database(client, app):
    """Verify /api/states returns data queried from the database without any JSON files."""
    init_db(app, seed=True)
    res = client.get("/api/states")
    assert res.status_code == 200
    states = res.get_json()
    assert isinstance(states, list)
    assert len(states) >= 36
    mh = next((s for s in states if s["id"] == "MH"), None)
    assert mh is not None
    assert mh["name"] == "Maharashtra"
