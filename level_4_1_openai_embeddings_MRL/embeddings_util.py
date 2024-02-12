from openai import OpenAI
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


def create_embeddings(df, file_name='df_with_openai_embeddings.pkl'):
    start_time = time.time()

    total_title_tokens = 0
    total_overview_tokens = 0
    # Check if the file exists
    if os.path.isfile(file_name):
        # Load DataFrame from the file
        df_with_embeddings = pd.read_pickle(file_name)
    else:
        # Initialize an empty list to store embeddings
        embeddings = []

        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            print(index)
            if row['vote_average'] < 6.5 or row['original_language'] != "en":
                continue

            categories = ""
            col_val = json.loads(row['genres'].replace("'", '"'))
            for category in col_val:
                categories += f" {category['name']}"

            total_title_tokens += num_tokens_from_string(str(row['title']) + " " + categories)
            total_overview_tokens += num_tokens_from_string(str(row['overview']))

            # Concatenate 'title' and 'overview' with a space in between
            concatenated_text = str(row['title']) + " " + str(row['overview']) + " " + categories

            # Generate embedding for the concatenated text
            # This is a placeholder; you'll need to adapt it to your actual model's API
            embedding = get_embedding(concatenated_text)
            #print(len(embedding))

            # Append the generated embedding to the list
            embeddings.append(embedding)

        # Convert the list of embeddings to a pandas Series and assign it as a new column in the DataFrame
        df['embeddings'] = embeddings

        # Save the DataFrame with embeddings to a file
        df.to_pickle(file_name)

        # Set df_with_embeddings to the modified df
        df_with_embeddings = df

    combined_total_tokens = total_title_tokens + total_overview_tokens

    # End time
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time

    print(f"The operation took {duration} seconds.")

    print(f"Title count : {total_title_tokens}")
    print(f"Overview count : {total_overview_tokens}")
    print(f"Total count : {combined_total_tokens}")

    return df_with_embeddings


df = parser.read_df_from_csv()
#count_tokens(df)
df_2 = df[:2]
# df_w_embeddings = create_embeddings(df)
count_tokens(df)
# print(df_w_embeddings)
