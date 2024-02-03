# Level 1: Basic String Matching 🔍

Welcome to Level 1 of our search and information retrieval crash course! In this level, we'll explore the fundamentals of search using basic string matching. Our goal is to search for a query term within the title and overview of movies in our dataset.

## 📘 Overview

To perform string matching, we convert all titles, overviews, and the search query to lower case and conduct a simple "contains" comparison. This approach, while straightforward, introduces us to the core concept of how search engines start understanding content matching.

## 🖋️ Implementation

Here's the code snippet for performing the comparison:

```
if (isinstance(row['title'], str) and search_query.lower() in row['title'].lower()) or (isinstance(row['overview'], str) and search_query.lower() in row['overview'].lower()):
    movies.add(row['title'])
```

## 🚀 Execution

I have used a few different search queries. Here are the results : 

```

Number of titles : 45466

Search query : Godfather
The operation took 0.84645676612854 seconds.
Result : {'Ed Hardy: Tattoo the World', 'César', 'Cinderfella', 'The Kennedys', 'The Freshman', 'Video Games: The Movie', 'In Search of Blind Joe Death: The Saga of John Fahey', "Jane Austen's Mafia!", 'The Godfather: Part III', 'The New Godfathers', 'Free Enterprise', 'Dad Savage', 'The Godfather Trilogy: 1972-1990', 'Uptown Saturday Night', '3 Godfathers', 'American Yakuza', 'Disco Godfather', 'Godfather', 'BMF: The Rise and Fall of a Hip-Hop Drug Empire', 'The Godfather', "Eurocrime! The Italian Cop and Gangster Films That Ruled the '70s", 'Tokyo Godfathers', 'First Love', 'The Nutcracker: The Untold Story', 'C(r)ook', 'Onimasa: A Japanese Godfather', 'I Knew It Was You: Rediscovering John Cazale', 'Porridge', 'Three Godfathers', 'The Godfather: Part II', 'Fog City Mavericks', 'The Nest', 'Ultimate Heist', 'The Last Godfather', 'Maqbool', 'Sighs of Spain', 'Above and Below', 'Bright Eyes', "Things to Do in Denver When You're Dead"}

Search query : God father
The operation took 0.8401479721069336 seconds.
Result : set()

Search query : The Godfather
The operation took 0.835745096206665 seconds.
Result : {'Fog City Mavericks', 'Ed Hardy: Tattoo the World', 'The Kennedys', 'The Godfather Trilogy: 1972-1990', 'Video Games: The Movie', 'Maqbool', 'In Search of Blind Joe Death: The Saga of John Fahey', 'The Godfather: Part III', "Jane Austen's Mafia!", 'BMF: The Rise and Fall of a Hip-Hop Drug Empire', 'The Godfather', 'I Knew It Was You: Rediscovering John Cazale', "Eurocrime! The Italian Cop and Gangster Films That Ruled the '70s", 'The Godfather: Part II'}

Search query : Man of Steel
The operation took 0.8357608318328857 seconds.
Result : {'Superman Returns', 'Superman/Batman: Public Enemies', 'Batman: The Dark Knight Returns, Part 2', 'Superman vs. The Elite', 'Man of Steel', 'LEGO DC Comics Super Heroes: Justice League vs. Bizarro League', 'The Mad Scientist', 'Superman: Brainiac Attacks', 'All Star Superman', 'Superman III', 'Superman II', "It's A Bird, It's A Plane, It's Superman!", 'Confessions of a Superhero', 'The Death of "Superman Lives": What Happened?', 'Superman IV: The Quest for Peace'}
```

The result seem decent! Let's analyse them.

## 📊 Analysis

- The first thing to notice is that there is no "ordering". When you perform a google search, the results always seem sorted with respect to how relevant they might be to your query. But in our case we don't really have any sorting.
- Although the results contain the movies we are looking for, it also contains a lot of junk. Ex: Why is the movie "Ed Hardy: Tattoo the World" the second result in the search for "The Godfather". Combined with the fact that there is no relevance sorting, the results are okayish.
- For the query "god father", there are no results. That seems a little odd.

## Conclusion

My conclusion is, it works but ehhhh. This is kinda basic and not super helpful. If a search engine did this to you, you would stop using it.

## 🔝 Advanced

There are a few things you could do here to get better results.

- Compare each word instead of comparing full strings. Keep a count of how many words match. A higher count could mean a better match and it would allow you to rank the results. Is there a way to do this efficiently? Check out Level 2 :)


