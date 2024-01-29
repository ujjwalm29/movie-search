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
Search query : the godfather
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

Some observations : 
- For "the godfather" the titles of the original movies match and give a non zero score. For everything else, including ALL overviews, the score is 0. This doesn't seem ideal.
- For "godfather", ALL scores across title and overviews is zero. This is a big red flag.
- For "god father", ALL titles are zero, 2 minor matches in overview.
- For "Man of steel", 1 title has a perfect score. Additionally, we see matches across titles and overview.

The above observations, especially point 2, are not ideal. Our search kinda sucks right now. What do you think is the problem?

Well, remember that all the titles and overview are split into bigrams. It seems like since the term "godfather" is 1 word, the index does not contain any singular godfather terms.
All the godfather words are combined with other words and present in the index (for example "the godfather").

Let's try and fix it!

### Step 2 : Fix it!

We found out that the problem might be bigrams.

I think we need to introduce unigrams in our index as well to match singular words across titles and overviews. The bigrams will help in precision but unigrams will help in recall. I would recommend you to read more about precision and recall.
Precision means getting the "correct" results to bubble up, but "recall" ensures that _some_ relevant results appear.

In the code, the vectorizers are defined as :
```
vectorizer_title = TfidfVectorizer(ngram_range=(2, 2))
vectorizer_overview = TfidfVectorizer(ngram_range=(2, 2))
```

To introduce unigrams, we can modify them to : 
```
vectorizer_title = TfidfVectorizer(ngram_range=(1, 2))
vectorizer_overview = TfidfVectorizer(ngram_range=(1, 2))
```

Let's run it again!

```
Search query : the godfather
Top 10 scores in similarities_title: [1.         0.66247551 0.66247551 0.64448446 0.62934108 0.46799578 0.38333228 0.38103037 0.36944792 0.36282461]
Top 10 scores in similarities_overview: [0.25168185 0.24899769 0.20350804 0.19688429 0.17867486 0.17221492 0.14695292 0.12873031 0.11081763 0.11031454]
The operation took 0.021055221557617188 seconds.
Results : ['The Godfather', 'Godfather', '3 Godfathers', 'The Godfather: Part II', 'The Godfather: Part III', 'Disco Godfather', 'The Godfather Trilogy: 1972-1990', 'Three Godfathers', 'The Last Godfather', 'Onimasa: A Japanese Godfather']

Search query : godfather
Top 10 scores in similarities_title: [1.         1.         0.66247551 0.57863615 0.55767786 0.543094 0.53206837 0.51714478 0.42695517 0.41692306]
Top 10 scores in similarities_overview: [0.25168185 0.24899769 0.20350804 0.19688429 0.17867486 0.17221492 0.14695292 0.12873031 0.11081763 0.11031454]
The operation took 0.018260955810546875 seconds.
Results : ['Godfather', '3 Godfathers', 'Disco Godfather', 'The Godfather', 'Three Godfathers', 'Tokyo Godfathers', 'The Last Godfather', 'The New Godfathers', 'Onimasa: A Japanese Godfather', 'The Godfather: Part II']

Search query : God father
Top 10 scores in similarities_title: [0.74104612 0.67145413 0.43924807 0.38789902 0.38789902 0.3828382 0.3828382  0.37127401 0.35984171 0.34911632]
Top 10 scores in similarities_overview: [0.24473007 0.1834853  0.13105711 0.12999122 0.12890206 0.12573952 0.12336889 0.10406436 0.10024817 0.09615167]
The operation took 0.02110886573791504 seconds.
Results : ['Father', 'Gods', 'The Father', "Fathers' Day", 'Our Father', "Father's Day", 'Our Fathers', 'Blood Father', 'Oh My God', 'Oh, God!']

Search query : Man of Steel
Top 10 scores in similarities_title: [1.    0.61627827 0.59264903 0.50981225 0.50981225 0.50981225 0.4278748  0.42537495 0.41562413 0.41562413]
Top 10 scores in similarities_overview: [0.34236535 0.29691966 0.29250448 0.22912267 0.17738596 0.1712126 0.16460193 0.16349751 0.16194437 0.15840618]
The operation took 0.019733905792236328 seconds.
Results : ['Man of Steel', 'Hands of Steel', 'Steel', 'Tears of Steel', 'Steel', 'Steel', 'Max Steel', 'Man of the World', 'Man of the House', 'Man of the Story']
```

MUCH BETTER!

- For "godfather", we have relevant results! All the movies shown have godfather in their titles.
- For "the godfather", we lost a little bit of precision, but movies from "the godfather" franchise still appear in the top 10 results.
- For "God father", we have matches for God and father, which is better than 10 random movies.
- For "Man of Steel", results have changed but the rest of the superman movies didn't show up.


For "Man of Steel", there seems to be a lot of matches for "Man of" or "Steel". Due to titles being short and how TF-IDF calculates scores, the titles are given a lot more importance than a small match in overview.

I could try and fix it but trying out a few things and giving "weights" to the title score and overview score, but I think I'll stop for now. You win some, you lose some. Let's move onto the next level!




