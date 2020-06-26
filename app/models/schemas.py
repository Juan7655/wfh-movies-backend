from datetime import datetime, date
from typing import TypeVar, Generic, List

from pydantic import BaseModel, HttpUrl, EmailStr
from pydantic.generics import GenericModel

T = TypeVar('T')


class Genre(BaseModel):
    id: str
    poster_path: HttpUrl = None

    class Config:
        orm_mode = True


class Section(BaseModel):
    id: str
    poster_function: str = 'query(Movie)'
    is_principal: bool = False
    description: str = ''
    section_ordering: int = 0

    class Config:
        orm_mode = True


class SectionRead(Section):
    poster_path: HttpUrl = None


class UserWrite(BaseModel):
    external_token: str = None
    name: str = None
    email: EmailStr = None
    genres: str = ''

    class Config:
        orm_mode = True


class UserRead(UserWrite):
    id: str


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


class MovieRecommendation(MovieRead):
    cosine_similarity: float = None


class MovieUserRecommendation(MovieRead):
    expected_rating: float = None


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
