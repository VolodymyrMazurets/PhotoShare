# DB connection will be there

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from src.models import Base

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:111111@localhost:5432/postgres"
SQLALCHEMY_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(
    'postgresql+psycopg://postgres:123456@db:5432/photoshare', echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
