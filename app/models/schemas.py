from typing import Optional, TypeVar, Generic, List, Type

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')


class Movie(BaseModel):
    title: str
    imdb_id: Optional[int]
    tmdb_id: Optional[int] = None
    poster_path: Optional[str] = None
    # release_date: Optional[str] = None
    budget: Optional[int] = None

    class Config:
        orm_mode = True


class MovieRead(Movie):
    id: int


class Rating(BaseModel):
    user: int
    movie: int
    rating: float
    timestamp: int = None

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
