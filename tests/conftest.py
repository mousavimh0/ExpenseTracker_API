import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///test.db"

test_engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(bind=test_engine)


def override_get_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def clean_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


@pytest.fixture
def db():
    db = TestSessionLocal()

    try:
        yield db

    finally:
        db.close()
