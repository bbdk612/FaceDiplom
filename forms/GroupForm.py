from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired, Length

class GroupForm(Form):
    number = StringField("Номер группы", validators=[DataRequired(), Length(1, 10)], )
    submit = SubmitField("")