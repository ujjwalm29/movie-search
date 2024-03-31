from elasticsearch import Elasticsearch, BadRequestError
import time
import pandas as pd
from level_3_elasticsearch_relevance_tuning.config import get_es_config

es_config = get_es_config()
es = Elasticsearch(
    [f"https://{es_config['url']}:{es_config['port']}"],
    basic_auth=(es_config['username'], es_config['password']),
    verify_certs=True,
    ca_certs="./http_ca.crt"
)
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


def check_elasticsearch_instance():

    if es.ping():
        print("Elasticsearch instance is running.")
    else:
        print("Elasticsearch instance is not running.")


def create_index(index_name=index_name, body=index_body):
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


def index_documents(df, index_name=index_name):
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


def search(body, index_name=index_name):
    return es.search(index=index_name, body=body)