import pytest
from unittest.mock import Mock
from main import app
from app.database import create_engine, sessionmaker, get_db
from fastapi.testclient import TestClient
from config import settings


engine = create_engine(
    settings.database_url, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def web_client():
    return client
