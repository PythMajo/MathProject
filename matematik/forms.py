from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,BooleanField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    plus_option = BooleanField('Plus', default=True)
    minus_option = BooleanField('Minus', default=True)
    multiply_option = BooleanField('Plus', default=True)
    submit = SubmitField('Gem')
