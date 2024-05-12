from wtforms import Form, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, DataRequired

class LessonForm(Form):
    name = StringField("Название занятия", validators=[InputRequired()])
    auditory = SelectField("Выберите аудиторию", validators=[DataRequired()])
    submit = SubmitField()
