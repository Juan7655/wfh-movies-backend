from fastapi import APIRouter

from app.models import schemas, models
from app.controllers.base_controller import crud

router = APIRouter()
crud(router, schemas.MovieRead, schemas.Movie, models.Movie, 'id')
