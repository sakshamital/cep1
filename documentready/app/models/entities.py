"""Dataclasses for DocumentReady domain entities."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Document:
    """A document, form, stamp paper, photo, or affidavit."""
    id: str
    name: str
    aliases: list[str]
    kind: str
    description: str
    issuing_authority: str
    prerequisites: list[str]
    guide_id: Optional[str]
    verified: bool
    source_note: str
    last_reviewed: Optional[str]

    jurisdiction: str = "Maharashtra"
    official_link: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "Document":
        return cls(
            id=d["id"],
            name=d["name"],
            aliases=d.get("aliases", []),
            kind=d["kind"],
            description=d.get("description", ""),
            issuing_authority=d.get("issuing_authority", ""),
            prerequisites=d.get("prerequisites", []),
            guide_id=d.get("guide_id"),
            verified=d.get("verified", False),
            source_note=d.get("source_note", ""),
            last_reviewed=d.get("last_reviewed"),
            jurisdiction=d.get("jurisdiction", "Maharashtra"),
            official_link=d.get("official_link"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "aliases": self.aliases,
            "kind": self.kind,
            "description": self.description,
            "issuing_authority": self.issuing_authority,
            "prerequisites": self.prerequisites,
            "guide_id": self.guide_id,
            "verified": self.verified,
            "source_note": self.source_note,
            "last_reviewed": self.last_reviewed,
            "jurisdiction": self.jurisdiction,
            "official_link": self.official_link,
        }


@dataclass
class ServiceRequirement:
    """A single requirement entry in a service."""
    necessity: str  # required | optional | conditional | any_of
    document_id: Optional[str] = None
    group: Optional[str] = None
    options: list[str] = field(default_factory=list)
    note: Optional[str] = None
    when: Optional[dict] = None

    @classmethod
    def from_dict(cls, d: dict) -> "ServiceRequirement":
        return cls(
            necessity=d["necessity"],
            document_id=d.get("document_id"),
            group=d.get("group"),
            options=d.get("options", []),
            note=d.get("note"),
            when=d.get("when"),
        )

    def to_dict(self) -> dict:
        out: dict = {"necessity": self.necessity}
        if self.document_id:
            out["document_id"] = self.document_id
        if self.group:
            out["group"] = self.group
        if self.options:
            out["options"] = self.options
        if self.note:
            out["note"] = self.note
        if self.when:
            out["when"] = self.when
        return out


@dataclass
class ApplicationInfo:
    """Information about how to apply for a service."""
    where: str
    mode: str
    steps: list[str]
    fee_note: str

    @classmethod
    def from_dict(cls, d: dict) -> "ApplicationInfo":
        return cls(
            where=d.get("where", ""),
            mode=d.get("mode", ""),
            steps=d.get("steps", []),
            fee_note=d.get("fee_note", ""),
        )

    def to_dict(self) -> dict:
        return {
            "where": self.where,
            "mode": self.mode,
            "steps": self.steps,
            "fee_note": self.fee_note,
        }


@dataclass
class Service:
    """A government service or scheme."""
    id: str
    name: str
    aliases: list[str]
    type: str
    department: str
    description: str
    applicant_categories: list[str]
    requirements: list[ServiceRequirement]
    application_info: ApplicationInfo
    verified: bool
    source_note: str
    last_reviewed: Optional[str]
    version: int = 1
    jurisdiction: str = "Maharashtra"
    official_source_url: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "Service":
        return cls(
            id=d["id"],
            name=d["name"],
            aliases=d.get("aliases", []),
            type=d["type"],
            department=d.get("department", ""),
            description=d.get("description", ""),
            applicant_categories=d.get("applicant_categories", []),
            requirements=[ServiceRequirement.from_dict(r) for r in d.get("requirements", [])],
            application_info=ApplicationInfo.from_dict(d.get("application_info", {})),
            verified=d.get("verified", False),
            source_note=d.get("source_note", ""),
            last_reviewed=d.get("last_reviewed"),
            version=d.get("version", 1),
            jurisdiction=d.get("jurisdiction", "Maharashtra"),
            official_source_url=d.get("official_source_url"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "aliases": self.aliases,
            "type": self.type,
            "department": self.department,
            "description": self.description,
            "applicant_categories": self.applicant_categories,
            "requirements": [r.to_dict() for r in self.requirements],
            "application_info": self.application_info.to_dict(),
            "verified": self.verified,
            "source_note": self.source_note,
            "last_reviewed": self.last_reviewed,
            "version": self.version,
            "jurisdiction": self.jurisdiction,
            "official_source_url": self.official_source_url,
        }


@dataclass
class Guide:
    """A 'How to obtain?' guide for a document."""
    id: str
    document_id: str
    what_it_is: str
    documents_required: list[str]
    procedure_steps: list[str]
    where_how_to_apply: str
    precautions: list[str]
    official_link: Optional[str]
    verified: bool

    @classmethod
    def from_dict(cls, d: dict) -> "Guide":
        return cls(
            id=d["id"],
            document_id=d["document_id"],
            what_it_is=d.get("what_it_is", ""),
            documents_required=d.get("documents_required", []),
            procedure_steps=d.get("procedure_steps", []),
            where_how_to_apply=d.get("where_how_to_apply", ""),
            precautions=d.get("precautions", []),
            official_link=d.get("official_link"),
            verified=d.get("verified", False),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "document_id": self.document_id,
            "what_it_is": self.what_it_is,
            "documents_required": self.documents_required,
            "procedure_steps": self.procedure_steps,
            "where_how_to_apply": self.where_how_to_apply,
            "precautions": self.precautions,
            "official_link": self.official_link,
            "verified": self.verified,
        }


@dataclass
class SearchHit:
    """A single search result."""
    id: str
    name: str
    kind: str  # "service" | "document"
    score: float
    matched_on: str
    description: str = ""
    type: str = ""
    used_by_services: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        out = {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "score": self.score,
            "matched_on": self.matched_on,
            "description": self.description,
            "type": self.type,
        }
        if self.kind == "document":
            out["used_by_services"] = self.used_by_services
        return out


@dataclass
class ResolvedRequirements:
    """The result of resolving which requirements apply to a service+category+state."""
    service: dict
    items: list[dict]
    hidden_conditional: list[str]
    state_rule: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            "service": self.service,
            "items": self.items,
            "hidden_conditional": self.hidden_conditional,
            "state_rule": self.state_rule,
        }


@dataclass
class ReadinessResult:
    """The result of the readiness engine."""
    ready: bool
    message: str
    progress: dict
    blockers: list[dict]
    unverified: list[dict]
    groups: list[dict]
    obtain_plan: list[str]
    ignored_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "ready": self.ready,
            "message": self.message,
            "progress": self.progress,
            "blockers": self.blockers,
            "unverified": self.unverified,
            "groups": self.groups,
            "obtain_plan": self.obtain_plan,
            "ignored_ids": self.ignored_ids,
        }
