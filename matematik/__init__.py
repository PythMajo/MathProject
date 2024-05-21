from flask import Flask
from pathlib import Path
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dotenv import load_dotenv

from sqlalchemy import MetaData

# fixes ValueError: Constraint must have a name
convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=convention))
migrate = Migrate(compare_type=True)

import logging
logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Set up the instance directory
    instance_path = Path(app.instance_path)
    instance_path.mkdir(parents=True, exist_ok=True)
    load_dotenv()

    config_name = os.getenv('FLASK_ENV')
    if test_config is None:

        if config_name == 'production':
            app.config.from_object('config.ProductionConfig')
            app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
        else:
            app.config.from_object('config.DevelopmentConfig')
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    logging.info(f'App started, configname: {config_name}')
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
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    # Register custom CLI command
    @app.cli.command("clear_and_fill_tables")
    def clear_and_fill_tables_command():

        clear_and_fill_tables(app)
        print("Tables have been cleared and filled with initial data.")



    # A simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


def clear_and_fill_tables(app):
    from .models import CollectableItems, SettingsOperators, SettingsLevel  # Import models here

    with app.app_context():
        # Clear existing data from the tables
        db.session.query(CollectableItems).delete()
        db.session.query(SettingsOperators).delete()
        db.session.query(SettingsLevel).delete()

        # Add predefined operators
        predefined_operators = [
            SettingsOperators(id=1, name='plus', operator='+'),
            SettingsOperators(id=2, name='minus', operator='-'),
            SettingsOperators(id=3, name='gange', operator='*')
        ]
        db.session.add_all(predefined_operators)

        # Add predefined collectable items
        predefined_items = [
            CollectableItems(id=1, fa_code='fa-solid fa-cow', color='#FFD43B'),
            CollectableItems(id=2, fa_code='fa-solid fa-hippo', color='#63E6BE'),
            CollectableItems(id=3, fa_code='fa-solid fa-otter', color='#74C0FC'),
            CollectableItems(id=4, fa_code='fa-solid fa-paw', color='#B197FC'),
            CollectableItems(id=5, fa_code='fa-solid fa-dog', color='#49a835'),
            CollectableItems(id=6, fa_code='fa-solid fa-fish', color='#FFD43B'),
            CollectableItems(id=7, fa_code='fa-solid fa-dragon', color='#63E6BE'),
            CollectableItems(id=8, fa_code='fa-solid fa-kiwi-bird', color='#74C0FC'),
            CollectableItems(id=9, fa_code='fa-solid fa-poo', color='#B197FC'),
            CollectableItems(id=10, fa_code='fa-solid fa-camera-retro', color='#49a835'),
            CollectableItems(id=11, fa_code='fa-solid fa-truck-fast', color='#FFD43B'),
            CollectableItems(id=12, fa_code='fa-solid fa-lemon', color='#63E6BE'),
            CollectableItems(id=13, fa_code='fa-solid fa-bell', color='#74C0FC'),
            CollectableItems(id=14, fa_code='fa-solid fa-bolt', color='#B197FC'),
            CollectableItems(id=15, fa_code='fa-solid fa-car', color='#49a835'),
            CollectableItems(id=16, fa_code='fa-solid fa-ghost', color='#FFD43B'),
            CollectableItems(id=17, fa_code='fa-solid fa-mug-hot', color='#63E6BE'),
            CollectableItems(id=18, fa_code='fa-solid fa-umbrella', color='#74C0FC'),
            CollectableItems(id=19, fa_code='fa-solid fa-gift', color='#B197FC'),
            CollectableItems(id=20, fa_code='fa-solid fa-book', color='#49a835'),
            CollectableItems(id=21, fa_code='fa-solid fa-headphones', color='#FFD43B'),
            CollectableItems(id=22, fa_code='fa-solid fa-camera', color='#63E6BE'),
            CollectableItems(id=23, fa_code='fa-solid fa-plane', color='#74C0FC'),
            CollectableItems(id=24, fa_code='fa-solid fa-key', color='#B197FC'),
            CollectableItems(id=25, fa_code='fa-solid fa-truck', color='#49a835'),
            CollectableItems(id=26, fa_code='fa-solid fa-tree', color='#FFD43B'),
            CollectableItems(id=27, fa_code='fa-solid fa-bicycle', color='#63E6BE'),
            CollectableItems(id=28, fa_code='fa-solid fa-flask', color='#74C0FC'),
            CollectableItems(id=29, fa_code='fa-solid fa-bath', color='#B197FC'),
            CollectableItems(id=30, fa_code='fa-solid fa-snowflake', color='#49a835'),
            CollectableItems(id=31, fa_code='fa-solid fa-feather', color='#FFD43B'),
            CollectableItems(id=32, fa_code='fa-solid fa-sun', color='#63E6BE'),
            CollectableItems(id=33, fa_code='fa-solid fa-fish', color='#74C0FC'),
            CollectableItems(id=34, fa_code='fa-solid fa-bug', color='#B197FC'),
            CollectableItems(id=35, fa_code='fa-solid fa-mug-saucer', color='#49a835')
        ]
        db.session.add_all(predefined_items)

        # Add predefined settings levels
        predefined_levels = [
            SettingsLevel(id=1, name='Easy'),
            SettingsLevel(id=2, name='Medium'),
            SettingsLevel(id=3, name='Hard')
        ]
        db.session.add_all(predefined_levels)

        db.session.commit()