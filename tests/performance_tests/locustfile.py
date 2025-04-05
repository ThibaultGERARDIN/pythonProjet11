from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("")

    @task
    def pointsBoard(self):
        data = {
            "clubs": [
                {"name": "Test Club", "email": "test@test.fr", "points": "11"},
                {"name": "Zero point club", "email": "zero@mail.fr", "points": "0"},
            ]
        }
        self.client.post("pointsBoard", data=data)

    @task
    def summary(self):
        data = {"email": "kate@shelifts.co.uk"}
        self.client.post("showSummary", data=data)

    @task
    def booking_page(self):
        club = "She Lifts"
        competition = "Fall Classic"
        self.client.get(
            f"book/{competition}/{club}",
        )

    @task
    def purchasePlaces(self):
        club = "She Lifts"
        competition = "Fall Classic"
        data = {"competition": competition, "club": club, "places": 1}
        self.client.post("purchasePlaces", data=data)

    @task
    def logout(self):
        self.client.get("logout")
