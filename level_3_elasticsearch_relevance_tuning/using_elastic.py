from elasticsearch_operations import check_elasticsearch_instance, create_index, index_documents, search
from dotenv import load_dotenv
import os
from scripts import parser
import time

load_dotenv()


def search_title_and_overview(search_query):
    print(f"Search query : {search_query}\n")
    start_time = time.time()
    # search_query_es = {
    #     "query": {
    #         "multi_match": {
    #             "query": search_query,  # The text you're searching for
    #             "fields": ["title", "overview"],  # List of fields to search across
    #             "type": "best_fields"
    #         }
    #     },
    #     "size": 10,  # Control the number of results
    # }

    # search_query_es = {
    #   "query": {
    #     "match": {
    #       "title": {
    #         "query": search_query,
    #         "fuzziness": "AUTO",
    #         "prefix_length": "1"
    #       }
    #     }
    #   }
    # }

    search_query_es = {
      "query": {
        "dis_max": {
          "queries": [
            {
              "match": {
                "title": {
                  "query": search_query,
                  "fuzziness": "AUTO"
                }
              }
            },
            {
              "match": {
                "overview": {
                  "query": search_query,
                  "boost": 1.3
                }
              }
            }
          ],
          "tie_breaker": 0.1
        }
      }
    }



    # Execute the search query against the specified index.
    response = search(search_query_es)

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
# search_title_and_overview('The godfather')
# search_title_and_overview('godfather')
# search_title_and_overview('God father')
# search_title_and_overview('Man of Steel')

search_title_and_overview('Man of Steel')
search_title_and_overview('the godafther')
search_title_and_overview('the godfather')

