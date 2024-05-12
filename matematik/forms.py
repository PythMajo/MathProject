from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,BooleanField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    plus_option = BooleanField('Plus', default=True)
    minus_option = BooleanField('Minus', default=True)
    multiply_option = BooleanField('Multiply', default=True)
    submit = SubmitField('Gem')

    def set_defaults(self, user_options_dict):
        """
        Set default values for form fields based on user options retrieved from the database.

        Args:
            user_options_dict (dict): Dictionary containing user options.
        """
        if user_options_dict:
            self.plus_option.default = bool(user_options_dict.get('operator_plus_option', False))
            self.minus_option.default = bool(user_options_dict.get('operator_minus_option', False))
            self.multiply_option.default = bool(user_options_dict.get('operator_multiply_option', False))

            print()