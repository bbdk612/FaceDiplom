from wtforms import Form, StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired

class AuditoryForm(Form):
    number = StringField("Номер аудитории", validators=[InputRequired()], render_kw={"placeholder": "4/401"})
    camera_address = StringField("Адресс камеры расположенной в аудитории", validators=[InputRequired()])
    submit = SubmitField(label="")
