import string

from abc import ABC, abstractmethod
from random import sample
from typing import Generic, List, Tuple, TypeVar

from clean_alchemy import BaseRepo, BaseEntity


REPO_TYPE = TypeVar("REPO_TYPE", bound=BaseRepo)
ENTITY_TYPE = TypeVar("ENTITY_TYPE", bound=BaseEntity)


class BaseService(ABC, Generic[REPO_TYPE, ENTITY_TYPE]):
    def __init__(self, repo: REPO_TYPE) -> None:
        self.repo = repo

    @staticmethod
    def _generate_key(prefix: str = "", postfix: str = "", length: int = 24) -> str:
        characters = string.ascii_letters + string.digits
        return f"{prefix}{''.join(sample(characters, k=length))}{postfix}"

    @abstractmethod
    def _create_entity_from_doc(self, doc: dict) -> ENTITY_TYPE:
        pass

    @abstractmethod
    def _update_entity_from_doc(self, entity: ENTITY_TYPE, doc: dict) -> ENTITY_TYPE:
        pass

    def create_many(self, docs: List[dict]) -> List[ENTITY_TYPE]:
        entities = [self._create_entity_from_doc(doc=doc) for doc in docs]
        return self.repo.create_many(entities=entities)

    def create(self, doc: dict) -> ENTITY_TYPE:
        entity = self._create_entity_from_doc(doc=doc)
        return self.repo.create(entity=entity)

    def retrieve(self, key: str) -> ENTITY_TYPE:
        return self.repo.retrieve(key=key)

    def retrieve_many(self, keys: List[str]) -> List[ENTITY_TYPE]:
        return self.repo.retrieve_many(keys=keys)

    def retrieve_all(self) -> List[ENTITY_TYPE]:
        return self.repo.retrieve_all()

    def update_many(
        self, entities_docs: List[Tuple[ENTITY_TYPE, dict]]
    ) -> List[ENTITY_TYPE]:
        entities = [
            self._update_entity_from_doc(entity=entity, doc=doc)
            for entity, doc in entities_docs
        ]
        return self.repo.update_many(entities=entities)

    def update(self, entity: ENTITY_TYPE, doc: dict) -> ENTITY_TYPE:
        entity = self._update_entity_from_doc(entity=entity, doc=doc)
        return self.repo.update(entity=entity)

    def delete_many(self, keys: List[str]) -> None:
        return self.repo.delete_many(keys=keys)

    def delete(self, key: str) -> None:
        return self.repo.delete(key=key)
