from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from dotenv import load_dotenv
from matematik.auth import login_required
import git
import os
import hmac
import hashlib

bp = Blueprint('blog', __name__)

# test 4

def is_valid_signature(x_hub_signature, data, private_key):
    # https://medium.com/@aadibajpai/deploying-to-pythonanywhere-via-github-6f967956e664
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret



    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


@bp.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        x_hub_signature = request.headers.get('X - Hub - Signature')

        load_dotenv()
        w_secret = os.getenv('w_secret')

        if is_valid_signature(x_hub_signature, request.data, w_secret):

            repo = git.Repo( os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))  # Update the path to one folder above
            origin = repo.remotes.origin
            origin.pull()
            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong key', 400
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





