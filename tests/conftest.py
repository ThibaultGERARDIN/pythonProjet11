import pytest
from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def client_noclubs():
    app = create_app({"TESTING": True, "TESTING_NOCLUBS": True})
    with app.test_client() as client:
        yield client
