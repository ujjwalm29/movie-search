from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import os
import tiktoken
from scripts import parser
import json
import pandas as pd
import time

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"))


def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def count_tokens(df):
    # Initialize counters
    total_title_tokens = 0
    total_overview_tokens = 0

    # Open a text file to write the titles
    with open('titles.txt', 'w') as file:
        # Loop over the DataFrame and count tokens
        for _, row in df.iterrows():
            # if row['vote_average'] < 6.5 or row['original_language'] != "en":
            #     continue

            categories = ""
            col_val = json.loads(row['genres'].replace("'", '"'))
            for category in col_val:
                categories += f" {category['name']}"

            total_title_tokens += num_tokens_from_string(str(row['title'])+" "+categories)
            total_overview_tokens += num_tokens_from_string(str(row['overview']))

            # Write the title to the file instead of printing
            file.write(str(row['title']) + '\n')

    combined_total_tokens = total_title_tokens + total_overview_tokens

    print(f"Title count : {total_title_tokens}")
    print(f"Overview count : {total_overview_tokens}")
    print(f"Total count : {combined_total_tokens}")


def get_embedding_for_row(row):
    """
    Generate embedding for a single row.
    """
    categories = ""
    if row['vote_average'] >= 6.5 and row['original_language'] == "en":
        col_val = json.loads(row['genres'].replace("'", '"'))
        for category in col_val:
            categories += f" {category['name']}"
        concatenated_text = str(row['title']) + " " + str(row['overview']) + " " + categories
        return get_embedding(concatenated_text)
    return None


def create_embeddings(df, file_name='df_with_openai_embeddings.pkl'):
    start_time = time.time()
    total_title_tokens = 0
    total_overview_tokens = 0

    if os.path.isfile(file_name):
        df_with_embeddings = pd.read_pickle(file_name)
    else:
        # Use ThreadPoolExecutor to parallelize embedding generation
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit all embedding generation tasks
            future_to_row = {executor.submit(get_embedding_for_row, row): index for index, row in df.iterrows()}

            embeddings = [None] * len(df)  # Initialize a list to hold embeddings
            for future in as_completed(future_to_row):
                index = future_to_row[future]
                print(index)
                try:
                    embedding = future.result()  # Obtain result
                    if embedding is not None:
                        embeddings[index] = embedding
                        # Update token counts here if needed
                except Exception as exc:
                    print(f"Row {index} generated an exception: {exc}")
                    embeddings[index] = None  # Handle failed requests if necessary

        # After collecting all embeddings, filter out None values if any rows were skipped
        #embeddings = [emb for emb in embeddings if emb is not None]
        df['embeddings'] = embeddings
        df.to_pickle(file_name)
        df_with_embeddings = df

    combined_total_tokens = total_title_tokens + total_overview_tokens
    end_time = time.time()
    print(f"The operation took {end_time - start_time} seconds.")
    print(f"Title count: {total_title_tokens}, Overview count: {total_overview_tokens}, Total count: {combined_total_tokens}")

    return df_with_embeddings


# df = parser.read_df_from_csv()
# #count_tokens(df)
# df_2 = df[:2]
# df_w_embeddings = create_embeddings(df)
# print(df_w_embeddings)
