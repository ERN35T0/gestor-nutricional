from sqlalchemy import create_engine


DATABASE_URL = (
    "postgresql+psycopg://gestor:gestor@localhost:5432/gestor_nutricional"
)


engine = create_engine(DATABASE_URL)

from sqlalchemy import text


def test_connection():
    """Comprueba que existe conexión con PostgreSQL."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar()
