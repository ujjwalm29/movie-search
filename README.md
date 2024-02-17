# 🚀 Search and Information Retrieval Crash Course

Hello and welcome to this crash course on search and information retrieval! 🌎

Search is everywhere. It's an essential part of our lives. Imagine life without Google! 🔍

The more technical term for search is Information Retrieval (IR). There are some nuances, but for now, I will use the terms interchangeably.

🔧 **In an ideal world, search... _just works_.** Basically, you look for something on the internet, and the search engine knows _exactly_ what you are looking for and gives it to you. Google has done a great job regarding this. If you search for an airport, it shows you flights from your nearby airport. If you search for a restaurant, it shows you a little pop-up which shows the menu, reviews, how busy the restaurant is, etc. It's pretty incredible, to be honest.

💡 All of these advancements in the field of IR have been a result of almost half a century of academia + corporate research and tens of billions of dollars spent on R&D.

More recently, machine learning and artificial intelligence are changing how we think about search.

Search is quite a complex topic which requires general IR knowledge, domain understanding, and data for personalization. For this tutorial, I am going to be focusing on just the IR concepts.

By going through the various levels, you can get a basic understanding of how search works and has progressed over the years. We will be using a movie dataset to go through this tutorial.

This tutorial is still under progress, so don't forget to star the repo to check back later! ⭐

I am not an expert in this field, so this means that your feedback is EXTREMELY valuable to me. Is something in the content wrong? Is there something that wasn't explained well? Feel free to open a discussion or a pull request to suggest changes!

## 📘 Table of Contents

- [How to Use This Course](#how-to-use-this-course)
- [Levels](#levels)
- [Contributing](#contributing)
- [Feedback](#feedback)
- [License](#license)

## Introduction

You are already here! 🎉

## How to Use This Course

For each of the levels go through the README files. In case you are interested in looking or executing the code, each level has the python code for the respective level.

## Levels

Let's dive into the levels:

- **Level 1:** [Basic String Matching](https://github.com/ujjwalm29/movie-search/tree/master/level_1_basic_string_matching) 📝
  - Basic python 'contains' string matching
- **Level 2:** [Preprocessing, TF-IDF, and Ranking](https://github.com/ujjwalm29/movie-search/tree/master/level_2_preprocessing_tfidf_ranked) 🔍
  - Preprocessing : Lemmatization, stop-words, Term Frequency-Inverse Document Frequency(TF-IDF), Bigrams, creating indexes
  - Search : vectors, dot-product, scoring
  - Advanced : Debugging relevance issues :- Unigrams + Bigrams
- **Level 3:** [Elasticsearch and relevance tuning](https://github.com/ujjwalm29/movie-search/tree/master/level_3_elasticsearch_relevance_tuning) ⚙️
  - Install docker, Elasticsearch, certificates
  - Indexing : types, analyzers, filters, tokenizer, custom shingles filter.
  - Search : match, boosting, multi_match, most_fields, best_fields, explain parameter, norms, fuzzy queries, function_score, dis_max, boolean queries.
  - Search results regression : How to avoid them?
- **Level 4:** [Semantic Search and Embeddings](https://github.com/ujjwalm29/movie-search/tree/master/level_4_embeddings_and_semantic_search) 🧠
  - Semantic search
  - cosine similarity
  - embedding models, sentence-transformers, huggingface, MTEB
- **Level 5:** [Embeddings through APIs and Matryoshka representation learning powered embeddings](https://github.com/ujjwalm29/movie-search/tree/master/level_5_openai_embeddings_MRL)
  - Medium article - [LINK](https://ujjwalm29.medium.com/matryoshka-representation-learning-a-guide-to-faster-semantic-search-1c9025543530)
  - Advantages and disadvantages of embeddings through APIs.
  - Why Matryoshka Representation embeddings are game changers.
- **Level 6.1:** Inverted File Index(IVF), Product Quantization(PQ), Optimized Product Quantization(OPQ), IVFOPQ
  - Use faiss to create indexes using the above techniques.
  - autofaiss
- **Level 6.2:** HNSW
- Hybrid search and RRF using Elasticsearch(coming soon) 
- Knowledge Graphs(coming soon)

## Contributing and Feedback

To contribute, open a PR or start a discussion!

## License

Idk to be honest.

