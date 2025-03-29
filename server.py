import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


def get_competition_from_name(name):
    try:
        competition = [competition for competition in competitions if competition["name"] == name][0]
        return competition
    except IndexError:
        return None


def get_club_from_name(name):
    try:
        club = [club for club in clubs if club["name"] == name][0]
        return club
    except IndexError:
        return None


def check_places(places, club):
    if not places or int(places) < 1:
        return "Places required must be a positive integer"
    if int(places) > int(club["points"]):
        return "Places required exceed club's total points"


def take_places(places, club, competition):
    try:
        competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places
        club["points"] = int(club["points"]) - places
        return True
    except Exception:
        return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = [club for club in clubs if club["email"] == request.form["email"]][0]
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = get_competition_from_name(request.form["competition"])
    club = get_club_from_name(request.form["club"])

    error_message = check_places(request.form["places"], club)
    if error_message:
        flash(error_message)
        return redirect(url_for("book", competition=competition["name"], club=club["name"]))
    places_required = int(request.form["places"])
    if take_places(places_required, club, competition):
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for("book", competition=competition["name"], club=club["name"]))


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
