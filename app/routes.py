"""
Setting up the routes for the html pages
"""

from flask import render_template, flash, redirect, request, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import db, app
from app.forms import LoginForm, SignUpForm, EditProfile
from app.models import Users, Activity, Category
from app.models import ActivityType
import sqlalchemy as sa
from urllib.parse import urlsplit
from datetime import date, time


# HOME
@app.route('/', methods=['GET'])
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(Users).where(Users.email == form.email.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sign up successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

# PROFILE
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')

# EDIT PROFILE
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile()

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Profile updated succesfully!')
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        form.email.data = current_user.email
        form.bio.data = current_user.bio

    return render_template('edit_profile.html', form=form)

# READ ACTIVITIES
@app.route("/activities")
@login_required
def activities():
    activities = Activity.query.all()
    return render_template("activities.html", activities=activities)


# CREATE ACTIVITY
@app.route("/activities/create", methods=["GET", "POST"])
@login_required
def create_activity():
    categories = Category.query.all()
    activity_types = ActivityType.query.all()

    if request.method == "POST":
        activity = Activity(
            title=request.form["title"],
            description=request.form["description"],
            location=request.form["location"],
            activity_date=date.fromisoformat(request.form["activity_date"]),
            activity_time=time.fromisoformat(request.form["activity_time"]),
            max_participants=int(request.form["max_participants"]),
            category_id=int(request.form["category_id"]),
            activity_type_id=int(request.form["activity_type_id"]),
            creator_id = current_user.id
        )
        db.session.add(activity)
        db.session.commit()
        flash("Activity created successfully!")
        return redirect(url_for("activities"))

    return render_template(
        "create_activity.html",
        categories=categories,
        activity_types=activity_types
    )


# EDIT ACTIVITY (GET + POST)
@app.route("/activities/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_activity(id):
    activity = Activity.query.get_or_404(id)
    categories = Category.query.all()
    activity_types = ActivityType.query.all()

    if request.method == "POST":
        activity.title = request.form["title"]
        activity.description = request.form["description"]
        activity.location = request.form["location"]
        activity.activity_date = date.fromisoformat(request.form["activity_date"])
        activity.activity_time = time.fromisoformat(request.form["activity_time"])
        activity.max_participants = int(request.form["max_participants"])
        activity.category_id = int(request.form["category_id"])
        activity.activity_type_id = int(request.form["activity_type_id"])

        db.session.commit()
        flash("Activity updated successfully!")
        return redirect(url_for("activities"))

    return render_template(
        "edit_activity.html",
        activity=activity,
        categories=categories,
        activity_types=activity_types
    )


# DELETE ACTIVITY
@app.route("/activities/<int:id>/delete", methods=["POST"])
@login_required
def delete_activity(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    flash("Activity deleted.")
    return redirect(url_for("activities"))


# CATEGORIES
@app.route("/categories")
@login_required
def categories():
    return render_template("categories.html")


# API: Get activity types by category
@app.route("/api/activity-types/<int:category_id>")
@login_required
def get_activity_types(category_id):
    """API endpoint to get activity types for a specific category"""
    activity_types = ActivityType.query.filter_by(category_id=category_id).all()
    return jsonify([
        {"id": at.id, "name": at.name}
        for at in activity_types
    ])


# ERROR
@app.route("/error")
def error():
    return render_template("error.html")