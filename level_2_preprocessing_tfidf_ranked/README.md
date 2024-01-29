# Level 2 : Preprocessing, TF-IDF and ranking

In this level, we are going to change the way we do things. We are going to use some new IR concepts and take advantage of preprocessing to 

## Terminology

Below are some concepts and terms which have been used in this level. The definitions are obtained from ChatGPT and slightly modified. 

- Lemmatization : Lemmatization is a natural language processing technique that involves reducing words to their base or root form, known as the lemma. It considers the context and the morphological analysis of words, aiming to remove inflectional endings and return the dictionary form of a word. For example, "running", "ran", and "runs" are all lemmatized to the base form "run", taking into account their part of speech and tense.
- Stop words removal : The removal of stop words in natural language processing involves discarding common words that carry minimal meaningful information for the intended analysis or processing task. Stop words typically include articles, prepositions, conjunctions, and sometimes common nouns or verbs, like "the", "is", "at", or "which".
- TF-IDF : TF-IDF, short for Term Frequency-Inverse Document Frequency, is a statistical measure used in information retrieval to evaluate the importance of a word to a document in a collection or corpus. It balances two concepts: term frequency (TF), which counts how often a word appears in a document, and inverse document frequency (IDF), which diminishes the weight of words that appear frequently across multiple documents. This combination helps in identifying words that are unique and significant to a specific document. TF-IDF is super interesting and I would recommend reading more about it.

## Preprocessing

### Lemmatization

As a preprocessing step, all the titles and overviews are lemmatized. For example, "running", "ran", and "runs" are all lemmatized to the base form "run". If a user searches for "runs", they are probably ok with results related "running" and "ran".

### Removal of stop words

In the next step, stop words like "the", "is", "at", or "which" are removed from overviews. 

But Ujjwal, why not remove stop words from the titles as well?

Aha! If you think about it, stop words in titles are relevant pieces of information. Movies are called "The Godfather" or "man of steel" and not "godfather" or "man steel"(hehe). So, we retain the stop words in titles but remove them from the overviews.

**This is an example of how Information Retrieval is an intricate play between the kind of data you have and the searches you expect. There are no fixed rules and everything is subjective.**

### TF-IDF : Term Frequency-Inverse Document Frequency

First, sentences are split into pairs of words, also called bigrams (`TfidfVectorizer(ngram_range=(2, 2))` in the code).

But, why bigrams?

It's all a matter of relevance. If you think about it, when we search for "The godfather", we are interested in titles which have _BOTH_ the words "the" and "godfather". If we don't use bigrams, our search results will have single keyword matching, which might not work in this case. PS : Check out the experiments section below where I search using single words instead of bigrams  

Using the bigrams, the term frequency(TF) and inverse document frequency(IDF) is calculated. The TF-IDF representation is helpful in giving "weights" to words. Words which appear across a lot of documents get less weight, words which are rare get more weight. I am not going to go into the details of TF-IDF, but I would encourage you to read about it.

The TF-IDF representations of titles and overview are stored in separate matrices. These are called __indexes__. An index is a general data structure which is used to improve performance of data retrieval at the cost of higher storage space. In our case, the indexes are TF-IDF matrices.

## Search

How is the search carried out?

1. The search_query is lemmatized.
2. search_query is converted into TF-IDF representation for title and overview separately.
3. The respective search_query vectors are compared with their tfidf matrix. The scores for title and overview are obtained separately.
4. The individual scores are added to get combined score.
5. The top 10 corresponding indices are obtained from the original dataframe.

## Execution

Let's see how it works!

```
Search query : the godfather
The operation took 0.01231694221496582 seconds.
Results : ['The Godfather', 'The Godfather: Part II', 'The Godfather: Part III', 'The Godfather Trilogy: 1972-1990', 'Solomon Kane', 'MacGruber', 'Marmaduke', 'Reindeerspotting - Escape From Santaland', 'The Dark Tower', 'Johnny Angel']

Search query : godfather
The operation took 0.010956764221191406 seconds.
Results : ['Queerama', 'Cargo', 'Ca$h', 'MacGruber', 'Marmaduke', 'Reindeerspotting - Escape From Santaland', 'The Dark Tower', 'Johnny Angel', 'Lebanon', 'Iron Man 2']

Search query : God father
The operation took 0.011175870895385742 seconds.
Results : ['Abraham', 'The Gospel', 'Queerama', 'Solomon Kane', 'MacGruber', 'Marmaduke', 'Reindeerspotting - Escape From Santaland', 'The Dark Tower', 'Johnny Angel', 'Lebanon']

Search query : Man of Steel
The operation took 0.010980844497680664 seconds.
Results : ['Man of Steel', 'Hands of Steel', 'Tears of Steel', 'Man of the World', 'Man of the Story', 'Man of the House', 'Man of the House', 'Man of the Year', 'Man of the Year', 'Man of Iron']
```

