from datetime import datetime, date
from typing import TypeVar, Generic, List

from pydantic import BaseModel, HttpUrl
from pydantic.generics import GenericModel

T = TypeVar('T')


class MovieGenre(BaseModel):
    genre: str

    class Config:
        orm_mode = True


class Movie(BaseModel):
    title: str
    imdb_id: int
    tmdb_id: int = None
    poster_path: HttpUrl = None
    release_date: date = None
    budget: int = None

    class Config:
        orm_mode = True


class MovieRead(Movie):
    id: int
    genres: List[MovieGenre] = []


class Rating(BaseModel):
    user: int
    movie: int
    rating: float
    timestamp: int = int(datetime.now().timestamp())

    class Config:
        orm_mode = True


class Page(GenericModel, Generic[T]):
    page: int
    total_pages: int
    total_items: int
    items_per_page: int
    has_next: bool
    has_prev: bool
    items: List[T]

    class Config:
        orm_mode = True


class Tag(BaseModel):
    user: int
    movie: int
    name: str
    timestamp: int

    class Config:
        orm_mode = True
