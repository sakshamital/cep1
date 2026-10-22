# Testing Strategy

We use `pytest` for all unit and integration testing.

## Running tests
```bash
pytest
```

## Coverage
- **`test_graph.py`**: Ensures cycle detection works and that topological sorting correctly processes shared prerequisites.
- **`test_requirements.py`**: Verifies `conditional` requirements hide or appear based on the category.
- **`test_readiness.py`**: The core test suite. Checks combinations of missing, unmarked, and available items across groups and individual items to ensure `ready` is correctly computed.
- **`test_search.py`**: Asserts fuzzy matching, synonym expansion, and minimum query length behavior.
- **`test_api.py`**: Validates status codes, error shapes, and payload limits.
- **`test_data_integrity.py`**: Runs schema validation and constraint checking on the actual `app/data/` JSON files to catch errors early.
