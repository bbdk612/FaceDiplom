from wtforms import Form, StringField, SubmitField
from wtforms.validators import InputRequired, DataRequired

class UpdateUserForm(Form):
    fio = StringField("Ф.И.О.", validators=[InputRequired()])
    login = StringField("Логин", validators=[DataRequired()])
    password = StringField("Пароль", validators=[DataRequired()]) 
    submit = SubmitField()
