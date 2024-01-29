import os
from scripts import parser
import time


def search_full_title_and_overview(dataframe, search_query="Godfather"):
    print(f"Search query : {search_query}")
    movies = set()
    start_time = time.time()
    for index, row in dataframe.iterrows():
        # if lower case title contains search term, add to list of movies with that search term in the title.
        if (isinstance(row['title'], str) and search_query.lower() in row['title'].lower()) or (isinstance(row['overview'], str) and search_query.lower() in row['overview'].lower()):
            movies.add(row['title'])

    # End time
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time

    print(f"The operation took {duration} seconds.")

    return movies



df = parser.read_df_from_csv()

print(f"\nNumber of titles : {len(df)}\n")

print(f"Result : {search_full_title_and_overview(df)}\n")

print(f"Result : {search_full_title_and_overview(df, 'God father')}\n")

print(f"Result : {search_full_title_and_overview(df, 'The Godfather')}\n")

print(f"Result : {search_full_title_and_overview(df, 'Man of Steel')}\n")
