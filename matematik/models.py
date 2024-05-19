from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from . import db
from datetime import datetime

from sqlalchemy.sql import func

# Create an instance of SQLAlchemy
class Post(db.Model):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created = Column(TIMESTAMP, nullable=False, server_default='CURRENT_TIMESTAMP')
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)


class Answer(db.Model):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    problem = Column(String, nullable=False)
    user_answer = Column(Boolean, nullable=False)


class UserOptions(db.Model):
    __tablename__ = 'user_options'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    operator_plus_option = Column(Boolean, nullable=False)
    operator_minus_option = Column(Boolean)
    operator_multiply_option = Column(Boolean)

# Define the association table for many-to-many relationship
users_settings_operators = db.Table(
    'users_settings_operators',
    db.Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    db.Column('settings_operator_id', Integer, ForeignKey('settings_operators.id'), primary_key=True)
)


users_collectable_items = db.Table(
    'users_collectable_items',
    #db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('collectable_items_id', db.Integer, db.ForeignKey('collectable_items.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow, nullable=False)
)

# Define User class
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(50), unique=True, nullable=False)
    password = db.Column(String, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    answers = db.relationship('Answer', backref='author', lazy=True)
    settings_operators = db.relationship("SettingsOperators", secondary=users_settings_operators, backref="users")
    collection = db.relationship("CollectableItems", secondary=users_collectable_items, backref="users")
    settings_level_id = db.Column(db.Integer, db.ForeignKey('settings_level.id'))
    created = Column(TIMESTAMP, nullable=True, server_default=func.current_timestamp())


# Define SettingsOperators class
class SettingsOperators(db.Model):
    __tablename__ = 'settings_operators'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100))
    operator = db.Column(String(2))

    def __str__(self):
        return self.name


class SettingsLevel(db.Model):
    __tablename__ = 'settings_level'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100))

    def __str__(self):
        return self.name


class CollectableItems(db.Model):
    __tablename__ = 'collectable_items'
    id = db.Column(Integer, primary_key=True)
    fa_code = db.Column(String(100))
    color = db.Column(String(100))

