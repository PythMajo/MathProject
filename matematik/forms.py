from flask_wtf import FlaskForm
from wtforms_alchemy import QuerySelectMultipleField, QuerySelectField
from wtforms import widgets
from matematik.models import SettingsLevel


class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SettingsOperatorsForm(FlaskForm):
    #TODO: add more fields
    operators = QuerySelectMultipleFieldWithCheckboxes("Operators")
    settings_level = QuerySelectField('Settings Level', get_pk=lambda x: x.id, get_label='name')
