from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers import paths
from app.controllers.base_controller import crud
from app.service.ratings_service import get_rolling_avg_movie_ratings
from app.database import get_db
from app.models import schemas, models
from app.models.models import Movie
from app.service.commons import create_instance, instance_existence, save_instance, error_docs, RatingsHistory
from app.util.decorators import error_handling
from app.util.errors import ResourceDoesNotExist
from app.service.pubsub_publisher import publish


def create(instance):
    publish(instance.dict())
    return 'Rating published successfully'


router = crud(schemas.Rating, schemas.Rating, models.Rating, 'movie_user', post=create)
paths['rating'] = router
