from clean_alchemy import BaseRepo

from tests.dummy_dao import DummyDAO
from tests.dummy_entity import DummyEntity


class DummyRepo(BaseRepo[DummyDAO, DummyEntity]):
    dao_class = DummyDAO
    entity_class = DummyEntity

    def _to_entity(self, dao: DummyDAO) -> DummyEntity:
        return DummyEntity(
            key=dao.key,
            created_at=dao.created_at,
            updated_at=dao.updated_at,
            archived=dao.archived,
            name=dao.name,
            age=dao.age,
        )

    def _to_dao(self, entity: DummyEntity) -> DummyDAO:
        return DummyDAO(
            key=entity.key,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            archived=entity.archived,
            name=entity.name,
            age=entity.age,
        )
