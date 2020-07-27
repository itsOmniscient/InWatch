from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=15, message=None)])
    email = StringField('Email', validators=[DataRequired(), Length(min=15, max=40), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[EqualTo('confirm', message="Password doesn't match!")])
    submit = SubmitField('Register')

class LoginForm():
    email = StringField('Email', validators=[DataRequired(), Length(min=15, max=40), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    button = BooleanField('Remember Me')
    submit = SubmitField('Login')
