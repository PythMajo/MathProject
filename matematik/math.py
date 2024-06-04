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

bp = Blueprint('math', __name__, url_prefix='/math')


def get_sorted_collectable_items(user_id):
    # Aliases for the tables
    collectable_item_alias = aliased(CollectableItems)
    user_collectable_item_alias = aliased(users_collectable_items)

    # Create a join between users_collectable_items and collectable_items
    join_stmt = join(user_collectable_item_alias, collectable_item_alias,
                     user_collectable_item_alias.c.collectable_items_id == collectable_item_alias.id)

    # Select the collectable items for the given user, sorted by timestamp
    stmt = select(collectable_item_alias).select_from(join_stmt).where(
        user_collectable_item_alias.c.user_id == user_id
    ).order_by(asc(user_collectable_item_alias.c.timestamp))

    # Execute the query
    result = db.session.execute(stmt).scalars().all()

    return result


def get_progress_for_user(user_id: int) -> int:
    correct_answers = Answer.query.filter(
        and_(
            Answer.author_id == user_id,
            Answer.user_answer == True
        )
    ).count()

    progress: int | Any = correct_answers % 10
    return progress


def generate_expression(level: int, operators: list = ['+', '-', '*']) -> str:

    # Define difficulty settings based on the level
    if level == 1:  # Easy
        num_terms = 2
        max_value = 10  # Default smaller numbers
    elif level == 2:  # Medium
        num_terms = randint(2, 3)
        max_value = 20  # Medium range numbers
    elif level == 3:  # Hard
        num_terms = randint(2, 4)
        max_value = 50  # Larger numbers
    else:
        raise ValueError("Level must be 1 (easy), 2 (medium), or 3 (hard)")

    # Adjust max value for specific operators in level 1
    if level == 1 and '+' in operators and len(operators) == 1:
        max_value = 20

    # Generate operands and operators
    operands = [randint(1, max_value) for _ in range(num_terms)]

    # Ensure positive results for subtraction in level 1
    if level == 1 and '-' in operators and len(operators) == 1:
        operands.sort(reverse=True)  # Ensure the first operand is greater
        operator = choice(operators)
        if operands[0] < operands[1]:  # If the first operand is smaller than the second
            operands[0], operands[1] = operands[1], operands[0]  # Swap them

    # Generate a list of random operators
    selected_operators = [choice(operators) for _ in range(num_terms - 1)]

    # Combine operands and operators to form the expression
    expression_parts = [f"{operands[i]} {selected_operators[i]}" for i in range(num_terms - 1)]
    expression_parts.append(str(operands[-1]))

    return ' '.join(expression_parts)


def generate_math_problem(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    settings_operators = [operator.operator for operator in user.settings_operators]
    settings_level = user.settings_level_id

    math_problem = generate_expression(level=settings_level, operators=settings_operators)
    return math_problem


@bp.route('/')
def index():
    return redirect(url_for('math.solve_problem'))


def get_chart_data(user_id):
    chart_data = db.session.query(func.strftime('%Y-%m-%d', Answer.created).label('day_created'),
                                  func.count().label('count')). \
        filter(Answer.author_id == user_id, Answer.user_answer == True). \
        group_by(func.strftime('%Y-%m-%d', Answer.created)).all()
    return [{'day_created': row.day_created, 'count': row.count} for row in chart_data]


def get_ratio_data(user_id):
    ratio_data = db.session.query(func.count().label('count'),
                                  func.case([(Answer.user_answer == True, 'Correct')],
                                            else_='Incorrect').label('answer_status')). \
        filter(Answer.author_id == user_id). \
        group_by(Answer.user_answer).all()
    return {row.count: row.answer_status for row in ratio_data}


@bp.route('/my_stat', methods=['GET'])
@login_required
def my_stat():
    ratio = get_chart_data(g.user.id)
    my_stat = get_chart_data(g.user_id.id)
    return render_template('math/my_stat.html', my_stat=my_stat, ratio=ratio)


@bp.route('/my_collection', methods=['GET'])
@login_required
def my_collection():
    # Assuming g.user.id contains the ID of the current user
    user = User.query.get(g.user.id)
    #collection = user.collection
    collection = get_sorted_collectable_items(g.user.id)

    return render_template('math/my_collection.html', my_collection=collection)


@bp.route('/solve_problem', methods=['GET', 'POST'])
@login_required
def solve_problem():
    if request.method == 'GET':
        correct_answers = get_progress_for_user(g.user.id)
        math_problem = generate_math_problem(g.user.id)
        return render_template('math/solve_problem.html', math_problem=math_problem, correct_answers=correct_answers)

    elif request.method == 'POST':
        user_answer = int(request.form['user_answer'])
        expression = str(request.form['expression'])

        correct_answer = eval(expression)

        # check for correct awnser
        user_answer_correct = user_answer == correct_answer

        if get_progress_for_user(g.user.id) == 9 and user_answer_correct:

            user_id = g.user.id
            # Query collectable items not already in the user's collection
            not_owned_items_query = (
                CollectableItems.query
                    .filter(~CollectableItems.users.any(id=user_id))
                # Exclude items already in the user's collection
            )

            # Get the count of collectable items not owned by the user
            not_owned_items_count = not_owned_items_query.count()

            # If there are no collectable items not owned by the user, exit or handle the situation accordingly
            if not_owned_items_count == 0:
                # Handle the case where there are no collectable items not owned by the user
                # For example, return an error message or take appropriate action
                # FIXME
                print("No collectable items available.")
                exit()

            # Randomly select a collectable item not owned by the user
            random_collectable_item = not_owned_items_query.offset(randint(0, not_owned_items_count - 1)).first()

            # Associate the random collectable item with the user
            new_association = users_collectable_items.insert().values(user_id=user_id,
                                                                      collectable_items_id=random_collectable_item.id)

            # Insert the association into the users_collectable_items table using the existing db.session()
            db.session.execute(new_association)

            # Commit the transaction
            db.session.commit()
            message = Markup(f'Correct!\nNew item in collection:  <span class="icon"><i class="{ random_collectable_item.fa_code } fa-xl"></i></span>')
            flash(message, 'warning')

        elif user_answer == correct_answer:
            message = Markup('<i class="fa fa-check" aria-hidden="true"></i> Rigtigt!')
            flash(message, 'success')
        else:
            flash(Markup('<i class="fa fa-times" aria-hidden="true"></i> Ikke rigtigt, prøv en ny <i class="fa fa-smile-o" aria-hidden="true"></i> '), 'danger')

        new_answer = Answer(problem=expression, user_answer=user_answer_correct, author_id=g.user.id)
        db.session.add(new_answer)
        db.session.commit()

        return redirect(url_for('math.solve_problem'))


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    user = User.query.get(g.user.id)

    form = SettingsOperatorsForm(data={
        "operators": user.settings_operators,
        "settings_level": user.settings_level_id
    })
    form.operators.query = SettingsOperators.query.all()
    form.settings_level.query = SettingsLevel.query.all()

    if form.validate_on_submit():
        user.settings_operators.clear()
        user.settings_operators.extend(form.operators.data)
        user.settings_level_id = form.settings_level.data.id
        db.session.commit()

    # Set initial data after form submission
    form.operators.data = user.settings_operators
    form.settings_level.data = user.settings_level_id

    return render_template("math/settings.html", form=form)
