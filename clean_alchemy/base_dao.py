from sqlalchemy import Column, Integer, DateTime, String, Boolean

from clean_alchemy.base import Base


class BaseDAO(Base):
    __abstract__ = True

    id = Column(Integer, autoincrement=True)
    key = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    archived = Column(Boolean, default=False, nullable=False, index=True)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseDAO):
            return False

        return (
            self.key == other.key
            and self.created_at == other.created_at
            and self.updated_at == other.updated_at
            and self.archived == other.archived
        )
