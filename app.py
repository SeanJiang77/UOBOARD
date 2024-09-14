from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 配置数据库连接字符串，确保SSL连接
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://uoboard_user:aC6qYFrX9OXClAjka3R6Sq5gJThtD9ea@dpkg-crje8rv2p9s7s83j2pt0-a.oregon-postgres.render.com:5432/uoboard?sslmode=require')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 定义Member模型
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    avalon_played = db.Column(db.Integer, default=0)
    avalon_wins = db.Column(db.Integer, default=0)
    werewolf_played = db.Column(db.Integer, default=0)
    werewolf_wins = db.Column(db.Integer, default=0)


# 定义Game模型
class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    game_type = db.Column(db.String(100), nullable=False)
    game_name = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(255), nullable=False)


# 在每次请求之前创建数据库表（如果尚未创建）
@app.before_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
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
            db.session.commit()


@app.route('/admin')
def admin_panel():
    members = Member.query.all()
    games = Game.query.all()
    return render_template('admin.html', members=members, games=games)


@app.route('/edit_member/<int:member_id>', methods=['POST'])
def edit_member(member_id):
    # 这里放置编辑成员信息的逻辑
    return redirect(url_for('admin_panel'))


@app.route('/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    member = Member.query.get(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
    return redirect(url_for('admin_panel'))


@app.route('/edit_game/<int:game_id>', methods=['POST'])
def edit_game(game_id):
    # 这里放置编辑游戏信息的逻辑
    return redirect(url_for('admin_panel'))


@app.route('/delete_game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
    return redirect(url_for('admin_panel'))


if __name__ == "__main__":
    app.run(debug=True)
