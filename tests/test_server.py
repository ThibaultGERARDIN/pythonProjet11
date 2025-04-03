class TestBooking:

    def test_valid_booking_future_competitions(self, client, test_club, future_competition):
        places = 1
        response = client.post(
            "/purchasePlaces",
            data={"competition": future_competition["name"], "club": test_club["name"], "places": places},
        )
        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data

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
