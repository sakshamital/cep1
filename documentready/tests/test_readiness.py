import pytest
from app.models.entities import Document, Service, ServiceRequirement, ApplicationInfo
from app.services.readiness import evaluate
from app.services.repository import reset_repo_for_testing

@pytest.fixture
def mock_data():
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
            ServiceRequirement("any_of", group="grp1", options=["A1", "A2"])
        ],
        ApplicationInfo("", "", [], ""), False, "", None
    )
    reset_repo_for_testing(documents=docs, services={"S1": svc})

def test_readiness_all_available(mock_data):
    res = evaluate("S1", {"D1": "available", "A1": "available"})
    assert res.ready is True
    assert "You're Ready to Apply." in res.message

def test_readiness_missing_required(mock_data):
    res = evaluate("S1", {"D1": "missing", "A1": "available"})
    assert res.ready is False
    assert len(res.blockers) == 1
    assert res.blockers[0]["document_id"] == "D1"
    assert res.blockers[0]["obtain_first"][0]["document_id"] == "D3"
    assert res.blockers[0]["obtain_first"][1]["document_id"] == "D2"
    assert res.obtain_plan == ["D3", "D2", "D1"]

def test_readiness_unmarked(mock_data):
    res = evaluate("S1", {"A1": "available"})
    assert res.ready is False
    assert len(res.unverified) == 1
    assert res.unverified[0]["document_id"] == "D1"

def test_readiness_any_of(mock_data):
    # One available
    res1 = evaluate("S1", {"D1": "available", "A1": "available", "A2": "missing"})
    assert res1.ready is True
    
    # All missing -> blocker
    res2 = evaluate("S1", {"D1": "available", "A1": "missing", "A2": "missing"})
    assert res2.ready is False
    assert len(res2.blockers) == 1
    assert res2.blockers[0]["group"] == "grp1"

def test_readiness_parent_available_prereq_missing(mock_data):
    res = evaluate("S1", {"D1": "available", "D2": "missing", "A1": "available"})
    assert res.ready is True # Prerequisite doesn't matter if parent is available

def test_readiness_optional_missing(mock_data):
    res = evaluate("S1", {"D1": "available", "O1": "missing", "A1": "available"})
    assert res.ready is True

def test_readiness_empty(mock_data):
    res = evaluate("S1", {})
    assert res.ready is False
    
def test_readiness_unknown_ignored(mock_data):
    res = evaluate("S1", {"UNKNOWN": "available"})
    assert "UNKNOWN" in res.ignored_ids
