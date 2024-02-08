from elasticsearch import Elasticsearch, BadRequestError
from dotenv import load_dotenv
import os
from scripts import parser
import pandas as pd
import time

load_dotenv()

url = os.getenv("URL")
port = os.getenv("PORT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

index_name = "movies"
index_body = {
    "settings": {
        "analysis": {
          "analyzer": {
            "my_shingle_analyzer": {
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "my_shingles_filter"
              ]
            }
          },
          "filter": {
            "my_shingles_filter": {
              "type": "shingle",
            }
          }
        }
      },
    "mappings": {
        "dynamic": "strict",
        "properties": {
              "title": {
                "type": "text",
                "analyzer": "my_shingle_analyzer",
                "norms": "false"
              },
              "overview": {
                "type": "text",
              }
        }
    }
}

es = Elasticsearch(
    [f"https://{url}:{port}"],
    basic_auth=(username, password),
    verify_certs=True,
    ca_certs="./http_ca.crt"
)


def check_elasticsearch_instance():

    if es.ping():
        print("Elasticsearch instance is running.")
    else:
        print("Elasticsearch instance is not running.")


def create_index():
    try:
        # Attempt to create the index
        response = es.indices.create(index=index_name, body=index_body)
        print(f"Index {index_name} created successfully.")
    except BadRequestError as e:
        if 'resource_already_exists_exception' in str(e):
            # If the index already exists, log it and move on
            print(f"Index {index_name} already exists. Moving on.")
        else:
            # If the exception is due to another reason, you might want to re-raise it
            raise


def index_documents(df):
    start_time = time.time()
    response = es.count(index=index_name, body={"query": {"match_all": {}}})
    if response["count"] >= len(df):
        print("Already indexed")
        return

    print(f"Indexing {len(df)} titles and overviews....")
    for index, row in df.iterrows():
        title = row['title'] if pd.notnull(row['title']) and str(row['title']).strip() else ""
        overview = row['overview'] if pd.notnull(row['overview']) and str(row['overview']).strip() else ""
        document = {
            "title": title,
            "overview": overview
        }
        es.index(index=index_name, body=document)
    print("Documents indexed successfully.")
    # End time
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time

    print(f"The operation took {duration} seconds.")


def search_title_and_overview(search_query):
    print(f"Search query : {search_query}")
    start_time = time.time()
    search_query = {
        "query": {
            "multi_match": {
                "query": search_query,  # The text you're searching for
                "fields": ["title", "overview"],  # List of fields to search across
                "type": "best_fields"
            }
        },
        "size": 10,  # Control the number of results
        # "explain": "true"
    }

    # Execute the search query against the specified index.
    response = es.search(index=index_name, body=search_query)

    # Print the search results.
    print(response)

    # To access just the hits part which contains the search results:
    hits = response['hits']['hits']
    for hit in hits:
        print(str(hit["_source"])[:200], end="...\n")  # This prints out the source document of each hit.

    # End time
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time

    print(f"The operation took {duration} seconds.")


check_elasticsearch_instance()

df = parser.read_df_from_csv()

create_index()
index_documents(df)
search_title_and_overview('The godfather')
search_title_and_overview('godfather')
search_title_and_overview('God father')
search_title_and_overview('Man of Steel')
