import os

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://gestor:gestor@localhost:5432/gestor_nutricional_test"
)

import pytest
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.database import engine
from app.db.session import SessionLocal
from app.main import app, get_db


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()
