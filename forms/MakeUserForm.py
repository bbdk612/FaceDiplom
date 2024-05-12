from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo

class MakeUserForm(Form):
    fio = StringField("Ф.И.О.", validators=[InputRequired()])
    login = StringField("Логин", validators=[InputRequired()])
    password = PasswordField("Пароль", validators=[InputRequired(), EqualTo('confirm', message="Пароли должны совпадать")])
    confirm = PasswordField("Подтвердите пароль")
    submit = SubmitField()
