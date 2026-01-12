from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from app import db
from app.models import Users
import sqlalchemy as sa
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(Users).where(
            Users.username == username.data))
        if user is not None:
            raise ValidationError('Username already taken. Please use a different username.')
    
    def validate_email(self, email):
        user = db.session.scalar(sa.select(Users).where(
            Users.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class EditProfile(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = StringField('Bio')
    submit = SubmitField('Save')

    def validate_email(self, email):
        # Checks if the email is not taken and different from the current one
        if email.data != current_user.email:
            user = db.session.scalar(sa.select(Users).where(
                Users.email == email.data))
            if user is not None:
                raise ValidationError('Please use a different email address.')