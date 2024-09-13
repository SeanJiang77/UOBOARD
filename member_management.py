import pandas as pd
from initialization import registration_file_path


def register_member(member_id, name, contact):
    df = pd.read_excel(registration_file_path)
    new_member = pd.DataFrame({"ID": [member_id], "Name": [name], "Contact": [contact]})
    df = pd.concat([df, new_member], ignore_index=True)
    df.to_excel(registration_file_path, index=False)
    print("Registration successful!")
