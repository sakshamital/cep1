import pytest
from app.services.repository import get_repo

def test_data_integrity():
    repo = get_repo()
    repo.load() # Should not raise exception
    docs = repo.get_all_documents()
    for doc in docs.values():
        if not doc.verified:
            assert doc.source_note != ""
