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
@app.route('/index')
def index():
    return render_template('index.html')