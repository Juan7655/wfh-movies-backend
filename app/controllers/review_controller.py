from fastapi import APIRouter

from app.controllers.base_controller import crud
from app.models import schemas, models


router = APIRouter()
crud(router, schemas.Review, schemas.Review, models.Review, 'movie_user')
