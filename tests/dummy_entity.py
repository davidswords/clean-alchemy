from datetime import datetime

from src.clean_alchemy import BaseEntity


class DummyEntity(BaseEntity):
    name: str
    age: int

    def __init__(
        self,
        key: str,
        created_at: datetime,
        updated_at: datetime,
        archived: bool,
        name: str,
        age: int,
    ):
        super().__init__(
            key=key,
            created_at=created_at,
            updated_at=updated_at,
            archived=archived,
            name=name,
            age=age,
        )
