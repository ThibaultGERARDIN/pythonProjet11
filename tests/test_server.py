from server import MAX_PER_CLUB


class TestBooking:

    def test_valid_booking_should_display_confirmation_message(self, client, test_club, test_competition):
        places = 1
        initial_club_points = int(test_club["points"])
        response = client.post(
            "/purchasePlaces",
            data={"competition": test_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        confirmation_message = "Great-booking complete!"
        assert confirmation_message in response.data.decode("utf-8")
        assert f"Points available: {initial_club_points-places}" in response.data.decode("utf-8")

    def test_shouldnt_book_more_than_max_per_club(self, client, test_club, test_competition):
        places = MAX_PER_CLUB + 1
        response = client.post(
            "/purchasePlaces",
            data={"competition": test_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        error_message = f"Cannot book - Trying to book more than maximum allowed ({MAX_PER_CLUB})"
        assert error_message in response.data.decode("utf-8")
