from server import loadClubs


class TestPointsBoard:

    def test_should_access_home(self, client):
        assert client.get("/").status_code == 200

    def test_board_correctly_displays_clubs(self, client):
        clubs = loadClubs("tests/test_dataset.json")

        response = client.post("/pointsBoard")
        assert response.status_code == 200

        data = response.data.decode("utf-8")
        for club in clubs:
            assert club["name"] in data
            assert str(club["points"]) in data

    def test_board_correctly_displays_no_clubs(self, client_noclubs):

        response = client_noclubs.post("/pointsBoard")
        assert response.status_code == 200
        data = response.data.decode("utf-8")
        assert "No clubs are registered" in data
