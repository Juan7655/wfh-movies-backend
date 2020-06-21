from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    external_token = Column(String, unique=True)
    ratings = relationship("Rating", backref="users", uselist=True, lazy=True)


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

    user = Column(Integer, ForeignKey("users.id"), primary_key=True)
    movie = Column(Integer, ForeignKey("movie.id"), primary_key=True)
    rating = Column(Float, nullable=False)
    timestamp = Column(Integer, default=int(datetime.now().timestamp()))


class Review(Base):
    __tablename__ = "review"

    user = Column(Integer, ForeignKey("users.id"), primary_key=True)
    movie = Column(Integer, ForeignKey("movie.id"), primary_key=True)
    comment = Column(String, nullable=False)
    timestamp = Column(Integer, default=int(datetime.now().timestamp()))


class Tag(Base):
    __tablename__ = "tag"

    user = Column(Integer, ForeignKey("users.id"), primary_key=True)
    movie = Column(Integer, ForeignKey("movie.id"), primary_key=True)
    name = Column(String, nullable=False, primary_key=True)
    timestamp = Column(Integer, default=int(datetime.now().timestamp()))


class Watchlist(Base):
    __tablename__ = "watchlist"

    user = Column(Integer, ForeignKey("users.id"), primary_key=True)
    movie = Column(Integer, ForeignKey("movie.id"), primary_key=True)
    timestamp = Column(Integer, default=int(datetime.now().timestamp()))


class Genre(Base):
    __tablename__ = "genre"

    id = Column(String, primary_key=True, index=True)
    poster_path = Column(String, nullable=True)


class Request(Base):
    __tablename__ = "request"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)
    verb = Column(String, nullable=False)
    response_status_code = Column(String)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float)
    with_token = Column(Boolean, default=False)
