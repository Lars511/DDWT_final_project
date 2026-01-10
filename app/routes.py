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

from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import db, app
from app.forms import LoginForm, SignUpForm
from app.models import Users
import sqlalchemy as sa
from urllib.parse import urlsplit

@app.route('/', methods=['GET'])
@app.route('/index')
#@login_required
def index():
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(Users).where(Users.username ==
        form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # Make sure the user is redirected if the link is not valid or authorised
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sign up succesful! You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/activities")
#@login_required
def activities():
    return render_template("activities.html")


@app.route("/activities/create")
#@login_required
def create_activity():
    return render_template("create_activity.html")


@app.route("/categories")
#@login_required
def categories():
    return render_template("categories.html")


@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == '__main__':
    app.run(debug=True)