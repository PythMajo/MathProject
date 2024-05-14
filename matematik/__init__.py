from flask import Flask
from pathlib import Path
from sqlalchemy.engine.url import make_url
#from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from . import models

from sqlalchemy import MetaData

# fixes ValueError: Constraint must have a name
convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

#db = SQLAlchemy()
db = SQLAlchemy(metadata=MetaData(naming_convention=convention))
migrate = Migrate()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Set up the instance directory
    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)

    # Set up database URI
    db_uri = 'sqlite:///' + str(instance_path / 'flaskr.sqlite')

    # Configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,  # Disable modification tracking
    )
    db.init_app(app)  # Initialize db with the Flask app instance
    migrate.init_app(app, db, render_as_batch=True)  # Initialize Flask-Migrate with the app and db

    if test_config is not None:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    else:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    # Ensure the instance folder exists
    instance_path.mkdir(exist_ok=True)

    # Initialize the database

    from matematik.models import User  # Import User model
    # Import and register blueprints
    from . import auth, math, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(math.bp)
    app.add_url_rule('/', endpoint='index')


    # A simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
