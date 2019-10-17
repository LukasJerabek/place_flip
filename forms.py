from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SetUpForm(FlaskForm):
    place = StringField('Place', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add place')
