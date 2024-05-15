from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Type

from sqlalchemy.orm import Session

from src.data.base_dao import BaseDAO
from src.domain.base_ent import BaseENT
from src.config import ENV

DAO_TYPE = TypeVar("DAO_TYPE", bound=BaseDAO)
ENT_TYPE = TypeVar("ENT_TYPE", bound=BaseENT)


class BaseRPO(ABC, Generic[DAO_TYPE, ENT_TYPE]):
    dao_class: Type[DAO_TYPE] = None
    ent_class: Type[ENT_TYPE] = None

    def __init__(cls, db_session: Session = None) -> None:
        cls.db_session = db_session

    def __init_subclass__(cls) -> None:
        if cls.dao_class is None:
            raise NotImplementedError("Must define a `dao_class` for a BaseRPO.")
        if cls.ent_class is None:
            raise NotImplementedError("Must define a `ent_class` for a BaseRPO.")

    @abstractmethod
    def _to_ent(self, dao: DAO_TYPE) -> ENT_TYPE:
        pass

    def _to_ents(self, daos: List[DAO_TYPE]) -> List[ENT_TYPE]:
        return [self._to_ent(dao) for dao in daos]

    @abstractmethod
    def _to_dao(self, ent: ENT_TYPE) -> DAO_TYPE:
        pass

    def _to_daos(self, ents: List[ENT_TYPE]) -> List[DAO_TYPE]:
        return [self._to_dao(ent) for ent in ents]

    def _commit(self) -> None:
        if ENV in ["production", "development"]:
            self.db_session.commit()
        else:
            self.db_session.flush()

    def _bulk_insert_mappings(self, mappings: List[dict]) -> None:
        self.db_session.bulk_insert_mappings(
            mapper=self.dao_class,
            mappings=mappings,
        )
        self._commit()

    def _to_mappings(self, ents: List[ENT_TYPE]) -> List[dict]:
        daos = self._to_daos(ents=ents)
        return [dao.__dict__.copy() for dao in daos]

    def create_many(self, ents: List[ENT_TYPE]) -> List[ENT_TYPE]:
        mappings = self._to_mappings(ents=ents)
        self._bulk_insert_mappings(mappings=mappings)
        return ents

    def create(self, ent: ENT_TYPE) -> ENT_TYPE:
        return self.create_many(ents=[ent]).pop()

    def _filter_by_keys(self, keys: List[str]) -> List[DAO_TYPE]:
        return (
            self.db_session.query(self.dao_class)
            .filter(
                self.dao_class.key.in_(keys),
                self.dao_class.archived.is_(False),
            )
            .all()
        )

    def retrieve_many(self, keys: List[str]) -> List[ENT_TYPE]:
        daos = self._filter_by_keys(keys=keys)
        return self._to_ents(daos=daos)

    def retrieve(self, key: str) -> ENT_TYPE:
        return self.retrieve_many(keys=[key]).pop()

    def _filter_by_all(self) -> List[DAO_TYPE]:
        return (
            self.db_session.query(self.dao_class)
            .filter(self.dao_class.archived.is_(False))
            .all()
        )

    def retrieve_all(self) -> List[ENT_TYPE]:
        daos = self._filter_by_all()
        return self._to_ents(daos=daos)

    def _bulk_update_mappings(self, mappings: List[dict]) -> None:
        self.db_session.bulk_update_mappings(
            mapper=self.dao_class,
            mappings=mappings,
        )
        self._commit()

    def update_many(self, ents: List[ENT_TYPE]) -> List[ENT_TYPE]:
        mappings = self._to_mappings(ents=ents)
        self._bulk_update_mappings(mappings=mappings)
        return ents

    def update(self, ent: ENT_TYPE) -> ENT_TYPE:
        return self.update_many(ents=[ent]).pop()

    def delete_many(self, keys: List[str]) -> None:
        mappings = [{"key": key, "archived": True} for key in keys]
        self._bulk_update_mappings(mappings=mappings)

    def delete(self, key: str) -> None:
        self.delete_many(keys=[key])
