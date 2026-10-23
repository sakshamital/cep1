"""
Core unit tests — data integrity, prerequisite graph, search, requirements resolution,
and readiness evaluation. These tests use in-memory repo fixtures and do not require
a database or running server.
"""
import pytest
from app.models.entities import (
    Document, Service, ServiceRequirement, ApplicationInfo,
)
from app.services.graph import assert_acyclic, CycleError, topological_order, prerequisite_closure
from app.services.search import search
from app.services.readiness import evaluate
from app.services.requirements import resolve_requirements, RequirementsError
from app.services.repository import get_repo, reset_repo_for_testing


# ── Data Integrity ────────────────────────────────────────────────────────────

def test_data_integrity():
    repo = get_repo()
    repo.load()  # Must not raise
    docs = repo.get_all_documents()
    for doc in docs.values():
        if not doc.verified:
            assert doc.source_note != ""


# ── Prerequisite Graph ────────────────────────────────────────────────────────

def test_assert_acyclic():
    docs = {
        "A": Document("A", "A", [], "other", "", "", ["B"], None, False, "", None),
        "B": Document("B", "B", [], "other", "", "", ["A"], None, False, "", None),
    }
    with pytest.raises(CycleError, match="A → B → A"):
        assert_acyclic(docs)

    docs2 = {
        "A": Document("A", "A", [], "other", "", "", ["B"], None, False, "", None),
        "B": Document("B", "B", [], "other", "", "", [], None, False, "", None),
    }
    assert_acyclic(docs2)  # Should not raise


def test_prerequisite_closure():
    docs = {
        "A": Document("A", "A", [], "other", "", "", ["B"], None, False, "", None),
        "B": Document("B", "B", [], "other", "", "", ["C"], None, False, "", None),
        "C": Document("C", "C", [], "other", "", "", [], None, False, "", None),
    }
    assert prerequisite_closure("A", docs) == {"B", "C"}


def test_topological_order():
    docs = {
        "A": Document("A", "A", [], "other", "", "", ["B", "C"], None, False, "", None),
        "B": Document("B", "B", [], "other", "", "", ["D"], None, False, "", None),
        "C": Document("C", "C", [], "other", "", "", ["D"], None, False, "", None),
        "D": Document("D", "D", [], "other", "", "", [], None, False, "", None),
    }
    order = topological_order(["A"], docs)
    assert order == ["D", "B", "C", "A"] or order == ["D", "C", "B", "A"]
    assert order.count("D") == 1  # Shared prerequisite appears once


# ── Search ────────────────────────────────────────────────────────────────────

def test_search():
    docs = {
        "D1": Document("D1", "Aadhaar Card", ["aadhar", "uid"], "other", "", "", [], None, False, "", None),
    }
    svcs = {
        "S1": Service("S1", "Caste Validity Certificate", ["cvc"], "scheme", "", "", [], [], ApplicationInfo("", "", [], ""), False, "", None),
    }
    reset_repo_for_testing(documents=docs, services=svcs, synonyms={"aadhar": ["aadhaar"]})

    hits = search("Caste Validity Certificate")
    assert len(hits) == 1 and hits[0].id == "S1"

    hits = search("cvc")
    assert len(hits) == 1 and hits[0].id == "S1"

    hits = search("aadhar")
    assert len(hits) == 1 and hits[0].id == "D1"

    hits = search("casst validty")
    assert len(hits) == 1 and hits[0].id == "S1"

    assert len(search("a")) == 0  # Too short


# ── Requirements Resolution ───────────────────────────────────────────────────

def test_resolve_requirements_conditional():
    svc = Service(
        id="S1", name="S1", aliases=[], type="scheme", department="", description="",
        applicant_categories=["student", "employee"],
        requirements=[
            ServiceRequirement("required", document_id="doc1"),
            ServiceRequirement("conditional", document_id="doc2", when={"applicant_category": ["student"]}),
        ],
        application_info=ApplicationInfo("", "", [], ""), verified=False, source_note="", last_reviewed=None,
    )
    reset_repo_for_testing(services={"S1": svc})

    res1 = resolve_requirements("S1", "student")
    assert len(res1.items) == 2
    assert res1.items[1]["document_id"] == "doc2"
    assert res1.items[1]["necessity"] == "required"

    res2 = resolve_requirements("S1", "employee")
    assert len(res2.items) == 1
    assert "doc2" in res2.hidden_conditional


