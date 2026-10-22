import pytest
from app.models.entities import Service, ServiceRequirement, ApplicationInfo
from app.services.requirements import resolve_requirements, RequirementsError
from app.services.repository import reset_repo_for_testing

def test_resolve_requirements_conditional():
    svc = Service(
        id="S1", name="S1", aliases=[], type="scheme", department="", description="",
        applicant_categories=["student", "employee"],
        requirements=[
            ServiceRequirement("required", document_id="doc1"),
            ServiceRequirement("conditional", document_id="doc2", when={"applicant_category": ["student"]})
        ],
        application_info=ApplicationInfo("", "", [], ""), verified=False, source_note="", last_reviewed=None
    )
    reset_repo_for_testing(services={"S1": svc})
    
    # Matching category
    res1 = resolve_requirements("S1", "student")
    assert len(res1.items) == 2
    assert res1.items[1]["document_id"] == "doc2"
    assert res1.items[1]["necessity"] == "required"
    
    # Non-matching category
    res2 = resolve_requirements("S1", "employee")
    assert len(res2.items) == 1
    assert "doc2" in res2.hidden_conditional
    
def test_resolve_requirements_invalid_category():
    svc = Service(
        id="S1", name="S1", aliases=[], type="scheme", department="", description="",
        applicant_categories=["student", "employee"],
        requirements=[],
        application_info=ApplicationInfo("", "", [], ""), verified=False, source_note="", last_reviewed=None
    )
    reset_repo_for_testing(services={"S1": svc})
    
    with pytest.raises(RequirementsError):
        resolve_requirements("S1", "alien")
