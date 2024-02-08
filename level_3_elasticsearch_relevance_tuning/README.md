# Elasticsearch and relevance tuning (Under construction)


blah blah blah

Took 2.5 minutes to index

Index body : 
```
index_body = {
    "mappings": {
        "dynamic": "strict",
        "properties": {
              "title": {
                "type": "text"
              },
              "overview": {
                "type": "text"
              }
        }
    }
}
```

Query : 
```
search_query = {
    "query": {
        "multi_match": {
            "query": search_query,  # The text you're searching for
            "fields": ["title", "overview"],  # List of fields to search across
            "type": "most_fields"
        }
    },
    "size": 10,  # Control the number of results
}
```

Output :

```
{'title': 'Disco Godfather', 'overview': 'A retired cop becomes a DJ/celebrity at the Blueberry Hill disco-- he\'s the "Disco Godfather!" All is well until his nephew flips out on a strange new drug that\'s sweeping the streets, called "angel dust," or PCP. Disco Godfather vows "to personally come down on the suckers that\'s producing this shit!" He takes to the streets, slaps drug dealers and even exposes a crooked cop that is covering for the dealers. In between, he still finds time to manage the Blueberry Hill and perform. "Put a little slide in yo\' glide," he pleads to the patrons, "Put some weight on it!" Disco Godfather tracks down the kingpin that is behind all the angel dust production, but not before he is kidnapped and forced to inhale PCP through a gas mask!'}
{'title': 'Onimasa: A Japanese Godfather', 'overview': 'Onimasa is the egocentric boss of a small yakuza clan on Shikoku Island, whose criminal duties conflict with his self-image as a chivalrous samurai. His struggles with his boss, the Shikoku Godfather, and the tumultuous life of his adopted daughter, Matsue, form the backdrop of this epic tale of justice, obedience, and bloody vengeance.'}
{'title': 'Godfather', 'overview': 'The story of Anjooran (N. N. Pillai), and his four sons Balaraman (Thilakan), Swaminathan (Innocent), Premachandran (Bheeman Raghu) and Ramabhadran (Mukesh) are in severe enmity with the Anappara family.'}
{'title': 'The Godfather', 'overview': 'Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barely survives an attempt on his life, his youngest son, Michael steps in to take care of the would-be killers, launching a campaign of bloody revenge.'}
{'title': 'The Nutcracker: The Untold Story', 'overview': "Set in 1920's Vienna, this a tale of a little girl, whose godfather gives her a special doll one Christmas Eve."}
{'title': 'I Knew It Was You: Rediscovering John Cazale', 'overview': "John Cazale was in only five films - The Godfather, The Conversation, The Godfather, Part Two, Dog Day Afternoon, and The Deer Hunter - each was nominated for Best Picture. Yet today most people don't even know his name. I KNEW IT WAS YOU is a fresh tour through movies that defined a generation."}
{'title': "Jane Austen's Mafia!", 'overview': 'Takeoff on the Godfather with the son of a mafia king taking over for his dying father.'}
{'title': 'The Last Godfather', 'overview': "Young-goo the son of mafia boss Don Carini, is too foolish to be part of the mafia elite. One day, Young-goo comes to his father and is trained by Tony V to be his father's successor. A few days later, Young-goo accidentally rescues Nancy, the only daughter of Don Bonfante, the boss of a rival mafia family. But Vinnie, an under-boss of the Bonfante family kidnapped her and fabricates that Young-goo has taken her. Vinnie's behavior provokes an armed conflict between the two families."}
{'title': 'C(r)ook', 'overview': 'A killer for the Russian Mafia in Vienna wants to retire and write a book about his passion - cooking. The mafia godfather suspects treason.'}
{'title': 'Bright Eyes', 'overview': 'An orphaned girl is taken in by a snobbish family at the insistence of their rich, crotchety uncle, even as her devoted aviator godfather fights for custody.'}
The operation took 0.018507003784179688 seconds.
```

This is good but we don't see all the godfather movies.

Let's apply a boost to the title.

Change the query to : 
```
"fields": ["title^10", "overview"]
```

