from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Boolean
from datetime import datetime


class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    imdb_id = Column(Integer)
    tmdb_id = Column(Integer)
    poster_path = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    budget = Column(Integer, nullable=True)
    rating = Column(Float, nullable=False, default=0)
    vote_count = Column(Integer, nullable=False, default=0)
    genres = Column(String, nullable=False, server_default='')
    description = Column(String, nullable=True)


class Rating(Base):
    __tablename__ = "rating"

    user = Column(Integer, primary_key=True)
    movie = Column(Integer, ForeignKey("movie.id"), primary_key=True)
    rating = Column(Float, nullable=False)
    timestamp = Column(Integer, default=int(datetime.now().timestamp()))
