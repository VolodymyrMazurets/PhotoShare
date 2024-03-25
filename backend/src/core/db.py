# DB connection will be there

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.models import Base

SQLALCHEMY_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@contextmanager
def db_transaction(session: Session):
    """
    The db_transaction function is a context manager that wraps the session object in a try/except block.
    If an exception occurs, it rolls back the transaction and raises the exception. If no exceptions occur,
    it commits the transaction and closes out the session.
    
    :param session: Session: Pass the session object to the function
    :return: A context manager
    """
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
