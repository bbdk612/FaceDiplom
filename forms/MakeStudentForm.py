from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired

class MakeStudentForm(Form):
    fio = StringField("Ф.И.О.", validators=[InputRequired()])
    image_url = StringField("Ссылка на изборажение студента", validators=[DataRequired()])
    submit = SubmitField(label="")
