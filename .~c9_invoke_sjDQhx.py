import os
import operator
import random
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, Markup
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd

# font aramanth
# export API_KEY=pk_ad361175b32244dba6e634edd3714f80
# CREATE TABLE 'matches' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 'wrestlerOne' INTEGER NOT NULL, 'wrestlerTwo' INTEGER NOT NULL, 'winnerId' INTEGER, 'loserId' INTEGER, 'date' DATE NOT NULL, FOREIGN KEY(wrestlerOne) REFERENCES wrestlers(id), FOREIGN KEY(wrestlerTwo) REFERENCES wrestlers(id), FOREIGN KEY(winnerId) REFERENCES wrestlers(id), FOREIGN KEY(loserId) REFERENCES wrestlers(id));
# CREATE TABLE 'wrestlers' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 'userid' INTEGER NOT NULL, 'name' TEXT NOT NULL, 'specialMove' TEXT NOT NULL, 'strength' NUMERIC NOT NULL, 'speed' NUMERIC NOT NULL, 'health' NUMERIC NOT NULL, 'finishingMove' TEXT NOT NULL, 'wins' NUMERIC NOT NULL, 'losses' NUMERIC NOT NULL, 'level' NUMERIC NOT NULL, 'isChampion' BOOLEAN NOT NULL, 'deleted' BOOLEAN NOT NULL, FOREIGN KEY(userid) REFERENCES users(id));
# CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL, 'points' NUMERIC NOT NULL DEFAULT 10000.00 );
# Configure application
app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# app.config["SESSION_FILE_DIR"] = mkdtemp()
Session(app)
#app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///wrestling.db")

# heroku db configuration
# db = SQL("postgres://qlcblfutafjovf:0ae0b6fbd8c878a4b9acd493afa8e600f7dda34a22efa58e2d75d0a9d0351ef9@ec2-54-221-212-126.compute-1.amazonaws.com:5432/d46a5n1cr97lsj")

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
date_string = now.strftime("%m/%d/%Y %H:%M:%S")

# date for leaderboard
dateForBoard = now.strftime("%m/%d/%Y %H:%M")

# current leader
currentLeader = ''

# user tips
tips = ["Each time a wrestler increases by one level their health points grow by 10",
        "The level bonus magnifies the impact of an attack greatly. Be careful challenging a wrestler with a level much higher than yours",
        "Due to his size, Yokuzuna has a custom strength level, and Almost no speed",
        "Your goal: Become the World Champion!!",
        "A fan was accidentally set on fire during a match at the ECW Arena in 1995"
        "Regardless of the outcome, a match will earn you 25 points",
        "Actor David Arqutte won the WCW World Championship in the year 2000",
        "The longest reigning champion in WWE history is Bruno Sammartino, who held the title from May 17, 1963 to January 18, 1971, for a total of 2,803 days",
        "In a battle in 1983 against The Iron Sheik, Hulk Hogan managed to be the first person to ever get out of the dreaded 'camel clutch,' the Sheik's finishing move. He followed that up with his trademark leg drop, winning his first ever WWF Championship title."]


@app.route("/")
@login_required
def index():
    userid = session["user_id"]
    message = Markup("Looks like you don't have and wrestlers, why not <a href='/create'>create </a>one?")
    # get wrestlers for current user
    wrestlers = db.execute("SELECT * FROM wrestlers WHERE userid = :userid and deleted = 0", userid=userid)
    if not wrestlers:
        return render_template("index.html", wrestlers=wrestlers, message=message, tips=random.choice(tips))
    else:
        return render_template("index.html", wrestlers=wrestlers, message="", tips=random.choice(tips))


@app.route("/users", methods=["GET"])
@login_required
def users():
    userRows = db.execute("SELECT * FROM users;")
    userRowsObject = []
    for user in userRows:
        totalWrestlers = db.execute("SELECT COUNT(*) FROM wrestlers WHERE userid = :userid and deleted = 0", userid=user['id'])
        topWrestler = db.execute(
            "SELECT MAX(wins) AS totalWins, name FROM wrestlers WHERE userid = :userid and deleted = 0", userid=user['id'])
        totalWins = db.execute(
            "SELECT MAX(wins) AS totalWins FROM wrestlers WHERE userid = :userid and deleted = 0", userid=user['id'])
        totalLosses = db.execute(
            "SELECT MAX(losses) AS totalLosses FROM wrestlers WHERE userid = :userid and deleted = 0", userid=user['id'])
        userItem = {
            "username": user['username'],
            "points": user['points'],
            "totalWrestlers": totalWrestlers[0]['COUNT(*)'],
            "topWrestler": topWrestler[0]['name'],
            "totalWins": totalWins[0]['totalWins'],
            "totalLosses": totalLosses[0]['totalLosses']
        }
        userRowsObject.append(userItem)
        userRowsObject.sort(key=operator.itemgetter('points'), reverse=True)
    return render_template("users.html", tips=random.choice(tips), now=dateForBoard, userRowsObject=userRowsObject)


