from fastapi import APIRouter

from app.models import schemas, models
from app.controllers.base_controller import crud

router = APIRouter()
crud(router, schemas.Genre, schemas.Genre, models.Genre, 'id')
