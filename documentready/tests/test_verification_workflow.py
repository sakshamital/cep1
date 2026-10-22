"""Tests for verification, approval, rejection, and rollback lifecycle."""
import pytest
from app.models.db_models import (
    DetectedChange,
    InAppNotification,
    ServiceRecord,
    ServiceVersion,
)
from app.services.database import get_db_session, init_db
from app.services.verification import (
    approve_and_publish_change,
    reject_change,
    rollback_service_version,
)


def test_approve_and_publish_workflow(app):
    """Verify approval applies changes, increments version, and creates notification."""
    init_db(app, seed=True)

    with get_db_session() as s:
        svc = s.query(ServiceRecord).first()
        svc_id = svc.id
        initial_version = svc.version

        # Create proposed change
        chg = DetectedChange(
            source_id="src_test",
            target_type="service",
            target_id=svc_id,
            change_type="new_requirement",
            summary="New requirement: Electricity Bill",
            previous_data_json="{}",
            proposed_data_json='{"added_requirement": {"document_id": "electricity_bill", "necessity": "required"}}',
            evidence_quote="Electricity bill is mandatory",
            evidence_source_url="https://aaplesarkar.mahaonline.gov.in/test",
            status="proposed",
        )
        s.add(chg)
        s.commit()
        chg_id = chg.id

    res = approve_and_publish_change(chg_id, reviewer_username="lead_reviewer", notes="Verified with GR")
    assert res["status"] == "success"
    assert res["new_version"] == initial_version + 1

    with get_db_session() as s:
        svc_after = s.query(ServiceRecord).filter_by(id=svc_id).first()
        assert svc_after.version == initial_version + 1
        assert svc_after.verified is True

        # Check notification was generated
        notif = s.query(InAppNotification).filter_by(service_id=svc_id).first()
        assert notif is not None
        assert "Electricity Bill" in notif.message


def test_rejection_workflow(app):
    """Verify rejection records reviewer reason and does not alter service."""
    init_db(app, seed=True)

    with get_db_session() as s:
        svc = s.query(ServiceRecord).first()
        initial_version = svc.version

        chg = DetectedChange(
            source_id="src_test",
            target_type="service",
            target_id=svc.id,
            change_type="changed_fee",
            summary="Fee updated to Rs 500",
            evidence_quote="Fake fee note",
            evidence_source_url="https://fake.gov.in",
            status="proposed",
        )
        s.add(chg)
        s.commit()
        chg_id = chg.id

    res = reject_change(chg_id, reviewer_username="lead_reviewer", reason="Spurious notification; non-official domain")
    assert res["status"] == "success"

    with get_db_session() as s:
        chg_after = s.query(DetectedChange).filter_by(id=chg_id).first()
        assert chg_after.status == "rejected"
        assert chg_after.review_notes == "Spurious notification; non-official domain"

        svc_after = s.query(ServiceRecord).filter_by(id=svc.id).first()
        assert svc_after.version == initial_version


def test_rollback_operation(app):
    """Verify rollback restores previous state while preserving version history."""
    init_db(app, seed=True)

    with get_db_session() as s:
        svc = s.query(ServiceRecord).first()
        svc_id = svc.id
        v1_version = svc.version

        # Snapshot v1 is already in DB from seed
        # Publish an update to create v2
        chg = DetectedChange(
            source_id="src_test",
            target_type="service",
            target_id=svc_id,
            change_type="changed_fee",
            summary="Updated fee note",
            previous_data_json="{}",
            proposed_data_json='{"fee_note": "Rs 100"}',
            evidence_quote="Prescribed fee Rs 100",
            evidence_source_url="https://aaplesarkar.mahaonline.gov.in/test",
            status="proposed",
        )
        s.add(chg)
        s.commit()
        approve_and_publish_change(chg.id, reviewer_username="admin")

    # Now rollback to v1
    res = rollback_service_version(svc_id, target_version_number=v1_version, reviewer_username="admin", reason="Incorrect fee published")
    assert res["status"] == "success"

    with get_db_session() as s:
        svc_restored = s.query(ServiceRecord).filter_by(id=svc_id).first()
        # Version number increments to document the rollback (v3)
        assert svc_restored.version == v1_version + 2
        # History maintains all version records (v1, v2, v3)
        versions = s.query(ServiceVersion).filter_by(service_id=svc_id).all()
        assert len(versions) >= 3
