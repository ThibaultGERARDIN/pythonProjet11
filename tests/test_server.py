class TestAuth:

    def test_should_access_home(self, client):
        assert client.get("/").status_code == 200

    def test_should_redirect_known_email(self, client, test_club):
        email = test_club["email"]
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 200

    def test_unknown_email_should_return_error(self, client):
        email = "certainlynotaknownadress@test.fr"
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 302
