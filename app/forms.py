from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    user_email = EmailField('Email', [DataRequired()])
    user_password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Input your name', [DataRequired()])
    user_email = EmailField('Input your email', [DataRequired()])
    password = PasswordField('Input your password', [DataRequired()])
    password_validate = PasswordField('Repeat your password', [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    @staticmethod
    def validate_exist_user_name(username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('User with the same name already exists')

    @staticmethod
    def validate_user_email_exist(email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('This email already exist')


class CreatePostForm(FlaskForm):
    title = StringField('Title for your post', [DataRequired()])
    post_content = TextAreaField()
    submit = SubmitField('Create post')

