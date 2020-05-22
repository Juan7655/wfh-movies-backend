import pytest
from unittest.mock import Mock
from main import app
from app.database import create_engine, sessionmaker, Base, get_db
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db is not None:
            db.rollback()
            db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def _db():
    db = Mock()

    for m in [db.add, db.add_all, db.commit, db.close, db.refresh]:
        m.return_value = None

    return db


@pytest.fixture
def web_client():
    return client
