from flask import Flask, flash, jsonify, redirect, render_template, request, session, Markup
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)
SECRET_KEY = "brendan"
