from datetime import datetime, date
from typing import TypeVar, Generic, List

from pydantic import BaseModel, HttpUrl
from pydantic.generics import GenericModel

T = TypeVar('T')


class Genre(BaseModel):
    id: str
    poster_path: HttpUrl = None

    class Config:
        orm_mode = True


class User(BaseModel):
    id: str
    external_token: str = None

    class Config:
        orm_mode = True


class Movie(BaseModel):
    title: str
    imdb_id: int
    tmdb_id: int = None
    poster_path: HttpUrl = None
    release_date: date = None
    budget: int = None
    genres: str = ""
    description: str = ""

    class Config:
        orm_mode = True


class MovieRead(Movie):
    id: int
    rating: float
    vote_count: int


class Rating(BaseModel):
    user: int
    movie: int
    rating: float
    timestamp: int = int(datetime.now().timestamp())

    class Config:
        orm_mode = True


class Review(BaseModel):
    user: int
    movie: int
    comment: str
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


class Watchlist(BaseModel):
    user: int
    movie: int
    timestamp: int = int(datetime.now().timestamp())

    class Config:
        orm_mode = True
