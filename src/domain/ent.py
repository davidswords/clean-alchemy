from datetime import datetime

from pydantic import BaseModel

class BaseENT(BaseModel):
    def __init__(
        self,
        key: str,
        created_at: datetime,
        updated_at: datetime,
        archived: bool,
    ):
        self.key = key
        self.created_at = created_at
        self.updated_at = updated_at
        self.archived = archived

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, BaseENT):
            return False

        return (
            self.key == value.key
            and self.created_at == value.created_at
            and self.updated_at == value.updated_at
            and self.archived == value.archived
        )
