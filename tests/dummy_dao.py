from sqlalchemy import Column, Integer, String

from src.data.base_dao import BaseDAO


class DummyDAO(BaseDAO):
    __tablename__ = "dummy"

    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
