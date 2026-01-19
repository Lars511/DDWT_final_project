"""
Setup for Flask
"""
from flask import Flask, render_template, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
import os
from flask_avatars import Avatars
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
avatars = Avatars(app)

basedir = os.path.abspath(os.path.dirname(__file__))

# Getting the secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(
    basedir, 'instance/activities.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Getting the secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Initializing flask login
login = LoginManager(app)
login.login_view = 'login'

from app import routes
from . import models


from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')