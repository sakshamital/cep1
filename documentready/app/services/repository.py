"""Repository: loads, validates, indexes domain entities from database at startup."""
from __future__ import annotations

import logging
from typing import Optional

from app.models.entities import Document, Service, Guide

logger = logging.getLogger(__name__)

DISCLAIMER = (
    "Document requirements may vary by department, location, applicant category "
    "and current government guidelines. Users should verify final requirements "
    "with the relevant official authority."
)


class RepositoryError(Exception):
    """Raised when data fails validation at startup."""


class _Repository:
    """Singleton in-memory store for all application data."""

    def __init__(self) -> None:
        self._documents: dict[str, Document] = {}
        self._services: dict[str, Service] = {}
        self._guides: dict[str, Guide] = {}
        self._guides_by_document: dict[str, Guide] = {}
        self._services_using_document: dict[str, list[str]] = {}
        self._synonyms: dict[str, list[str]] = {}
        self._loaded = False

    # ── Load / validate ───────────────────────────────────────────────────────

    def load(self, force_json: bool = False) -> None:
        """Load and validate all data from database. Seeds initial database records if empty."""
        from app.services.database import get_db_session, get_engine, seed_initial_data
        from app.models.db_models import Base, DocumentRecord

        engine = get_engine()
        Base.metadata.create_all(engine)

        with get_db_session() as session:
            if session.query(DocumentRecord).count() == 0:
                seed_initial_data(session)
            self.load_from_db(session)

    def reload_from_db(self) -> None:
        """Explicitly refresh repository data from the persistent database."""
        from app.services.database import get_db_session
        with get_db_session() as session:
            self.load_from_db(session)

    def load_from_db(self, session) -> None:
        """Load and index domain entities directly from the database session."""
        from app.models.db_models import DocumentRecord, ServiceRecord, GuideRecord, SynonymRecord
        from app.models.entities import Document, Service, Guide

        doc_records = session.query(DocumentRecord).all()
        svc_records = session.query(ServiceRecord).all()
        guide_records = session.query(GuideRecord).all()
        syn_records = session.query(SynonymRecord).all()

        documents = {d.id: Document.from_dict(d.to_dict()) for d in doc_records}
        services = {s.id: Service.from_dict(s.to_dict()) for s in svc_records}
        guides = {g.id: Guide.from_dict(g.to_dict()) for g in guide_records}

        if syn_records:
            self._synonyms = {s.term: s.synonyms for s in syn_records}
        else:
            from app.data.initial_data import SYNONYMS_SEED
            self._synonyms = dict(SYNONYMS_SEED)

        self._build_indices(documents, services, guides)

    def _build_indices(
        self,
        documents: dict[str, Document],
        services: dict[str, Service],
        guides: dict[str, Guide],
    ) -> None:
        errors = self._check_integrity(documents, services, guides)
        if errors:
            msg = "Data integrity errors:\n" + "\n".join(f"  • {e}" for e in errors)
            raise RepositoryError(msg)

        guides_by_doc: dict[str, Guide] = {}
        for g in guides.values():
            guides_by_doc[g.document_id] = g

        svc_using: dict[str, list[str]] = {d: [] for d in documents}
        for svc in services.values():
            for req in svc.requirements:
                if req.document_id and req.document_id in svc_using:
                    if svc.id not in svc_using[req.document_id]:
                        svc_using[req.document_id].append(svc.id)
                for opt in req.options:
                    if opt in svc_using:
                        if svc.id not in svc_using[opt]:
                            svc_using[opt].append(svc.id)

        from app.services.graph import assert_acyclic, CycleError
        try:
            assert_acyclic(documents)
        except CycleError as e:
            raise RepositoryError(f"Dependency cycle detected: {e}") from e

        self._documents = documents
        self._services = services
        self._guides = guides
        self._guides_by_document = guides_by_doc
        self._services_using_document = svc_using
        self._loaded = True
        logger.info(
            "Repository loaded: %d documents, %d services, %d guides",
            len(documents), len(services), len(guides),
        )


    def _check_integrity(
        self,
        documents: dict[str, Document],
        services: dict[str, Service],
        guides: dict[str, Guide],
    ) -> list[str]:
        errors: list[str] = []
        doc_ids = set(documents)

        # Documents: prerequisites must exist
        for doc in documents.values():
            for prereq in doc.prerequisites:
                if prereq not in doc_ids:
                    errors.append(
                        f"Document '{doc.id}' has unknown prerequisite '{prereq}'"
                    )
            if not doc.verified and not doc.source_note:
                errors.append(
                    f"Document '{doc.id}' has verified=false but no source_note"
                )

        # Services: all document_ids and option ids must exist
        for svc in services.values():
            for req in svc.requirements:
                if req.document_id and req.document_id not in doc_ids:
                    errors.append(
                        f"Service '{svc.id}' requirement references unknown document '{req.document_id}'"
                    )
                for opt in req.options:
                    if opt not in doc_ids:
                        errors.append(
                            f"Service '{svc.id}' any_of group references unknown document '{opt}'"
                        )

        # Guides: document_id must exist
        for guide in guides.values():
            if guide.document_id not in doc_ids:
                errors.append(
                    f"Guide '{guide.id}' references unknown document '{guide.document_id}'"
                )

        return errors

    # ── Accessors ─────────────────────────────────────────────────────────────

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self.load()

    def get_document(self, doc_id: str) -> Optional[Document]:
        self._ensure_loaded()
        return self._documents.get(doc_id)

    def get_all_documents(self) -> dict[str, Document]:
        self._ensure_loaded()
        return self._documents

    def get_service(self, svc_id: str) -> Optional[Service]:
        self._ensure_loaded()
        return self._services.get(svc_id)

    def get_all_services(self) -> dict[str, Service]:
        self._ensure_loaded()
        return self._services

    def get_guide_by_document(self, doc_id: str) -> Optional[Guide]:
        self._ensure_loaded()
        return self._guides_by_document.get(doc_id)

    def get_guide(self, guide_id: str) -> Optional[Guide]:
        self._ensure_loaded()
        return self._guides.get(guide_id)

    def get_services_using_document(self, doc_id: str) -> list[str]:
        self._ensure_loaded()
        return self._services_using_document.get(doc_id, [])

    def get_synonyms(self) -> dict[str, list[str]]:
        self._ensure_loaded()
        return self._synonyms


# Module-level singleton
_repo = _Repository()


def get_repo() -> _Repository:
    """Return the singleton repository, loading data on first call."""
    if not _repo._loaded:
        _repo.load()
    return _repo


def reset_repo_for_testing(
    documents: dict | None = None,
    services: dict | None = None,
    guides: dict | None = None,
    synonyms: dict | None = None,
) -> None:
    """Test helper: inject data directly without loading from disk."""
    _repo._documents = documents or {}
    _repo._services = services or {}
    _repo._guides = guides or {}
    _repo._guides_by_document = {g.document_id: g for g in (guides or {}).values()}
    _repo._synonyms = synonyms or {}

    # Rebuild reverse index
    svc_using: dict[str, list[str]] = {d: [] for d in _repo._documents}
    for svc in _repo._services.values():
        for req in svc.requirements:
            if req.document_id and req.document_id in svc_using:
                if svc.id not in svc_using[req.document_id]:
                    svc_using[req.document_id].append(svc.id)
            for opt in req.options:
                if opt in svc_using:
                    if svc.id not in svc_using[opt]:
                        svc_using[opt].append(svc.id)
    _repo._services_using_document = svc_using
    _repo._loaded = True
