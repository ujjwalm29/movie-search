import faiss
from scripts import parser
from level_5_openai_embeddings_MRL import embeddings_util
import numpy as np
import time


def perform_ivf_search(df, index, search_query):

    print(f"Search query : {search_query}")
    embedding_np = np.array([embeddings_util.get_embedding(search_query)], dtype='float32')

    start_time = time.time()
    D, I = index.search(embedding_np, 10)

    # End time
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time

    titles = []  # Create an empty list to hold the titles

    for i in I[0]:  # Assuming I is a 2D array, iterate over the first row
        titles.append(df.iloc[i]["title"])

    print(f"The operation took {duration} seconds.")
    print(titles)
    print("")


def get_IVF_index(df):
    # Assuming df['embeddings'] contains your embeddings
    embedding_dim = len(df.iloc[0]['embeddings'])

    # Create a quantizer with the L2 metric
    quantizer = faiss.IndexFlatL2(embedding_dim)

    nlist = 100  # Number of clusters; adjust based on your dataset size and needs
    index = faiss.IndexIVFFlat(quantizer, embedding_dim, nlist, faiss.METRIC_INNER_PRODUCT)

    embeddings_matrix = np.stack(df['embeddings'].values)
    index.train(embeddings_matrix)

    index.nprobe = 10

    index.add(embeddings_matrix)

    return index


df = parser.get_dataframe_from_pkl_file("../df_with_openai_embeddings_full.pkl")
index = get_IVF_index(df)
perform_ivf_search(df, index, "scary movie")

perform_ivf_search(df, index, "the godfather")
perform_ivf_search(df, index, "godfather")
perform_ivf_search(df, index, "God father")
perform_ivf_search(df, index, "Man of Steel")
perform_ivf_search(df, index, "flying super hero")