Results : 
```
{'took': 13, 'timed_out': False, '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, 'hits': {'total': {'value': 10000, 'relation': 'gte'}, 'max_score': 118.34159, 'hits': [{'_index': 'movies', '_id': '0t5MhY0BZNRj-difj00b', '_score': 118.34159, '_source': {'title': 'Godfather', 'overview': 'The story of Anjooran (N. N. Pillai), and his four sons Balaraman (Thilakan), Swaminathan (Innocent), Premachandran (Bheeman Raghu) and Ramabhadran (Mukesh) are in severe enmity with the Anappara family.'}}, {'_index': 'movies', '_id': 'CN1KhY0BZNRj-dif3M-C', '_score': 113.91931, '_source': {'title': 'The Godfather', 'overview': 'Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barely survives an attempt on his life, his youngest son, Michael steps in to take care of the would-be killers, launching a campaign of bloody revenge.'}}, {'_index': 'movies', '_id': 'KN5MhY0BZNRj-difBCLd', '_score': 108.79006, '_source': {'title': 'Disco Godfather', 'overview': 'A retired cop becomes a DJ/celebrity at the Blueberry Hill disco-- he\'s the "Disco Godfather!" All is well until his nephew flips out on a strange new drug that\'s sweeping the streets, called "angel dust," or PCP. Disco Godfather vows "to personally come down on the suckers that\'s producing this shit!" He takes to the streets, slaps drug dealers and even exposes a crooked cop that is covering for the dealers. In between, he still finds time to manage the Blueberry Hill and perform. "Put a little slide in yo\' glide," he pleads to the patrons, "Put some weight on it!" Disco Godfather tracks down the kingpin that is behind all the angel dust production, but not before he is kidnapped and forced to inhale PCP through a gas mask!'}}, {'_index': 'movies', '_id': 'O95LhY0BZNRj-dif8Bue', '_score': 98.45302, '_source': {'title': 'The Last Godfather', 'overview': "Young-goo the son of mafia boss Don Carini, is too foolish to be part of the mafia elite. One day, Young-goo comes to his father and is trained by Tony V to be his father's successor. A few days later, Young-goo accidentally rescues Nancy, the only daughter of Don Bonfante, the boss of a rival mafia family. But Vinnie, an under-boss of the Bonfante family kidnapped her and fabricates that Young-goo has taken her. Vinnie's behavior provokes an armed conflict between the two families."}}, {'_index': 'movies', '_id': 'YN1KhY0BZNRj-dif4dBE', '_score': 86.69548, '_source': {'title': 'The Godfather: Part II', 'overview': 'In the continuing saga of the Corleone crime family, a young Vito Corleone grows up in Sicily and in 1910s New York. In the 1950s, Michael Corleone attempts to expand the family business into Las Vegas, Hollywood and Cuba.'}}, {'_index': 'movies', '_id': 'QN1KhY0BZNRj-dif69N-', '_score': 86.593216, '_source': {'title': 'The Godfather: Part III', 'overview': 'In the midst of trying to legitimize his business dealings in 1979 New York and Italy, aging mafia don, Michael Corleone seeks forgiveness for his sins while taking a young protege under his wing.'}}, {'_index': 'movies', '_id': 'Zt5MhY0BZNRj-difzWAk', '_score': 83.33334, '_source': {'title': 'Onimasa: A Japanese Godfather', 'overview': 'Onimasa is the egocentric boss of a small yakuza clan on Shikoku Island, whose criminal duties conflict with his self-image as a chivalrous samurai. His struggles with his boss, the Shikoku Godfather, and the tumultuous life of his adopted daughter, Matsue, form the backdrop of this epic tale of justice, obedience, and bloody vengeance.'}}, {'_index': 'movies', '_id': 'xN5NhY0BZNRj-difH3d_', '_score': 77.46196, '_source': {'title': 'The Godfather Trilogy: 1972-1990', 'overview': 'The multigenerational saga of the rise and fall of the Corleone crime family.'}}, {'_index': 'movies', '_id': 'rd5MhY0BZNRj-difBiJt', '_score': 23.972761, '_source': {'title': 'The Nutcracker: The Untold Story', 'overview': "Set in 1920's Vienna, this a tale of a little girl, whose godfather gives her a special doll one Christmas Eve."}}, {'_index': 'movies', '_id': 'DN1LhY0BZNRj-difReuc', '_score': 21.39139, '_source': {'title': 'The Nest', 'overview': 'Laborie is a high-flying officer in the French special forces. Her mission is to escort Abedin Nexhep, a godfather of the Albanian mafia. Charged with heading a wide-reaching prostitution network, this formidable criminal is due to stand trial before a European court. During the transfer, killers hired by Nexhep set up an ambush to free their boss but Laborie and her men manage to escape...'}}]}}
{'title': 'Godfather', 'overview': 'The story of Anjooran (N. N. Pillai), and his four sons Balaraman (Thilakan), Swaminathan (Innocent), Premachandran (Bheeman Raghu) and Ramabhadran (Mukesh) are in ...
{'title': 'The Godfather', 'overview': 'Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barel...
{'title': 'Disco Godfather', 'overview': 'A retired cop becomes a DJ/celebrity at the Blueberry Hill disco-- he\'s the "Disco Godfather!" All is well until his nephew flips out on a strange new drug t...
{'title': 'The Last Godfather', 'overview': "Young-goo the son of mafia boss Don Carini, is too foolish to be part of the mafia elite. One day, Young-goo comes to his father and is trained by Tony V t...
{'title': 'The Godfather: Part II', 'overview': 'In the continuing saga of the Corleone crime family, a young Vito Corleone grows up in Sicily and in 1910s New York. In the 1950s, Michael Corleone att...
{'title': 'The Godfather: Part III', 'overview': 'In the midst of trying to legitimize his business dealings in 1979 New York and Italy, aging mafia don, Michael Corleone seeks forgiveness for his sin...
{'title': 'Onimasa: A Japanese Godfather', 'overview': 'Onimasa is the egocentric boss of a small yakuza clan on Shikoku Island, whose criminal duties conflict with his self-image as a chivalrous samu...
{'title': 'The Godfather Trilogy: 1972-1990', 'overview': 'The multigenerational saga of the rise and fall of the Corleone crime family.'}...
{'title': 'The Nutcracker: The Untold Story', 'overview': "Set in 1920's Vienna, this a tale of a little girl, whose godfather gives her a special doll one Christmas Eve."}...
{'title': 'The Nest', 'overview': 'Laborie is a high-flying officer in the French special forces. Her mission is to escort Abedin Nexhep, a godfather of the Albanian mafia. Charged with heading a wide...
```

