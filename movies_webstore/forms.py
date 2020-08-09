from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Корисничко име', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('E-mail адреса', validators=[DataRequired(), Email()])
    password = PasswordField('Лозинка', validators=[DataRequired(), Length(min=5, max=25)])
    confirm_pass = PasswordField('Внесете ја лозинката повторно', validators=[DataRequired(), EqualTo('password', message="Password doesn't match!")])
    submit = SubmitField('Регистрирај се')

class LoginForm(FlaskForm):
    email = StringField('E-mail адреса', validators=[DataRequired(), Email()])
    password = PasswordField('Лозинка', validators=[DataRequired()])
    button = BooleanField('Запамти ме')
    submit = SubmitField('Најава')
