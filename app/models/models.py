from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)


class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    imdb_id = Column(Integer)
    tmdb_id = Column(Integer)
    poster_path = Column(String, nullable=True)
    release_date = Column(Date, nullable=True)
    budget = Column(Integer, nullable=True)


class Rating(Base):
    __tablename__ = "rating"

    user = Column(Integer, ForeignKey("users.id"), primary_key=True)
    movie = Column(Integer, ForeignKey("movie.id"), primary_key=True)
    rating = Column(Float, nullable=False)
    timestamp = Column(Integer, default=int(datetime.now().timestamp()))


class Tag(Base):
    __tablename__ = "tag"

    user = Column(Integer, ForeignKey("users.id"), primary_key=True)
    movie = Column(Integer, ForeignKey("movie.id"), primary_key=True)
    name = Column(String, index=True, nullable=False)
    timestamp = Column(Integer, default=int(datetime.now().timestamp()))


class Genre(Base):
    __tablename__ = "genre"

    id = Column(String, primary_key=True, index=True)


class MovieGenre(Base):
    __tablename__ = "movie_genre"

    movie = Column(Integer, ForeignKey("movie.id"), primary_key=True)
    genre = Column(String, ForeignKey("genre.id"), primary_key=True)