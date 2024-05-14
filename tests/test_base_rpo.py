import pytest

from tests.dummy_factory import DummyFactory
from tests.dummy_rpo import DummyRPO

@pytest.fixture
def mock_db_session(mocker):
    return mocker.MagicMock()

@pytest.fixture
def dummy_repo(mock_db_session):
    return DummyRPO(db_session=mock_db_session)

@pytest.fixture
def dummy_dao():
    return DummyFactory.build()

@pytest.fixture
def dummy_ent(dummy_repo, dummy_dao):
    return dummy_repo._to_ent(dao=dummy_dao)

class TestBaseRPOToENTShould:
    def test__to_ent(self, dummy_repo, dummy_dao):
        # Arrange, Act
        ent = dummy_repo._to_ent(dao=dummy_dao)
        
        # Assert 
        assert ent.key == dummy_dao.key
        assert ent.created_at == dummy_dao.created_at
        assert ent.updated_at == dummy_dao.updated_at
        assert ent.archived == dummy_dao.archived
        assert ent.name == dummy_dao.name
        assert ent.age == dummy_dao.age

    def test__to_dao(self, dummy_repo, dummy_ent):
        dao = dummy_repo._to_dao(ent=dummy_ent)
        assert dao.key == dummy_ent.key
        assert dao.created_at == dummy_ent.created_at
        assert dao.updated_at == dummy_ent.updated_at
        assert dao.archived == dummy_ent.archived
        assert dao.name == dummy_ent.name
        assert dao.age == dummy_ent.age

    def test_create(self, dummy_repo, dummy_dao, dummy_ent):
        dummy_repo._bulk_insert_mappings = mocker.MagicMock()
        dummy_repo._to_daos = mocker.MagicMock(return_value=[dummy_dao])
        dummy_repo.create(ent=dummy_ent)
        dummy_repo._to_daos.assert_called_once_with(ents=[dummy_ent])
        dummy_repo._bulk_insert_mappings.assert_called_once_with(mappings=[dummy_dao.__dict__])

    def test_create_many(self, dummy_repo, dummy_dao, dummy_ent):
        dummy_repo._bulk_insert_mappings = mocker.MagicMock()
        dummy_repo._to_daos = mocker.MagicMock(return_value=[dummy_dao])
        dummy_repo.create_many(ents=[dummy_ent])
        dummy_repo._to_daos.assert_called_once_with(ents=[dummy_ent])
        dummy_repo._bulk_insert_mappings.assert_called_once_with(mappings=[dummy_dao.__dict__])

    def test_retrieve(self, dummy_repo, dummy_dao, dummy_ent):
        dummy_repo._filter_by_keys = mocker.MagicMock(return_value=[dummy_dao])
        dummy_repo._to_ents = mocker.MagicMock(return_value=[dummy_ent])
        ent = dummy_repo.retrieve(key=dummy_ent.key)
        dummy_repo._filter_by_keys.assert_called_once_with(keys=[dummy_ent.key])
        dummy_repo._to_ents.assert_called_once_with(daos=[dummy_dao])
        assert ent == dummy_ent

    def test_retrieve_many(self, dummy_repo, dummy_dao, dummy_ent):
        dummy_repo._filter_by_keys = mocker.MagicMock(return_value=[dummy_dao])
        dummy_repo._to_ents = mocker.MagicMock(return_value=[dummy_ent])
        ents = dummy_repo.retrieve_many(keys=[dummy_ent.key])
        dummy_repo._filter_by_keys.assert_called_once_with(keys=[dummy_ent.key])
        dummy_repo._to_ents.assert_called_once_with(daos=[dummy_dao])
        assert ents == [dummy_ent]