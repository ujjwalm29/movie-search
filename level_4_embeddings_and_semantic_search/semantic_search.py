from sentence_transformers import SentenceTransformer
from scripts import parser
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ast

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # 8 minutes
model_2_large = SentenceTransformer('thenlper/gte-large')   # 30 minutes


def create_embeddings(df, model_to_use, file_name='df_with_embeddings.pkl', ):
    # Check if the file exists
    if os.path.isfile(file_name):
        # Load DataFrame from the file
        df_with_embeddings = pd.read_pickle(file_name)
    else:
        # Concatenate 'title' and 'overview' with a space in between
        concatenated_texts = df['title'].astype(str) + " " + df['overview'].astype(str)

        # Generate embeddings
        embeddings = model_to_use.encode(concatenated_texts, show_progress_bar=True)

        # Convert embeddings to a pandas Series and name the column 'embeddings'
        df['embeddings'] = list(embeddings)

        # Save the DataFrame with embeddings to a file
        df.to_pickle(file_name)

        # Set the df_with_embeddings to df
        df_with_embeddings = df

    return df_with_embeddings


def search_and_rank(query, model_to_use, df):
    print(f"Search query : {query}")
    # Generate the embedding for the query
    query_embedding = model_to_use.encode([query])

    # Convert the 'embeddings' column back to numpy array
    df_embeddings = np.array(df['embeddings'].tolist())

    # Calculate similarities (cosine similarity)
    similarities = cosine_similarity(query_embedding, df_embeddings).flatten()

    # Get the indices of the top 10 most similar entries
    top_indices = np.argsort(similarities)[::-1][:10]

    # Get the titles of the top 10 results
    top_titles = df.iloc[top_indices]['title']

    return top_titles.tolist()


df = parser.read_df_from_csv()
df_w_embeddings = create_embeddings(df, model, 'df_with_embeddings.pkl')

print(f"Results : {search_and_rank('the godfather', model, df_w_embeddings)}\n")
print(f"Results : {search_and_rank('godfather', model, df_w_embeddings)}\n")
print(f"Results : {search_and_rank('God father', model, df_w_embeddings)}\n")
print(f"Results : {search_and_rank('Man of Steel', model, df_w_embeddings)}\n")
print(f"Results : {search_and_rank('flying super hero', model, df_w_embeddings)}\n")

df_w_embeddings = create_embeddings(df, model_2_large, 'df_with_embeddings_large.pkl')

print(f"Results : {search_and_rank('the godfather', model_2_large, df_w_embeddings)}\n")
print(f"Results : {search_and_rank('godfather', model_2_large, df_w_embeddings)}\n")
print(f"Results : {search_and_rank('God father', model_2_large, df_w_embeddings)}\n")
print(f"Results : {search_and_rank('Man of Steel', model_2_large, df_w_embeddings)}\n")
print(f"Results : {search_and_rank('flying super hero', model_2_large, df_w_embeddings)}\n")


