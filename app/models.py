"""
Setting up the classes for users, activities and the api
"""
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app import db
from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import date

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = db.paginate(query, page=page, per_page=per_page,
                                error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class Users(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    birthday = db.Column(db.Date, nullable=True)
    bio = db.Column(db.String(256))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    password_hash = db.Column(db.String(128), nullable=False)

    """
    For creation of the API token
    token: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(32), index=True, unique=True)
    token_expiration: so.Mapped[Optional[datetime]]
    """

    # Password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def age(self):
        if not self.birthday:
            return None
        today = date.today()

        return today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )
        

# Loading the user
@login.user_loader
def load_user(id):
    return db.session.get(Users, int(id))


class Category(db.Model):
    """Category model for activity types"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationship to activity types
    activity_types = db.relationship('ActivityType', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


class ActivityType(db.Model):
    """Activity type model for specific activity types within categories"""
    __tablename__ = 'activity_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Ensure unique activity type names within each category
    __table_args__ = (
        db.UniqueConstraint('name', 'category_id', name='unique_type_per_category'),
    )

    def __repr__(self):
        return f'<ActivityType {self.name}>'


class Activity(PaginatedAPIMixin, db.Model):
    """Activity model for social events"""
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255), nullable=False)
    activity_date = db.Column(db.Date, nullable=False)
    activity_time = db.Column(db.Time, nullable=False)
    max_participants = db.Column(db.Integer, default=10)

    # Foreign Keys
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    activity_type_id = db.Column(db.Integer, db.ForeignKey('activity_types.id'), nullable=False)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def to_dict(self):
        data = {
            'Id': self.id,
            'Title': self.title,
            'Description': self.description,
            'Location':self.location,
            'Date': self.activity_date.isoformat() if self.activity_date else None,
            'Time': self.activity_time.isoformat() if self.activity_time else None,
            'Max_participants': self.max_participants,
            'Creator':self.creator_id,
            'Category': self.category_id,
            'Type': self.activity_type_id,
            'Created': self.created_at.isoformat() if self.created_at else None,
            'Updated': self.updated_at.isoformat() if self.updated_at else None
        }
        
        return data
    
    def from_dict(self, data, new_activity=False):
        for field in ['Title', 'Description', 'Location', 'Date', 'Time', 
                      'Max_participants', 'Category', 'Type']:
            if field in data:
                setattr(self, field, data[field])
    
    def __repr__(self):
        return f'<Activity {self.title}>'

    def get_creator(self):
        """Get the creator user object"""
        return Users.query.get(self.creator_id)

    def get_category(self):
        """Get the category object"""
        return Category.query.get(self.category_id)

    def get_activity_type(self):
        """Get the activity type object"""
        return ActivityType.query.get(self.activity_type_id)

    def get_participant_count(self):
        """Get current number of participants"""
        return ActivityParticipant.query.filter_by(activity_id=self.id).count()

    def is_full(self):
        """Check if activity is at capacity"""
        return self.get_participant_count() >= self.max_participants

    def has_user_joined(self, user_id):
        """Check if user has already joined"""
        return ActivityParticipant.query.filter_by(
            activity_id=self.id,
            user_id=user_id
        ).first() is not None


class ActivityParticipant(db.Model):
    """Track which users joined which activities"""
    __tablename__ = 'activity_participants'

    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Ensure a user can only join an activity once
    __table_args__ = (
        db.UniqueConstraint('activity_id', 'user_id', name='unique_activity_user'),
    )

    def __repr__(self):
        return f'<Participant User:{self.user_id} Activity:{self.activity_id}>'

    def get_activity(self):
        """Get the activity object"""
        return Activity.query.get(self.activity_id)

    def get_user(self):
        """Get the user object"""
        return Users.query.get(self.user_id)