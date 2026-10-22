"""Database engine, session management, and idempotent seed migration for PostgreSQL and SQLite."""
from __future__ import annotations

import json
import logging
import os
from contextlib import contextmanager
from datetime import datetime
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from app.models.db_models import (
    Base,
    DocumentRecord,
    DocumentVersion,
    GuideRecord,
    GuideVersion,
    ServiceRecord,
    ServiceRequirementRecord,
    ServiceVersion,
    SourceRegistry,
    StateRecord,
    StateRuleRecord,
    SynonymRecord,
    UserAccount,
    AuditEvent,
    utc_now,
)
from app.data.initial_data import (
    DOCUMENTS_SEED,
    SERVICES_SEED,
    GUIDES_SEED,
    STATES_SEED,
    STATE_RULES_SEED,
    SYNONYMS_SEED,
    SOURCES_SEED,
)

logger = logging.getLogger(__name__)

_engine = None
_SessionFactory = None
_scoped_session = None


def normalize_db_uri(uri: Optional[str] = None) -> str:
    """Normalize database connection string for SQLAlchemy compatibility.

    Render provides URLs starting with postgres:// but SQLAlchemy 2.0+ requires
    postgresql:// and defaults to the psycopg (v3) driver. We explicitly specify
    psycopg2 since that is the installed driver (psycopg2-binary).
    """
    raw = uri or os.environ.get("DATABASE_URL") or "sqlite:///instance/documentready.db"
    if raw.startswith("postgres://"):
        raw = raw.replace("postgres://", "postgresql+psycopg2://", 1)
    elif raw.startswith("postgresql://"):
        raw = raw.replace("postgresql://", "postgresql+psycopg2://", 1)
    return raw


def get_engine(db_uri: Optional[str] = None):
    """Create or return the global SQLAlchemy engine with connection pooling and pre-ping."""
    global _engine, _SessionFactory, _scoped_session
    if _engine is None or db_uri:
        uri = normalize_db_uri(db_uri)
        engine_kwargs = {"pool_pre_ping": True}
        if uri.startswith("sqlite"):
            engine_kwargs["connect_args"] = {"check_same_thread": False}
        else:
            engine_kwargs["pool_size"] = int(os.environ.get("DB_POOL_SIZE", "10"))
            engine_kwargs["max_overflow"] = int(os.environ.get("DB_MAX_OVERFLOW", "20"))
            engine_kwargs["pool_recycle"] = 1800
        _engine = create_engine(uri, **engine_kwargs)
        _SessionFactory = sessionmaker(bind=_engine, expire_on_commit=False)
        _scoped_session = scoped_session(_SessionFactory)
    return _engine


