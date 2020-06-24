from typing import List, Set, Tuple

import numpy as np
from sqlalchemy import func, desc, or_
from sqlalchemy.orm import Session

from app.models.models import Movie, Rating, User
from app.util.errors import ResourceStateConflict


def similar_movies(db: Session, movie: Movie) -> List[Movie]:
    movies_similarities = get_similar_items(Rating.user, Rating.rating, db, 'movie', movie.id)
    movies_recommendations = db.query(Movie).filter(Movie.id.in_(movies_similarities.keys())).all()
    [setattr(movie, 'cosine_similarity', movies_similarities.get(movie.id)) for movie in movies_recommendations]
    return movies_recommendations


def get_movie_ratings_users(db: Session, movie_id: int) -> Set[int]:
    movie_ratings_users = db.query(Rating.user).filter_by(movie=movie_id).all()
    return set(i for i, in movie_ratings_users)


def calculate_movie_similarity(db: Session, movie_id_1: int, movie_id_2: int) -> float:
    users_movie_1 = get_movie_ratings_users(db=db, movie_id=movie_id_1)
    users_movie_2 = get_movie_ratings_users(db=db, movie_id=movie_id_2)
    common_users = users_movie_1 & users_movie_2
    ratings_movie_1 = get_movie_ratings_filter_by_users(common_users, db, movie_id_1)
    ratings_movie_2 = get_movie_ratings_filter_by_users(common_users, db, movie_id_2)

    np_1 = np.array(ratings_movie_1)
    np_2 = np.array(ratings_movie_2)

    return np.sum(np_1 * np_2) / np.sqrt(np.sum(np_1 * np_1) * np.sum(np_2 * np_2))


def get_movie_ratings_filter_by_users(common_users, db, movie_id):
    return db.query(Rating.rating) \
        .filter_by(movie=movie_id) \
        .filter(Rating.user.in_(common_users)) \
        .order_by(desc(Rating.user)) \
        .all()


def get_similar_items(col_comparison, col_value, db, entity_col_name, entity_id):
    items = select_distinct_by(db=db, select_col=col_comparison, **{entity_col_name: entity_id})
    if len(items) < 5:
        raise ResourceStateConflict(
            f'To give a proper recommendation, the {entity_col_name} should have at least 5 ratings')
    entity_col = getattr(Rating, entity_col_name)
    most_shared_items = get_shared_items(col_comparison, db, entity_col, items)
    similar = set(similar_entity for similar_entity, in most_shared_items if similar_entity != entity_id)

    def similarity_to(i):
        return calculate_similarity(
            db=db,
            id_1=entity_id,
            id_2=i,
            col_comparison=col_comparison,
            col_value=col_value,
            entity_col=entity_col_name
        )

    results = [(i, similarity_to(i)) for i in similar]
    results.sort(key=lambda x: -x[1])  # sort desc by similarity
    return {similar_id: similarity for similar_id, similarity in results[:5]}


def get_shared_items(col_comparison, db, entity_col, items):
    return db.query(entity_col) \
        .filter(col_comparison.in_(items)) \
        .group_by(entity_col) \
        .order_by(desc(func.count(entity_col))) \
        .limit(21) \
        .all()


def calculate_similarity(db: Session, id_1: int, id_2: int, col_comparison, col_value, entity_col) -> float:
    users_movie_1 = select_distinct_by(db=db, select_col=col_comparison, **{entity_col: id_1})
    users_movie_2 = select_distinct_by(db=db, select_col=col_comparison, **{entity_col: id_2})

    common_users = users_movie_1 & users_movie_2
    ratings_movie_1 = get_ordered_query(common_set=common_users, db=db, select_col=col_value,
                                        sort_col=col_comparison, **{entity_col: id_1})
    ratings_movie_2 = get_ordered_query(common_set=common_users, db=db, select_col=col_value,
                                        sort_col=col_comparison, **{entity_col: id_2})

    np_1 = np.array(ratings_movie_1)
    np_2 = np.array(ratings_movie_2)

    return np.sum(np_1 * np_2) / np.sqrt(np.sum(np_1 * np_1) * np.sum(np_2 * np_2))


def select_distinct_by(db: Session, select_col, **kwargs) -> Set[int]:
    filtered_query = db.query(select_col).filter_by(**kwargs).all()
    return set(i for i, in filtered_query)


def get_ordered_query(common_set, db, select_col, sort_col, **kwargs) -> List[float]:
    return db.query(select_col) \
        .filter_by(**kwargs) \
        .filter(sort_col.in_(common_set)) \
        .order_by(desc(sort_col)) \
        .all()


def user_recommendations(db: Session, user: User) -> List[Movie]:
    movies_rated: List[Rating] = user.ratings

    if len(movies_rated) < 5:
        return db.query(Movie) \
            .filter(or_(*tuple(Movie.genres.ilike(f'%{v}%') for v in user.genres.split('|')))) \
            .filter(Movie.vote_count > 10) \
            .filter(Movie.id.notin_([r.movie for r in movies_rated])) \
            .order_by(desc(Movie.rating)) \
            .limit(5) \
            .all()

    user_similarities = get_similar_items(
        db=db,
        entity_id=user.id,
        col_comparison=Rating.movie,
        col_value=Rating.rating,
        entity_col_name='user'
    )

    results: List[Tuple[Movie, float]] = db.query(Movie, func.max(Rating.rating)) \
        .filter(Rating.user.in_(user_similarities.keys())) \
        .filter(Rating.movie.notin_([r.movie for r in movies_rated])) \
        .filter(Rating.movie == Movie.id) \
        .group_by(Movie.id) \
        .order_by(desc(func.max(Rating.rating))) \
        .limit(5) \
        .all()

    [setattr(movie, 'expected_rating', rating) for movie, rating in results]
    return [movie for movie, rating in results]
