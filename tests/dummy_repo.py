from src.clean_alchemy import BaseRepo

from tests.dummy_dao import DummyDAO
from tests.dummy_entity import DummyEntity


class DummyRepo(BaseRepo[DummyDAO, DummyEntity]):
    dao_class = DummyDAO
    ent_class = DummyEntity

    def _to_ent(self, dao: DummyDAO) -> DummyEntity:
        return DummyEntity(
            key=dao.key,
            created_at=dao.created_at,
            updated_at=dao.updated_at,
            archived=dao.archived,
            name=dao.name,
            age=dao.age,
        )

    def _to_dao(self, ent: DummyEntity) -> DummyDAO:
        return DummyDAO(
            key=ent.key,
            created_at=ent.created_at,
            updated_at=ent.updated_at,
            archived=ent.archived,
            name=ent.name,
            age=ent.age,
        )
