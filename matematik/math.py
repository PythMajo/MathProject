from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from sqlalchemy import func
from werkzeug.exceptions import abort
from matematik.auth import login_required
from matematik.models import User, Answer, UserOptions
from matematik import db
import random
from .forms import SettingsForm


bp = Blueprint('math', __name__, url_prefix='/math')


def generate_math_problem():
    # Generate two random numbers between 1 and 10
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    # Choose a random operation (+, -, *)
    operator = random.choice(['+', '-'])

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


@bp.route('/solve_problem', methods=['GET', 'POST'])
@login_required
def solve_problem():
    if request.method == 'GET':
        math_problem = generate_math_problem()
        return render_template('math/solve_problem.html', math_problem=math_problem)

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
            db.session.add(new_answer)
            db.session.commit()
        else:
            flash('Incorrect. Try again.', 'danger')
            new_answer = Answer(problem=problem, user_answer=False, author_id=g.user.id)
            db.session.add(new_answer)
            db.session.commit()
        return redirect(url_for('math.solve_problem'))


@bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    form = SettingsForm(plus_option=False)
    if form.validate_on_submit():
        user_options = UserOptions.query.filter_by(author_id=g.user.id).first()
        if user_options:
            user_options.operator_plus_option = form.plus_option.data
        else:
            user_options = UserOptions(author_id=g.user.id, operator_plus_option=form.plus_option.data)
        db.session.add(user_options)
        db.session.commit()
        return redirect(url_for('math.solve_problem'))
    user_options = UserOptions.query.filter_by(author_id=g.user.id).first()
    if user_options:
        form.set_defaults(user_options)
    return render_template('math/submit.html', form=form)
