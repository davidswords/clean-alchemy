import string

from abc import ABC, abstractmethod
from random import choice
from typing import Generic, List, Tuple, TypeVar

from src.data.rpo import BaseRPO
from src.domain.ent import BaseENT


RPO_TYPE = TypeVar("RPO_TYPE", bound=BaseRPO)
ENT_TYPE = TypeVar("ENT_TYPE", bound=BaseENT)


class BaseSRV(ABC, Generic[RPO_TYPE, ENT_TYPE]):
    def __init__(cls, rpo: RPO_TYPE) -> None:
        cls.rpo = rpo

    @staticmethod
    def _generate_key(length: int = 24) -> str:
        characters = string.ascii_letters + string.digits
        return "".join(choice(characters, k=length))

    @abstractmethod
    def _generate_metadata(self) -> dict:
        pass

    @abstractmethod
    def _create_ent_from_doc(self, doc: dict) -> ENT_TYPE:
        pass

    @abstractmethod
    def _update_ent_from_doc(self, ent: ENT_TYPE, doc: dict) -> ENT_TYPE:
        pass

    def create_many(self, docs: List[dict]) -> List[ENT_TYPE]:
        ents = [self._create_ent_from_doc(doc=doc) for doc in docs]
        return self.rpo.create_many(ents=ents)

    def create(self, doc: dict) -> ENT_TYPE:
        ent = self._create_ent_from_doc(doc=doc)
        return self.rpo.create(ent=ent)

    def retrieve(self, key: str) -> ENT_TYPE:
        return self.rpo.retrieve(key=key)

    def retrieve_many(self, keys: List[str]) -> List[ENT_TYPE]:
        return self.rpo.retrieve_many(keys=keys)

    def retrieve_all(self) -> List[ENT_TYPE]:
        return self.rpo.retrieve_all()

    def update_many(self, ents_docs: List[Tuple[ENT_TYPE, dict]]) -> List[ENT_TYPE]:
        ents = [self._update_ent_from_doc(ent=ent, doc=doc) for ent, doc in ents_docs]
        return self.rpo.update_many(ents=ents)

    def update(self, ent: ENT_TYPE, doc: dict) -> ENT_TYPE:
        ent = self._update_ent_from_doc(ent=ent, doc=doc)
        return self.rpo.update(ent=ent)

    def delete_many(self, keys: List[str]) -> List[ENT_TYPE]:
        return self.rpo.delete_many(keys=keys)

    def delete(self, key: str) -> ENT_TYPE:
        return self.rpo.delete(key=key)