Much better! But still, my query is "The Godfather", why aren't "The Godfather" movies bubbling up?

Guess what we are going to use to fix this? Bigrams. Bigrams are like pizza. I love pizza.

Anyway, introducing bigrams is not quite straightforward as vanilla python. Elasticsearch uses something called analyzers to index data. Think of an analyzer as a set of instructions or preprocesses that the input goes through before getting indexed.

[This](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-shingle-tokenfilter.html) page in the Elasticsearch docs explains how to setup the "shingles" analyzer for a field.

Now, our index structure looks like this :

```
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
                "analyzer": "my_shingle_analyzer"
              },
              "overview": {
                "type": "text"
              }
        }
    }
}
```

I used the [standard analyzer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-analyzer.html) and added an additional filter `my_shingles_filter` on top of it. The my_shingles_filter is defined just below that.

Let's reindex the data and see the results : 

```
{'title': 'The Godfather', 'overview': 'Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barel...
{'title': 'Godfather', 'overview': 'The story of Anjooran (N. N. Pillai), and his four sons Balaraman (Thilakan), Swaminathan (Innocent), Premachandran (Bheeman Raghu) and Ramabhadran (Mukesh) are in ...
{'title': 'Disco Godfather', 'overview': 'A retired cop becomes a DJ/celebrity at the Blueberry Hill disco-- he\'s the "Disco Godfather!" All is well until his nephew flips out on a strange new drug t...
{'title': 'The Last Godfather', 'overview': "Young-goo the son of mafia boss Don Carini, is too foolish to be part of the mafia elite. One day, Young-goo comes to his father and is trained by Tony V t...
{'title': 'The Godfather: Part II', 'overview': 'In the continuing saga of the Corleone crime family, a young Vito Corleone grows up in Sicily and in 1910s New York. In the 1950s, Michael Corleone att...
{'title': 'The Godfather: Part III', 'overview': 'In the midst of trying to legitimize his business dealings in 1979 New York and Italy, aging mafia don, Michael Corleone seeks forgiveness for his sin...
{'title': 'The Godfather Trilogy: 1972-1990', 'overview': 'The multigenerational saga of the rise and fall of the Corleone crime family.'}...
{'title': 'Onimasa: A Japanese Godfather', 'overview': 'Onimasa is the egocentric boss of a small yakuza clan on Shikoku Island, whose criminal duties conflict with his self-image as a chivalrous samu...
{'title': 'The Nutcracker: The Untold Story', 'overview': "Set in 1920's Vienna, this a tale of a little girl, whose godfather gives her a special doll one Christmas Eve."}...
{'title': 'The Nest', 'overview': 'Laborie is a high-flying officer in the French special forces. Her mission is to escort Abedin Nexhep, a godfather of the Albanian mafia. Charged with heading a wide...
```

