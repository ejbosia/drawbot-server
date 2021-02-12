from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectMultipleField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class LoadForm(FlaskForm):
    pass
