from src.data.rpo import BaseRPO
from tests.dummy_dao import DummyDAO
from tests.dummy_ent import DummyENT


class DummyRPO(BaseRPO[DummyDAO, DummyENT]):
    dao_class = DummyDAO
    ent_class = DummyENT

    def _to_ent(self, dao: DummyDAO) -> DummyENT:
        return DummyENT(
            key=dao.key,
            created_at=dao.created_at,
            updated_at=dao.updated_at,
            archived=dao.archived,
            name=dao.name,
            age=dao.age,
        )

    def _to_dao(self, ent: DummyENT) -> DummyDAO:
        return DummyDAO(
            key=ent.key,
            created_at=ent.created_at,
            updated_at=ent.updated_at,
            archived=ent.archived,
            name=ent.name,
            age=ent.age,
        )