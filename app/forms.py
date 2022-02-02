from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    user_email = EmailField('Email', [DataRequired()])
    user_password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Sign in')
