from typing import Any

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from sqlalchemy import func, and_

from werkzeug.exceptions import abort
from matematik.auth import login_required
from matematik.models import User, Answer, UserOptions, SettingsOperators, CollectableItems, users_collectable_items
from matematik import db
from random import randint, choice
from .forms import SettingsOperatorsForm


bp = Blueprint('math', __name__, url_prefix='/math')


def get_progress_for_user(user_id: int) -> int:
    correct_answers = Answer.query.filter(
        and_(
            Answer.author_id == user_id,
            Answer.user_answer == True
        )
    ).count()

    progress: int | Any = correct_answers % 10
    return progress





def generate_math_problem():
    # Generate two random numbers between 1 and 10
    num1 = randint(1, 10)
    num2 = randint(1, 10)

    # Choose a random operation (+, -, *)
    operator = choice(['+', '-'])

    # Calculate the correct answer
    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    else:
        answer = num1 * num2

    # Return the problem as a dictionary
    return {
        'num1': num1,
        'num2': num2,
        'operator': operator,
        'answer': answer
    }


@bp.route('/')
def index():
    return render_template('math/index.html')


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
    collection = [item.fa_code for item in user.collection]

    return render_template('math/my_collection.html', my_collection=collection)




@bp.route('/solve_problem', methods=['GET', 'POST'])
@login_required
def solve_problem():
    if request.method == 'GET':
        correct_answers = get_progress_for_user(g.user.id)
        math_problem = generate_math_problem()
        return render_template('math/solve_problem.html', math_problem=math_problem, correct_answers=correct_answers)

    elif request.method == 'POST':
        user_answer = int(request.form['user_answer'])
        math_problem = {
            'num1': int(request.form['num1']),
            'num2': int(request.form['num2']),
            'operator': request.form['operator'],
            'answer': int(request.form['answer'])
        }
        problem = f"{math_problem['num1']} {math_problem['operator']} {math_problem['num2']}"
        correct_answer = eval(problem)
        if user_answer == correct_answer:
            flash('Correct!', 'success')
            new_answer = Answer(problem=problem, user_answer=True, author_id=g.user.id)

            #check if new items i needed
            if get_progress_for_user(g.user.id) == 9:
                flash('New item in collection', 'warning')

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
                    #FIXME
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

            db.session.add(new_answer)
            db.session.commit()
        else:
            flash('Incorrect. Try again.', 'danger')
            new_answer = Answer(problem=problem, user_answer=False, author_id=g.user.id)
            db.session.add(new_answer)
            db.session.commit()
        return redirect(url_for('math.solve_problem'))


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    user = User.query.get(g.user.id)
    form = SettingsOperatorsForm(data={"operators": user.settings_operators})
    form.operators.query = SettingsOperators.query.all()

    if form.validate_on_submit():
        user.settings_operators.clear()
        user.settings_operators.extend(form.operators.data)
        db.session.commit()

    return render_template("math/settings.html", form=form)

