from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm

class SetUpForm(FlaskForm):
    place = StringField('Place', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add place')

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
