import os

from sqlalchemy import create_engine, text

from app.db.base import Base
from app.models import Product, Space, InventoryItem


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://gestor:gestor@localhost:5432/gestor_nutricional"
)


engine = create_engine(DATABASE_URL)


def create_tables():
    """
    Crea las tablas definidas en los modelos SQLAlchemy.
    """
    Base.metadata.create_all(bind=engine)


def test_connection():
    """
    Comprueba que existe conexión con PostgreSQL.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar()
