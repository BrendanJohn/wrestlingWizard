from flask import Flask, flash, jsonify, redirect, render_template, request, session, Markup
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)
SECRET_KEY = "brendan"
# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True