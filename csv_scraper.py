import pandas as pd

def get_winners(csv_path, name_column):
    df = pd.read_csv(csv_path)
    df = df[name_column]
    df = df.to_list()
    return df