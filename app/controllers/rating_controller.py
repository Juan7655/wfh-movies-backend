from fastapi import APIRouter

from app.models import schemas, models
from app.util.decorators import crud

router = APIRouter()
crud(router, schemas.Rating, schemas.Rating, models.Rating, 'movie_user')
