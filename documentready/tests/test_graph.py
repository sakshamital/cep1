import pytest
from app.models.entities import Document
from app.services.graph import assert_acyclic, CycleError, topological_order, prerequisite_closure

def test_assert_acyclic():
    docs = {
        "A": Document("A", "A", [], "other", "", "", ["B"], None, False, "", None),
        "B": Document("B", "B", [], "other", "", "", ["A"], None, False, "", None)
    }
    with pytest.raises(CycleError, match="A → B → A"):
        assert_acyclic(docs)
        
    docs2 = {
        "A": Document("A", "A", [], "other", "", "", ["B"], None, False, "", None),
        "B": Document("B", "B", [], "other", "", "", [], None, False, "", None)
    }
    assert_acyclic(docs2) # Should not raise

def test_prerequisite_closure():
    docs = {
        "A": Document("A", "A", [], "other", "", "", ["B"], None, False, "", None),
        "B": Document("B", "B", [], "other", "", "", ["C"], None, False, "", None),
        "C": Document("C", "C", [], "other", "", "", [], None, False, "", None)
    }
    assert prerequisite_closure("A", docs) == {"B", "C"}
    
def test_topological_order():
    docs = {
        "A": Document("A", "A", [], "other", "", "", ["B", "C"], None, False, "", None),
        "B": Document("B", "B", [], "other", "", "", ["D"], None, False, "", None),
        "C": Document("C", "C", [], "other", "", "", ["D"], None, False, "", None),
        "D": Document("D", "D", [], "other", "", "", [], None, False, "", None)
    }
    # D is a shared prerequisite
    order = topological_order(["A"], docs)
    assert order == ["D", "B", "C", "A"] or order == ["D", "C", "B", "A"]
    # Shared prerequisite appears once
    assert order.count("D") == 1
