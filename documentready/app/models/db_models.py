"""SQLAlchemy Database Models for DocumentReady.

Provides persistence for services, documents, guides, version history,
source registry, source checks, detected changes, verification workflow,
audit events, users, and notifications.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

Base = declarative_base()


class ServiceRecord(Base):
    """Persistent storage for government services / schemes."""
    __tablename__ = "services"

    id = Column(String(64), primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    aliases_json = Column(Text, default="[]")
    type = Column(String(64), nullable=False, index=True)
    department = Column(String(255), default="")
    jurisdiction = Column(String(64), default="Maharashtra", index=True)
    description = Column(Text, default="")
    applicant_categories_json = Column(Text, default="[]")
    application_info_json = Column(Text, default="{}")
    verified = Column(Boolean, default=False, index=True)
    source_note = Column(Text, default="")
    official_source_url = Column(String(1024), nullable=True)
    last_reviewed = Column(String(64), nullable=True)
    last_verified_at = Column(DateTime, nullable=True)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    requirements = relationship(
        "ServiceRequirementRecord",
        back_populates="service",
        cascade="all, delete-orphan",
        order_by="ServiceRequirementRecord.order_index",
    )
    versions = relationship(
        "ServiceVersion",
        back_populates="service",
        cascade="all, delete-orphan",
        order_by="ServiceVersion.version_number.desc()",
    )

    @property
    def aliases(self) -> list[str]:
        return json.loads(self.aliases_json or "[]")

    @aliases.setter
    def aliases(self, val: list[str]):
        self.aliases_json = json.dumps(val or [])

    @property
    def applicant_categories(self) -> list[str]:
        return json.loads(self.applicant_categories_json or "[]")

    @applicant_categories.setter
    def applicant_categories(self, val: list[str]):
        self.applicant_categories_json = json.dumps(val or [])

    @property
    def application_info(self) -> dict:
        return json.loads(self.application_info_json or "{}")

    @application_info.setter
    def application_info(self, val: dict):
        self.application_info_json = json.dumps(val or {})

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "aliases": self.aliases,
            "type": self.type,
            "department": self.department or "",
            "jurisdiction": self.jurisdiction or "Maharashtra",
            "description": self.description or "",
            "applicant_categories": self.applicant_categories,
            "requirements": [r.to_dict() for r in self.requirements],
            "application_info": self.application_info,
            "verified": bool(self.verified),
            "source_note": self.source_note or "",
            "official_source_url": self.official_source_url,
            "last_reviewed": self.last_reviewed,
            "last_verified_at": self.last_verified_at.isoformat() if self.last_verified_at else None,
            "version": self.version,
        }


class ServiceRequirementRecord(Base):
    """A requirement associated with a service."""
    __tablename__ = "service_requirements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String(64), ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    necessity = Column(String(32), nullable=False)  # required, optional, conditional, any_of
    document_id = Column(String(64), nullable=True)
    group_name = Column(String(64), nullable=True)
    options_json = Column(Text, default="[]")
    note = Column(Text, nullable=True)
    when_clause_json = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)

    service = relationship("ServiceRecord", back_populates="requirements")

    @property
    def options(self) -> list[str]:
        return json.loads(self.options_json or "[]")

    @options.setter
    def options(self, val: list[str]):
        self.options_json = json.dumps(val or [])

    @property
    def when_clause(self) -> Optional[dict]:
        return json.loads(self.when_clause_json) if self.when_clause_json else None

    @when_clause.setter
    def when_clause(self, val: Optional[dict]):
        self.when_clause_json = json.dumps(val) if val else None

    def to_dict(self) -> dict:
        out: dict = {"necessity": self.necessity}
        if self.document_id:
            out["document_id"] = self.document_id
        if self.group_name:
            out["group"] = self.group_name
        if self.options:
            out["options"] = self.options
        if self.note:
            out["note"] = self.note
        if self.when_clause:
            out["when"] = self.when_clause
        return out


class ServiceVersion(Base):
    """Historical snapshot of a service for audit and rollback."""
    __tablename__ = "service_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String(64), ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    snapshot_json = Column(Text, nullable=False)
    change_summary = Column(Text, nullable=False)
    created_by = Column(String(64), default="system")
    created_at = Column(DateTime, default=utc_now)

    service = relationship("ServiceRecord", back_populates="versions")

    @property
    def snapshot(self) -> dict:
        return json.loads(self.snapshot_json)


class DocumentRecord(Base):
    """Persistent storage for document definitions."""
    __tablename__ = "documents"

    id = Column(String(64), primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    aliases_json = Column(Text, default="[]")
    kind = Column(String(64), nullable=False)
    description = Column(Text, default="")
    issuing_authority = Column(String(255), default="")
    jurisdiction = Column(String(64), default="Maharashtra")
    prerequisites_json = Column(Text, default="[]")
    guide_id = Column(String(64), nullable=True)
    verified = Column(Boolean, default=False, index=True)
    source_note = Column(Text, default="")
    official_link = Column(String(1024), nullable=True)
    last_reviewed = Column(String(64), nullable=True)
    last_verified_at = Column(DateTime, nullable=True)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    versions = relationship(
        "DocumentVersion",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="DocumentVersion.version_number.desc()",
    )

    @property
    def aliases(self) -> list[str]:
        return json.loads(self.aliases_json or "[]")

    @aliases.setter
    def aliases(self, val: list[str]):
        self.aliases_json = json.dumps(val or [])

    @property
    def prerequisites(self) -> list[str]:
        return json.loads(self.prerequisites_json or "[]")

    @prerequisites.setter
    def prerequisites(self, val: list[str]):
        self.prerequisites_json = json.dumps(val or [])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "aliases": self.aliases,
            "kind": self.kind,
            "description": self.description or "",
            "issuing_authority": self.issuing_authority or "",
            "jurisdiction": self.jurisdiction or "Maharashtra",
            "prerequisites": self.prerequisites,
            "guide_id": self.guide_id,
            "verified": bool(self.verified),
            "source_note": self.source_note or "",
            "official_link": self.official_link,
            "last_reviewed": self.last_reviewed,
            "last_verified_at": self.last_verified_at.isoformat() if self.last_verified_at else None,
            "version": self.version,
        }


class DocumentVersion(Base):
    """Historical snapshot of a document for audit and rollback."""
    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String(64), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    snapshot_json = Column(Text, nullable=False)
    change_summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    document = relationship("DocumentRecord", back_populates="versions")

    @property
    def snapshot(self) -> dict:
        return json.loads(self.snapshot_json)


class GuideRecord(Base):
    """Persistent storage for document guides."""
    __tablename__ = "guides"

    id = Column(String(64), primary_key=True)
    document_id = Column(String(64), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    what_it_is = Column(Text, default="")
    documents_required_json = Column(Text, default="[]")
    procedure_steps_json = Column(Text, default="[]")
    where_how_to_apply = Column(Text, default="")
    precautions_json = Column(Text, default="[]")
    official_link = Column(String(1024), nullable=True)
    verified = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    versions = relationship(
        "GuideVersion",
        back_populates="guide",
        cascade="all, delete-orphan",
        order_by="GuideVersion.version_number.desc()",
    )

    @property
    def documents_required(self) -> list[str]:
        return json.loads(self.documents_required_json or "[]")

    @documents_required.setter
    def documents_required(self, val: list[str]):
        self.documents_required_json = json.dumps(val or [])

    @property
    def procedure_steps(self) -> list[str]:
        return json.loads(self.procedure_steps_json or "[]")

    @procedure_steps.setter
    def procedure_steps(self, val: list[str]):
        self.procedure_steps_json = json.dumps(val or [])

    @property
    def precautions(self) -> list[str]:
        return json.loads(self.precautions_json or "[]")

    @precautions.setter
    def precautions(self, val: list[str]):
        self.precautions_json = json.dumps(val or [])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "document_id": self.document_id,
            "what_it_is": self.what_it_is or "",
            "documents_required": self.documents_required,
            "procedure_steps": self.procedure_steps,
            "where_how_to_apply": self.where_how_to_apply or "",
            "precautions": self.precautions,
            "official_link": self.official_link,
            "verified": bool(self.verified),
            "version": self.version,
        }


class GuideVersion(Base):
    """Historical snapshot of a guide for audit and rollback."""
    __tablename__ = "guide_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    guide_id = Column(String(64), ForeignKey("guides.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    snapshot_json = Column(Text, nullable=False)
    change_summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    guide = relationship("GuideRecord", back_populates="versions")

    @property
    def snapshot(self) -> dict:
        return json.loads(self.snapshot_json)



class SourceRegistry(Base):
    """Registry of permitted official government sources for automated monitoring."""
    __tablename__ = "sources"

    id = Column(String(64), primary_key=True)
    name = Column(String(255), nullable=False)
    department = Column(String(255), default="")
    jurisdiction = Column(String(64), default="Maharashtra")
    official_base_url = Column(String(1024), nullable=False)
    monitored_url = Column(String(1024), nullable=False)
    source_type = Column(String(32), default="html")  # html, pdf, json_api, rss
    adapter = Column(String(64), default="generic_html")
    associated_service_ids_json = Column(Text, default="[]")
    associated_document_ids_json = Column(Text, default="[]")
    check_frequency_minutes = Column(Integer, default=360)
    enabled = Column(Boolean, default=True, index=True)
    priority = Column(String(32), default="normal")  # high, normal, low
    verification_policy = Column(String(32), default="manual_review")  # manual_review, auto_publish_minor
    last_attempted_check = Column(DateTime, nullable=True)
    last_successful_check = Column(DateTime, nullable=True)
    last_detected_change = Column(DateTime, nullable=True)
    last_verified_update = Column(DateTime, nullable=True)
    current_fingerprint = Column(String(64), nullable=True)
    etag = Column(String(128), nullable=True)
    last_modified_header = Column(String(128), nullable=True)
    last_http_status = Column(Integer, nullable=True)
    consecutive_failures = Column(Integer, default=0)
    last_error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    fetches = relationship("SourceFetchHistory", back_populates="source", cascade="all, delete-orphan", order_by="SourceFetchHistory.attempted_at.desc()")
    changes = relationship("DetectedChange", back_populates="source")

    @property
    def associated_service_ids(self) -> list[str]:
        return json.loads(self.associated_service_ids_json or "[]")

    @associated_service_ids.setter
    def associated_service_ids(self, val: list[str]):
        self.associated_service_ids_json = json.dumps(val or [])

    @property
    def associated_document_ids(self) -> list[str]:
        return json.loads(self.associated_document_ids_json or "[]")

    @associated_document_ids.setter
    def associated_document_ids(self, val: list[str]):
        self.associated_document_ids_json = json.dumps(val or [])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department or "",
            "jurisdiction": self.jurisdiction or "Maharashtra",
            "official_base_url": self.official_base_url,
            "monitored_url": self.monitored_url,
            "source_type": self.source_type,
            "adapter": self.adapter,
            "associated_service_ids": self.associated_service_ids,
            "associated_document_ids": self.associated_document_ids,
            "check_frequency_minutes": self.check_frequency_minutes,
            "enabled": bool(self.enabled),
            "priority": self.priority,
            "verification_policy": self.verification_policy,
            "last_attempted_check": self.last_attempted_check.isoformat() if self.last_attempted_check else None,
            "last_successful_check": self.last_successful_check.isoformat() if self.last_successful_check else None,
            "last_detected_change": self.last_detected_change.isoformat() if self.last_detected_change else None,
            "last_verified_update": self.last_verified_update.isoformat() if self.last_verified_update else None,
            "current_fingerprint": self.current_fingerprint,
            "etag": self.etag,
            "last_modified_header": self.last_modified_header,
            "last_http_status": self.last_http_status,
            "consecutive_failures": self.consecutive_failures,
            "last_error_message": self.last_error_message,
        }


class SourceFetchHistory(Base):
    """Detailed log of each fetch attempt for a source."""
    __tablename__ = "source_fetch_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String(64), ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True)
    attempted_at = Column(DateTime, default=utc_now, index=True)
    http_status = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    content_fingerprint = Column(String(64), nullable=True)
    change_detected = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)

    source = relationship("SourceRegistry", back_populates="fetches")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "attempted_at": self.attempted_at.isoformat() if self.attempted_at else None,
            "http_status": self.http_status,
            "response_time_ms": self.response_time_ms,
            "content_fingerprint": self.content_fingerprint,
            "change_detected": bool(self.change_detected),
            "error_message": self.error_message,
        }


class SourceDocument(Base):
    """Metadata and raw text for documents/circulars downloaded during monitoring."""
    __tablename__ = "source_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String(64), ForeignKey("sources.id", ondelete="SET NULL"), nullable=True, index=True)
    url = Column(String(1024), nullable=False)
    title = Column(String(255), default="")
    publication_date = Column(String(64), nullable=True)
    retrieval_timestamp = Column(DateTime, default=utc_now)
    content_hash = Column(String(64), nullable=False, index=True)
    file_path = Column(String(512), nullable=True)
    extracted_text = Column(Text, nullable=True)
    extracted_metadata_json = Column(Text, default="{}")
    is_scanned = Column(Boolean, default=False)
    ocr_applied = Column(Boolean, default=False)

    @property
    def extracted_metadata(self) -> dict:
        return json.loads(self.extracted_metadata_json or "{}")

    @extracted_metadata.setter
    def extracted_metadata(self, val: dict):
        self.extracted_metadata_json = json.dumps(val or {})


class DetectedChange(Base):
    """A detected difference between official sources and application records."""
    __tablename__ = "detected_changes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String(64), ForeignKey("sources.id", ondelete="SET NULL"), nullable=True, index=True)
    target_type = Column(String(32), nullable=False)  # service, document
    target_id = Column(String(64), nullable=False, index=True)
    change_type = Column(String(64), nullable=False)  # new_requirement, removed_requirement, modified_eligibility, modified_procedure, changed_fee, changed_link, ambiguous
    summary = Column(Text, nullable=False)
    previous_data_json = Column(Text, default="{}")
    proposed_data_json = Column(Text, default="{}")
    evidence_quote = Column(Text, nullable=False)
    evidence_source_url = Column(String(1024), nullable=False)
    evidence_section = Column(String(255), nullable=True)
    confidence_score = Column(Float, default=1.0)
    status = Column(String(32), default="proposed", index=True)  # proposed, approved, rejected, published, rolled_back
    detected_at = Column(DateTime, default=utc_now, index=True)
    reviewed_by = Column(String(64), nullable=True)
    review_notes = Column(Text, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    effective_date = Column(String(64), nullable=True)

    source = relationship("SourceRegistry", back_populates="changes")

    @property
    def previous_data(self) -> dict:
        return json.loads(self.previous_data_json or "{}")

    @previous_data.setter
    def previous_data(self, val: dict):
        self.previous_data_json = json.dumps(val or {})

    @property
    def proposed_data(self) -> dict:
        return json.loads(self.proposed_data_json or "{}")

    @proposed_data.setter
    def proposed_data(self, val: dict):
        self.proposed_data_json = json.dumps(val or {})

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "change_type": self.change_type,
            "summary": self.summary,
            "previous_data": self.previous_data,
            "proposed_data": self.proposed_data,
            "evidence_quote": self.evidence_quote,
            "evidence_source_url": self.evidence_source_url,
            "evidence_section": self.evidence_section,
            "confidence_score": self.confidence_score,
            "status": self.status,
            "detected_at": self.detected_at.isoformat() if self.detected_at else None,
            "reviewed_by": self.reviewed_by,
            "review_notes": self.review_notes,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "effective_date": self.effective_date,
        }


class VerificationDecision(Base):
    """Audit log of human or policy verification decisions."""
    __tablename__ = "verification_decisions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    change_id = Column(Integer, ForeignKey("detected_changes.id", ondelete="CASCADE"), nullable=False, index=True)
    decision = Column(String(32), nullable=False)  # approved, rejected, rollback
    reviewer_username = Column(String(64), nullable=False)
    notes = Column(Text, nullable=True)
    decided_at = Column(DateTime, default=utc_now)


class AuditEvent(Base):
    """System-wide security and operational audit trail."""
    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(64), nullable=False, index=True)
    actor = Column(String(64), default="system")
    details_json = Column(Text, default="{}")
    ip_address = Column(String(64), nullable=True)
    timestamp = Column(DateTime, default=utc_now, index=True)

    @property
    def details(self) -> dict:
        return json.loads(self.details_json or "{}")

    @details.setter
    def details(self, val: dict):
        self.details_json = json.dumps(val or {})

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "actor": self.actor,
            "details": self.details,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


class UserAccount(Base):
    """Administrative user accounts."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), default="reviewer")  # admin, reviewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)
    last_login_at = Column(DateTime, nullable=True)


