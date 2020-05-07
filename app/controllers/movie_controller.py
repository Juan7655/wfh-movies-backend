from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models import schemas
from sqlalchemy.orm import Session
from app.database import get_db
from app.service import movie_service

router = APIRouter()


@router.post("", response_model=schemas.MovieRead)
def create_movie(movie: schemas.Movie, db: Session = Depends(get_db)):
    db_user = movie_service.get_movie_by_title(db, title=movie.title)
    if db_user:
        raise HTTPException(status_code=400, detail="Movie already registered")
    return movie_service.create_movie(db=db, movie=movie)


@router.get("", response_model=List[schemas.MovieRead])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return movie_service.get_movies(db, skip=skip, limit=limit)


@router.get("/{movie_id}", response_model=schemas.MovieRead)
async def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = movie_service.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie
