import time
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from embeddings_util import get_embedding
from scripts import parser


def search_and_rank_without_MRL(query, df):

    print(f"Search query : {query}")
    # Generate the embedding for the query
    query_embedding = get_embedding(query)
    query_embedding_arr = np.array(query_embedding)


    # Convert the 'embeddings' column back to numpy array
    df_embeddings = np.array(df['embeddings'].tolist())

    start_time = time.time()
    # Calculate similarities (cosine similarity)
    similarities = cosine_similarity(query_embedding_arr.reshape(1, -1), df_embeddings).flatten()

    # Get the indices of the top 10 most similar entries
    top_indices = np.argsort(similarities)[::-1][:10]

    # Get the titles of the top 10 results
    top_titles = df.iloc[top_indices]['title']

    # End time
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time

    print(f"The operation took {duration} seconds.")

    return top_titles.tolist()


def search_and_rank_with_MRL(query, df):

    print(f"Search query : {query}")
    # Generate the embedding for the query
    query_embedding = get_embedding(query)
    query_embedding_arr_short = np.array(normalize_l2(query_embedding[:256]))

    # Phase 1
    # Convert the 'embeddings' column back to numpy array
    df_embeddings = np.array(df['normalized_embeddings'].tolist())

    start_time = time.time()
    # Calculate similarities (cosine similarity)
    similarities = cosine_similarity(query_embedding_arr_short.reshape(1, -1), df_embeddings).flatten()

    # Get the indices of the top 20 most similar entries
    top_indices_unranked = np.argsort(similarities)[::-1][:20]

    # Phase 2
    top_unranked_embeddings = np.array(df.iloc[top_indices_unranked]['embeddings'].tolist())
    refined_similarities = cosine_similarity(np.array(query_embedding).reshape(1, -1), top_unranked_embeddings).flatten()

    # Get the indices of the top 10 most similar entries, based on refined similarities
    top_indices = top_indices_unranked[np.argsort(refined_similarities)[::-1][:10]]

    # Get the titles of the top 10 results
    top_titles = df.iloc[top_indices]['title']

    # End time
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time

    print(f"The operation took {duration} seconds.")

    return top_titles.tolist()


def normalize_l2(x):
    x = np.array(x)
    if x.ndim == 1:
        norm = np.linalg.norm(x)
        if norm == 0:
            return x
        return x / norm
    else:
        norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
        return np.where(norm == 0, x, x / norm)


def get_short_embeddings(df_w_embeddings):
    df_w_embeddings['normalized_embeddings'] = df_w_embeddings['embeddings'].apply(lambda x: normalize_l2(x[:256]))
    return df_w_embeddings


df_w_embeddings = parser.get_dataframe_from_pkl_file("../df_with_openai_embeddings_full.pkl")

print(len(df_w_embeddings))

df_w_short_embedding = get_short_embeddings(df_w_embeddings)

# One initial random search to load everything into memory
print(f"Results : {search_and_rank_without_MRL('scary movie', df_w_embeddings)}\n")

print(f"Results : {search_and_rank_with_MRL('the godfather', df_w_embeddings)}\n")
print(f"Results : {search_and_rank_with_MRL('godfather', df_w_embeddings)}\n")
print(f"Results : {search_and_rank_with_MRL('God father', df_w_embeddings)}\n")
print(f"Results : {search_and_rank_with_MRL('Man of Steel', df_w_embeddings)}\n")
print(f"Results : {search_and_rank_with_MRL('flying super hero', df_w_embeddings)}\n")

print(f"Results : {search_and_rank_without_MRL('the godfather', df_w_embeddings)}\n")
print(f"Results : {search_and_rank_without_MRL('godfather', df_w_embeddings)}\n")
print(f"Results : {search_and_rank_without_MRL('God father', df_w_embeddings)}\n")
print(f"Results : {search_and_rank_without_MRL('Man of Steel', df_w_embeddings)}\n")
print(f"Results : {search_and_rank_without_MRL('flying super hero', df_w_embeddings)}\n")



