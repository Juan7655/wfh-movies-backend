from pydantic import BaseModel
from datetime import datetime


class Rating(BaseModel):
    user: int
    movie: int
    rating: float
    timestamp: int = int(datetime.now().timestamp())

    class Config:
        orm_mode = True