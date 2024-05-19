import string
from abc import ABC, abstractmethod
from random import sample
from typing import Generic, List, Tuple, TypeVar, Type

from clean_alchemy import BaseRepo, BaseEntity

REPO_TYPE = TypeVar("REPO_TYPE", bound=BaseRepo)
ENTITY_TYPE = TypeVar("ENTITY_TYPE", bound=BaseEntity)


class BaseService(ABC, Generic[REPO_TYPE, ENTITY_TYPE]):
    """
    A base service class providing common CRUD operations for repositories.

    Attributes:
        repo_class (Type[REPO_TYPE]): The repository class associated with the service.
        entity_class (Type[ENTITY_TYPE]): The entity class associated with the service.
        repo (REPO_TYPE): The repository instance used for data operations.
    """

    repo_class: Type[REPO_TYPE] = None
    entity_class: Type[ENTITY_TYPE] = None

    def __init__(self, repo: REPO_TYPE) -> None:
        """
        Initializes the BaseService with a given repository.

        Args:
            repo (REPO_TYPE): The repository instance to use for data operations.
        """
        self.repo = repo

    def __init_subclass__(cls) -> None:
        """
        Ensures that subclasses define repo_class and entity_class attributes.

        Raises:
            NotImplementedError: If repo_class or entity_class is not defined in the subclass.
        """
        if cls.repo_class is None:
            raise NotImplementedError("Must define a `repo_class` for a BaseService.")
        if cls.entity_class is None:
            raise NotImplementedError("Must define a `entity_class` for a BaseService.")

    @staticmethod
    def _generate_key(prefix: str = "", postfix: str = "", length: int = 24) -> str:
        """
        Generates a random key with optional prefix and postfix.

        Args:
            prefix (str): A string to be added at the beginning of the key. Default is an empty string.
            postfix (str): A string to be added at the end of the key. Default is an empty string.
            length (int): The length of the random part of the key. Default is 24.

        Returns:
            str: The generated key.
        """
        characters = string.ascii_letters + string.digits
        return f"{prefix}{''.join(sample(characters, k=length))}{postfix}"

    @abstractmethod
    def _create_entity_from_doc(self, doc: dict) -> ENTITY_TYPE:
        """
        Abstract method to create an entity from a dictionary.

        Args:
            doc (dict): The dictionary containing entity data.

        Returns:
            ENTITY_TYPE: The created entity.
        """
        pass

    @abstractmethod
    def _update_entity_from_doc(self, entity: ENTITY_TYPE, doc: dict) -> ENTITY_TYPE:
        """
        Abstract method to update an entity from a dictionary.

        Args:
            entity (ENTITY_TYPE): The entity to update.
            doc (dict): The dictionary containing updated entity data.

        Returns:
            ENTITY_TYPE: The updated entity.
        """
        pass

    def create_many(self, docs: List[dict]) -> List[ENTITY_TYPE]:
        """
        Creates multiple entities from a list of dictionaries.

        Args:
            docs (List[dict]): A list of dictionaries containing entity data.

        Returns:
            List[ENTITY_TYPE]: A list of created entities.
        """
        entities = [self._create_entity_from_doc(doc=doc) for doc in docs]
        return self.repo.create_many(entities=entities)

    def create(self, doc: dict) -> ENTITY_TYPE:
        """
        Creates a single entity from a dictionary.

        Args:
            doc (dict): The dictionary containing entity data.

        Returns:
            ENTITY_TYPE: The created entity.
        """
        entity = self._create_entity_from_doc(doc=doc)
        return self.repo.create(entity=entity)

    def retrieve(self, key: str) -> ENTITY_TYPE:
        """
        Retrieves an entity by its key.

        Args:
            key (str): The key of the entity to retrieve.

        Returns:
            ENTITY_TYPE: The retrieved entity.
        """
        return self.repo.retrieve(key=key)

    def retrieve_many(self, keys: List[str]) -> List[ENTITY_TYPE]:
        """
        Retrieves multiple entities by their keys.

        Args:
            keys (List[str]): A list of keys of the entities to retrieve.

        Returns:
            List[ENTITY_TYPE]: A list of retrieved entities.
        """
        return self.repo.retrieve_many(keys=keys)

    def retrieve_all(self) -> List[ENTITY_TYPE]:
        """
        Retrieves all entities.

        Returns:
            List[ENTITY_TYPE]: A list of all entities.
        """
        return self.repo.retrieve_all()

    def update_many(self, entities_docs: List[Tuple[ENTITY_TYPE, dict]]) -> None:
        """
        Updates multiple entities using a list of tuples containing entities and update data.

        Args:
            entities_docs (List[Tuple[ENTITY_TYPE, dict]]): A list of tuples where each tuple contains an entity and a
            dictionary of update data.
        """
        updated_entities = [
            self._update_entity_from_doc(entity=entity, doc=doc)
            for entity, doc in entities_docs
        ]
        self.repo.update_many(entities=updated_entities)

    def update(self, entity: ENTITY_TYPE, doc: dict) -> None:
        """
        Updates a single entity using a dictionary of update data.

        Args:
            entity (ENTITY_TYPE): The entity to update.
            doc (dict): The dictionary containing updated entity data.
        """
        updated_entity = self._update_entity_from_doc(entity=entity, doc=doc)
        self.repo.update(entity=updated_entity)

    def delete_many(self, keys: List[str]) -> None:
        """
        Deletes multiple entities by their keys.

        Args:
            keys (List[str]): A list of keys of the entities to delete.
        """
        self.repo.delete_many(keys=keys)

    def delete(self, key: str) -> None:
        """
        Deletes a single entity by its key.

        Args:
            key (str): The key of the entity to delete.
        """
        self.repo.delete(key=key)