Hmm, it's a little better. The actual "The Godfather" is the first search result. "The Godfather Trilogy: 1972-1990" is 1 position up.

But still, I want the Part II and Part III movies to be at the top.

Elasticsearch has debugging capabilities. If you set the option `explain: "True"` in the query, the elasticsearch response will have an in depth explanation of how Apache Lucene(the udnerlying tech of ES) scored the results.
I am not going to paste the debugging json since it's extremely verbose. I encourage you to give it a shot.

After looking at the debugging output, my understanding is that "The Godfather: Part II" and "The Godfather: Part III" are being punished since the strings are of larger length than "Godfather" and "The Last Godfather". Due to how TF-IDF scoring works, a match in a longer string holds less weight. Yes, there is an extra match with the word "The", but since the word is common, it doesn't contribute much to the score.

I wonder if there's a way to _NOT_ consider the lengths of the strings while scoring...

Turns out there is!

I modified the index structure and added a "norm" = false to the title field.
```
"properties": {
      "title": {
        "type": "text",
        "analyzer": "my_shingle_analyzer",
        "norms": "false"
      },
      "overview": {
        "type": "text"
      }
}
```

Let's index and look at the results
```
{'title': 'The Godfather Trilogy: 1972-1990', 'overview': 'The multigenerational saga of the rise and fall of the Corleone crime family.'}...
{'title': 'The Godfather: Part II', 'overview': 'In the continuing saga of the Corleone crime family, a young Vito Corleone grows up in Sicily and in 1910s New York. In the 1950s, Michael Corleone att...
{'title': 'The Godfather', 'overview': 'Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barel...
{'title': 'The Godfather: Part III', 'overview': 'In the midst of trying to legitimize his business dealings in 1979 New York and Italy, aging mafia don, Michael Corleone seeks forgiveness for his sin...
{'title': 'The Last Godfather', 'overview': "Young-goo the son of mafia boss Don Carini, is too foolish to be part of the mafia elite. One day, Young-goo comes to his father and is trained by Tony V t...
{'title': 'Disco Godfather', 'overview': 'A retired cop becomes a DJ/celebrity at the Blueberry Hill disco-- he\'s the "Disco Godfather!" All is well until his nephew flips out on a strange new drug t...
{'title': 'Onimasa: A Japanese Godfather', 'overview': 'Onimasa is the egocentric boss of a small yakuza clan on Shikoku Island, whose criminal duties conflict with his self-image as a chivalrous samu...
{'title': 'Godfather', 'overview': 'The story of Anjooran (N. N. Pillai), and his four sons Balaraman (Thilakan), Swaminathan (Innocent), Premachandran (Bheeman Raghu) and Ramabhadran (Mukesh) are in ...
{'title': 'The Nutcracker: The Untold Story', 'overview': "Set in 1920's Vienna, this a tale of a little girl, whose godfather gives her a special doll one Christmas Eve."}...
{'title': "Eurocrime! The Italian Cop and Gangster Films That Ruled the '70s", 'overview': "A documentary concerning the violent Italian 'poliziotteschi' cinematic movement of the 1970s which, at firs...
The operation took 0.01680588722229004 seconds.
``` 

