# Using FAISS and faster semantic search - IVF, PQ, OPQ, IVFOPQ

Alright folks, I think I can safely say amateur hour is over. We're going to be using FAISS, IVFOPQ and maybe little bit of AdANNS for this level.

Basically, we are going to be exploring some techniques to get faster semantic search.

Just a heads up, these techniques are not straightforward and I probably won't to do a great job of explaining them.
I would advise you to the attached resources OR use ChatGPT to understand these topics(I did this).

Let's begin!

## FAISS

[faiss](https://faiss.ai/index.html) is a widely used library for clustering and retrieval of dense vectors. We won't have to code most things from scratch in this tutorial. We'll just use faiss.


**A note on accuracy**: When dealing with vectors, we need to keep in mind that these are just sets of numbers. Yes, in our context they mean movies, but they are *just numbers*.
When measuring accuracy of the search, I will continue to say "oh these movies look totally relevant!". But that's not very sciency. In reality, we can literally measure distances between vectors and give numerical values to our accuracy.
I am not implementing that(for now), but just something to keep in mind.

## Inverted File Index (IVF)

IVF essentially means clustering of dense vectors. At index creation, vectors are clustered. At search time, we calculate which cluster does the query_vector belong to.
Once the cluster(and nearby) clusters are recognized, we do a linear comparison with all vectors and choose the best scores.

Here is the code for IVF : 
```
def get_IVF_index(df):
    # Assuming df['embeddings'] contains your embeddings
    embedding_dim = len(df.iloc[0]['embeddings'])

    # Create a quantizer with the L2 metric
    quantizer = faiss.IndexFlatIP(embedding_dim)

    nlist = 100  # Number of clusters; adjust based on your dataset size and needs
    index = faiss.IndexIVFFlat(quantizer, embedding_dim, nlist, faiss.METRIC_INNER_PRODUCT)
    
    embeddings_matrix = np.stack(df['embeddings'].values)
    index.train(embeddings_matrix)
    
    index.nprobe = 10
    
    index.add(embeddings_matrix)

    return index
```

Notice that IVF has some parameters like nlist and nprobe. For now, I am using some random parameters. In real applications, you would want to do something to find the optimal parameters.

Let's run our searches and see what's up!

```
dims = 1568
nlist = 100
index.nprobe = 10

The index creation took 3.321593999862671 seconds.

Search query : the godfather
The operation took 0.002373218536376953 seconds.
['The Godfather Trilogy: 1972-1990', 'The Godfather: Part III', 'The Godfather: Part II', 'The Godfather', 'The Last Godfather', 'Counselor at Crime', 'The New Godfathers', "Jane Austen's Mafia!", 'Pay or Die!', 'Big Deal on Madonna Street']

Search query : godfather
The operation took 0.0015649795532226562 seconds.
['Counselor at Crime', 'The Last Godfather', 'The Godfather Trilogy: 1972-1990', 'The Godfather: Part III', 'The Godfather', 'House of Strangers', 'The Godfather: Part II', 'Street People', 'Gotti', "Jane Austen's Mafia!"]

Search query : God father
The operation took 0.0013928413391113281 seconds.
['God Willing', 'Oh, God!', 'God Tussi Great Ho', 'Godfather', 'Walter', 'Varalaru', 'The Holy Man', 'The Little Devil', 'The Goddess', 'God Is Brazilian']

Search query : Man of Steel
The operation took 0.001811981201171875 seconds.
['Man of Steel', 'The Mad Scientist', 'Superman II', 'Superman Returns', "It's A Bird, It's A Plane, It's Superman!", 'Batman v Superman: Dawn of Justice', 'Superman vs. The Elite', 'Atom Man vs Superman', 'Superman III', 'Superman IV: The Quest for Peace']

Search query : flying super hero
The operation took 0.0010712146759033203 seconds.
['The Flying Man', 'A Flying Jatt', 'Phantom Boy', 'Sky High', 'Superhero Movie', 'Superheroes', 'American Hero', 'Hero at Large', 'Up, Up, and Away', 'Crumbs']
```

WOAH! What just happened? This is actually insane! The searches are literally taking less than 1/100th of a second! 
It's quite phenomenal but at the same time, I am a little sad that I tried SO MANY other things before trying this out.

Few thoughts : 
1. I feel like the dataset is not large enough. Remember, we have 45K+ 1568 dimensions of embeddings. And still, the search almost takes no time. Crazy.
2. The search times are extremely small and are reaching a threshold where it would not be wise to compare them with other methods. I will still try other methods, but take the conclusions with a grain of salt.

### Parameters

Turns out, there's a library called [autofaiss](https://github.com/criteo/autofaiss) which computes and selects the best indexing parameters.
Honestly, for our use case and results, it doesn't seem super useful to "optimize" parameters. But it's cool to see an open source library like this!

## Product Quantization(PQ) and Optimized Product Quantization(OPQ)

Next comes product quantization. In PQ, we take a big vector, split it into sub vectors and assign each sub-vector to a predefined codebook. This helps save significant space for a tradeoff in accuracy.

OPQ optimizes PQ by normalizing/rotating the original dense vector to make it more suitable for quantization.

Didn't understand? That's ok. It took me a couple of days to get the hang of PQ and OPQ.

Let's implement them in faiss!

## PQ in FAISS

Here's the code. `m` and `bits` are parameters.
```
def get_PQ_index(df, m=8, bits=8):
    embedding_dim = len(df.iloc[0]['embeddings'])

    # m is Number of sub-vector quantizers
    # bits is Number of bits per sub-vector quantizer
    index = faiss.IndexPQ(embedding_dim, m, bits, faiss.METRIC_INNER_PRODUCT)

    embeddings_matrix = np.stack(df['embeddings'].values)

    index.train(embeddings_matrix)

    index.add(embeddings_matrix)

    return index
```

Results : 
```

The index creation took 6.678642272949219 seconds.

Search query : the godfather
The operation took 0.00017189979553222656 seconds.
['The Palermo Connection', 'Crime Boss', 'Suburra', 'Street Law', 'Pay or Die!', 'The Godfather: Part III', 'The Godfather', 'Mean Frank and Crazy Tony', 'The Sicilian Connection', 'Emergency Squad']

Search query : godfather
The operation took 0.0001399517059326172 seconds.
['The Palermo Connection', 'Crime Boss', 'Lo sgarbo', 'Hunted City', 'Convoy Busters', 'Emergency Squad', 'Delitto al Blue Gay', 'Little Italy', 'A Man Called Magnum', 'The Mad Dog Killer']

Search query : God father
The operation took 0.0001380443572998047 seconds.
['Modris', 'The Son of Joseph', 'Family Law', 'The Keys to the House', 'Second Best', 'Everything Will Be Okay', "Daddy's Dyin'... Who's Got the Will?", 'Touching Home', 'Aurora Borealis', 'Most']

Search query : Man of Steel
The operation took 0.0001380443572998047 seconds.
['JLA Adventures: Trapped in Time', 'Justice League: War', 'Justice League: Crisis on Two Earths', 'Justice League: The Flashpoint Paradox', 'Superman: Unbound', 'Justice League: Doom', 'Superman/Batman: Public Enemies', 'Superman: Doomsday', 'All Star Superman', 'Justice League: The New Frontier']

Search query : flying super hero
The operation took 0.0001399517059326172 seconds.
['Superman', 'Atom Man vs Superman', 'The Phantom', 'Superman/Shazam!: The Return of Black Adam', 'Superman vs. The Elite', 'Superheroes', 'Black Lightning', 'The Flying Man', 'Superhero Movie', 'Super Capers']
```

Man, as soon as I think the search times can't be smaller, these new techniques surprise me! Less than 1/1000th of a second!

But if you notice, our search results are not that great. Simple queries like the godfather and man of steel aren't returning great results.
We need to fix this!

### Fixing PQ search

After thinking about it for a bit and browsing the internet, I decided to experiment with m and bits.

Let's change the value of m first. It should give us better precision at the expense of higher memory consumption and higher search times.

```
index_pq = get_PQ_index(df, 64, 8)
```

Results :
```

The index creation took 26.56769824028015 seconds.

Search query : the godfather
The operation took 0.0009100437164306641 seconds.
['The Godfather', 'The Godfather Trilogy: 1972-1990', 'The Godfather: Part III', 'The Godfather: Part II', 'Mafioso', 'The Last Godfather', 'Counselor at Crime', 'House of Strangers', 'Big Deal on Madonna Street', 'Crime Boss']

Search query : godfather
The operation took 0.0008997917175292969 seconds.
['Counselor at Crime', 'The Godfather: Part III', 'House of Strangers', 'The Godfather', 'The Last Godfather', 'Mafioso', 'The Godfather: Part II', 'Two Bits', 'A Man Called Magnum', 'Rulers of the City']

Search query : God father
The operation took 0.0009441375732421875 seconds.
['The Father and the Foreigner', 'God Willing', 'God Tussi Great Ho', 'Oh, God!', "Father's Day", 'Our Father', 'Varalaru', 'The Little Devil', 'King', 'Postscript']

Search query : Man of Steel
The operation took 0.0009119510650634766 seconds.
['Man of Steel', 'The Mad Scientist', 'All Star Superman', 'Mercury Man', 'Superman Returns', 'Superman', 'Superman II', 'Superman/Batman: Apocalypse', 'Superman IV: The Quest for Peace', 'Superman vs. The Elite']

Search query : flying super hero
The operation took 0.0009019374847412109 seconds.
['The Flying Man', 'LEGO DC Comics Super Heroes: Batman: Be-Leaguered', 'American Hero', 'Heroes Wanted', 'Superheroes', 'Supersonic Man', 'Sky High', 'Superhero Movie', 'LEGO DC Comics Super Heroes: Justice League - Gotham City Breakout', 'The Bulleteers']
```

The precision seems to be much better. A higher `m` means each large vector will be broken into higher number of sub-vectors.

Let's keep `m` constant and play with `bits`. Higher `bits` should help precision.

```

The index creation took 42.97942900657654 seconds.

Search query : the godfather
The operation took 0.005672931671142578 seconds.
['The Godfather: Part II', 'The Godfather Trilogy: 1972-1990', 'The Godfather', 'The Godfather: Part III', 'Big Deal on Madonna Street', 'Mafioso', 'Counselor at Crime', 'Scarface', 'The Last Godfather', 'Across 110th Street']

Search query : godfather
The operation took 0.005684852600097656 seconds.
['Counselor at Crime', 'The Godfather: Part II', 'House of Strangers', 'The Last Godfather', 'The Mobfathers', 'The Godfather', 'Crime Boss', 'Mafioso', 'Padre Padrone', 'Rulers of the City']

Search query : God father
The operation took 0.005604743957519531 seconds.
['God Willing', 'The Father and the Foreigner', 'I Am Your Father', 'God Tussi Great Ho', 'Padre Padrone', 'Daddy, Father Frost Is Dead', 'Big Daddy', 'Superdad', 'Journey with Papa', 'The Goddess']

Search query : Man of Steel
The operation took 0.0056171417236328125 seconds.
['Man of Steel', 'The Mad Scientist', 'Superman vs. The Elite', 'Justice League', 'Superman III', 'All Star Superman', 'Superman II', 'Atom Man vs Superman', 'Superman Returns', 'Batman v Superman: Dawn of Justice']

Search query : flying super hero
The operation took 0.005644083023071289 seconds.
['The Flying Man', 'Up, Up, and Away', 'Superheroes', 'Sky High', 'Superhero Movie', 'Supersonic Man', 'LEGO DC Comics Super Heroes: Batman: Be-Leaguered', 'American Hero', 'Atomic Rulers', 'Iron Man & Hulk: Heroes United']
```

Hmmm, this doesn't look too good. My focus is on the "godfather" query. The godfather movies are not bubbling up to the top 10 movies. Also the time to search has increased significantly.
Almost 2x-3x the time for IVF search(but the index size for PQ would be lower, which is helpful in larger datasets).  

At this point we have 2 things to try : 
1. Increase bits value.
2. Increase m value.

It's my tutorial, so I'm going to try both!

```
index_pq = get_PQ_index(df, 128, 9)
```

Results:
```

The index creation took 76.77314829826355 seconds.

Search query : the godfather
The operation took 0.011253118515014648 seconds.
['The Godfather: Part II', 'The Godfather: Part III', 'The Godfather', 'The Godfather Trilogy: 1972-1990', 'Counselor at Crime', 'The Last Godfather', "Jane Austen's Mafia!", 'The New Godfathers', '3 Godfathers', 'Scarface']

Search query : godfather
The operation took 0.011274099349975586 seconds.
['Counselor at Crime', 'The Godfather: Part III', "Jane Austen's Mafia!", 'The Last Godfather', 'The Godfather', 'House of Strangers', '3 Godfathers', 'The Godfather Trilogy: 1972-1990', 'Gotti', 'The Godfather: Part II']

Search query : God father
The operation took 0.011340856552124023 seconds.
['The Father and the Foreigner', 'Oh, God!', "Father's Day", 'God Willing', 'Just a Father', 'Daddy, Father Frost Is Dead', 'Godfather', 'The Goddess', 'Blood Father', 'God Tussi Great Ho']

Search query : Man of Steel
The operation took 0.011244058609008789 seconds.
['Man of Steel', 'Superman Returns', 'Superman vs. The Elite', 'Batman v Superman: Dawn of Justice', 'Superman II', 'Superman III', 'The Mad Scientist', 'Superman IV: The Quest for Peace', 'Phenomenon', 'Justice League']

Search query : flying super hero
The operation took 0.011287927627563477 seconds.
['The Flying Man', 'A Flying Jatt', 'Superhero Movie', 'Sky High', 'Phantom Boy', 'Alter Egos', 'LEGO DC Comics Super Heroes: Justice League - Gotham City Breakout', 'American Hero', 'Crumbs', 'Superheroes']
```

The results are a little better, but again, the godfather movies are still on the far end of the top results.

Let's try increasing the value of bits:
```
index_pq = get_PQ_index(df, 128, 10)
```

Results:
```

The index creation took 136.9402129650116 seconds.

Search query : the godfather
The operation took 0.012477874755859375 seconds.
['The Godfather Trilogy: 1972-1990', 'The Godfather: Part II', 'The Godfather', 'The Godfather: Part III', 'The Last Godfather', 'Counselor at Crime', "Jane Austen's Mafia!", 'The New Godfathers', 'Mafioso', 'Pay or Die!']

Search query : godfather
The operation took 0.012566089630126953 seconds.
['Counselor at Crime', 'The Godfather Trilogy: 1972-1990', 'House of Strangers', 'The Godfather: Part II', 'The Godfather', 'The Godfather: Part III', 'The Last Godfather', "Jane Austen's Mafia!", 'Mafioso', 'The Mobfathers']

Search query : God father
The operation took 0.012490987777709961 seconds.
['The Father and the Foreigner', 'Oh, God!', 'God Willing', 'Superdad', 'The Holy Man', 'Just a Father', 'The Goddess', "Father's Day", 'For My Father', 'Blood Father']

Search query : Man of Steel
The operation took 0.012476921081542969 seconds.
['Man of Steel', 'Superman II', 'Superman Returns', 'Superman III', 'Batman v Superman: Dawn of Justice', 'Superman IV: The Quest for Peace', 'All Star Superman', 'Justice League', 'The Mad Scientist', 'Superman vs. The Elite']

Search query : flying super hero
The operation took 0.012449026107788086 seconds.
['The Flying Man', 'A Flying Jatt', 'American Hero', 'Superheroes', 'Sky High', 'Superhero Movie', 'Phantom Boy', 'Hero at Large', 'Sky Captain and the World of Tomorrow', 'Alter Egos']
```

The results are a little better. The search times haven't increased drastically. But the index creation time has increased drastically.

For now, I think I'll let this go, since I want to try out OPQ and IVFOPQ. An option would be to see how to use autofaiss for optimal parameters.


## OPQ in FAISS

Let's try to create OPQ indexes using faiss.

This is the code:
```
def get_OPQ_index(df, m=8, bits=8):
    embedding_dim = len(df.iloc[0]['embeddings'])

    start_time = time.time()

    # m is Number of sub-vector quantizers
    # bits is Number of bits per sub-vector quantizer
    pq = faiss.IndexPQ(embedding_dim, m, bits, faiss.METRIC_INNER_PRODUCT)

    embeddings_matrix = np.stack(df['embeddings'].values)

    # Wrap the PQ index with OPQ for optimized quantization
    opq = faiss.OPQMatrix(embedding_dim, m)
    index = faiss.IndexPreTransform(opq, pq)

    index.train(embeddings_matrix)

    index.add(embeddings_matrix)

    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"The index creation took {duration} seconds.")

    return index
```

Let's execute.

```
index_opq = get_OPQ_index(df, 64, 8)
```

Results
```
The index creation took 766.8714137077332 seconds.


Search query : the godfather
The operation took 0.0015277862548828125 seconds.
['The Godfather Trilogy: 1972-1990', 'The Godfather: Part III', 'The Godfather: Part II', 'The Godfather', 'The Last Godfather', 'Counselor at Crime', 'Scarface', 'Pay or Die!', 'Big Deal on Madonna Street', 'Black Hand']

Search query : godfather
The operation took 0.0011310577392578125 seconds.
['Counselor at Crime', 'The Last Godfather', 'The Godfather Trilogy: 1972-1990', 'Mafioso', 'The Godfather: Part III', 'The Godfather', 'House of Strangers', 'The Godfather: Part II', 'The Mobfathers', "Jane Austen's Mafia!"]

Search query : God father
The operation took 0.0010979175567626953 seconds.
['Oh, God!', 'Walter', 'The Father and the Foreigner', 'God Willing', 'Just a Father', 'Father of Four: Never Gives Up!', "Father's Day", 'Varalaru', 'The Little Devil', 'God Tussi Great Ho']

Search query : Man of Steel
The operation took 0.0011358261108398438 seconds.
['Man of Steel', 'Batman v Superman: Dawn of Justice', 'The Mad Scientist', 'Superman II', 'Superman vs. The Elite', "It's A Bird, It's A Plane, It's Superman!", 'Atom Man vs Superman', 'Superman III', 'Superman Returns', 'Superman']

Search query : flying super hero
The operation took 0.0011000633239746094 seconds.
['The Flying Man', 'A Flying Jatt', 'Sky High', 'Phantom Boy', 'Hero at Large', 'Sky Captain and the World of Tomorrow', 'Superheroes', 'American Hero', 'Last Action Hero', 'Up, Up, and Away']
```

This is great! The results are good for all the queries. The optimization process before PQ seems to really help. But, the index creation time is a lot higher.

Now, let's move on to IVFOPQ

## IVFPQ in faiss

In IVFPQ, we will first create an IVF. Then, we will apply PQ to our data. This should make our queries faster.

Code :
```
def get_IVFPQ_index(df, m=8, nlist=100, bits=8):
    embedding_dim = len(df.iloc[0]['embeddings'])

    start_time = time.time()

    # m is Number of sub-vector quantizers
    # nlist is the number of clusters for the coarse quantizer
    # bits is Number of bits per sub-vector quantizer

    # Create a coarse quantizer for the IVF structure
    quantizer = faiss.IndexFlatIP(embedding_dim)  # Use IndexFlatL2 for L2 metric

    # Combine OPQ and PQ with the IVF quantizer to create an IVFOPQ index
    index = faiss.IndexIVFPQ(quantizer, embedding_dim, nlist, m, bits, faiss.METRIC_INNER_PRODUCT)

    embeddings_matrix = np.stack(df['embeddings'].values).astype('float32')

    # Train the index
    index.train(embeddings_matrix)

    # Add embeddings to the index
    index.add(embeddings_matrix)

    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"The index creation took {duration} seconds.")

    return index
```

Results:
```
The index creation took 25.758468866348267 seconds.

Search query : the godfather
The operation took 0.00018215179443359375 seconds.
['The Godfather Trilogy: 1972-1990', 'The Godfather: Part III', 'The Godfather: Part II', 'The Godfather', 'The New Godfathers', 'Counselor at Crime', 'Pay or Die!', 'The Last Godfather', 'Scarface', "Jane Austen's Mafia!"]

Search query : godfather
The operation took 0.00012493133544921875 seconds.
['Counselor at Crime', 'The Godfather Trilogy: 1972-1990', "Jane Austen's Mafia!", 'Street People', 'The Godfather', 'I Am the Law', 'The Last Godfather', 'House of Strangers', 'The Godfather: Part III', 'The Godfather: Part II']

Search query : God father
The operation took 0.00012230873107910156 seconds.
['Walter', 'The Little Devil', 'Barabbas', 'The Priest', 'Begotten', 'The Brand New Testament', 'OMG: Oh My God!', 'Calvary', 'The Discovery of Heaven', 'Son of God']

Search query : Man of Steel
The operation took 0.00012421607971191406 seconds.
['Man of Steel', 'The Mad Scientist', 'Batman v Superman: Dawn of Justice', 'Superman II', 'Superman IV: The Quest for Peace', 'Superman', "It's A Bird, It's A Plane, It's Superman!", 'Superman Returns', 'Kryptonita', 'Superman III']

Search query : flying super hero
The operation took 0.0001239776611328125 seconds.
['The Flying Man', 'A Flying Jatt', 'Superhero Movie', 'Up, Up, and Away', 'Sky High', 'Phantom Boy', 'American Hero', 'The Return of Captain Invincible', 'The Invincible Iron Man', 'The Meteor Man']
```

Results are fast! The "godfather" query results don't seem to be upto the mark as the OPQ results, even though parameters are the same.

Let's try IVFOPQ!

## IVFOPQ in faiss

### faiss - index_factory

faiss has thing called `index_factory`. It allows you to enter a string which defines what kind of index will be created. 
[This](https://www.pinecone.io/learn/series/faiss/composite-indexes/) link explains index_factory really well. Side note, James Briggs(the author) is the only person who has explained IVFOPQ, HNSW and faiss in detail online. 
Check out this entire book called Faiss : The missing manual. Also, check out his youtube videos for visual explanations.

Back to `index_factory`. An interesting experiment is mentioned in the article. Create the same index using a predefined function and create one using `index_factory`. 
Compare the outputs. If they are the same, congrats! you know how to use `index_factory`.

Let's use `index_factory` to create IVFOPQ index.
```
def get_IVFOPQ_index(df, m=8, nlist=100, bits=8):
    embedding_dim = len(df.iloc[0]['embeddings'])

    start_time = time.time()

    # m is Number of sub-vector quantizers
    # nlist is the number of clusters for the coarse quantizer
    # bits is Number of bits per sub-vector quantizer

    index = faiss.index_factory(embedding_dim, f"OPQ{m},IVF{nlist},PQ{m}x{bits}", faiss.METRIC_INNER_PRODUCT)

    embeddings_matrix = np.stack(df['embeddings'].values).astype('float32')

    opq = faiss.OPQMatrix(embedding_dim, m)
    index = faiss.IndexPreTransform(opq, index)

    # Since we're using METRIC_INNER_PRODUCT, ensure embeddings are normalized
    faiss.normalize_L2(embeddings_matrix)

    # Train the index
    index.train(embeddings_matrix)

    # Add embeddings to the index
    index.add(embeddings_matrix)

    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time
    print(f"The index creation took {duration} seconds.")

    return index
```

Results :
```
The index creation took 789.4752860069275 seconds.

Search query : the godfather
The operation took 0.0006871223449707031 seconds.
['The Godfather Trilogy: 1972-1990', 'The Godfather: Part II', 'The Godfather: Part III', 'The Godfather', 'The Last Godfather', 'The New Godfathers', 'Counselor at Crime', 'Mafioso', 'Pay or Die!', 'Donnie Brasco']

Search query : godfather
The operation took 0.00046324729919433594 seconds.
['Counselor at Crime', 'The Last Godfather', 'House of Strangers', 'The Godfather: Part III', 'The Godfather', 'Street People', 'Mafioso', 'The Godfather: Part II', 'Gotti', 'The Godfather Trilogy: 1972-1990']

Search query : God father
The operation took 0.0003600120544433594 seconds.
['Walter', 'The Little Devil', 'Romulus, My Father', 'The God of Cookery', 'There Be Dragons', 'Alleluja & Sartana Are Sons... Sons of God', 'On Earth as It Is in Heaven', 'The Brand New Testament', 'Son of God', 'Abraham']

Search query : Man of Steel
The operation took 0.0005257129669189453 seconds.
['Man of Steel', "It's A Bird, It's A Plane, It's Superman!", 'Batman v Superman: Dawn of Justice', 'Superman', 'Superman II', 'The Mad Scientist', 'Atom Man vs Superman', 'Superman III', 'Superman Returns', 'Superman vs. The Elite']

Search query : flying super hero
The operation took 0.0004222393035888672 seconds.
['The Flying Man', 'A Flying Jatt', 'Hero at Large', 'Phantom Boy', 'Superheroes', 'Superhero Movie', 'Sky High', 'Up, Up, and Away', 'Sky Captain and the World of Tomorrow', 'LEGO DC Comics Super Heroes: Justice League - Gotham City Breakout']
```
 
The "godfather" results aren't great. The index creation time seems high enough to believe the vectors are being optimized.

## HNSW


