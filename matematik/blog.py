from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from matematik.auth import login_required
import git
import os


bp = Blueprint('blog', __name__)


@bp.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo( os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))  # Update the path to one folder above
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

@bp.route('/')
def index():
    # db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    #return render_template('blog/index.html', posts=posts)
    redirect('math.index')





