from sqlalchemy import Column, Integer, DateTime, String, Boolean

from clean_alchemy.base import Base


class BaseDAO(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    archived = Column(Boolean, default=False, nullable=False)
    archived_at = Column(DateTime, nullable=True)
