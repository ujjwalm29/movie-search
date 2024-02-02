import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
import time
from nltk import word_tokenize
from nltk.corpus import stopwords
from scripts import parser
import numpy as np

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
file_path_vectorizer = 'tfidf_vectorizer.pkl'
file_path_vectorizer_overview = 'tfidf_vectorizer_overview.pkl'

# Initialize TF-IDF Vectorizer for bigrams
vectorizer_title = TfidfVectorizer(ngram_range=(2, 2))
vectorizer_overview = TfidfVectorizer(ngram_range=(2, 2))


def lemmatize(text):
    # Check if the text is a string
    if not isinstance(text, str):
        return ""
    lemmatizer = WordNetLemmatizer()
    # stemmer = PorterStemmer()
    tokens = word_tokenize(text)
    return ' '.join([lemmatizer.lemmatize(token) for token in tokens])


def lemmatize_and_remove_stop_words(text):
    # Check if the text is a string
    if not isinstance(text, str):
        return ""

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)

    # Lemmatize and remove stop words
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.lower() not in stop_words]

    return ' '.join(lemmatized_tokens)


def create_tfidf_embeddings_title(df):
    # Preprocess titles
    df['processed_title'] = df['title'].apply(lambda x: lemmatize(x.lower() if isinstance(x, str) else x))

    tfidf_matrix = vectorizer_title.fit_transform(df['processed_title'])

    return tfidf_matrix


def create_tfidf_embeddings_overview(df):
    # Preprocess titles
    df['processed_overview'] = df['overview'].apply(lambda x: lemmatize_and_remove_stop_words(x.lower() if isinstance(x, str) else x))

    tfidf_matrix = vectorizer_overview.fit_transform(df['processed_overview'])

    return tfidf_matrix


# Function to search and apply BM25
def search_and_rank(query, df, tfidf_matrix_title, tfidf_matrix_overview):
    print(f"Search query : {query}")
    start_time = time.time()

    # Convert the query to a TF-IDF vector for title and overview
    query_vector_title = vectorizer_title.transform([lemmatize(query)])
    query_vector_overview = vectorizer_overview.transform([lemmatize_and_remove_stop_words(query)])

    # Compute similarities for title and overview
    similarities_title = np.dot(tfidf_matrix_title, query_vector_title.T).toarray().ravel()
    similarities_overview = np.dot(tfidf_matrix_overview, query_vector_overview.T).toarray().ravel()

    # Get top 10 scores in similarities_title and similarities_overview
    top_scores_title = np.sort(similarities_title)[::-1][:10]
    top_scores_overview = np.sort(similarities_overview)[::-1][:10]

    print("Top 10 scores in similarities_title:", top_scores_title)
    print("Top 10 scores in similarities_overview:", top_scores_overview)

    # Combine the similarities
    combined_similarities = similarities_title + similarities_overview

    # Get top 10 indices
    top_indices = np.argsort(combined_similarities)[::-1][:10]

    # Retrieve the original titles
    top_titles = df.iloc[top_indices]['title'].tolist()

    # End time
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time

    print(f"The operation took {duration} seconds.")

    return top_titles


df = parser.read_df_from_csv()

tfidf_matrix_title = create_tfidf_embeddings_title(df)
tfidf_matrix_overview = create_tfidf_embeddings_overview(df)

print(f"Results : {search_and_rank('the godfather', df, tfidf_matrix_title, tfidf_matrix_overview)}\n")
print(f"Results : {search_and_rank('godfather', df, tfidf_matrix_title, tfidf_matrix_overview)}\n")
print(f"Results : {search_and_rank('God father', df, tfidf_matrix_title, tfidf_matrix_overview)}\n")
print(f"Results : {search_and_rank('Man of Steel', df, tfidf_matrix_title, tfidf_matrix_overview)}\n")

