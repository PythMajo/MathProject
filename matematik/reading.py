from dataclasses import dataclass
from random import randint

from typing import Any

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from sqlalchemy import func, and_, desc, select, join, asc
from sqlalchemy.orm import aliased

from markupsafe import Markup

from werkzeug.exceptions import abort
from matematik.auth import login_required
from .models import User, Answer, SettingsLevel, SettingsOperators, CollectableItems, users_collectable_items
from . import db
from random import randint, choice
from .forms import SettingsOperatorsForm

bp = Blueprint('reading', __name__, url_prefix='/reading')


@dataclass
class Missing_Letter:
    word: str = ''

    def __post_init__(self):
        index = randint(0, len(self.word) - 1)
        # Ensure that parts are calculated whenever a new word is set
        self.first_part, self.second_part, self.missing_letter = self.word[:index], self.word[index + 1:], self.word[
            index]


@bp.route('/')
def index():
    words = ['sagde', 'hende', 'ham', 'ost']

    problem = Missing_Letter(choice(words))

    return f'{problem.first_part}_{problem.second_part}'
