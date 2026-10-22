"""Verification, Approval, Publication, and Rollback lifecycle engine."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.db_models import (
    AuditEvent,
    DetectedChange,
    DocumentRecord,
    DocumentVersion,
    InAppNotification,
    ServiceRecord,
    ServiceRequirementRecord,
    ServiceVersion,
    SourceRegistry,
    VerificationDecision,
    utc_now,
)
from app.services.database import get_db_session
from app.services.repository import get_repo

logger = logging.getLogger(__name__)


class VerificationError(Exception):
    """Raised on invalid verification or rollback operations."""


def approve_and_publish_change(
    change_id: int,
    reviewer_username: str,
    notes: Optional[str] = None,
    session: Optional[Session] = None,
) -> dict:
    """Approve a proposed change, publish it to active records, update versions, and notify citizens."""
    if session is not None:
        return _execute_approval(change_id, reviewer_username, notes, session)
    else:
        with get_db_session() as s:
            return _execute_approval(change_id, reviewer_username, notes, s)


def _execute_approval(
    change_id: int,
    reviewer_username: str,
    notes: Optional[str],
    session: Session,
) -> dict:
    change = session.query(DetectedChange).filter_by(id=change_id).first()
    if not change:
        raise VerificationError(f"Change ID {change_id} not found.")

    if change.status not in ("proposed", "discovered", "parsed"):
        raise VerificationError(f"Change ID {change_id} is in status '{change.status}' and cannot be approved.")

    now = utc_now()
    change.status = "published"
    change.reviewed_by = reviewer_username
    change.review_notes = notes
    change.reviewed_at = now

    # Record decision audit
    decision = VerificationDecision(
        change_id=change.id,
        decision="approved",
        reviewer_username=reviewer_username,
        notes=notes,
        decided_at=now,
    )
    session.add(decision)

    # Apply changes to target entity
    if change.target_type == "service":
        svc = session.query(ServiceRecord).filter_by(id=change.target_id).first()
        if not svc:
            raise VerificationError(f"Target service '{change.target_id}' not found.")

        # Update service version and verification status
        svc.version += 1
        svc.verified = True
        svc.last_verified_at = now
        svc.last_reviewed = now.strftime("%Y-%m-%d")
        if change.evidence_source_url:
            svc.official_source_url = change.evidence_source_url

        proposed = change.proposed_data
        if change.change_type == "new_requirement":
            added_req = proposed.get("added_requirement", {})
            if added_req:
                max_order = len(svc.requirements)
                new_req_record = ServiceRequirementRecord(
                    service_id=svc.id,
                    necessity=added_req.get("necessity", "required"),
                    document_id=added_req.get("document_id"),
                    group_name=added_req.get("group"),
                    note=added_req.get("note"),
                    order_index=max_order,
                )
                if added_req.get("options"):
                    new_req_record.options = added_req["options"]
                if added_req.get("when"):
                    new_req_record.when_clause = added_req["when"]
                session.add(new_req_record)

        elif change.change_type == "changed_fee":
            new_fee = proposed.get("fee_note")
            if new_fee:
                app_info = dict(svc.application_info)
                app_info["fee_note"] = new_fee
                svc.application_info = app_info

        elif change.change_type == "changed_link":
            new_link = proposed.get("official_link")
            if new_link:
                app_info = dict(svc.application_info)
                app_info["where"] = f"Official Portal: {new_link}"
                svc.application_info = app_info
                svc.official_source_url = new_link

        elif change.change_type == "removed_requirement":
            rem_doc_id = proposed.get("document_id") or proposed.get("removed_document_id")
            if rem_doc_id:
                session.query(ServiceRequirementRecord).filter_by(
                    service_id=svc.id, document_id=rem_doc_id
                ).delete()

        session.flush()

        # Create new service version snapshot
        version_rec = ServiceVersion(
            service_id=svc.id,
            version_number=svc.version,
            snapshot_json=json.dumps(svc.to_dict()),
            change_summary=f"Approved change ({change.change_type}): {change.summary}",
            created_by=reviewer_username,
            created_at=now,
        )
        session.add(version_rec)

        # Update associated source last_verified_update
        if change.source_id:
            src = session.query(SourceRegistry).filter_by(id=change.source_id).first()
            if src:
                src.last_verified_update = now

        # Create In-App Notification for citizens
        notif = InAppNotification(
            title=f"Verified update for {svc.name}",
            message=change.summary,
            service_id=svc.id,
            source_url=change.evidence_source_url,
            change_type=change.change_type,
            published_at=now,
        )
        session.add(notif)

        # Audit Event
        audit = AuditEvent(
            event_type="change_published",
            actor=reviewer_username,
            details_json=json.dumps({
                "change_id": change.id,
                "target_type": "service",
                "target_id": svc.id,
                "version": svc.version,
                "notes": notes,
            }),
        )
        session.add(audit)
        session.commit()

        # Synchronize repository in-memory state
        try:
            get_repo().reload_from_db()
        except Exception as e:
            logger.warning("Error refreshing repo cache after approval: %s", e)

        return {
            "status": "success",
            "message": f"Change {change_id} published successfully. Service version incremented to {svc.version}.",
            "new_version": svc.version,
        }

    elif change.target_type == "document":
        doc = session.query(DocumentRecord).filter_by(id=change.target_id).first()
        if not doc:
            raise VerificationError(f"Target document '{change.target_id}' not found.")

        doc.version += 1
        doc.verified = True
        doc.last_verified_at = now
        doc.last_reviewed = now.strftime("%Y-%m-%d")
        if change.evidence_source_url:
            doc.official_link = change.evidence_source_url

        session.flush()

        doc_ver = DocumentVersion(
            document_id=doc.id,
            version_number=doc.version,
            snapshot_json=json.dumps(doc.to_dict()),
            change_summary=f"Approved change ({change.change_type}): {change.summary}",
            created_at=now,
        )
        session.add(doc_ver)

        if change.source_id:
            src = session.query(SourceRegistry).filter_by(id=change.source_id).first()
            if src:
                src.last_verified_update = now

        notif = InAppNotification(
            title=f"Verified update for {doc.name}",
            message=change.summary,
            document_id=doc.id,
            source_url=change.evidence_source_url,
            change_type=change.change_type,
            published_at=now,
        )
        session.add(notif)

        audit = AuditEvent(
            event_type="change_published",
            actor=reviewer_username,
            details_json=json.dumps({
                "change_id": change.id,
                "target_type": "document",
                "target_id": doc.id,
                "version": doc.version,
                "notes": notes,
            }),
        )
        session.add(audit)
        session.commit()

        try:
            get_repo().reload_from_db()
        except Exception as e:
            logger.warning("Error refreshing repo cache after approval: %s", e)

        return {
            "status": "success",
            "message": f"Change {change_id} published successfully. Document version incremented to {doc.version}.",
            "new_version": doc.version,
        }

    raise VerificationError(f"Target type '{change.target_type}' not supported for automatic publication.")


def reject_change(
    change_id: int,
    reviewer_username: str,
    reason: str,
    session: Optional[Session] = None,
) -> dict:
    """Reject a proposed change with a stated reason."""
    if session is not None:
        return _execute_rejection(change_id, reviewer_username, reason, session)
    else:
        with get_db_session() as s:
            return _execute_rejection(change_id, reviewer_username, reason, s)


def _execute_rejection(
    change_id: int,
    reviewer_username: str,
    reason: str,
    session: Session,
) -> dict:
    change = session.query(DetectedChange).filter_by(id=change_id).first()
    if not change:
        raise VerificationError(f"Change ID {change_id} not found.")

    now = utc_now()
    change.status = "rejected"
    change.reviewed_by = reviewer_username
    change.review_notes = reason
    change.reviewed_at = now

    decision = VerificationDecision(
        change_id=change.id,
        decision="rejected",
        reviewer_username=reviewer_username,
        notes=reason,
        decided_at=now,
    )
    session.add(decision)

    audit = AuditEvent(
        event_type="change_rejected",
        actor=reviewer_username,
        details_json=json.dumps({"change_id": change.id, "reason": reason}),
    )
    session.add(audit)
    session.commit()

    return {"status": "success", "message": f"Change {change_id} rejected."}


def rollback_service_version(
    service_id: str,
    target_version_number: int,
    reviewer_username: str,
    reason: str,
    session: Optional[Session] = None,
) -> dict:
    """Safely restore a service to a previous version snapshot without destroying audit history."""
    if session is not None:
        return _execute_rollback(service_id, target_version_number, reviewer_username, reason, session)
    else:
        with get_db_session() as s:
            return _execute_rollback(service_id, target_version_number, reviewer_username, reason, s)


def _execute_rollback(
    service_id: str,
    target_version_number: int,
    reviewer_username: str,
    reason: str,
    session: Session,
) -> dict:
    svc = session.query(ServiceRecord).filter_by(id=service_id).first()
    if not svc:
        raise VerificationError(f"Service '{service_id}' not found.")

    target_ver = (
        session.query(ServiceVersion)
        .filter_by(service_id=service_id, version_number=target_version_number)
        .first()
    )
    if not target_ver:
        raise VerificationError(
            f"Version {target_version_number} for service '{service_id}' not found in history."
        )

    snapshot = target_ver.snapshot
    now = utc_now()

    # Restore fields
    svc.name = snapshot.get("name", svc.name)
    svc.aliases = snapshot.get("aliases", [])
    svc.type = snapshot.get("type", svc.type)
    svc.department = snapshot.get("department", svc.department)
    svc.description = snapshot.get("description", svc.description)
    svc.applicant_categories = snapshot.get("applicant_categories", [])
    svc.application_info = snapshot.get("application_info", {})
    svc.verified = snapshot.get("verified", False)
    svc.official_source_url = snapshot.get("official_source_url")
    svc.last_reviewed = now.strftime("%Y-%m-%d")

    # Clear current requirements and restore from snapshot
    session.query(ServiceRequirementRecord).filter_by(service_id=svc.id).delete()
    for idx, req_data in enumerate(snapshot.get("requirements", [])):
        r = ServiceRequirementRecord(
            service_id=svc.id,
            necessity=req_data["necessity"],
            document_id=req_data.get("document_id"),
            group_name=req_data.get("group"),
            note=req_data.get("note"),
            order_index=idx,
        )
        r.options = req_data.get("options", [])
        r.when_clause = req_data.get("when")
        session.add(r)

    # Increment version
    svc.version += 1
    session.flush()

    # Create new rollback version entry
    new_ver = ServiceVersion(
        service_id=svc.id,
        version_number=svc.version,
        snapshot_json=json.dumps(svc.to_dict()),
        change_summary=f"Rolled back to version {target_version_number}. Reason: {reason}",
        created_by=reviewer_username,
        created_at=now,
    )
    session.add(new_ver)

    audit = AuditEvent(
        event_type="service_rollback",
        actor=reviewer_username,
        details_json=json.dumps({
            "service_id": service_id,
            "restored_version": target_version_number,
            "new_version": svc.version,
            "reason": reason,
        }),
    )
    session.add(audit)
    session.commit()

    try:
        get_repo().reload_from_db()
    except Exception as e:
        logger.warning("Error refreshing repo cache after rollback: %s", e)

    return {
        "status": "success",
        "message": f"Service '{service_id}' successfully restored to version {target_version_number}. Active version is now {svc.version}.",
        "new_version": svc.version,
    }
