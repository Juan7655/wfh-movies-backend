from pydantic import BaseSettings
import os
import logging as log

log.basicConfig(level=log.DEBUG)


class Settings(BaseSettings):
    database_url: str = os.environ["HEROKU_POSTGRESQL_IVORY_URL"]
    SQLALCHEMY_DATABASE_URI: str = os.environ["HEROKU_POSTGRESQL_IVORY_URL"]
    audit: str = ''
    api_key: str = ''


settings = Settings()