Let's goooooooo!!! We got all the godfather movies as the top 4 results. This was amazing!

*BUT*, we haven't seen what happens with the other queries. Let's see : 

```
Search query : The godfather
{'took': 28, 'timed_out': False, '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}, 'hits': {'total': {'value': 10000, 'relation': 'gte'}, 'max_score': 149.70709, 'hits': [{'_index': 'movies', '_id': 'xuFPho0BZNRj-difa--6', '_score': 149.70709, '_source': {'title': 'The Godfather Trilogy: 1972-1990', 'overview': 'The multigenerational saga of the rise and fall of the Corleone crime family.'}}, {'_index': 'movies', '_id': 'YuFNho0BZNRj-difCkgY', '_score': 149.6907, '_source': {'title': 'The Godfather: Part II', 'overview': 'In the continuing saga of the Corleone crime family, a young Vito Corleone grows up in Sicily and in 1910s New York. In the 1950s, Michael Corleone attempts to expand the family business into Las Vegas, Hollywood and Cuba.'}}, {'_index': 'movies', '_id': 'CuFNho0BZNRj-difBUem', '_score': 149.66008, '_source': {'title': 'The Godfather', 'overview': 'Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barely survives an attempt on his life, his youngest son, Michael steps in to take care of the would-be killers, launching a campaign of bloody revenge.'}}, {'_index': 'movies', '_id': 'QuFNho0BZNRj-difFUvG', '_score': 149.58844, '_source': {'title': 'The Godfather: Part III', 'overview': 'In the midst of trying to legitimize his business dealings in 1979 New York and Italy, aging mafia don, Michael Corleone seeks forgiveness for his sins while taking a young protege under his wing.'}}, {'_index': 'movies', '_id': 'PeFOho0BZNRj-difHJPx', '_score': 146.15224, '_source': {'title': 'The Last Godfather', 'overview': "Young-goo the son of mafia boss Don Carini, is too foolish to be part of the mafia elite. One day, Young-goo comes to his father and is trained by Tony V to be his father's successor. A few days later, Young-goo accidentally rescues Nancy, the only daughter of Don Bonfante, the boss of a rival mafia family. But Vinnie, an under-boss of the Bonfante family kidnapped her and fabricates that Young-goo has taken her. Vinnie's behavior provokes an armed conflict between the two families."}}, {'_index': 'movies', '_id': 'KuFOho0BZNRj-difNZol', '_score': 136.9802, '_source': {'title': 'Disco Godfather', 'overview': 'A retired cop becomes a DJ/celebrity at the Blueberry Hill disco-- he\'s the "Disco Godfather!" All is well until his nephew flips out on a strange new drug that\'s sweeping the streets, called "angel dust," or PCP. Disco Godfather vows "to personally come down on the suckers that\'s producing this shit!" He takes to the streets, slaps drug dealers and even exposes a crooked cop that is covering for the dealers. In between, he still finds time to manage the Blueberry Hill and perform. "Put a little slide in yo\' glide," he pleads to the patrons, "Put some weight on it!" Disco Godfather tracks down the kingpin that is behind all the angel dust production, but not before he is kidnapped and forced to inhale PCP through a gas mask!'}}, {'_index': 'movies', '_id': 'aOFPho0BZNRj-difGdiw', '_score': 135.3726, '_source': {'title': 'Onimasa: A Japanese Godfather', 'overview': 'Onimasa is the egocentric boss of a small yakuza clan on Shikoku Island, whose criminal duties conflict with his self-image as a chivalrous samurai. His struggles with his boss, the Shikoku Godfather, and the tumultuous life of his adopted daughter, Matsue, form the backdrop of this epic tale of justice, obedience, and bloody vengeance.'}}, {'_index': 'movies', '_id': '1OFOho0BZNRj-dif2MWR', '_score': 127.90725, '_source': {'title': 'Godfather', 'overview': 'The story of Anjooran (N. N. Pillai), and his four sons Balaraman (Thilakan), Swaminathan (Innocent), Premachandran (Bheeman Raghu) and Ramabhadran (Mukesh) are in severe enmity with the Anappara family.'}}, {'_index': 'movies', '_id': 'r-FOho0BZNRj-difNprz', '_score': 31.521828, '_source': {'title': 'The Nutcracker: The Untold Story', 'overview': "Set in 1920's Vienna, this a tale of a little girl, whose godfather gives her a special doll one Christmas Eve."}}, {'_index': 'movies', '_id': 'y-FOho0BZNRj-difj7Gj', '_score': 28.459045, '_source': {'title': "Eurocrime! The Italian Cop and Gangster Films That Ruled the '70s", 'overview': "A documentary concerning the violent Italian 'poliziotteschi' cinematic movement of the 1970s which, at first glance, seem to be rip-offs of American crime films like DIRTY HARRY or THE GODFATHER, but which really address Italian issues like the Sicilian Mafia and red terrorism. Perhaps even more interesting than the films themselves were the rushed methods of production (stars performing their own stunts, stealing shots, no live sound) and the bleed-over between real-life crime and movie crime."}}]}}
{'title': 'The Godfather Trilogy: 1972-1990', 'overview': 'The multigenerational saga of the rise and fall of the Corleone crime family.'}...
{'title': 'The Godfather: Part II', 'overview': 'In the continuing saga of the Corleone crime family, a young Vito Corleone grows up in Sicily and in 1910s New York. In the 1950s, Michael Corleone att...
{'title': 'The Godfather', 'overview': 'Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barel...
{'title': 'The Godfather: Part III', 'overview': 'In the midst of trying to legitimize his business dealings in 1979 New York and Italy, aging mafia don, Michael Corleone seeks forgiveness for his sin...
{'title': 'The Last Godfather', 'overview': "Young-goo the son of mafia boss Don Carini, is too foolish to be part of the mafia elite. One day, Young-goo comes to his father and is trained by Tony V t...
{'title': 'Disco Godfather', 'overview': 'A retired cop becomes a DJ/celebrity at the Blueberry Hill disco-- he\'s the "Disco Godfather!" All is well until his nephew flips out on a strange new drug t...
{'title': 'Onimasa: A Japanese Godfather', 'overview': 'Onimasa is the egocentric boss of a small yakuza clan on Shikoku Island, whose criminal duties conflict with his self-image as a chivalrous samu...
{'title': 'Godfather', 'overview': 'The story of Anjooran (N. N. Pillai), and his four sons Balaraman (Thilakan), Swaminathan (Innocent), Premachandran (Bheeman Raghu) and Ramabhadran (Mukesh) are in ...
{'title': 'The Nutcracker: The Untold Story', 'overview': "Set in 1920's Vienna, this a tale of a little girl, whose godfather gives her a special doll one Christmas Eve."}...
{'title': "Eurocrime! The Italian Cop and Gangster Films That Ruled the '70s", 'overview': "A documentary concerning the violent Italian 'poliziotteschi' cinematic movement of the 1970s which, at firs...
The operation took 0.03306412696838379 seconds.

Search query : godfather
{'title': 'Disco Godfather', 'overview': 'A retired cop becomes a DJ/celebrity at the Blueberry Hill disco-- he\'s the "Disco Godfather!" All is well until his nephew flips out on a strange new drug t...
{'title': 'Onimasa: A Japanese Godfather', 'overview': 'Onimasa is the egocentric boss of a small yakuza clan on Shikoku Island, whose criminal duties conflict with his self-image as a chivalrous samu...
{'title': 'The Godfather', 'overview': 'Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barel...
{'title': 'The Godfather: Part III', 'overview': 'In the midst of trying to legitimize his business dealings in 1979 New York and Italy, aging mafia don, Michael Corleone seeks forgiveness for his sin...
{'title': 'The Godfather: Part II', 'overview': 'In the continuing saga of the Corleone crime family, a young Vito Corleone grows up in Sicily and in 1910s New York. In the 1950s, Michael Corleone att...
{'title': 'The Last Godfather', 'overview': "Young-goo the son of mafia boss Don Carini, is too foolish to be part of the mafia elite. One day, Young-goo comes to his father and is trained by Tony V t...
{'title': 'Godfather', 'overview': 'The story of Anjooran (N. N. Pillai), and his four sons Balaraman (Thilakan), Swaminathan (Innocent), Premachandran (Bheeman Raghu) and Ramabhadran (Mukesh) are in ...
{'title': 'The Godfather Trilogy: 1972-1990', 'overview': 'The multigenerational saga of the rise and fall of the Corleone crime family.'}...
{'title': 'I Knew It Was You: Rediscovering John Cazale', 'overview': "John Cazale was in only five films - The Godfather, The Conversation, The Godfather, Part Two, Dog Day Afternoon, and The Deer Hu...
{'title': "Jane Austen's Mafia!", 'overview': 'Takeoff on the Godfather with the son of a mafia king taking over for his dying father.'}...
The operation took 0.005291938781738281 seconds.

Search query : God father
{'title': 'My God, My God, Why Hast Thou Forsaken Me?', 'overview': 'A.D. 2015: A virus has been spreading in many cities worldwide. It is a suicidal disease and the virus is infected by pictures. Peo...
{'title': 'Father and Daughter', 'overview': 'A father says goodbye to his young daughter. In time the daughter grows old, but within her there is always a deep longing for her father.'}...
{'title': 'My Father the Hero', 'overview': 'A teenage girl on vacation in the Bahamas with her divorced father tries to impress a potential boyfriend by saying that her father is actually her lover.'...
{'title': 'My Father the Hero', 'overview': 'Veronique, living with her divorced mother, is going on holiday to Mauritius with her father. To impress a local boy, Benjamin, she manages to complicate t...
{'title': 'My So-Called Father', 'overview': "A daughter helps her estranged father who's lost his memory."}...
{'title': 'When Did You Last See Your Father?', 'overview': "The story of a son's conflicting memories of his dying father."}...
{'title': 'Father and Son', 'overview': 'A small family "a father and a son" lives on the top floor of an old house. The father retired from the military, when he was a student in flight school, he ex...
{'title': 'I Never Sang for My Father', 'overview': "Hackman plays a New York professor who wants a change in his life, and plans to get married to his girlfriend and move to California. His mother un...
{'title': 'Like Father, Like Son', 'overview': 'The story of a small-town football star, who defies society, morals and his God and gets into so much trouble that he is expelled from school. Told in f...
{'title': 'Lies My Father Told Me', 'overview': "A Jewish boy grows up in 1920s Montreal with a grandfather who tells stories and a father who won't work."}...
The operation took 0.006492137908935547 seconds.

Search query : Man of Steel
{'title': 'Man of Steel', 'overview': 'A young boy learns that he has extraordinary powers and is not of this earth. As a young man, he journeys to discover where he came from and what he was sent her...
{'title': 'The Flower with Petals of Steel', 'overview': "Wealthy surgeon Andreas Valenti accidentally kills one of his lovers, Daniella, with an unusual objet d'arte and covers it up by dismembering ...
{'title': 'Hands of Steel', 'overview': 'A story about a cyborg who is programmed to kill a scientist who holds the fate of mankind in his hands.'}...
{'title': 'Tears of Steel', 'overview': 'The film’s premise is about a group of warriors and scientists, who gathered at the “Oude Kerk” in Amsterdam to stage a crucial event from the past, in a despe...
{'title': 'Ring of Fire II: Blood and Steel', 'overview': 'Johnny Woo and Julie play an enduring couple who survive all sorts of interference from rival kick-box gangs in their effort to put a little ...
{'title': 'Max Steel', 'overview': 'The adventures of teenager Max McGrath and alien companion Steel, who must harness and combine their tremendous new powers to evolve into the turbo-charged superher...
{'title': 'Steel Toes', 'overview': 'Steel Toes is a provocative exploration of the inescapable and insidious presence of racial and religious intolerance in our society.'}...
{'title': 'Steel', 'overview': 'Justice. Safe streets. Payback. Metallurgist John Henry Irons (O\'Neal) vows to claim them all when a renegade military reject (Judd Nelson) puts new superweapons in da...
{'title': 'Slow Southern Steel', 'overview': 'Slow Southern Steel is a film about heavy music in the modern American\n South, as told by the very people who have created this music during\n the last t...
{'title': 'Steel', 'overview': 'Here, the steel worker works on a continuous cycle, twenty-four hours a day and never stops. There, by the sea, on the island of Elba there is a paradise and the unreac...
```


