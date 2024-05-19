from datetime import datetime

from pydantic import BaseModel


class BaseEntity(BaseModel):
    key: str
    created_at: datetime
    updated_at: datetime
    archived: bool = False
    archived_at: datetime = None
