from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    database_url: str
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://postres:admin123@localhost:5432/wfh-movies'


settings = Settings()