def test_resolve_requirements_invalid_category():
    svc = Service(
        id="S1", name="S1", aliases=[], type="scheme", department="", description="",
        applicant_categories=["student", "employee"],
        requirements=[],
        application_info=ApplicationInfo("", "", [], ""), verified=False, source_note="", last_reviewed=None,
    )
    reset_repo_for_testing(services={"S1": svc})
    with pytest.raises(RequirementsError):
        resolve_requirements("S1", "alien")


# ── Readiness Evaluation ──────────────────────────────────────────────────────

@pytest.fixture
def readiness_data():
    docs = {
        "D1": Document("D1", "Doc 1", [], "other", "", "", ["D2"], None, False, "", None),
        "D2": Document("D2", "Doc 2", [], "other", "", "", ["D3"], None, False, "", None),
        "D3": Document("D3", "Doc 3", [], "other", "", "", [], None, False, "", None),
        "O1": Document("O1", "Opt 1", [], "other", "", "", [], None, False, "", None),
        "A1": Document("A1", "Any 1", [], "other", "", "", [], None, False, "", None),
        "A2": Document("A2", "Any 2", [], "other", "", "", [], None, False, "", None),
    }
    svc = Service(
        "S1", "S1", [], "scheme", "", "", [],
        [
            ServiceRequirement("required", document_id="D1"),
            ServiceRequirement("optional", document_id="O1"),
            ServiceRequirement("any_of", group="grp1", options=["A1", "A2"]),
        ],
        ApplicationInfo("", "", [], ""), False, "", None,
    )
    reset_repo_for_testing(documents=docs, services={"S1": svc})


def test_readiness_all_available(readiness_data):
    res = evaluate("S1", {"D1": "available", "A1": "available"})
    assert res.ready is True
    assert "You're Ready to Apply." in res.message


def test_readiness_missing_required(readiness_data):
    res = evaluate("S1", {"D1": "missing", "A1": "available"})
    assert res.ready is False
    assert len(res.blockers) == 1
    assert res.blockers[0]["document_id"] == "D1"
    assert res.blockers[0]["obtain_first"][0]["document_id"] == "D3"
    assert res.blockers[0]["obtain_first"][1]["document_id"] == "D2"
    assert res.obtain_plan == ["D3", "D2", "D1"]


def test_readiness_unmarked(readiness_data):
    res = evaluate("S1", {"A1": "available"})
    assert res.ready is False
    assert len(res.unverified) == 1
    assert res.unverified[0]["document_id"] == "D1"


def test_readiness_any_of(readiness_data):
    res1 = evaluate("S1", {"D1": "available", "A1": "available", "A2": "missing"})
    assert res1.ready is True

    res2 = evaluate("S1", {"D1": "available", "A1": "missing", "A2": "missing"})
    assert res2.ready is False
    assert len(res2.blockers) == 1
    assert res2.blockers[0]["group"] == "grp1"


def test_readiness_parent_available_prereq_missing(readiness_data):
    res = evaluate("S1", {"D1": "available", "D2": "missing", "A1": "available"})
    assert res.ready is True  # Prerequisite irrelevant if parent is available


def test_readiness_optional_missing(readiness_data):
    res = evaluate("S1", {"D1": "available", "O1": "missing", "A1": "available"})
    assert res.ready is True


def test_readiness_empty(readiness_data):
    assert evaluate("S1", {}).ready is False


def test_readiness_unknown_ignored(readiness_data):
    res = evaluate("S1", {"UNKNOWN": "available"})
    assert "UNKNOWN" in res.ignored_ids
