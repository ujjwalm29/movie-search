import faiss
from scripts import parser
from level_5_openai_embeddings_MRL import embeddings_util
import numpy as np
import time


def perform_search(df, index, search_query):

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


def do_searches(df, index):
    queries = ["scary movie", "the godfather", "godfather", "God father", "Man of Steel", "flying super hero"]

    for query in queries:
        perform_search(df, index, query)


def get_IVF_index(df):
    # Assuming df['embeddings'] contains your embeddings
    embedding_dim = len(df.iloc[0]['embeddings'])

    start_time = time.time()

    # Create a quantizer with the cosine_sim metric
    quantizer = faiss.IndexFlatIP(embedding_dim)

    nlist = 100  # Number of clusters; adjust based on your dataset size and needs
    index = faiss.IndexIVFFlat(quantizer, embedding_dim, nlist, faiss.METRIC_INNER_PRODUCT)

    embeddings_matrix = np.stack(df['embeddings'].values)
    index.train(embeddings_matrix)

    index.nprobe = 10

    index.add(embeddings_matrix)

    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"The index creation took {duration} seconds.")

    return index


def get_PQ_index(df, m=8, bits=8):
    embedding_dim = len(df.iloc[0]['embeddings'])

    start_time = time.time()

    # m is Number of sub-vector quantizers
    # bits is Number of bits per sub-vector quantizer
    index = faiss.IndexPQ(embedding_dim, m, bits, faiss.METRIC_INNER_PRODUCT)

    embeddings_matrix = np.stack(df['embeddings'].values)

    index.train(embeddings_matrix)

    index.add(embeddings_matrix)

    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"The index creation took {duration} seconds.")

    return index


def get_OPQ_index(df, m=8, bits=8):
    embedding_dim = len(df.iloc[0]['embeddings'])

    start_time = time.time()

    # m is Number of sub-vector quantizers
    # bits is Number of bits per sub-vector quantizer
    pq = faiss.IndexPQ(embedding_dim, m, bits, faiss.METRIC_INNER_PRODUCT)

    embeddings_matrix = np.stack(df['embeddings'].values)

    # Wrap the PQ index with OPQ for optimized quantization
    opq = faiss.OPQMatrix(embedding_dim, m)
    index = faiss.IndexPreTransform(opq, pq)

    index.train(embeddings_matrix)

    index.add(embeddings_matrix)

    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"The index creation took {duration} seconds.")

    return index


def get_IVFPQ_index(df, m=8, nlist=100, bits=8):
    embedding_dim = len(df.iloc[0]['embeddings'])

    start_time = time.time()

    # m is Number of sub-vector quantizers
    # nlist is the number of clusters for the coarse quantizer
    # bits is Number of bits per sub-vector quantizer

    # Create a coarse quantizer for the IVF structure
    quantizer = faiss.IndexFlatIP(embedding_dim)  # Use IndexFlatL2 for L2 metric

    # Combine OPQ and PQ with the IVF quantizer to create an IVFOPQ index
    index = faiss.IndexIVFPQ(quantizer, embedding_dim, nlist, m, bits, faiss.METRIC_INNER_PRODUCT)

    embeddings_matrix = np.stack(df['embeddings'].values).astype('float32')

    # Train the index
    index.train(embeddings_matrix)

    # Add embeddings to the index
    index.add(embeddings_matrix)

    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"The index creation took {duration} seconds.")

    return index



def get_IVFOPQ_index(df, m=8, nlist=100, bits=8):
    embedding_dim = len(df.iloc[0]['embeddings'])

    start_time = time.time()

    # m is Number of sub-vector quantizers
    # nlist is the number of clusters for the coarse quantizer
    # bits is Number of bits per sub-vector quantizer

    index = faiss.index_factory(embedding_dim, f"OPQ{m},IVF{nlist},PQ{m}x{bits}", faiss.METRIC_INNER_PRODUCT)

    embeddings_matrix = np.stack(df['embeddings'].values).astype('float32')

    opq = faiss.OPQMatrix(embedding_dim, m)
    index = faiss.IndexPreTransform(opq, index)

    # Since we're using METRIC_INNER_PRODUCT, ensure embeddings are normalized
    faiss.normalize_L2(embeddings_matrix)

    # Train the index
    index.train(embeddings_matrix)

    # Add embeddings to the index
    index.add(embeddings_matrix)

    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"The index creation took {duration} seconds.")

    return index


def get_HNSW_index(df, M=32):
    embedding_dim = len(df.iloc[0]['embeddings'])

    start_time = time.time()

    # m is Number of sub-vector quantizers
    # bits is Number of bits per sub-vector quantizer
    index = faiss.IndexHNSWFlat(embedding_dim, M)

    embeddings_matrix = np.stack(df['embeddings'].values)

    index.hnsw.efConstruction = 256

    index.add(embeddings_matrix)

    index.hnsw.efSearch = 128

    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"The index creation took {duration} seconds.")

    return index


df = parser.get_dataframe_from_pkl_file("../df_with_openai_embeddings_full.pkl")

# index = get_IVF_index(df)
# do_searches(df, index)
#
# index_pq = get_PQ_index(df)
# do_searches(df, index_pq)
#
# index_pq = get_PQ_index(df, 64, 8)
# do_searches(df, index_pq)
#
# index_pq = get_PQ_index(df, 64, 9)
# do_searches(df, index_pq)
#
# index_pq = get_PQ_index(df, 128, 9)
# do_searches(df, index_pq)
#
# index_pq = get_PQ_index(df, 128, 10)
# do_searches(df, index_pq)

# index_opq = get_OPQ_index(df, 64, 8)
# do_searches(df, index_opq)

# index_ivfpq = get_IVFPQ_index(df, 64, 100, 8)
# do_searches(df, index_ivfpq)

index_hnsw = get_HNSW_index(df, 32)
do_searches(df, index_hnsw)
