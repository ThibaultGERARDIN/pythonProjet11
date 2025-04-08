import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

MAX_PER_CLUB = 12


def loadClubs(clubs_json):
    with open(clubs_json) as c:
        listOfClubs = json.load(c)["clubs"]
        for club in listOfClubs:
            club["points"] = int(club["points"])
        return listOfClubs


def loadCompetitions(competitions_json):
    with open(competitions_json) as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        date_format = "%Y-%m-%d %H:%M:%S"
        for competition in listOfCompetitions:
            competition["date"] = datetime.strptime(competition["date"], date_format)
            if competition["date"] < datetime.now():
                competition["is_past"] = True
            else:
                competition["is_past"] = False
        return listOfCompetitions


def create_app(config={}):
    app = Flask(__name__)
    app.config.update(config)
    app.secret_key = "something_special"

    competitions_json = "competitions.json"
    clubs_json = "clubs.json"

    if app.config.get("TESTING_NOCLUBS"):
        competitions_json = "tests/test_dataset_noclubs.json"
        clubs_json = "tests/test_dataset_noclubs.json"
    elif app.config.get("TESTING"):
        competitions_json = "tests/test_dataset.json"
        clubs_json = "tests/test_dataset.json"

    competitions = loadCompetitions(competitions_json)
    clubs = loadClubs(clubs_json)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/showSummary", methods=["POST"])
    def showSummary():
        email = request.form["email"]
        try:
            club = [club for club in clubs if club["email"] == email][0]
        except IndexError:
            flash("Sorry, that email wasn't found.")
            return redirect(url_for("index"))
        return render_template("welcome.html", club=club, competitions=competitions)

    @app.route("/book/<competition>/<club>")
    def book(competition, club):
        try:
            foundClub = [c for c in clubs if c["name"] == club][0]
        except IndexError:
            flash("Something went wrong, try again.")
            return bad_request()
        try:
            foundCompetition = [c for c in competitions if c["name"] == competition][0]
        except IndexError:
            flash("Something went wrong, try again.")
            return bad_request()

        club_places = int(foundClub["points"])
        if club_places == 0:
            flash("Sorry you don't have any points left.")
            return bad_request()

        return render_template("booking.html", club=foundClub, competition=foundCompetition)

    @app.route("/purchasePlaces", methods=["POST"])
    def purchasePlaces():
        competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        places_required = int(request.form["places"])
        places_remaining = int(competition["numberOfPlaces"])
        club_places = int(club["points"])
        if competition["is_past"] is True:
            flash("Cannot book past competitions.")
            return bad_request()
        if club_places == 0:
            flash("Sorry you don't have any points left.")
            return bad_request()
        elif places_required > MAX_PER_CLUB:
            flash(f"Cannot book - Trying to book more than maximum allowed ({MAX_PER_CLUB})")
            return render_template("booking.html", club=club, competition=competition)
        elif places_required > club_places:
            flash(f"Cannot book - trying to book more than what you have ({club_places} places).")
            return render_template("booking.html", club=club, competition=competition)
        elif places_required > places_remaining:
            flash(f"Cannot book - trying to book more than what remains ({places_remaining} places).")
            return render_template("booking.html", club=club, competition=competition)
        elif places_required < 0:
            flash(f"Cannot book - trying to book negative places ({places_required} places).")
            return render_template("booking.html", club=club, competition=competition)
        elif places_required == 0:
            flash("You booked 0 places, try again !")
            return render_template("welcome.html", club=club, competitions=competitions)
        else:
            flash(f"Great, succesfully booked {places_required} place(s)!")
            club["points"] = club_places - places_required
            competition["numberOfPlaces"] = places_remaining - places_required
            return render_template("welcome.html", club=club, competitions=competitions)

    @app.route("/pointsBoard")
    def pointsBoard():
        return render_template("points_board.html", clubs=clubs)

    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))

    @app.errorhandler(400)
    def bad_request():
        return render_template("exception.html"), 400

    return app
