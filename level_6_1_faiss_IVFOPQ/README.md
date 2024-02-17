# Using FAISS and faster semantic search - IVFOPQ

Alright folks, I think I can safely say amateur hour is over. We're going to be using FAISS, IVFOPQ and maybe little bit of AdANNS for this level.

Basically, we are going to be exploring some techniques to get faster semantic search.

Just a heads up, these techniques are not straightforward and I probably won't to do a great job of explaining them.
I would advise you to the attached resources OR use ChatGPT to understand these topics(I did this).

Let's begin!

## FAISS

[faiss](https://faiss.ai/index.html) is a widely used library for clustering and retrieval of dense vectors. We won't have to code most things from scratch in this tutorial. We'll just use faiss.


## Inverted File Index (IVF)

IVF essentially means clustering of dense vectors. At index creation, vectors are clustered. At search time, we calculate which cluster does the query_vector belong to.
Once the cluster(and nearby) clusters are recognized, we do a linear comparison with all vectors and choose the best scores.

Here is the code for IVF : 
```
def get_IVF_index(df):
    # Assuming df['embeddings'] contains your embeddings
    embedding_dim = len(df.iloc[0]['embeddings'])

    # Create a quantizer with the L2 metric
    quantizer = faiss.IndexFlatL2(embedding_dim)

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

Search query : the godfather
The operation took 0.002531766891479492 seconds.
['The Godfather Trilogy: 1972-1990', 'The Godfather: Part III', 'The Godfather: Part II', 'The Godfather', 'The Last Godfather', 'Counselor at Crime', 'The New Godfathers', "Jane Austen's Mafia!", 'Pay or Die!', 'Big Deal on Madonna Street']

Search query : godfather
The operation took 0.0016467571258544922 seconds.
['Counselor at Crime', 'The Last Godfather', 'The Godfather Trilogy: 1972-1990', 'The Godfather: Part III', 'The Godfather', 'House of Strangers', 'The Godfather: Part II', 'Street People', 'Gotti', "Jane Austen's Mafia!"]

Search query : God father
The operation took 0.0020287036895751953 seconds.
['God Willing', 'Oh, God!', 'God Tussi Great Ho', 'Godfather', 'Walter', 'Varalaru', 'The Holy Man', 'The Little Devil', 'The Goddess', 'God Is Brazilian']

Search query : Man of Steel
The operation took 0.0021986961364746094 seconds.
['Man of Steel', 'The Mad Scientist', 'Superman II', 'Superman Returns', "It's A Bird, It's A Plane, It's Superman!", 'Batman v Superman: Dawn of Justice', 'Superman vs. The Elite', 'Atom Man vs Superman', 'Superman III', 'Superman IV: The Quest for Peace']

Search query : flying super hero
The operation took 0.0012509822845458984 seconds.
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



