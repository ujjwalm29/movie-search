# Level 3 : Semantic search and embeddings 🧠

Welcome to Level 3! In this level, we are going to be talking about how the field of IR and search has completely been transformed using Artificial Intelligence(AI).

## 🤖 Semantic search

Let's first try to answer _what_ is the problem with TF-IDF and _why_ do we need semantic search?

As a recap, remember that TF-IDF works by splitting text into parts and storing them in an index.
If you think about it, at the end of the day, the precise _words_ are being stored in the index.

Let's say you want to search for the word "fruit" and your index only contains "apple". There is no way simple TF-IDF can recognize that fruit is in fact a close enough term to apple.
To do something like this in TF-IDF, you need to synonyms list etc. Basically, it's not scalable for products which do not have search as their major feature.

In comes semantic search. Semantic search uses AI models that are able to group similar items together. Look at the image below.

![Semantic Search](SemanticSearch.png "Semantic Search. Credit : Sentence-Transformer documentation")

For our example, the "Relevant Document" would be "apple"(in our index) and the "Query" would be "fruit". Through the magic of AI, we are able to put similar object nearby.

So how does semantic search work?

### 📁 Indexing

Each model takes text as input. First step is to decide what will be our input. For our case, I have taken the concatenation of title and overview as the input.

```
concatenated_texts = df['title'].astype(str) + " " + df['overview'].astype(str)
```

The embeddings model converts this string into a vector of many dimensions. **Usually, a higher dimension embedding means better accuracy but at the cost of higher processing time and storage.**

An advantage of using embedding models is that you do not necessarily need to preprocess your text(it is still recommended). This is due to the fact that words like "run", "running" and "ran" would usually be semantically similar.

### 🔍 Search

While searching, take the search query and use it as input into the model. The model will give you a vector of the same dimension as the indexed data
(Important : the same model needs to be used while indexing and searching data).

Once the vector is obtained, calculate the [cosine similarity](https://www.sciencedirect.com/topics/computer-science/cosine-similarity) between the query vector and all the indexed vectors. The 10 highest scores are our search results.

Now that you have a basic understanding of how semantic search works, let's give it a spin!

## 🚀 Execution

For this demonstration, I have added a new search query : "flying super hero" to see how search behaves

I have used 2 embedding models to show how models behave differently. All models have been obtained from [HuggingFace](https://huggingface.co/).

The first model being used is : [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). It produces vectors of size 384.

384 is a relatively small size vector. Hence, embedding data with the model is very fast(8 minutes).

Execution results : 
```
Search query : the godfather
Results : ["Jane Austen's Mafia!", 'The Godfather Trilogy: 1972-1990', 'The Godfather: Part II', 'The Godfather: Part III', 'The Godfather', '3 Godfathers', 'The Mafia Kills Only in Summer', 'I Knew It Was You: Rediscovering John Cazale', 'The New Godfathers', 'Donnie Brasco']

Search query : godfather
Results : ["Jane Austen's Mafia!", 'The Godfather Trilogy: 1972-1990', 'The Godfather: Part III', 'The Godfather', 'The Godfather: Part II', '3 Godfathers', 'The Mafia Kills Only in Summer', "Assassin's Creed: Lineage", 'The New Godfathers', 'C(r)ook']

Search query : God father
Results : ['Father of Four: Never Gives Up!', 'Just a Father', 'Son of Sam', "Who's Your Daddy?", 'Oh My God', 'The Father and the Foreigner', 'For My Father', 'Most', 'Daddy', 'Romulus, My Father']

Search query : Man of Steel
Results : ['Man of Steel', 'Steel', 'Iron Man', 'Iron Man: Rise of Technovore', 'John Henry', 'Steel Frontier', 'Iron Man 3', 'The Invincible Iron Man', 'Strongman', 'The Mad Scientist']

Search query : flying super hero
Results : ['The Flying Man', 'Super Fly', 'Crumbs', 'Super Capers', 'A Flying Jatt', 'Super', 'Knight Rider', 'Sunshine Superman', 'God Is My Co-Pilot', 'Supersonic Man']
```

The results look good!
- "the godfather" and "godfather" has all the parts of godfather trilogy mentioned, although the top result is not from the trilogy.
- "Man of steel" has decent results but there seem to be more mentions for Iron man than superman. This is probably due to the semantic similarity between Iron and Steel.
- "flying super hero" has a lot of titles with "fly" but only 1 mention of superman.

Let's try the second model : [gte-large](https://huggingface.co/thenlper/gte-large). It produces vectors of size 1024.

Since the vector is bigger, indexing took longer(30 minutes) but we should expect better accuracy.

Execution results : 
```
Search query : the godfather
Results : ['The Godfather Trilogy: 1972-1990', 'The Godfather', "Jane Austen's Mafia!", 'The Godfather: Part III', 'The Last Godfather', 'The Godfather: Part II', 'Godfather', 'Underworld', 'The New Godfathers', '3 Godfathers']

Search query : godfather
Results : ['The Godfather', "Jane Austen's Mafia!", 'The Godfather Trilogy: 1972-1990', 'The Godfather: Part III', 'The Last Godfather', 'Godfather', 'The Godfather: Part II', '3 Godfathers', 'The New Godfathers', 'Underworld']

Search query : God father
Results : ['God Willing', 'Oh, God!', 'Godheten', 'The Brand New Testament', 'Oh, God! Book II', 'Oh My God', 'Ordet', 'God Tussi Great Ho', 'Abraham', "God's Gun"]

Search query : Man of Steel
Results : ["It's A Bird, It's A Plane, It's Superman!", 'The Mad Scientist', 'Man of Steel', 'Superman vs. The Elite', 'All Star Superman', 'Superman III', 'Superman II', 'Superman IV: The Quest for Peace', 'A Man Who Was Superman', 'Superman/Batman: Public Enemies']

Search query : flying super hero
Results : ['The Flying Man', 'A Flying Jatt', 'Supersonic Man', 'Up, Up, and Away', 'Phantom Boy', 'Sunshine Superman', 'Crumbs', 'Look, Up in the Sky: The Amazing Story of Superman', 'Sky High', 'American Hero']
```

The results look _much_ better!
- "the godfather" and "godfather" has all the parts of godfather trilogy mentioned and the top result is from the trilogy.
- "Man of Steel" has many more mentions of superman(almost all, infact).
- "flying super hero" has mentions of a lot of flying super hero movies including superman!(Although I have to warn you the second search result 'A Flying Jatt' is a shitty movie and my search application should be burnt down for pulling that up)

❗Semantic search is relatively straightforward to implement for small projects and applications. Unfortunately, it doesn't _solve_ search relevance issues and relevance engineering is very much required.
One might say relevance engineering is even more important since the embeddings models essentially behave like black boxes(we don't know _why_ they do what they do).





