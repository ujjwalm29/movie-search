from level_3_elasticsearch_relevance_tuning.elasticsearch_operations import (check_elasticsearch_instance, create_index,
                                                                             index_documents, search)
from scripts import parser
import time


def get_should_clause(term, boost):
    return {
            "match": {
                "overview": {
                    "query": term,
                    "boost": boost
                }
            }
        }


def query_expansion(query: str):
    search_body = {
        "query": {
            "match": {"overview": query}
        },
        "aggregations": {
            "my_sample": {
                "sampler": {
                    "shard_size": 200
                },
                "aggregations": {
                    "keywords": {
                        "significant_text": {"field": "overview"}
                    }
                }
            }
        }
    }

    results = search(search_body)

    # print(results)

    expanded_query = []
    boost = 0.3

    for bucket in results['aggregations']['my_sample']['keywords']['buckets'][1:3]:
        should_clause = get_should_clause(bucket['key'], boost)

        expanded_query.append(should_clause)
        boost /= 2


    return expanded_query


def search_title_and_overview(search_query, expanded_query):
    print(f"\nSearch query : {search_query}")
    print(f"Expanded query : {expanded_query}")
    start_time = time.time()

    search_query_es = {
        "query": {
            "bool": {
                "should": [
                    {
                        "dis_max": {
                            "queries": [
                                {"match": {"title": {"query": search_query, "fuzziness": "AUTO"}}},
                                {"match": {"overview": {"query": search_query, "boost": 1.3}}}
                            ],
                            "tie_breaker": 0.1
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        }
    }

    search_query_es['query']['bool']['should'].extend(expanded_query)

    # print(search_query_es)

    # Execute the search query against the specified index.
    response = search(search_query_es)

    # Print the search results.
    # print(response)

    # To access just the hits part which contains the search results:
    hits = response['hits']['hits']
    for hit in hits:
        print(str(hit["_source"])[:200], end="...\n")  # This prints out the source document of each hit.

    # End time
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time

    print(f"The operation took {duration} seconds.")


def expand_query_and_search(query):
    expanded_query = query_expansion(query)
    search_title_and_overview(query, expanded_query)


check_elasticsearch_instance()

df = parser.read_df_from_csv()

create_index()
index_documents(df)

expand_query_and_search("Superman")
expand_query_and_search("The godfather")
expand_query_and_search("Man of Steel")
expand_query_and_search("Steel")
search_title_and_overview("Steel", [])
