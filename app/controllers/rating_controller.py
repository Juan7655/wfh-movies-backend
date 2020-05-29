from fastapi import APIRouter

from app.controllers.base_controller import crud
from app.models import schemas, models
from app.models.models import Movie
from app.service.commons import create_instance, instance_existence, save_instance


def create(db, instance, model):
    movie_instance: Movie = instance_existence(Movie, 'id')(id_value=instance.movie, db=db)
    old_rating_sum = movie_instance.rating * movie_instance.vote_count
    new_rating_sum = old_rating_sum + instance.rating
    movie_instance.rating = new_rating_sum / (movie_instance.vote_count + 1)
    movie_instance.vote_count += 1
    save_instance(movie_instance, db=db)

    return create_instance(db=db, instance=instance, model=model)


router = APIRouter()
crud(router, schemas.Rating, schemas.Rating, models.Rating, 'movie_user', post=create)
