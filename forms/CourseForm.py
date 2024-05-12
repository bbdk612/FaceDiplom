from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import InputRequired

class MultiSelectField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label="False")
    option_widget = widgets.CheckboxInput()

class CoursesForm(FlaskForm):
    name = StringField("Название курса", validators=[InputRequired()])
    students = MultiSelectField("Студенты", coerce=int)
    submit = SubmitField("Отправить")
