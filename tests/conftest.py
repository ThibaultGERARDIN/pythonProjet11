import pytest
from server import create_app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_club():
    return loadClubs("tests/test_dataset.json")[0]


@pytest.fixture
def test_competition():
    return loadCompetitions("tests/test_dataset.json")[0]


@pytest.fixture
def zero_point_club():
    clubs = loadClubs("tests/test_dataset.json")
    return [club for club in clubs if club["points"] == 0][0]


@pytest.fixture
def future_competition():
    competitions = loadCompetitions("tests/test_dataset.json")
    return [comp for comp in competitions if comp["name"] == "Future Competition"][0]


@pytest.fixture
def past_competition():
    competitions = loadCompetitions("tests/test_dataset.json")
    return [comp for comp in competitions if comp["name"] == "Past Competition"][0]
