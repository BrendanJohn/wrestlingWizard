from flask import Flask, flash, jsonify, redirect, render_template, request, session, Markup
from flask_session import Session
from tempfile import mkdtemp
import os

# font aramanth
# export API_KEY=pk_ad361175b32244dba6e634edd3714f80
# CREATE TABLE 'matches' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 'wrestlerOne' INTEGER NOT NULL, 'wrestlerTwo' INTEGER NOT NULL, 'winnerId' INTEGER, 'loserId' INTEGER, 'date' DATE NOT NULL, FOREIGN KEY(wrestlerOne) REFERENCES wrestlers(id), FOREIGN KEY(wrestlerTwo) REFERENCES wrestlers(id), FOREIGN KEY(winnerId) REFERENCES wrestlers(id), FOREIGN KEY(loserId) REFERENCES wrestlers(id));
# CREATE TABLE 'wrestlers' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 'userid' INTEGER NOT NULL, 'name' TEXT NOT NULL, 'specialMove' TEXT NOT NULL, 'strength' NUMERIC NOT NULL, 'speed' NUMERIC NOT NULL, 'health' NUMERIC NOT NULL, 'finishingMove' TEXT NOT NULL, 'wins' NUMERIC NOT NULL, 'losses' NUMERIC NOT NULL, 'level' NUMERIC NOT NULL, 'isChampion' BOOLEAN NOT NULL, 'deleted' BOOLEAN NOT NULL, FOREIGN KEY(userid) REFERENCES users(id));
# CREATE TABLE IF NOT EXISTS 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL, 'points' NUMERIC NOT NULL DEFAULT 10000.00 );
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.urandom(12)
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure CS50 Library to use SQLite database
db = SQL("postgres://qlcblfutafjovf:0ae0b6fbd8c878a4b9acd493afa8e600f7dda34a22efa58e2d75d0a9d0351ef9@ec2-54-221-212-126.compute-1.amazonaws.com:5432/d46a5n1cr97lsj")