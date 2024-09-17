# models.py
from extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    game_type = db.Column(db.String(100), nullable=False)
    game_name = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(255), nullable=False)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    avalon_played = db.Column(db.Integer, default=0)
    avalon_wins = db.Column(db.Integer, default=0)
    werewolf_played = db.Column(db.Integer, default=0)
    werewolf_wins = db.Column(db.Integer, default=0)
