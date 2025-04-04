from server import MAX_PER_CLUB, loadClubs


class TestBooking:

    def test_valid_booking_should_update_points_and_tell_number(self, client, test_club, test_competition):
        places = 1
        initial_club_points = int(test_club["points"])
        initial_places_in_comp = int(test_competition["numberOfPlaces"])
        response = client.post(
            "/purchasePlaces",
            data={"competition": test_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        assert f"Points available: {initial_club_points - places}" in response.data.decode()
        assert f"Great, succesfully booked {places} place(s)" in response.data.decode()
        assert f"Number of Places: {initial_places_in_comp - places}" in response.data.decode()

    def test_shouldnt_book_more_than_max_per_club(self, client, test_club, test_competition):
        places = MAX_PER_CLUB + 1
        response = client.post(
            "/purchasePlaces",
            data={"competition": test_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        error_message = f"Cannot book - Trying to book more than maximum allowed ({MAX_PER_CLUB})"
        assert error_message in response.data.decode("utf-8")

    def test_valid_booking_should_update_points(self, client, test_club, test_competition):
        places = 1
        initial_club_points = int(test_club["points"])
        remainingPlaces = int(test_competition["numberOfPlaces"])
        response = client.post(
            "/purchasePlaces",
            data={"competition": test_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        assert f"Great, succesfully booked {places} place(s)" in response.data.decode()
        assert f"Points available: {initial_club_points-places}" in response.data.decode()
        assert f"Number of Places: {remainingPlaces - places}" in response.data.decode()

    def test_not_enough_points_to_book(self, client, test_club, test_competition):
        places = int(test_club["points"]) + 1
        response = client.post(
            "/purchasePlaces",
            data={"competition": test_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        error_message = f"Cannot book - trying to book more than what you have ({int(test_club["points"])} places)."
        assert error_message in response.data.decode()

    def test_shouldnt_book_more_than_remaining(self, client, test_club, test_competition):
        places = int(test_competition["numberOfPlaces"]) + 1
        response = client.post(
            "/purchasePlaces",
            data={"competition": test_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        error_message = (
            f"Cannot book - trying to book more than what remains ({test_competition["numberOfPlaces"]} places)."
        )
        assert error_message in response.data.decode()

    def test_shouldnt_book_negative_points(self, client, test_club, test_competition):
        places = -1
        response = client.post(
            "/purchasePlaces",
            data={"competition": test_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        error_message = f"Cannot book - trying to book negative places ({places} places)."
        assert error_message in response.data.decode()

    def test_shouldnt_book_zero_points(self, client, test_club, test_competition):
        places = 0
        response = client.post(
            "/purchasePlaces",
            data={"competition": test_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        error_message = "You booked 0 places, try again !"
        assert error_message in response.data.decode()

    def test_should_redirect_when_0_points(self, client, test_competition, zero_point_club):
        competition = test_competition["name"]
        club = zero_point_club["name"]
        response = client.get(f"/book/{competition}/{club}")
        assert response.status_code == 302
        assert response.location == "/"

    def test_valid_booking_future_competitions(self, client, test_club, future_competition):
        places = 1
        response = client.post(
            "/purchasePlaces",
            data={"competition": future_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        assert f"Great, succesfully booked {places} place(s)" in response.data.decode()

    def test_shouldnt_book_past_competitions(self, client, test_club, past_competition):
        places = 1
        response = client.post(
            "/purchasePlaces",
            data={"competition": past_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 400
        assert b"Cannot book past competitions." in response.data

    def test_shouldnt_have_booking_link(self, client, test_club):
        email = test_club["email"]
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 200
        assert b"Competition is passed, you cannot book places anymore." in response.data


class TestAuth:

    def test_should_redirect_known_email(self, client, test_club):
        email = test_club["email"]
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 200

    def test_unknown_email_should_return_error(self, client):
        email = "certainlynotaknownadress@test.fr"
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 302


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
