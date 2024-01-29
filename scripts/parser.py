import pandas as pd
import os


def read_df_from_csv():
    # Get the current working directory
    current_directory = os.getcwd()

    # Get the parent directory
    parent_directory = os.path.dirname(current_directory)

    # Change the current working directory
    os.chdir(parent_directory)

    raw_path = os.path.join(os.getcwd(), 'data/raw_files/dataset2/movies_metadata.csv')
    df = pd.read_csv(raw_path, low_memory=False)
    return df
