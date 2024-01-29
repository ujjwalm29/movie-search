import os
from scripts import parser
from level_2_preprocessing_tfidf_ranked import tfidf

raw_path = os.path.join(os.getcwd(), 'data/raw_files/dataset2/movies_metadata.csv')

df = parser.read_df_from_csv(raw_path)

print(df.columns)
print(len(df))

tfidf_matrix_title = tfidf.create_tfidf_embeddings_title(df)
tfidf_matrix_overview = tfidf.create_tfidf_embeddings_overview(df)
titles = tfidf.search_and_rank("the godfather", df, tfidf_matrix_title, tfidf_matrix_overview)
print(titles)

titles = tfidf.search_and_rank("the god father", df, tfidf_matrix_title, tfidf_matrix_overview)

print(titles)

print(f"Result : {tfidf.search_and_rank('Man of Steel', df, tfidf_matrix_title, tfidf_matrix_overview)}")
