from app.api import bp
from app.models import Activity, Category, Users, ActivityType
from app import db
import sqlalchemy as sa
from flask import request, url_for, abort
from app.api.errors import bad_request
from app.api.auth import token_auth
from datetime import datetime

@bp.route('activities/<int:id>',  methods=['GET'])
@token_auth.login_required
def get_activity(id):
    return db.get_or_404(Activity, id).to_dict()

@bp.route('/activities', methods=['GET'])
@token_auth.login_required
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
@bp.route('categories/<int:id>')
@token_auth.login_required
def get_category(id):
    """Creates a list with all activities of that category, such as Sport and Fitness."""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Activity.to_collection_dict(sa.select(Activity).where(Activity.category_id == id), page, per_page,
                                   'api.get_category', id=id)

@bp.route('categories/activity_type/<type>', methods=['GET'])
@token_auth.login_required
def get_activity_type(type):
    """Creates a list with all activities of that type, such as Tennis.
    The list of all activities is in populate_activities.py. Keep in mind
    that these names are case sensitive"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Activity.to_collection_dict(sa.select(Activity).join(ActivityType).where(ActivityType.name == type), page, per_page,
                                   'api.get_activity_type', type=type)

@bp.route('/profile/activities_created/<name>', methods=['GET'])
@token_auth.login_required
def get_created_activities(name):
    """Creates a list of all activities created by that user"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Activity.to_collection_dict(sa.select(Activity).join(Users).where(Users.username == name), page, per_page,
                                   'api.get_created_activities', name=name)

"""make one here to create and edit activity. Then write a script to prove it works"""

@bp.route('/create_activities', methods=['POST'])
@token_auth.login_required
def create_activity():
    """Creates a new activity through the API"""
    creator = token_auth.current_user()
    data = request.get_json()
    data['creator_id'] = creator.id

    if not data:
        return bad_request('error: Message body must be JSON')
    if 'title' not in data or 'location' not in data or 'max_participants' not in data:
        return bad_request('must include Title, location and max_participants')
    if 'activity_time' not in data or 'activity_date' not in data:
        return bad_request('must include activity_time and activity_date (DD/MM/YYYY)')
    if 'category_id' not in data:
        return bad_request('Must include category_id. Full list is in populate_activities.py')
    if 'activity_type_id' not in data:
        return bad_request('Must include activity_type_id. Full list is in populate_activities.py')
    if 'activity_date' and 'activity_time' in data:
        data['activity_date'] = datetime.strptime(data['activity_date'], '%d/%m/%Y')
        data['activity_time'] = datetime.strptime(data['activity_time'], '%H:%M').time()
    
    
    activity = Activity()
    activity.from_dict(data, new_activity=True)
    db.session.add(activity)
    db.session.commit()
    return activity.to_dict(), 201, {'Location': url_for('api.create_activity', id=activity.id)}

@bp.route('/edit_activity/<int:id>', methods=['PUT'])
@token_auth.login_required
def edit_activity(id):
    """
    Updates an activity through the API with the activity id. 
    """
    user = db.get_or_404(Activity, id)
    data = request.get_json()
    user.from_dict(data, new_activity=False)
    db.session.commit()
    return user.to_dict()

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

@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    """
    Updates a user profile through the API using user id. User id can be found through
    api/profile/username
    """
    user = db.get_or_404(Users, id)
    data = request.get_json()
    if 'username' in data and data['username'] != user.username and \
        db.session.scalar(sa.select(Users).where(
            Users.username == data['username'])):
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
        db.session.scalar(sa.select(Users).where(
            Users.email == data['email'])):
        return bad_request('please use a different email address')
    user.from_dict(data, signup=False)
    db.session.commit()
    return user.to_dict()

@bp.route('/profiles')
@token_auth.login_required
def get_profiles():
    """Creates a list of all profiles"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Users.to_collection_dict(sa.select(Users), page, per_page,
                                   'api.get_profiles')

@bp.route('/profile/<username>')
@token_auth.login_required
def get_profile(username):
    """Pulls a specific profile"""
    user = db.session.scalar(
        sa.select(Users).where(Users.username == username)
    )
    if user is None:
        abort(404, description="User not found")
    return user.to_dict()