## Analysis

For me, the results are a mixed bag. Let's discuss the pros and cons.

### Pros :

1. All queries have _some_ results. When using TF-IDF for search, a score is generated for each entry in the index. In the worst case, a search query matches with nothing. Still, 10 random(need to check if it's random, could depend on sequence of indexing) entries will be shown to the user.
2. Results are ranked. When searching for "the godfather", the relevant movies bubbled to the top due to high scores.
3. Search is significantly faster. If you look in level 1, all searches took around 0.83 seconds. Initially, that doesn't seem so bad.
But think about 2 factors. Firstly, we have very limited data. We have around 40k movie titles and overviews. Overviews are generally 2-3 sentences.
Imagine doing this for billions of documents and web pages. Secondly, there is only 1 search being executed at a time. Google handles 100,000 search queries each second.
Considering these 2 factors, the TF-IDF search is much faster(0.013 seconds, almost 64 times faster, even for our limited dataset!). This is perhaps the single most important reason to use indexes.

### Cons :
1. The results for our searches aren't _great_. Searches for "the godfather" and "god father" seem ok. Search for "godfather" returns none of the godfather movies(sad). 
Search for "Man of steel" returns only the "Man of steel" movie but none of the synonymous superman movies(like it did in level 1).

Problems like these come under a field called **relevance** engineering. Relevance engineering is challenging since you need to decide what is relevant and then figure out some way of engineer that into your code.
Book recommendation : [Relevant Search](https://www.manning.com/books/relevant-search). The technical aspects of Elasticsearch discussed might have become outdated now, but it helped me get an "essence" of
what relevant search means, including non-code related activities.

I will be debugging this problem in the advanced section. Feel free to take a look or move on to the next level, where we integrate ML and AI into search. See you!

## Advanced

Let's debug our search problems.

### Step 1 : Debug

All TF-IDF search queries are essentially matrix multiplications between the query and the index. The ones with the highest score get picked.

To debug this problem, we will print the top 10 scores associated with the title and overview WRT the search query.
To do this, I added these lines of code in the search_and_rank function.
```
# Get top 10 scores in similarities_title and similarities_overview
    top_scores_title = np.sort(similarities_title)[::-1][:10]
    top_scores_overview = np.sort(similarities_overview)[::-1][:10]

    print("Top 10 scores in similarities_title:", top_scores_title)
    print("Top 10 scores in similarities_overview:", top_scores_overview)
```

Let's run it!

```
Top 10 scores in similarities_title: [1.   0.59909386 0.58740975 0.4678763  0. 0. 0. 0. 0. 0. ]
Top 10 scores in similarities_overview: [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
The operation took 0.0331578254699707 seconds.
Results : ['The Godfather', 'The Godfather: Part II', 'The Godfather: Part III', 'The Godfather Trilogy: 1972-1990', 'Solomon Kane', 'MacGruber', 'Marmaduke', 'Reindeerspotting - Escape From Santaland', 'The Dark Tower', 'Johnny Angel']

Search query : godfather
Top 10 scores in similarities_title: [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
Top 10 scores in similarities_overview: [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
The operation took 0.013511896133422852 seconds.
Results : ['Queerama', 'Cargo', 'Ca$h', 'MacGruber', 'Marmaduke', 'Reindeerspotting - Escape From Santaland', 'The Dark Tower', 'Johnny Angel', 'Lebanon', 'Iron Man 2']

Search query : God father
Top 10 scores in similarities_title: [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
Top 10 scores in similarities_overview: [0.24633402 0.1775144  0. 0. 0. 0. 0. 0. 0. 0. ]
The operation took 0.01304483413696289 seconds.
Results : ['Abraham', 'The Gospel', 'Queerama', 'Solomon Kane', 'MacGruber', 'Marmaduke', 'Reindeerspotting - Escape From Santaland', 'The Dark Tower', 'Johnny Angel', 'Lebanon']

Search query : Man of Steel
Top 10 scores in similarities_title: [1.         0.57877191 0.55932902 0.44555475 0.43433571 0.4290386 0.4290386  0.41359976 0.41359976 0.40282436]
Top 10 scores in similarities_overview: [0.30508379 0.26613069 0.25388286 0.20354637 0.15606526 0.15466245 0.14824868 0.14806945 0.14428463 0.1313919 ]
The operation took 0.012663125991821289 seconds.
Results : ['Man of Steel', 'Hands of Steel', 'Tears of Steel', 'Man of the World', 'Man of the Story', 'Man of the House', 'Man of the House', 'Man of the Year', 'Man of the Year', 'Man of Iron']
```






