from flask import Flask, flash, jsonify, redirect, render_template, request, session, Markup
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Ensure templates are auto-reloaded


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True