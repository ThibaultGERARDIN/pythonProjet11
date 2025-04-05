class TestIntegrationClass:

    def test_should_access_home_and_login_logout(self, client, test_club):
        """Tests login and logout"""
        assert client.get("/").status_code == 200

        # Login
        data = {"email": test_club["email"]}
        response = client.post("/showSummary", data=data)
        assert response.status_code == 200

        # Logout
        logout_page = client.get("/logout")
        assert logout_page.status_code == 302

    def test_complete_booking_scenario(self, client, test_club, future_competition):

        assert client.get("/").status_code == 200

        # Login
        data = {"email": test_club["email"]}
        response = client.post("/showSummary", data=data)
        assert response.status_code == 200

        # Reach booking page
        booking_page = client.get(f'/book/{future_competition["name"]}/{test_club["name"]}')
        assert booking_page.status_code == 200

        # Book one entry
        places = 1
        initial_club_points = int(test_club["points"])
        initial_competition_places = int(future_competition["numberOfPlaces"])
        data = {"club": test_club["name"], "competition": future_competition["name"], "places": places}
        reservation = client.post("/purchasePlaces", data=data)
        assert reservation.status_code == 200
        remaining_points = initial_club_points - places
        remaining_places = initial_competition_places - places
        assert f"Points available: {remaining_points}" in reservation.data.decode()
        assert f"Number of Places: {remaining_places}" in reservation.data.decode()

        # Logout
        logout_page = client.get("/logout")
        assert logout_page.status_code == 302

        # Check club points on pointboard
        points_board = client.post("/pointsBoard", data=data)
        assert f'{test_club["name"]}' in points_board.data.decode()