class InAppNotification(Base):
    """In-application updates for citizens regarding verified requirement changes."""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    service_id = Column(String(64), nullable=True, index=True)
    document_id = Column(String(64), nullable=True)
    source_url = Column(String(1024), nullable=True)
    change_type = Column(String(64), nullable=False)
    published_at = Column(DateTime, default=datetime.utcnow, index=True)
    is_read = Column(Boolean, default=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "service_id": self.service_id,
            "document_id": self.document_id,
            "source_url": self.source_url,
            "change_type": self.change_type,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "is_read": bool(self.is_read),
        }


class StateRecord(Base):
    """Persistent storage for Indian states and union territories."""
    __tablename__ = "states"

    id = Column(String(8), primary_key=True)
    name = Column(String(128), nullable=False)
    name_hi = Column(String(128), nullable=True)
    name_mr = Column(String(128), nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "name_hi": self.name_hi or self.name,
            "name_mr": self.name_mr or self.name,
        }


class StateRuleRecord(Base):
    """State-specific portal URLs, statutory rules, authorities, and additional prerequisites."""
    __tablename__ = "state_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String(64), ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    state_id = Column(String(8), ForeignKey("states.id", ondelete="CASCADE"), nullable=False, index=True)
    authority = Column(String(255), default="")
    portal_name = Column(String(255), default="")
    portal_url = Column(String(1024), default="")
    statutory_rule = Column(Text, default="")
    additional_requirements_json = Column(Text, default="[]")
    application_steps_json = Column(Text, default="[]")
    raw_data_json = Column(Text, default="{}")

    @property
    def additional_requirements(self) -> list[dict]:
        return json.loads(self.additional_requirements_json or "[]")

    @additional_requirements.setter
    def additional_requirements(self, val: list[dict]):
        self.additional_requirements_json = json.dumps(val or [])

    @property
    def application_steps(self) -> list[str]:
        return json.loads(self.application_steps_json or "[]")

    @application_steps.setter
    def application_steps(self, val: list[str]):
        self.application_steps_json = json.dumps(val or [])

    def to_dict(self) -> dict:
        out = json.loads(self.raw_data_json or "{}")
        out["state_id"] = self.state_id
        out["authority"] = self.authority
        out["portal_name"] = self.portal_name
        out["portal_url"] = self.portal_url
        out["statutory_rule"] = self.statutory_rule
        out["additional_requirements"] = self.additional_requirements
        out["application_steps"] = self.application_steps
        return out


class SynonymRecord(Base):
    """Search query synonym mapping."""
    __tablename__ = "synonyms"

    term = Column(String(64), primary_key=True)
    synonyms_json = Column(Text, default="[]")

    @property
    def synonyms(self) -> list[str]:
        return json.loads(self.synonyms_json or "[]")

    @synonyms.setter
    def synonyms(self, val: list[str]):
        self.synonyms_json = json.dumps(val or [])

