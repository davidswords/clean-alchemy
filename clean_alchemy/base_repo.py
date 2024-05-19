from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TypeVar, List, Type, Any

from sqlalchemy.orm import Session, Query

from clean_alchemy import BaseDAO, BaseEntity
from clean_alchemy.config import ENV

DAO_TYPE = TypeVar("DAO_TYPE", bound=BaseDAO)
ENTITY_TYPE = TypeVar("ENTITY_TYPE", bound=BaseEntity)


class BaseRepo(ABC, Generic[DAO_TYPE, ENTITY_TYPE]):
    """
    A base repository class providing common database operations for data access objects (DAOs) and entities.

    Attributes:
        dao_class (Type[DAO_TYPE]): The DAO class associated with the repository.
        entity_class (Type[ENTITY_TYPE]): The entity class associated with the repository.
        db_session (Session): The SQLAlchemy database session.
    """

    dao_class: Type[DAO_TYPE] = None
    entity_class: Type[ENTITY_TYPE] = None

    def __init__(self, db_session: Session = None) -> None:
        """
        Initializes the BaseRepo with a given database session.

        Args:
            db_session (Session): The SQLAlchemy database session to use for data operations.
        """
        self.db_session = db_session

    def __init_subclass__(cls) -> None:
        """
        Ensures that subclasses define dao_class and entity_class attributes.

        Raises:
            NotImplementedError: If dao_class or entity_class is not defined in the subclass.
        """
        if cls.dao_class is None:
            raise NotImplementedError("Must define a `dao_class` for a BaseRepo.")
        if cls.entity_class is None:
            raise NotImplementedError("Must define an `entity_class` for a BaseRepo.")

    @abstractmethod
    def _to_entity(self, dao: DAO_TYPE) -> ENTITY_TYPE:
        """
        Converts a DAO to an entity.

        Args:
            dao (DAO_TYPE): The DAO to convert.

        Returns:
            ENTITY_TYPE: The converted entity.
        """
        pass

    def _to_entities(self, daos: List[DAO_TYPE]) -> List[ENTITY_TYPE]:
        """
        Converts a list of DAOs to a list of entities.

        Args:
            daos (List[DAO_TYPE]): A list of DAOs to convert.

        Returns:
            List[ENTITY_TYPE]: A list of converted entities.
        """
        return [self._to_entity(dao) for dao in daos]

    @abstractmethod
    def _to_dao(self, entity: ENTITY_TYPE) -> DAO_TYPE:
        """
        Converts an entity to a DAO.

        Args:
            entity (ENTITY_TYPE): The entity to convert.

        Returns:
            DAO_TYPE: The converted DAO.
        """
        pass

    def _to_daos(self, entities: List[ENTITY_TYPE]) -> List[DAO_TYPE]:
        """
        Converts a list of entities to a list of DAOs.

        Args:
            entities (List[ENTITY_TYPE]): A list of entities to convert.

        Returns:
            List[DAO_TYPE]: A list of converted DAOs.
        """
        return [self._to_dao(entity) for entity in entities]

    def _commit(self) -> None:
        """
        Commits the current transaction if in production or development environment, otherwise flushes the session.
        """
        if ENV in ["production", "development"]:
            self.db_session.commit()
        else:
            self.db_session.flush()

    def _bulk_insert_mappings(self, mappings: List[dict]) -> None:
        """
        Performs a bulk insert of mappings into the database.

        Args:
            mappings (List[dict]): A list of dictionaries representing the data to insert.
        """
        self.db_session.bulk_insert_mappings(
            mapper=self.dao_class,
            mappings=mappings,
        )
        self._commit()

    def _to_mappings(self, entities: List[ENTITY_TYPE]) -> List[dict]:
        """
        Converts a list of entities to a list of mappings (dictionaries).

        Args:
            entities (List[ENTITY_TYPE]): A list of entities to convert.

        Returns:
            List[dict]: A list of dictionaries representing the entities.
        """
        daos = self._to_daos(entities=entities)
        return [dao.__dict__.copy() for dao in daos]

    def create_many(self, entities: List[ENTITY_TYPE]) -> List[ENTITY_TYPE]:
        """
        Creates multiple entities in the database.

        Args:
            entities (List[ENTITY_TYPE]): A list of entities to create.

        Returns:
            List[ENTITY_TYPE]: A list of created entities.
        """
        mappings = self._to_mappings(entities=entities)
        self._bulk_insert_mappings(mappings=mappings)
        return entities

    def create(self, entity: ENTITY_TYPE) -> ENTITY_TYPE:
        """
        Creates a single entity in the database.

        Args:
            entity (ENTITY_TYPE): The entity to create.

        Returns:
            ENTITY_TYPE: The created entity.
        """
        return self.create_many(entities=[entity]).pop()

    def _filter_by_all(self) -> Query[Any]:
        """
        Filters all DAOs that are not archived.

        Returns:
            Query[Any]: A SQLAlchemy query for non-archived DAOs.
        """
        return self.db_session.query(self.dao_class).filter(
            self.dao_class.archived.is_(False)
        )

    def _filter_by_keys(self, keys: List[str]) -> Query[Any]:
        """
        Filters DAOs by a list of keys.

        Args:
            keys (List[str]): A list of keys to filter by.

        Returns:
            Query[Any]: A SQLAlchemy query for DAOs matching the keys.
        """
        return self._filter_by_all().filter(self.dao_class.key.in_(keys))

    def retrieve_many(self, keys: List[str]) -> List[ENTITY_TYPE]:
        """
        Retrieves multiple entities by their keys.

        Args:
            keys (List[str]): A list of keys of the entities to retrieve.

        Returns:
            List[ENTITY_TYPE]: A list of retrieved entities.
        """
        daos = self._filter_by_keys(keys=keys).all()
        return self._to_entities(daos=daos)

    def retrieve(self, key: str) -> ENTITY_TYPE:
        """
        Retrieves a single entity by its key.

        Args:
            key (str): The key of the entity to retrieve.

        Returns:
            ENTITY_TYPE: The retrieved entity.
        """
        return self.retrieve_many(keys=[key]).pop()

    def retrieve_all(self) -> List[ENTITY_TYPE]:
        """
        Retrieves all non-archived entities.

        Returns:
            List[ENTITY_TYPE]: A list of all non-archived entities.
        """
        daos = self._filter_by_all().all()
        return self._to_entities(daos=daos)

    def _bulk_update_mappings(self, mappings: List[dict]) -> None:
        """
        Performs a bulk update of mappings in the database.

        Args:
            mappings (List[dict]): A list of dictionaries representing the data to update.
        """
        self.db_session.bulk_update_mappings(
            mapper=self.dao_class,
            mappings=mappings,
        )
        self._commit()

    def update_many(self, entities: List[ENTITY_TYPE]) -> None:
        """
        Updates multiple entities in the database.

        Args:
            entities (List[ENTITY_TYPE]): A list of entities to update.
        """
        mappings = self._to_mappings(entities=entities)
        self._bulk_update_mappings(mappings=mappings)

    def update(self, entity: ENTITY_TYPE) -> None:
        """
        Updates a single entity in the database.

        Args:
            entity (ENTITY_TYPE): The entity to update.
        """
        self.update_many(entities=[entity])

    def delete_many(self, keys: List[str]) -> None:
        """
        Deletes (archives) multiple entities by their keys.

        Args:
            keys (List[str]): A list of keys of the entities to delete (archive).
        """
        mappings = [
            {
                "key": key,
                "archived": True,
                "archived_at": datetime.now(),
            }
            for key in keys
        ]
        self._bulk_update_mappings(mappings=mappings)

    def delete(self, key: str) -> None:
        """
        Deletes (archives) a single entity by its key.

        Args:
            key (str): The key of the entity to delete (archive).
        """
        self.delete_many(keys=[key])
