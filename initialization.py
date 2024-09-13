import pandas as pd

# 定义两个文件的路径
registration_file_path = "registration_data.xlsx"
games_file_path = "games_data.xlsx"


def initialize_files():
    create_file_if_not_exists(registration_file_path, ["ID", "Name", "Contact"])
    create_file_if_not_exists(games_file_path, ["GameID", "Date", "GameName", "Participants", "Result"])


def create_file_if_not_exists(file_path, columns):
    try:
        # 尝试读取文件，确认是否存在
        pd.read_excel(file_path)
    except FileNotFoundError:
        # 如果文件不存在，创建一个新的
        df = pd.DataFrame(columns=columns)
        df.to_excel(file_path, index=False)
