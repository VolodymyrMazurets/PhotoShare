# DB connection will be there

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.core.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:111111@localhost:5432/postgres"
SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()