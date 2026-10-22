import pytest
from app.models.entities import Document, Service, ApplicationInfo
from app.services.search import search
from app.services.repository import reset_repo_for_testing

def test_search():
    docs = {
        "D1": Document("D1", "Aadhaar Card", ["aadhar", "uid"], "other", "", "", [], None, False, "", None)
    }
    svcs = {
        "S1": Service("S1", "Caste Validity Certificate", ["cvc"], "scheme", "", "", [], [], ApplicationInfo("", "", [], ""), False, "", None)
    }
    reset_repo_for_testing(documents=docs, services=svcs, synonyms={"aadhar": ["aadhaar"]})
    
    # Exact
    hits = search("Caste Validity Certificate")
    assert len(hits) == 1
    assert hits[0].id == "S1"
    
    # Alias
    hits = search("cvc")
    assert len(hits) == 1
    assert hits[0].id == "S1"
    
    # Synonym
    hits = search("aadhar")
    assert len(hits) == 1
    assert hits[0].id == "D1"
    
    # Typo
    hits = search("casst validty")
    assert len(hits) == 1
    assert hits[0].id == "S1"
    
    # Too short
    assert len(search("a")) == 0
