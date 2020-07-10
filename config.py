from pydantic import BaseSettings
import logging

log = logging.getLogger("api")
log.setLevel(level=logging.DEBUG)


class Settings(BaseSettings):
    database_url: str
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://postres:admin123@localhost:5432/wfh-movies'
    audit: str = ''
    api_key: str = ''
    project_id: str = "hey-movie"
    topic_name: str = "HeyMovieTema"


settings = Settings()
