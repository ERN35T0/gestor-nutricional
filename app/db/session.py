from sqlalchemy.orm import sessionmaker

from app.db.database import engine


# Crea sesiones de conexión contra PostgreSQL
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
