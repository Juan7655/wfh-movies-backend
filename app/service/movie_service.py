from sqlalchemy.orm import Session

from app.models import schemas, models
from typing import List


def get_movie(db: Session, movie_id: int) -> models.Movie:
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def get_movie_by_title(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title == title).first()


def get_movies(db: Session, skip: int = 0, limit: int = 100) -> List[models.Movie]:
    return db.query(models.Movie).offset(skip).limit(limit).all()


def create_movie(db: Session, movie: schemas.Movie):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
