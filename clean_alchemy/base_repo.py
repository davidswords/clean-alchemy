from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Type

from sqlalchemy.orm import Session

from clean_alchemy import BaseDAO, BaseEntity
from clean_alchemy.config import ENV

DAO_TYPE = TypeVar("DAO_TYPE", bound=BaseDAO)
ENTITY_TYPE = TypeVar("ENTITY_TYPE", bound=BaseEntity)


class BaseRepo(ABC, Generic[DAO_TYPE, ENTITY_TYPE]):
    dao_class: Type[DAO_TYPE] = None
    entity_class: Type[ENTITY_TYPE] = None

    def __init__(self, db_session: Session = None) -> None:
        self.db_session = db_session

    def __init_subclass__(cls) -> None:
        if cls.dao_class is None:
            raise NotImplementedError("Must define a `dao_class` for a BaseRepo.")
        if cls.entity_class is None:
            raise NotImplementedError("Must define a `entity_class` for a BaseRepo.")

    @abstractmethod
    def _to_entity(self, dao: DAO_TYPE) -> ENTITY_TYPE:
        pass

    def _to_entities(self, daos: List[DAO_TYPE]) -> List[ENTITY_TYPE]:
        return [self._to_entity(dao) for dao in daos]

    @abstractmethod
    def _to_dao(self, entity: ENTITY_TYPE) -> DAO_TYPE:
        pass

    def _to_daos(self, entities: List[ENTITY_TYPE]) -> List[DAO_TYPE]:
        return [self._to_dao(entity) for entity in entities]

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

    def _to_mappings(self, entities: List[ENTITY_TYPE]) -> List[dict]:
        daos = self._to_daos(entities=entities)
        return [dao.__dict__.copy() for dao in daos]

    def create_many(self, entities: List[ENTITY_TYPE]) -> List[ENTITY_TYPE]:
        mappings = self._to_mappings(entities=entities)
        self._bulk_insert_mappings(mappings=mappings)
        return entities

    def create(self, entity: ENTITY_TYPE) -> ENTITY_TYPE:
        return self.create_many(entities=[entity]).pop()

    def _filter_by_keys(self, keys: List[str]) -> List[DAO_TYPE]:
        return (
            self.db_session.query(self.dao_class)
            .filter(
                self.dao_class.key.in_(keys),
                self.dao_class.archived.is_(False),
            )
            .all()
        )

    def retrieve_many(self, keys: List[str]) -> List[ENTITY_TYPE]:
        daos = self._filter_by_keys(keys=keys)
        return self._to_entities(daos=daos)

    def retrieve(self, key: str) -> ENTITY_TYPE:
        return self.retrieve_many(keys=[key]).pop()

    def _filter_by_all(self) -> List[DAO_TYPE]:
        return (
            self.db_session.query(self.dao_class)
            .filter(self.dao_class.archived.is_(False))
            .all()
        )

    def retrieve_all(self) -> List[ENTITY_TYPE]:
        daos = self._filter_by_all()
        return self._to_entities(daos=daos)

    def _bulk_update_mappings(self, mappings: List[dict]) -> None:
        self.db_session.bulk_update_mappings(
            mapper=self.dao_class,
            mappings=mappings,
        )
        self._commit()

    def update_many(self, entities: List[ENTITY_TYPE]) -> List[ENTITY_TYPE]:
        mappings = self._to_mappings(entities=entities)
        self._bulk_update_mappings(mappings=mappings)
        return entities

    def update(self, entity: ENTITY_TYPE) -> ENTITY_TYPE:
        return self.update_many(entities=[entity]).pop()

    def delete_many(self, keys: List[str]) -> None:
        mappings = [{"key": key, "archived": True} for key in keys]
        self._bulk_update_mappings(mappings=mappings)

    def delete(self, key: str) -> None:
        self.delete_many(keys=[key])
