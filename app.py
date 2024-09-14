from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import psycopg2
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql://uoboard_user:aC6qYFrX9OXClAjka3R6Sq5gUJhtD9ea@dpkg-crje8rv2p9s7s'
                                         '83j2pt0-a.oregon-postgres.render.com/uoboard')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    avalon_played = db.Column(db.Integer, default=0)
    avalon_wins = db.Column(db.Integer, default=0)
    werewolf_played = db.Column(db.Integer, default=0)
    werewolf_wins = db.Column(db.Integer, default=0)
    # 添加更多游戏类型的字段


class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    game_type = db.Column(db.String(100), nullable=False)
    game_name = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(255), nullable=False)


def get_db_connection():
    conn = psycopg2.connect(
        dbname="uoboard",
        user="uoboard_user",
        password="aC6qYFrX9OXClAjka3R6Sq5gJThtD9ea",
        host="dpkg-crje8rv2p9s7s83j2pt0-a.oregon-postgres.render.com",
        port="5432"
    )
    return conn


@app.before_request
def create_tables():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register_member():
    data = request.json
    new_member = Member(name=data['name'], contact=data['contact'])
    try:
        db.session.add(new_member)
        db.session.commit()
        return jsonify({"message": "Registration successful!"})
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Member already exists!"}), 400


@app.route('/add_game', methods=['POST'])
def add_game():
    data = request.json
    new_game = Game(
        date=data['date'],
        game_type=data['game_type'],
        game_name=data['game_name'],
        participants=', '.join(data['participants']),
        result=data['result']
    )
    db.session.add(new_game)
    db.session.commit()

    # 更新每个参与者的游戏统计信息
    update_participants_statistics(data['participants'], data['result'].split(' ')[0], data['game_type'])

    return jsonify({"message": "Game record added!"})


def update_participants_statistics(participants, winner, game_type):
    for participant in participants:
        member = Member.query.filter_by(name=participant).first()
        if member:
            if game_type == 'Avalon':
                member.avalon_played += 1
                if participant == winner:
                    member.avalon_wins += 1
            elif game_type == 'Werewolf':
                member.werewolf_played += 1
                if participant == winner:
                    member.werewolf_wins += 1
            # 添加更多游戏类型的统计
            db.session.commit()


# 管理页面路由
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    dbname="uoboard",
    user="uoboard_user",
    password="aC6qYFrX9OXClAjka3R6Sq5gJThtD9ea",
    host="dpkg-crje8rv2p9s7s83j2pt0-a.oregon-postgres.render.com",
    port="5432"
)


@app.route('/admin')
def admin_panel():
    cur = conn.cursor()

    # Fetch members
    cur.execute("SELECT * FROM members")
    members = cur.fetchall()

    # Fetch games
    cur.execute("SELECT * FROM games")
    games = cur.fetchall()

    return render_template('admin.html', members=members, games=games)


@app.route('/edit_member/<int:member_id>', methods=['POST'])
def edit_member(member_id):
    # Logic for editing member information goes here
    return redirect(url_for('admin_panel'))


@app.route('/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM members WHERE id = %s", (member_id,))
    conn.commit()
    return redirect(url_for('admin_panel'))


@app.route('/edit_game/<int:game_id>', methods=['POST'])
def edit_game(game_id):
    # Logic for editing game information goes here
    return redirect(url_for('admin_panel'))


@app.route('/delete_game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM games WHERE game_id = %s", (game_id,))
    conn.commit()
    return redirect(url_for('admin_panel'))


if __name__ == "__main__":
    app.run(debug=True)