def get_session_factory():
    if _SessionFactory is None:
        get_engine()
    return _SessionFactory


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Provide a transactional database session scope."""
    factory = get_session_factory()
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db(app=None, uri: Optional[str] = None, seed: bool = True):
    """Create all database tables and optionally seed data idempotently."""
    db_uri = uri or (app.config.get("SQLALCHEMY_DATABASE_URI") if app else None)
    engine = get_engine(db_uri)
    Base.metadata.create_all(engine)
    logger.info("Database tables initialized successfully.")

    if seed:
        with get_db_session() as session:
            seed_count = seed_initial_data(session)
            logger.info("Seed migration complete: %s records synchronized.", seed_count)


def seed_initial_data(session: Session) -> dict[str, int]:
    """Idempotently seed documents, services, guides, sources, states, state rules, and synonyms.

    Preserves all existing records, unverified demo flags, and ensures no duplicate entries.
    """
    counts = {
        "documents": 0,
        "services": 0,
        "guides": 0,
        "sources": 0,
        "states": 0,
        "state_rules": 0,
        "synonyms": 0,
    }

    # 1. Documents
    for d in DOCUMENTS_SEED:
        existing = session.query(DocumentRecord).filter_by(id=d["id"]).first()
        if not existing:
            doc = DocumentRecord(
                id=d["id"],
                name=d["name"],
                kind=d["kind"],
                description=d.get("description", ""),
                issuing_authority=d.get("issuing_authority", ""),
                jurisdiction=d.get("jurisdiction", "India"),
                guide_id=d.get("guide_id"),
                verified=d.get("verified", True),
                source_note=d.get("source_note", ""),
                official_link=d.get("official_link"),
                last_reviewed=d.get("last_reviewed"),
                last_verified_at=utc_now() if d.get("verified") else None,
                version=1,
            )
            doc.aliases = d.get("aliases", [])
            doc.prerequisites = d.get("prerequisites", [])
            session.add(doc)
            session.flush()

            dv = DocumentVersion(
                document_id=doc.id,
                version_number=1,
                snapshot_json=json.dumps(doc.to_dict()),
                change_summary="Initial seed import",
            )
            session.add(dv)
            counts["documents"] += 1
        else:
            existing.name = d["name"]
            existing.kind = d["kind"]
            existing.description = d.get("description", "")
            existing.issuing_authority = d.get("issuing_authority", "")
            existing.jurisdiction = d.get("jurisdiction", "India")
            existing.guide_id = d.get("guide_id")
            existing.official_link = d.get("official_link")
            existing.aliases = d.get("aliases", [])
            existing.prerequisites = d.get("prerequisites", [])
            existing.verified = d.get("verified", True)
            existing.source_note = d.get("source_note", "")
            existing.last_reviewed = d.get("last_reviewed")
            if d.get("verified") and not existing.last_verified_at:
                existing.last_verified_at = utc_now()

    # 2. Guides
    for g in GUIDES_SEED:
        existing = session.query(GuideRecord).filter_by(id=g["id"]).first()
        if not existing:
            guide = GuideRecord(
                id=g["id"],
                document_id=g["document_id"],
                what_it_is=g.get("what_it_is", ""),
                where_how_to_apply=g.get("where_how_to_apply", ""),
                official_link=g.get("official_link"),
                verified=g.get("verified", True),
                version=1,
            )
            guide.documents_required = g.get("documents_required", [])
            guide.procedure_steps = g.get("procedure_steps", [])
            guide.precautions = g.get("precautions", [])
            session.add(guide)
            session.flush()

            gv = GuideVersion(
                guide_id=guide.id,
                version_number=1,
                snapshot_json=json.dumps(guide.to_dict()),
                change_summary="Initial seed import",
            )
            session.add(gv)
            counts["guides"] += 1
        else:
            existing.verified = g.get("verified", True)
            existing.official_link = g.get("official_link")
            existing.what_it_is = g.get("what_it_is", "")
            existing.where_how_to_apply = g.get("where_how_to_apply", "")
            existing.procedure_steps = g.get("procedure_steps", [])
            existing.precautions = g.get("precautions", [])
            existing.documents_required = g.get("documents_required", [])

    # 3. Services
    for s in SERVICES_SEED:
        existing = session.query(ServiceRecord).filter_by(id=s["id"]).first()
        if not existing:
            svc = ServiceRecord(
                id=s["id"],
                name=s["name"],
                type=s["type"],
                department=s.get("department", ""),
                jurisdiction="Maharashtra",
                description=s.get("description", ""),
                verified=s.get("verified", True),
                source_note=s.get("source_note", ""),
                official_source_url=s.get("official_source_url"),
                last_reviewed=s.get("last_reviewed"),
                last_verified_at=utc_now() if s.get("verified") else None,
                version=1,
            )
            svc.aliases = s.get("aliases", [])
            svc.applicant_categories = s.get("applicant_categories", [])
            svc.application_info = s.get("application_info", {})
            session.add(svc)
            session.flush()

            # Add requirements
            reqs = s.get("requirements", [])
            for idx, r in enumerate(reqs):
                req_rec = ServiceRequirementRecord(
                    service_id=svc.id,
                    necessity=r["necessity"],
                    document_id=r.get("document_id"),
                    group_name=r.get("group"),
                    note=r.get("note"),
                    order_index=idx,
                )
                req_rec.options = r.get("options", [])
                req_rec.when_clause = r.get("when")
                session.add(req_rec)

            sv = ServiceVersion(
                service_id=svc.id,
                version_number=1,
                snapshot_json=json.dumps(svc.to_dict()),
                change_summary="Initial seed import",
            )
            session.add(sv)
            counts["services"] += 1
        else:
            existing.name = s["name"]
            existing.department = s.get("department", "")
            existing.description = s.get("description", "")
            existing.verified = s.get("verified", True)
            existing.source_note = s.get("source_note", "")
            existing.official_source_url = s.get("official_source_url")
            existing.last_reviewed = s.get("last_reviewed")
            existing.application_info = s.get("application_info", {})
            if s.get("verified") and not existing.last_verified_at:
                existing.last_verified_at = utc_now()

    # 4. Verified Government Source Registry
    for s_info in SOURCES_SEED:
        existing = session.query(SourceRegistry).filter_by(id=s_info["id"]).first()
        if not existing:
            src = SourceRegistry(
                id=s_info["id"],
                name=s_info["name"],
                department=s_info["department"],
                jurisdiction=s_info["jurisdiction"],
                official_base_url=s_info["official_base_url"],
                monitored_url=s_info["monitored_url"],
                source_type=s_info["source_type"],
                adapter=s_info["adapter"],
                check_frequency_minutes=s_info["check_frequency_minutes"],
                enabled=s_info["enabled"],
                priority=s_info["priority"],
                verification_policy=s_info["verification_policy"],
            )
            src.associated_service_ids = s_info["associated_service_ids"]
            src.associated_document_ids = s_info["associated_document_ids"]
            session.add(src)
            counts["sources"] += 1

    # 5. States & UTs
    for st in STATES_SEED:
        existing = session.query(StateRecord).filter_by(id=st["id"]).first()
        if not existing:
            session.add(
                StateRecord(
                    id=st["id"],
                    name=st["name"],
                    name_hi=st.get("name_hi"),
                    name_mr=st.get("name_mr"),
                )
            )
            counts["states"] += 1

    # 6. State Rules
    for svc_id, states_map in STATE_RULES_SEED.items():
        for st_id, rule_data in states_map.items():
            existing = session.query(StateRuleRecord).filter_by(service_id=svc_id, state_id=st_id).first()
            if not existing:
                rule_rec = StateRuleRecord(
                    service_id=svc_id,
                    state_id=st_id,
                    authority=rule_data.get("authority", ""),
                    portal_name=rule_data.get("portal_name", ""),
                    portal_url=rule_data.get("portal_url", ""),
                    statutory_rule=rule_data.get("statutory_rule", ""),
                    raw_data_json=json.dumps(rule_data),
                )
                rule_rec.additional_requirements = rule_data.get("additional_requirements", [])
                rule_rec.application_steps = rule_data.get("application_steps", [])
                session.add(rule_rec)
                counts["state_rules"] += 1

    # 7. Search Synonyms
    for term, syn_list in SYNONYMS_SEED.items():
        existing = session.query(SynonymRecord).filter_by(term=term).first()
        if not existing:
            syn_rec = SynonymRecord(term=term)
            syn_rec.synonyms = syn_list
            session.add(syn_rec)
            counts["synonyms"] += 1

    session.commit()
    return counts
