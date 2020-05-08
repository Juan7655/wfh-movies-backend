from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.util.decorators import crud
from app.models import schemas, models
from sqlalchemy.orm import Session
from app.database import get_db
from app.service import movie_service

router = APIRouter()
crud(router, schemas.Rating, schemas.Rating, models.Rating, 'user')
