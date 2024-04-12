from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, SelectMultipleField, \
    RadioField, TextAreaField, FileField
from wtforms.validators import DataRequired


class AnketaForm(FlaskForm):
    graduate_choices = ['Начальное', 'Среднее', 'Высшее', 'Выше высшего']
    job_choices = ['Инженер-исследователь', 'Инженер-строитель', 'Пилот', 'Метеоролог', 'Инженер по жизнеобеспечению',
                   'Инженер по радиационной защите', 'Врач']
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField("Введите адрес вашей электронной почты", validators=[DataRequired()])
    graduate = SelectField('Какое у Вас образование?', choices=graduate_choices)
    job = SelectMultipleField('Какие у Вас есть профессии?', choices=job_choices)
    gender = RadioField('Укажите Пол', choices=['мужской', 'женский'])
    reason = TextAreaField('Почему Вы хотите принять участие в миссии?')
    photo = FileField('Приложите фотографию')
    stay_at_mars = BooleanField('Готовы остаться на Марсе?')
    submit = SubmitField("Войти")
