from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import paths
from app.database import get_db
from app.models import schemas, models
from app.models.models import User, Movie
from app.models.schemas import Page
from app.service.commons import error_docs, instance_existence
from app.service.recommendation_service import similar_movies, user_recommendations
from app.util.decorators import error_handling
from app.util.errors import ResourceDoesNotExist, ResourceStateConflict

router = APIRouter()
paths['recommendation'] = router


def recommendations_paginator(res: List[Movie]) -> Page[schemas.Movie]:
    return Page(page=1, total_pages=1, total_items=len(res), items_per_page=5, has_next=False, has_prev=False, items=res)


@router.get(
    '/movie/{id}',
    response_model=Page[schemas.MovieRecommendation],
    responses=error_docs(
        models.Movie.__name__,
        ResourceDoesNotExist,
        ResourceStateConflict('To give a proper recommendation, the movie should have at least 5 ratings')))
@error_handling
def movie_similarities(
        db: Session = Depends(get_db),
        movie: Movie = Depends(instance_existence(Movie, id_field='id'))
):
    movies = similar_movies(db=db, movie=movie)
    return recommendations_paginator(movies)


@router.get('/user/{id}',
            response_model=Page[schemas.MovieUserRecommendation],
            responses=error_docs(models.User.__name__, ResourceDoesNotExist))
@error_handling
def get_user_recommendations(
        db: Session = Depends(get_db),
        user: User = Depends(instance_existence(User, id_field='id'))
):
    recommendations = user_recommendations(db=db, user=user)
    return recommendations_paginator(recommendations)
