from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# 定义数据文件的相对路径
data_folder = "data"
registration_file_path = os.path.join(data_folder, "registration_data.xlsx")
games_file_path = os.path.join(data_folder, "games_data.xlsx")


# 读取 Excel 文件的函数
def read_excel(file_path):
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    else:
        return pd.DataFrame()


# 保存数据到 Excel 文件的函数
def save_to_excel(df, file_path):
    df.to_excel(file_path, index=False)


def read_and_append_to_excel(file_path, new_data):
    # 如果文件不存在，创建一个空的 DataFrame 并写入文件
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=new_data.keys())
        df.to_excel(file_path, index=False)
    else:
        df = pd.read_excel(file_path)

    # 追加新数据并保存回文件
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_excel(file_path, index=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register_member():
    if request.method == 'POST':
        data = request.json
        new_member = {
            "ID": data['id'],
            "Name": data['name'],
            "Contact": data['contact']
        }

        read_and_append_to_excel(registration_file_path, new_member)
        return jsonify({"message": "Registration successful!"})
    return render_template('index.html')


@app.route('/add_game', methods=['POST'])
def add_game():
    data = request.json
    game_type = data['game_type']
    game_name = data['game_name']
    participants = data['participants'].split(', ')
    winner = data['result'].split(' ')[0]  # 假设winner name是result的第一个词

    new_game = {
        "GameID": data['game_id'],
        "Date": data['date'],
        "GameType": game_type,
        "GameName": game_name,
        "Participants": ', '.join(participants),
        "Result": data['result']
    }

    # 读取现有的 Excel 文件
    df = pd.read_excel(games_file_path)

    # 重新排列列的顺序
    df = df[["GameID", "Date", "GameType", "GameName", "Participants", "Result"]]

    # 保存回 Excel 文件
    df.to_excel(games_file_path, index=False)

    df = pd.DataFrame([new_game], columns=["GameID", "Date", "GameType", "GameName", "Participants", "Result"])
    read_and_append_to_excel(games_file_path, new_game)

    # 更新每个参与者的游戏统计信息
    update_participants_statistics(participants, winner, game_type)

    return jsonify({"message": "Game record added!"})


def update_participants_statistics(participants, winner, game_type):
    df = pd.read_excel(registration_file_path)

    for participant in participants:
        # 更新参与者的游戏统计数据
        df.loc[df['Name'] == participant, f'{game_type}_played'] = df.get(f'{game_type}_played', 0) + 1
        if participant == winner:
            df.loc[df['Name'] == participant, f'{game_type}_wins'] = df.get(f'{game_type}_wins', 0) + 1

    # 保存更新后的数据
    df.to_excel(registration_file_path, index=False)


def calculate_winrate(member_name, game_type):
    df = pd.read_excel(registration_file_path)
    games_played = df.loc[df['Name'] == member_name, f'{game_type}_played'].values[0]
    games_won = df.loc[df['Name'] == member_name, f'{game_type}_wins'].values[0]
    winrate = (games_won / games_played) * 100 if games_played > 0 else 0
    return winrate


# 管理页面路由
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        action = request.form['action']

        if action == 'add_member':
            new_member = {
                "ID": request.form['id'],
                "Name": request.form['name'],
                "Contact": request.form['contact']
            }
            members_df = read_excel(registration_file_path)
            members_df = members_df.append(new_member, ignore_index=True)
            save_to_excel(members_df, registration_file_path)

        elif action == 'add_game':
            new_game = {
                "GameID": request.form['game_id'],
                "Date": request.form['date'],
                "GameType": request.form['game_type'],
                "GameName": request.form['game_name'],
                "Participants": request.form['participants'],
                "Result": request.form['result']
            }
            games_df = read_excel(games_file_path)
            games_df = games_df.append(new_game, ignore_index=True)
            save_to_excel(games_df, games_file_path)

        elif action == 'delete_member':
            member_id = int(request.form['id'])
            members_df = read_excel(registration_file_path)
            members_df = members_df[members_df['ID'] != member_id]
            save_to_excel(members_df, registration_file_path)

        elif action == 'delete_game':
            game_id = int(request.form['game_id'])
            games_df = read_excel(games_file_path)
            games_df = games_df[games_df['GameID'] != game_id]
            save_to_excel(games_df, games_file_path)

    # 读取数据以显示在页面上
    members_df = read_excel(registration_file_path)
    games_df = read_excel(games_file_path)

    return render_template('admin.html', members=members_df.to_dict(orient='records'),
                           games=games_df.to_dict(orient='records'))


if __name__ == "__main__":
    app.run(debug=True)
