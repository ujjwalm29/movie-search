import pandas as pd
import os
from .config import DATA_PATH


def read_df_from_csv():
    df = pd.read_csv(DATA_PATH, low_memory=False)
    return df


def get_dataframe_from_pkl_file(file_name: str):
    if os.path.isfile(file_name):
        # Load DataFrame from the file
        df_with_embeddings = pd.read_pickle(file_name)
    else:
        print("File does not exist")
        return

    return df_with_embeddings
