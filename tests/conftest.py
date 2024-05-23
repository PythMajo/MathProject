import pytest
from matematik import create_app, db
from matematik.models import User



@pytest.fixture(scope='module')
def new_user():
    password = 'password'
    user = User(username='test_user', password=password, settings_level_id=1)
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
def init_database():
    """
    Initializes the database before tests and drops it after tests.
    """
    flask_app = create_app(test_config=True)

    with flask_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