@app.route("/history")
@login_required
def history():
    userId = session["user_id"]
    matchRows = db.execute("SELECT * FROM matches ORDER BY date DESC LIMIT 25;")
    matchHistory = []
    for match in matchRows:
        winnerName = db.execute("SELECT name FROM wrestlers WHERE id = :id", id=match["winnerId"])
        loserName = db.execute("SELECT name FROM wrestlers WHERE id = :id", id=match["loserId"])
        matchItem = {
            "winnerName": winnerName[0]['name'],
            "loserName": loserName[0]['name'],
            "date": match["date"]
        }
        matchHistory.append(matchItem)
        matchHistory.sort(key=operator.itemgetter('date'), reverse=True)

    return render_template("history.html", matchHistory=matchHistory, tips=random.choice(tips))


@app.route("/leaderBoard")
@login_required
def leaderBoard():
    userid = session["user_id"]
    currentLeader = ""
    # get all wrestlers
    wrestlers = db.execute("SELECT * FROM wrestlers WHERE deleted = 0")
    leaderBoardRows = []
    for wrestler in wrestlers:
        leaderWrestler = {
            "rank": 0,
            "name": wrestler["name"],
            "level": wrestler["level"],
            "wins": wrestler["wins"],
            "losses": wrestler["losses"]
        }
        leaderBoardRows.append(leaderWrestler)
    leaderBoardRows.sort(key=operator.itemgetter('wins'), reverse=True)
    # sets the rank of each wrestler
    for wrestler in leaderBoardRows:
        wrestler['rank'] = (leaderBoardRows.index(wrestler) + 1)
        if (wrestler["rank"] == 1):
            currentLeader = wrestler["name"]

    return render_template("leaderboard.html", leaderBoardRows=leaderBoardRows, now=dateForBoard, currentLeader=currentLeader, tips=random.choice(tips))


def sortBy(element):
    return element["totalSumTotal"]


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", tips=random.choice(tips))


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/create", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("create.html", tips=random.choice(tips))
    else:
        userid = session["user_id"]
        name = request.form.get("name")
        specialMove = request.form.get("specialMove")
        strength = request.form.get("strength")
        speed = request.form.get("speed")
        finishingMove = request.form.get("finishingMove")
        level = 1
        # Query database for existing wrestler
        rows = db.execute("SELECT * FROM wrestlers WHERE name = :name",
                          name=request.form.get("name"))

        # Ensure wrestler does not already exist
        if len(rows) > 0:
            return apology("wrestler already exists", 403)

        # create a wrestler
        db.execute("INSERT INTO wrestlers (userid, name, specialMove, strength, speed, health, finishingMove, wins, losses, level, isChampion, deleted)VALUES (:userid, :name, :specialMove, :strength, :speed, :health, :finishingMove, :wins, :losses, :level, :isChampion, :deleted)",
                   userid=userid, name=name, specialMove=specialMove, strength=strength, speed=speed, health=100, finishingMove=finishingMove, wins=0, losses=0, level=level, isChampion=False, deleted=False)
    return redirect("/")


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    id = [request.form['entry_id']]
    deleted = True
    # delete a wrestler
    db.execute("UPDATE wrestlers SET deleted = :deleted WHERE id = :id", deleted=deleted, id=id)
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", tips=random.choice(tips))
    else:
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username does not already exist
        if len(rows) > 0:
            return apology("username already exists", 403)
        # Ensure username is not blank
        elif username == '':
            return apology("username cannot be blank", 403)
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)
            # Redirect user to login form
            return redirect("/")


