# Semantic Knowledge Graphs

For our search queries so far, we have mostly depended on our search query matching something in our index.
For keyword search, the query had to be an almost match.
For vector search, we depended on the model underneath to understand the context and give vectors closer to itself.

With semantic knowledge graphs, we are going to try something new : Query expansion.

When a user searches for "Man Of Steel", our hope is that something in our title and overview hopefully matches to the query.
But what if we had a way to automatically include a search for the term "Superman" when a user enters "Man of Steel".

Well, one way to do that would be to manually maintain a synonyms list. Obviously, that's tedious and I ain't got time.

So, we'll try to do this automatically. We are going to use an inverted index and a forward index(reverse of inverted index).

The idea is, when a search is triggered, the inverted index gives us a list of documents that the query occurs in.
Then, we use those document IDs to check which word occurs most in those documents. There is a chance, we might find terms
that are similar to each other and can be used for query expansion.

Only 1 way to find out!

## Creating graph

We'll use good ol' elasticsearch here to manage indexes.

First, we use the existing libraries that we created to create the index.

