from pydantic import BaseSettings
import logging as log

log.basicConfig(level=log.DEBUG)


class Settings(BaseSettings):
    database_url: str
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://postres:admin123@localhost:5432/wfh-movies'
    audit: str = ''
    api_key: str = ''


settings = Settings()
