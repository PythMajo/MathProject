import pytest
from matematik import create_app, db
from matematik.models import User
from matematik.models import User, SettingsOperators


@pytest.fixture(scope='module')
def app():
    app = create_app(test_config=True)
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def init_database(app):
    with app.app_context():
        db.create_all()

        default_operators = [
            SettingsOperators(id=1, name='plus', operator='+'),
            SettingsOperators(id=2, name='minus', operator='-'),
            SettingsOperators(id=3, name='gange', operator='*')
        ]

        db.session.add_all(default_operators)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def new_user(init_database):
    """
    Create a new user for the tests.
    """
    user = User(username='test_user', password='password', settings_level_id=1)
    db.session.add(user)
    db.session.commit()

    # Add a default operator to the user
    default_operator = SettingsOperators.query.get(1)
    user.settings_operators.append(default_operator)
    db.session.commit()

    return user


@pytest.fixture(scope='module')
def test_client():
    """
    Creates a Flask application configured for testing,
    and a test client for sending HTTP requests.
    """
    flask_app = create_app(test_config=True)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context before running the tests
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def test_client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def existing_user():
    user = User(username='existing_user', password='password', settings_level_id=1)
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()
