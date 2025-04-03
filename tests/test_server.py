class TestAuth:

    def test_valid_booking_should_update_points(self, client, test_club, test_competition):
        places = 1
        initial_club_points = int(test_club["points"])
        remainingPlaces = int(test_competition["numberOfPlaces"])
        response = client.post(
            "/purchasePlaces",
            data={"competition": test_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data
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
