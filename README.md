
# Welcome to HeyMovie!

  

****HeyMovie**** is a movie recommendation platform that helps users find 
movies in an easy and ordered way. The project is composed of a mobile 
application and a backend service. The API operation is going to be explained 
in further detail in this document.

# How to Use:

The API has a set of capabilities that allow managing the following objects:

- Movies

- Ratings

- Tags

- Genres

In each one of those you can perform CRUD operations.

The API service documentation can be found in the following links (whichever 
format you may prefer):

- [https://wfh-movies.herokuapp.com/docs](https://wfh-movies.herokuapp.com/docs)

- [https://wfh-movies.herokuapp.com/redoc](https://wfh-movies.herokuapp.com/redoc)

  

## Manage GET Movies:

In order to let the user to search a movie of interest the get method for all 
the objects has the following functionalities that should be sent as parameters 
in the request :

### Limit:

You can send the number of elements that you want to receive, for example, if 
you want only 20 movies per request you should use this :

  

[https://wfh-movies.herokuapp.com/movie?limit=20](https://wfh-movies.herokuapp.com/movie?limit=20 "https://wfh-movies.herokuapp.com/movie?limit=20")

### Page:

Allows the selection of the result page in a set of results, the total number 
of pages is sent by the request.

  

[https://wfh-movies.herokuapp.com/movie?limit=20&page=2](https://wfh-movies.herokuapp.com/movie?limit=20&page=2 "https://wfh-movies.herokuapp.com/movie?limit=20&page=2")

### Sort:

The API allows the user to sort the response given a field, you can sort by 
ascending or descending order, just have to send in the parameter sort, the 
field name, and the keyword asc or desc.

Example :

  

[https://wfh-movies.herokuapp.com/movie?sort=title.asc](https://wfh-movies.herokuapp.com/movie?sort=title.asc "https://wfh-movies.herokuapp.com/movie?sort=title.asc")

  

In this case, we are sorting the tittle in ascending mode.

### Filter:

Allows to filter the information of the object by fields using the following queries:

Filter data. Input format: operation(field, value). Available operations:

- ****exact****: Matches the exact value.

- ****partial****: Matches the value as contained in the field.

- ****start****: Matches the value as start of field.

- ****end****: Matches the value as end of field.

- ****word_start****: Matches the start of any word in the field.

- ****anyOf****: Matches any field whose value is any from the given set.

- ****lt****: Matches any field whose value is less than the input value. 
Equivalent to `field < value`. Only for use in comparable (i.e. numeric) fields

- ****le****: Matches any field whose value is less than or equal to the input 
value. Equivalent to `field <= value`.Only for use in comparable (i.e. numeric) 
fields

- ****gt****: Matches any field whose value is greater than the input value. 
Equivalent to `field > value`.Only for use in comparable (i.e. numeric) fields

- ****ge****: Matches any field whose value is greater than or equal to the 
input value. Equivalent to `field >= value`. Only for use in comparable 
(i.e. numeric) fields


In the case of movies exist an additional filter for the genre:

- ****superset****:  Allows to filter by one or more genres.

## Examples:

### Search Movie Title :

[https://wfh-movies.herokuapp.com/movie?filter=partial(title, Toy)](https://wfh-movies.herokuapp.com/movie?filter=partial%28title,%20Toy%29)

### Search Movie by genre with sorts:

[https://wfh-movies.herokuapp.com/movie?filter=superset(genres, \[Adventure\])&sort=title.asc](https://wfh-movies.herokuapp.com/movie?filter=superset%28genres,%20%5BAdventure%5D%29&sort=title.asc)

[https://wfh-movies.herokuapp.com/movie?filter=superset(genres, \[Adventure|Animation\])&sort=budget.desc&sort=release_date.asc](https://wfh-movies.herokuapp.com/movie?filter=superset%28genres,%20%5BAdventure%7CAnimation%5D%29&sort=budget.desc&sort=release_date.asc)

