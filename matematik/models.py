from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from matematik import db
from flask_sqlalchemy import SQLAlchemy

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
    created = Column(TIMESTAMP, nullable=False, server_default='CURRENT_TIMESTAMP')
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

# Define User class
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(50), unique=True, nullable=False)
    password = db.Column(String, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    answers = db.relationship('Answer', backref='author', lazy=True)
    options = db.relationship('UserOptions', backref='user', uselist=False, lazy=True)
    settings_operators = db.relationship("SettingsOperators", secondary=users_settings_operators, backref="users")

# Define SettingsOperators class
class SettingsOperators(db.Model):
    __tablename__ = 'settings_operators'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100))

    def __str__(self):
        return self.name
