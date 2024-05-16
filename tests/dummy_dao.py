from sqlalchemy import Column, Integer, String

from clean_alchemy.base_dao import BaseDAO


class DummyDAO(BaseDAO):
    __tablename__ = "dummy"

    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
