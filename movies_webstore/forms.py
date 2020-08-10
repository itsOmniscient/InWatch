from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from movies_webstore.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Корисничко име', validators=[DataRequired(), Length(min=4, max=20, message="Минимум 4 а максимум 20 карактери.")])
    email = StringField('E-mail адреса', validators=[DataRequired(), Email(message="Внесете валидна е-mail адреса.")])
    password = PasswordField('Лозинка', validators=[DataRequired(), Length(min=5, max=30, message="Минимум 5 а максимум 30 карактери.")])
    confirm_pass = PasswordField('Внесете ја лозинката повторно', validators=[DataRequired(), EqualTo('password', message="Лозинката не се совпаѓа!")])
    submit = SubmitField('Регистрирај се')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Постоечко корисничко име.')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Постоечка е-mail адреса.')



class LoginForm(FlaskForm):
    email = StringField('E-mail адреса', validators=[DataRequired(), Email()])
    password = PasswordField('Лозинка', validators=[DataRequired()])
    button = BooleanField('Запамти ме')
    submit = SubmitField('Најава')