def damageDealer(wrestlerOne, wrestlerTwo):
    wrestlers = [wrestlerOne, wrestlerTwo]
    actionList = ["Punch", "Kick", "Special move", "Finishing move", "Irish whip", "Power bomb"]
    attacker = random.choice(wrestlers)
    damageNums = range(10)
    damagePoints = random.choice(damageNums)
    action = random.choice(actionList)
    if (attacker == wrestlerOne):
        victim = wrestlerTwo
    else:
        victim = wrestlerOne

    detailList = ["",
                  "" + victim[0]["name"] + " is barely moving!",
                  "Stop the FIGHT!",
                  "Fans are going crazy!",
                  "Speed bonus +" + str(attacker[0]["speed"]) + " damage",
                  "Strength bonus +" + str(attacker[0]["strength"]) + " damage",
                  "Level bonus damage multiplied x " + str(attacker[0]["level"]),
                  ""]
    details = random.choice(detailList)
    if (action == "Special move"):
        damagePoints = damagePoints + 1
        details = "Special move bonus +1 damage"
        action = attacker[0]["specialMove"]
    elif (action == "Finishing move"):
        damagePoints = damagePoints + 2
        details = "Finishing move bonus +2 damage"
        action = attacker[0]["finishingMove"]
    elif ("Speed" in details):
        damagePoints = damagePoints + attacker[0]["speed"]
    elif ("Strength" in details):
        damagePoints = damagePoints + attacker[0]["strength"]
    elif ("Level" in details):
        damagePoints = damagePoints * attacker[0]["level"]

    damage = {
        "damagePoints": damagePoints,
        "details": details,
        "attacker": attacker,
        "victim": victim,
        "action": action
    }
    return damage


def levelCalculator(wrestlers):
    for wrestler in wrestlers:
        totalMatches = wrestler[0]["wins"] + wrestler[0]["losses"]
        if totalMatches <= 10:
            db.execute("UPDATE wrestlers SET level = :level WHERE id = :id", level=1, id=wrestler[0]["id"])
            db.execute("UPDATE wrestlers SET health = :health WHERE id = :id", health=100, id=wrestler[0]["id"])
        elif totalMatches <= 20:
            db.execute("UPDATE wrestlers SET level = :level WHERE id = :id", level=2, id=wrestler[0]["id"])
            db.execute("UPDATE wrestlers SET health = :health WHERE id = :id", health=110, id=wrestler[0]["id"])
        elif totalMatches <= 30:
            db.execute("UPDATE wrestlers SET level = :level WHERE id = :id", level=3, id=wrestler[0]["id"])
            db.execute("UPDATE wrestlers SET health = :health WHERE id = :id", health=120, id=wrestler[0]["id"])
        elif totalMatches <= 50:
            db.execute("UPDATE wrestlers SET level = :level WHERE id = :id", level=4, id=wrestler[0]["id"])
            db.execute("UPDATE wrestlers SET health = :health WHERE id = :id", health=130, id=wrestler[0]["id"])
        elif totalMatches <= 75:
            db.execute("UPDATE wrestlers SET level = :level WHERE id = :id", level=5, id=wrestler[0]["id"])
            db.execute("UPDATE wrestlers SET health = :health WHERE id = :id", health=140, id=wrestler[0]["id"])
        elif totalMatches <= 100:
            db.execute("UPDATE wrestlers SET level = :level WHERE id = :id", level=6, id=wrestler[0]["id"])
            db.execute("UPDATE wrestlers SET health = :health WHERE id = :id", health=150, id=wrestler[0]["id"])
        elif totalMatches <= 150:
            db.execute("UPDATE wrestlers SET level = :level WHERE id = :id", level=7, id=wrestler[0]["id"])
            db.execute("UPDATE wrestlers SET health = :health WHERE id = :id", health=160, id=wrestler[0]["id"])
        else:
            db.execute("UPDATE wrestlers SET level = :level WHERE id = :id", level=8, id=wrestler[0]["id"])
            db.execute("UPDATE wrestlers SET health = :health WHERE id = :id", health=170, id=wrestler[0]["id"])


