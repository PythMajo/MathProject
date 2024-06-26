from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, abort
)
from werkzeug.exceptions import abort
from dotenv import load_dotenv
from matematik.auth import login_required
import git
import os
import hmac
import hashlib
from flask_migrate import upgrade

bp = Blueprint('blog', __name__)


def is_valid_signature(x_hub_signature, data, private_key):
    # https://medium.com/@aadibajpai/deploying-to-pythonanywhere-via-github-6f967956e664
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret

    hash_algorithm, github_signature = x_hub_signature.split('=', 1)

    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Abort and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.data)
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (X-Hub-Signature-256)
    """
    if not signature_header:
        abort(403, description="x-hub-signature-256 header is missing!")

    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()



    if not hmac.compare_digest(expected_signature, signature_header):
        abort(403, description="Request signatures didn't match!")

    return True


@bp.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':

        # Debugging: Print all headers

        payload_body = request.get_data()

        # Check for empty payload
        if not payload_body:
            abort(403, description="Payload body is empty!")

        signature_header = request.headers.get('X-Hub-Signature-256')
        load_dotenv()
        WEBHOOK_SECRET = os.getenv('w_secret')

        try:
            if verify_signature(payload_body, WEBHOOK_SECRET, signature_header):
                # Process the valid payload
                repo = git.Repo(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                             '..'))  # Update the path to one folder above
                origin = repo.remotes.origin
                origin.pull()

                # Apply database migrations
                with bp.app_context():
                    upgrade()

                return "Payload verified and processed, database upgraded", 200

        except Exception as e:
            abort(403, description=str(e))



@bp.route('/')
def index():
    return redirect(url_for('math.index'))





