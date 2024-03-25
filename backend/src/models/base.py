from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, func
from sqlalchemy.sql.sqltypes import DateTime


class CommonBase(object):
    id = Column(Integer, primary_key=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('update_at', DateTime, default=func.now())


Base = declarative_base(cls=CommonBase)
