import math
import os

import pandas as pd
import requests
from sqlalchemy import create_engine

from extras.db_manager import decorator, db_url

data_path = "data/ml-latest-small/%s.csv"
movie_db_host = os.getenv('MOVIE_DB_HOST')


def get_movie_info(movie):
    year = movie.title.split('(')[-1][:-1]
    movie_result = search_movie_by_title(movie.title.replace(f'({year})', ''), year)
    if movie_result is None:
        print('problems with movie ', movie)
        return movie
    movie['budget'] = get_budget_from_id(movie_result.get('id'))
    movie['release_date'] = movie_result.get('release_date')
    result_poster_path = movie_result.get('poster_path')
    if result_poster_path is not None:
        movie['poster_path'] = 'http://image.tmdb.org/t/p/w185/' + result_poster_path
    return movie


def get_movie_description(title):
    year = title.split('(')[-1][:-1]
    movie_result = search_movie_by_title(title.replace(f'({year})', ''), year)
    if movie_result is None:
        print('problems with movie ', title)
        return ''
    return movie_result.get('overview')


def search_movie_by_title(title: str, year: str = None, retry=0, altern=None):
    path = f'search/movie'
    formatted_title = title.replace(", The ", '').replace(', A ', '').replace(', An ', '') \
        .replace(', Le ', '').replace(', La ', '').strip()
    complete_path = movie_db_host % path + f'&query={formatted_title}'
    if year is not None:
        complete_path = complete_path + '&year=' + year
    json = requests.get(complete_path).json()

    if json.get('total_results') == 0 and retry == 0:
        return search_movie_by_title(title, retry=retry + 1)
    elif json.get('total_results') == 0 and retry == 1:
        split = title.split('(')
        if len(split) < 2:
            return None
        return search_movie_by_title(split[0], retry=retry + 1, altern=split[1].strip()[:-1])
    elif json.get('total_results') == 0 and retry == 2:
        print(f"didn't work with <{formatted_title}> trying with <{altern}>")
        return search_movie_by_title(altern, retry=retry + 1)
    elif json.get('total_results') == 0 and retry > 2:
        print("that didn't go well for ", formatted_title)
        return None
    return json.get('results')[0]


def get_budget_from_id(movie_id):
    response = requests.get(movie_db_host % f'movie/{movie_id}')
    return response.json().get('budget')


def scrape_movie_data():
    links = pd.read_csv(data_path % 'links')
    movies = pd.read_csv(data_path % 'movies')
    joined = movies.set_index('movieId').join(links.set_index('movieId'))
    return joined.apply(get_movie_info, result_type='expand', axis=1)


@decorator
def update_movie_description(id, description):
    description = description.replace("'", "''")
    return f"UPDATE movie SET description='{description}' WHERE id={id}"


def scrape_movies_descriptions():
    movies = get_movies_title(fetchall=True)
    movies_descriptions = ((movie[0], get_movie_description(movie[1])) for movie in movies)
    [update_movie_description(id=id, description=description) for id, description in movies_descriptions]


def scrape_genres_poster_path():
    genres = (result[0] for result in get_genres(fetchall=True))
    posters = ((genre, get_genre_best_movie_poster(genre=genre, fetchall=False)) for genre in genres)
    [update_genre_poster_path(genre=genre, poster_path=poster) for genre, poster in posters]


def upload_data():
    print('Beginning to scrape data')
    df = scrape_movie_data()
    genres = df.genres.str.split('|').apply(pd.Series).unstack().dropna().unique()
    print('Creating genres')
    create_genres(genres=genres)
    print('Creating movie_genre relations')
    df.apply(lambda m: create_movie_genre_relation(movie=m), axis=1)
    df = None  # free memory space
    print('Complete migration for tables Movie, Genre, Movie_Genre')

    print('Reading Rating and Tag data')
    df_ratings = pd.read_csv('../data/ml-latest-small/ratings.csv')
    df_tags = pd.read_csv('../data/ml-latest-small/tags.csv')
    print('Creating users')
    users = df_ratings.userId.append(df_tags.userId).unique()
    create_users(users=users)
    print('Creating tags')
    df_tags.apply(lambda m: create_tag(tag=m), axis=1)
    print('Creating ratings')
    create_ratings(ratings=df_ratings)
    print('Migration complete')


@decorator
def create_genres(genres):
    base_insert = "INSERT INTO genre(id) VALUES ('%s')"
    return base_insert % "'), ('".join(genres)


@decorator
def create_users(users):
    base_insert = "INSERT INTO users(id) VALUES (%s)"
    return base_insert % "), (".join(users.astype('str'))


@decorator
def create_movie_genre_relation(movie):
    create_movie(movie=movie)
    movie_id = movie.movieId
    genres = movie.genres.split('|')
    base_insert = f"INSERT INTO movie_genre(movie, genre) VALUES ({movie_id}, '%s')"
    return base_insert % f"'), ({movie_id}, '".join(genres)


@decorator
def get_movies_title():
    return f"SELECT id, title FROM movie where description isnull"


@decorator
def get_genres():
    return f"SELECT id FROM genre"


@decorator
def get_genre_best_movie_poster(genre):
    return f"""SELECT poster_path FROM movie WHERE genres LIKE '%{genre}%' AND vote_count > 10 
            ORDER BY rating DESC LIMIT 1
            """


@decorator
def update_genre_poster_path(genre, poster_path):
    return f"""UPDATE genre SET poster_path = '{poster_path}' WHERE id = '{genre}'"""


@decorator
def create_tag(tag):
    def format_title(title):
        return title.replace("'", "''")

    base_insert = f'INSERT INTO tag("user", movie, name, timestamp) VALUES '
    return base_insert + f"({tag.userId}, {tag.movieId}, '{format_title(tag.tag)}', {tag.timestamp})"


def create_ratings(ratings):
    engine = create_engine(db_url)
    ratings = ratings.rename(columns={'userId': 'user', 'movieId': 'movie'})
    ratings.to_sql(name='rating', con=engine, if_exists='append', index=False)


@decorator
def create_movie(movie):
    def format_title(title):
        return title.replace("'", "''")

    def remove_nan(field, is_text=False):
        if is_text:
            try:
                if math.isnan(field):
                    return "null"
            except:
                pass
            return f"'{field}'" if field else "null"
        else:
            if math.isnan(field):
                return "null"
            else:
                return field

    base_insert = "INSERT INTO movie(id, title, imdb_id, tmdb_id, poster_path, release_date, budget) VALUES "
    return base_insert + f"({movie.movieId}, '{format_title(movie.title)}', {remove_nan(movie.imdbId)}, " \
                         f"{remove_nan(movie.tmdbId)}, {remove_nan(movie.poster_path, is_text=True)}, " \
                         f"{remove_nan(movie.release_date, is_text=True)}, {remove_nan(movie.budget)})"


scrape_genres_poster_path()
# scrape_movies_descriptions()
# upload_data()
