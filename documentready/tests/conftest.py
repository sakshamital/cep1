import pytest
from app import create_app
from app.services.repository import reset_repo_for_testing

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_repo():
    reset_repo_for_testing({}, {}, {}, {})
    yield
    reset_repo_for_testing({}, {}, {}, {})
