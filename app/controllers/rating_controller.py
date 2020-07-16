from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers import paths
from app.controllers.base_controller import crud
from app.database import get_db
from app.models import schemas, models
from app.models.models import Movie
from app.service.commons import create_instance, instance_existence, save_instance, error_docs, RatingsHistory
from app.service.ratings_service import get_rolling_avg_movie_ratings
from app.util.decorators import error_handling
from app.util.errors import ResourceDoesNotExist


def create(db, instance, model):
    movie_instance: Movie = instance_existence(Movie, 'id')(id_value=instance.movie, db=db)
    old_rating_sum = movie_instance.rating * movie_instance.vote_count
    new_rating_sum = old_rating_sum + instance.rating
    movie_instance.rating = new_rating_sum / (movie_instance.vote_count + 1)
    movie_instance.vote_count += 1
    save_instance(movie_instance, db=db)

    return create_instance(db=db, instance=instance, model=model)


router = crud(schemas.Rating, schemas.Rating, models.Rating, 'movie_user', post=create)
paths['rating'] = router


@router.get(
    "/rolling-avg/{id}",
    responses={200: RatingsHistory().definition, **error_docs('Movie', ResourceDoesNotExist)}
)
@error_handling
def get_movie_ratings_history_by_year(
        db: Session = Depends(get_db),
        movie: Movie = Depends(instance_existence(Movie, id_field='id'))
):
    return get_rolling_avg_movie_ratings(db, movie.id)
