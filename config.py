from pydantic import BaseSettings
import logging

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('google').setLevel(level=logging.ERROR)
logging.getLogger('urllib3').setLevel(level=logging.ERROR)


class Settings(BaseSettings):
    database_url: str
    SQLALCHEMY_DATABASE_URI: str
    project_id: str
    subscription_name: str


settings = Settings()
