from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from movies_webstore.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20, message="Minimum 4 and maximum 20 characters.")])
    email = StringField('E-mail address', validators=[DataRequired(), Email(message="Please type valid E-mail address")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=30, message="Minimum 5 and maximum 30 characters.")])
    confirm_pass = PasswordField('Enter password again', validators=[DataRequired(), EqualTo('password', message="Password does not match.")])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username already exists.')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('E-mail address already exists.')

class LoginForm(FlaskForm):
    email = StringField('E-mail address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    button = BooleanField('Remember me')
    submit = SubmitField('Login')
