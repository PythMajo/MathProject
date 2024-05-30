from matematik import create_app, db
import pytest
from flask import url_for
from matematik.models import User


def test_register_page_loads(app, test_client):
    """
    GIVEN a Flask application
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    """
    with app.test_request_context():
        response = test_client.get(url_for('auth.register'))
        assert response.status_code == 200
        assert b"Register" in response.data


def test_register_without_username(app, test_client):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to without a username
    THEN check that an error is flashed
    """
    with app.test_request_context():
        response = test_client.post(url_for('auth.register'), data={'username': '', 'password': 'password'})
        assert response.status_code == 200
        assert b"Username is required." in response.data


def test_register_without_password(app, test_client):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to without a password
    THEN check that an error is flashed
    """
    with app.test_request_context():
        response = test_client.post(url_for('auth.register'), data={'username': 'test_user', 'password': ''})
        assert response.status_code == 200
        assert b"Password is required." in response.data


def test_register_with_existing_username(app, test_client, new_user, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to with an existing username
    THEN check that an error is flashed
    """

    with app.test_request_context():
        response = test_client.post(url_for('auth.register'), data={'username': 'test_user', 'password': 'password'})
        assert response.status_code == 200
        assert b"User test_user is already registered." in response.data


def test_register_success(app, test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/register' page is posted to with valid credentials
    THEN check that the user is redirected to the login page
    """

    with app.test_request_context():
        response = test_client.post(url_for('auth.register'), data={
            'username': 'new_user',
            'password': 'password'
        })
        assert response.status_code == 302
        assert url_for('auth.login') in response.headers['Location']

        # Verify the user was added to the database
        new_user = User.query.filter_by(username='new_user').first()
        assert new_user is not None
        assert new_user.username == 'new_user'

        # Verify the default settings operator association
        # assert default_operator in new_user.settings_operators

        # assert default_operator in new_user.settings_operators #TODO


def test_login_page_loads(app, test_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is requested (GET)
    THEN check that the response is valid
    """
    with app.test_request_context():
        response = test_client.get(url_for('auth.login'))
        assert response.status_code == 200
        assert b"Log In" in response.data


def test_login_success(app, test_client, init_database, existing_user):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to with valid credentials
    THEN check that the user is redirected to the index page
    """

    with app.test_request_context():
        response = test_client.post(url_for('auth.login'), data={'username': 'existing_user', 'password': 'password'})
        assert response.status_code == 302
        assert url_for('math.index') in response.headers['Location']


def test_login_invalid_username(app, test_client, init_database):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to with an invalid username
    THEN check that the user sees an error message
    """
    with app.test_request_context():
        response = test_client.post(url_for('auth.login'), data={'username': 'wrong_user', 'password': 'password'})
        assert response.status_code == 200
        assert b"Incorrect username." in response.data


def test_login_invalid_password(app, test_client, init_database, existing_user):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to with an invalid password
    THEN check that the user sees an error message
    """
    with app.test_request_context():
        response = test_client.post(url_for('auth.login'),
                                    data={'username': 'existing_user', 'password': 'wrong_password'})
        assert response.status_code == 200
        assert b"Incorrect password." in response.data
