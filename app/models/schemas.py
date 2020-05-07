from typing import List, Optional

from pydantic import BaseModel


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
