from app.api import bp
from app.models import Activity, Category
from app import db
import sqlalchemy as sa
from flask import request, url_for

@bp.route('activities/<int:id>',  methods=['GET'])
def get_activity(id):
    return db.get_or_404(Activity, id).to_dict()

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
@bp.route('categories/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Activity.to_collection_dict(sa.select(Activity).where(Activity.category_id == id), page, per_page,
                                   'api.get_category', id=id)

@bp.route('/profile/<name>', methods=['GET'])
def created_activities(name):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    return Activity.to_collection_dict(sa.select(Activity).where(Activity.creator_id == name), page, per_page,
                                   'api.created_activities', name=name)
