from fastapi import APIRouter

from app.models import schemas, models
from app.util.decorators import crud

router = APIRouter()
crud(router, schemas.MovieRead, schemas.Movie, models.Movie, 'id')
