import pandas as pd
from initialization import games_file_path


def add_game(game_id, date, game_name, participants, result):
    df = pd.read_excel(games_file_path)
    new_game = pd.DataFrame({"GameID": [game_id], "Date": [date], "GameName": [game_name],
                             "Participants": [participants], "Result": [result]})
    df = pd.concat([df, new_game], ignore_index=True)
    df.to_excel(games_file_path, index=False)
    print("Game record added!")


def delete_game(game_id):
    df = pd.read_excel(games_file_path)
    df = df[df["GameID"] != game_id]
    df.to_excel(games_file_path, index=False)
    print("Game record deleted!")


def update_game(game_id, **kwargs):
    df = pd.read_excel(games_file_path)
    for key, value in kwargs.items():
        df.loc[df["GameID"] == game_id, key] = value
    df.to_excel(games_file_path, index=False)
    print("Game record updated!")


def query_games(**kwargs):
    df = pd.read_excel(games_file_path)
    for key, value in kwargs.items():
        df = df[df[key] == value]
    print(df)
