from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import paths
from app.database import get_db
from app.models import schemas, models
from app.models.models import User, Movie
from app.service.commons import error_docs, instance_existence
from app.service.recommendation_service import similar_movies, user_recommendations
from app.util.decorators import error_handling
from app.util.errors import ResourceDoesNotExist, ResourceStateConflict

router = APIRouter()
paths['recommendation'] = router


@router.get(
    '/movie/{id}',
    response_model=List[schemas.MovieRecommendation],
    responses=error_docs(
        models.Movie.__name__,
        ResourceDoesNotExist,
        ResourceStateConflict('To give a proper recommendation, the movie should have at least 5 ratings')
    ))
@error_handling
def movie_similarities(
        db: Session = Depends(get_db),
        movie: Movie = Depends(instance_existence(Movie, id_field='id'))
):
    return similar_movies(db=db, movie=movie)


@router.get('/user/{id}',
            response_model=List[schemas.MovieUserRecommendation],
            responses=error_docs(models.User.__name__, ResourceDoesNotExist))
@error_handling
def get_user_recommendations(
        db: Session = Depends(get_db),
        user: User = Depends(instance_existence(User, id_field='id'))
):
    return user_recommendations(db=db, user=user)
