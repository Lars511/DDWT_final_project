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

@bp.route('/profile/<name>', methods=['GET'])
def get_user(name):
    pass

