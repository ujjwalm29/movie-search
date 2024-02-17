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


def get_dataframe_from_pkl_file(file_name: str):
    if os.path.isfile(file_name):
        # Load DataFrame from the file
        df_with_embeddings = pd.read_pickle(file_name)
    else:
        print("File does not exist")
        return

    return df_with_embeddings
