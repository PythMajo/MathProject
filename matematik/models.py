from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from matematik import db
from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy



class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship('Post', backref='author', lazy=True)
    answers = relationship('Answer', backref='author', lazy=True)
    options = relationship('UserOptions', backref='user', uselist=False, lazy=True)


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
