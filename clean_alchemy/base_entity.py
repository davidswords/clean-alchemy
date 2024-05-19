from datetime import datetime

from pydantic import BaseModel


class BaseEntity(BaseModel):
    key: str
    created_at: datetime
    updated_at: datetime
    archived: bool

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseEntity):
            return False

        return (
            self.key == value.key
            and self.created_at == value.created_at
            and self.updated_at == value.updated_at
            and self.archived == value.archived
        )
