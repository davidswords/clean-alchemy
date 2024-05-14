from datetime import datetime
from src.domain.ent import BaseENT


class DummyENT(BaseENT):
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
        )

        self.name = name
        self.age = age
