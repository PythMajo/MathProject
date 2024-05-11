from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from matematik.auth import login_required
from matematik.db import get_db
import random
from . forms import SettingsForm

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



def get_user_score(user_id):

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m-%d', created) AS day_created, COUNT(*) 
        FROM awnsers 
        WHERE author_id = ? AND user_awnser = 1 
        GROUP BY day_created;
        """, (user_id,)

    )
    data = cursor.fetchall()
    # Convert data to a list of dictionaries
    chart_data = [{'day_created': row[0], 'count': row[1]} for row in data]

    
    cursor.execute("""
        SELECT COUNT(*) as count,
       CASE WHEN user_awnser = 1 THEN 'Correct' 
            ELSE 'Incorrect' END as answer_status
        FROM awnsers 
        WHERE author_id = 1 
        GROUP BY user_awnser;
                        """)
    ratio_data = cursor.fetchall()
    ratio_dict = {row[0]: row[1] for row in ratio_data}


    db.close()
    
    return chart_data, ratio_dict



@bp.route('/my_stat', methods=['GET'])
@login_required
def my_stat():
    my_score, ratio =  get_user_score(g.user['id'])
    
    return render_template('math/my_stat.html', my_score=my_score, ratio=ratio)
    
    


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
        problem = f"{math_problem['num1']}  {math_problem['operator']}  {math_problem['num2']}"
        correct_answer = eval(problem)
        db = get_db()
        if user_answer == correct_answer:
            flash('Correct!', 'success')
            
            db.execute(
                'INSERT INTO awnsers (problem, user_awnser, author_id)'
                ' VALUES (?, ?, ?)',
                (problem, True, g.user['id'])
            )
            db.commit()


        else:
            flash('Incorrect. Try again.', 'danger')
            db.execute(
                'INSERT INTO awnsers (problem, user_awnser, author_id)'
                ' VALUES (?, ?, ?)',
                (problem, False, g.user['id'])
            )
            db.commit()

        return redirect(url_for('math.solve_problem'))


@bp.route('/submit', methods=['GET', 'POST'])
def submit():
    form = SettingsForm(plus_option=False)
    if form.validate_on_submit():
        db = get_db()
        cursor = db.cursor()
        # Check if the user already has options in the database
        cursor.execute("SELECT * FROM user_options WHERE author_id = ?", (g.user['id'],))
        existing_record = cursor.fetchone()
        if existing_record:
            # Update existing record
            cursor.execute("UPDATE user_options SET operator_plus_option = ? WHERE author_id = ?",
                           (form.plus_option.data, g.user['id']))
        else:
            # Insert new record
            cursor.execute("INSERT INTO user_options (author_id, operator_plus_option) VALUES (?, ?)",
                           (g.user['id'], form.plus_option.data))

            # Commit changes to the database
        db.commit()

        # Close the connection
        db.close()

        return redirect(url_for('math.solve_problem'))
    return render_template('math/submit.html', form=form)