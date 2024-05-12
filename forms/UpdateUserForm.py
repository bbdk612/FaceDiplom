from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo

class UpdateUserForm(Form):
    fio = StringField("Ф.И.О.", validators=[InputRequired()])
    submit = SubmitField()
