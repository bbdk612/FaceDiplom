from wtforms import Form, StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(Form):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
