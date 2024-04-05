from sqlalchemy import Column, Integer, func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.schema import MetaData

metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
