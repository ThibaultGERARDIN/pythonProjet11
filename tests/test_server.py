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