@app.route("/match", methods=["GET", "POST"])
@login_required
def match():
    userid = session["user_id"]
    outcome = ""
    overallResults = ""
    # get wrestlers for current user
    myWrestlers = db.execute("SELECT * FROM wrestlers WHERE userid = :userid and deleted = 0", userid=userid)
    # get computer generated wretlers
    compWrestlers = db.execute("SELECT * FROM wrestlers WHERE deleted = 0")
    random.shuffle(compWrestlers)
    if request.method == "GET":
        if not myWrestlers:
            return render_template("noWrestlersYet.html", tips=random.choice(tips))
        else:
            return render_template("match.html", overallResults=overallResults, myWrestlers=myWrestlers, compWrestlers=compWrestlers, outcome=outcome, tips=random.choice(tips))

    else:
        wrestlerOne = db.execute("SELECT * FROM wrestlers WHERE id = :wrestlerOne and deleted = 0",
                                 wrestlerOne=request.form.get("wrestlerOne"))
        wrestlerTwo = db.execute("SELECT * FROM wrestlers WHERE id = :wrestlerTwo and deleted = 0",
                                 wrestlerTwo=request.form.get("wrestlerTwo"))
        wrestlers = [wrestlerOne, wrestlerTwo]
        matchEvents = []
        healthCounterOne = wrestlerOne[0]["health"]
        healthCounterTwo = wrestlerOne[0]["health"]
        finalBlow = ""
        finalHealth = 0
        totalMoves = 0
        wrestlerOneMovesCounter = 0
        wrestlerTwoMovesCounter = 0
        completed = False
        winner = ""
        loser = ""
        while completed == False:
            eventDamage = damageDealer(wrestlerOne, wrestlerTwo)
            if eventDamage["victim"] == wrestlerOne:
                healthCounterOne = healthCounterOne - eventDamage["damagePoints"]
                wrestlerTwoMovesCounter = wrestlerTwoMovesCounter + 1
            else:
                healthCounterTwo = healthCounterTwo - eventDamage["damagePoints"]
                wrestlerOneMovesCounter = wrestlerOneMovesCounter + 1
            event = {
                "wrestlerOne": wrestlerOne[0]["name"],
                "wrestlerTwo": wrestlerTwo[0]["name"],
                "wrestlerOneHealth": healthCounterOne,
                "wrestlerTwoHealth": healthCounterTwo,
                "attacker": eventDamage["attacker"][0]["name"],
                "victim": eventDamage["victim"][0]["name"],
                "action": eventDamage["action"],
                "damage": eventDamage["damagePoints"],
                "bonus": eventDamage["details"]
            }
            matchEvents.append(event)

            if healthCounterOne <= 0:
                winner = wrestlerTwo
                loser = wrestlerOne
                matchEvents.reverse()
                finalBlow = eventDamage["action"]
                finalHealth = healthCounterTwo
                totalMoves = wrestlerTwoMovesCounter
                completed = True
            elif healthCounterTwo <= 0:
                winner = wrestlerOne
                loser = wrestlerTwo
                matchEvents.reverse()
                finalBlow = eventDamage["action"]
                finalHealth = healthCounterOne
                totalMoves = wrestlerOneMovesCounter
                completed = True

        overallResults = {
            "winnerName": winner[0]["name"],
            "winnerId": winner[0]["id"],
            "loserName": loser[0]["name"],
            "loserId": loser[0]["id"],
            "date": date_string,
            "finalHealth": finalHealth,
            "finalBlow": finalBlow,
            "totalMoves": totalMoves
        }
        # insert a row into matches table
        db.execute("INSERT INTO matches (wrestlerOne, wrestlerTwo, winnerId, loserId, date) VALUES (:wrestlerOne, :wrestlerTwo, :winnerId, :loserId, :date)",
                   wrestlerOne=wrestlerOne[0]["id"], wrestlerTwo=wrestlerTwo[0]["id"], winnerId=overallResults["winnerId"], loserId=overallResults["loserId"], date=date_string)

        # update the wrestlers win/loss/points records
        db.execute("UPDATE wrestlers SET wins = wins + 1 WHERE id = :id", id=overallResults["winnerId"])
        db.execute("UPDATE wrestlers SET losses = losses + 1 WHERE id = :id", id=overallResults["loserId"])
        db.execute("UPDATE users SET points = points + 25 WHERE id = :id", id=userid)

        # level up the wrestlers
        levelCalculator(wrestlers)
        outcome = Markup("<span class='winner-winner'>" +
                         overallResults["winnerName"] + " wins !!<img class='logo' src='/static/images/trophy.JPG'></span>")
        return render_template("match.html", overallResults=overallResults, myWrestlers=myWrestlers, matchEvents=matchEvents, compWrestlers=compWrestlers, tips=random.choice(tips), outcome=outcome)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
