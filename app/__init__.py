"""
Setup for Flask
"""
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
import os

load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Getting the secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(
    basedir, 'instance/movies.db')
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