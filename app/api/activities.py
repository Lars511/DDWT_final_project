from app.api import bp
from app.models import Activity, Category, Users, ActivityType
from app import db
import sqlalchemy as sa
from flask import request, url_for
from app.api.errors import bad_request
from app.api.auth import token_auth

@token_auth.login_required
@bp.route('activities/<int:id>',  methods=['GET'])
def get_activity(id):
    return db.get_or_404(Activity, id).to_dict()

@token_auth.login_required
@bp.route('/activities', methods=['GET'])
def get_activities():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Activity.to_collection_dict(sa.select(Activity), page, per_page,
                                   'api.get_activities')

""" 
Categories are numbered in the following way:
1 = sport and fitness
2 = study and work 
3 = casual and social
4 = outdoor and leisure
5 = hobbies and entertainment
6 = university and student life
7 = other/custom
"""
@token_auth.login_required
@bp.route('categories/<int:id>')
def get_category(id):
    """Creates a list with all activities of that category, such as Sport and Fitness"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Activity.to_collection_dict(sa.select(Activity).where(Activity.category_id == id), page, per_page,
                                   'api.get_category', id=id)

# Keep in mind that activity type names are case sensitive
@token_auth.login_required
@bp.route('categories/activity_type/<type>')
def get_activity_type(type):
    """Creates a list with all activities of that type, such as tennis"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Activity.to_collection_dict(sa.select(Activity).join(ActivityType).where(ActivityType.name == type), page, per_page,
                                   'api.get_activity_type', type=type)

@token_auth.login_required
@bp.route('/profile/activities_created/<name>', methods=['GET'])
def get_created_activities(name):
    """Creates a list of all activities created by that user"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Activity.to_collection_dict(sa.select(Activity).join(Users).where(Users.username == name), page, per_page,
                                   'api.get_created_activities', name=name)

# Pulling from the Users table

@bp.route('/users', methods=['POST'])
def create_user():
    """Creates a new user through the API"""
    data = request.get_json()
    if not data:
        return bad_request('error: Message body must be JSON')
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if db.session.scalar(sa.select(Users).where(
            Users.username == data['username'])):
        return bad_request('please use a different username')
    if db.session.scalar(sa.select(Users).where(
            Users.email == data['email'])):
        return bad_request('please use a different email address')
    user = Users()
    user.from_dict(data, signup=True)
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), 201, {'Location': url_for('api.create_user',
                                                     id=user.id)}

""" 
Make one for editing user profile
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis
"""

@token_auth.login_required
@bp.route('/profile')
def get_profiles():
    """Creates a list of all profiles"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Users.to_collection_dict(sa.select(Users), page, per_page,
                                   'api.get_profiles')

@token_auth.login_required
@bp.route('/profile/<name>')
def get_profile(name):
    """Pulls a specific profile"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Users.to_collection_dict(sa.select(Users).where(Users.username == name), page, per_page,
                                   'api.get_profile', name=name)