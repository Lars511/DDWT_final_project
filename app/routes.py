"""
Setting up the routes for the html pages
Needs:
- Login
- home
- registering new user
- adding activities
- deleting activities
- logout
- joining activities
"""

from flask import render_template
from app import app

@app.route('/', methods=['GET'])
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/activities")
def activities():
    return render_template("activities.html")


@app.route("/activities/create")
def create_activity():
    return render_template("create_activity.html")


@app.route("/categories")
def categories():
    return render_template("categories.html")


@app.route("/error")
def error():
    return render_template("error.html")