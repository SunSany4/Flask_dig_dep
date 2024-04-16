from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, SelectMultipleField, \
    RadioField, TextAreaField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    """прописать форму регистрации нового пользователя
    обязательно должно быть два поля для ввода пароля 'пароль' и 'введите пароль повторно'"""
    pass
