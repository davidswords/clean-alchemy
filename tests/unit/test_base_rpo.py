import pytest
from pytest_mock import MockerFixture

from tests.dummy_factory import DummyFactory
from tests.dummy_rpo import DummyRPO


@pytest.fixture
def mock_db_session(mocker: MockerFixture):
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
    def test_convert_to_ent_successfully(self, dummy_repo, dummy_dao):
        # Arrange, Act
        ent = dummy_repo._to_ent(dao=dummy_dao)

        # Assert
        assert ent.key == dummy_dao.key
        assert ent.created_at == dummy_dao.created_at
        assert ent.updated_at == dummy_dao.updated_at
        assert ent.archived == dummy_dao.archived
        assert ent.name == dummy_dao.name
        assert ent.age == dummy_dao.age


class TestBaseRPOToDAOShould:
    def test_convert_to_dao_successfully(self, dummy_repo, dummy_ent):
        # Arrange, Act
        dao = dummy_repo._to_dao(ent=dummy_ent)

        # Assert
        assert dao.key == dummy_ent.key
        assert dao.created_at == dummy_ent.created_at
        assert dao.updated_at == dummy_ent.updated_at
        assert dao.archived == dummy_ent.archived
        assert dao.name == dummy_ent.name
        assert dao.age == dummy_ent.age


class TestBaseRPOCreateManyShould:
    def test_create_many(
        self,
        mocker: MockerFixture,
        dummy_repo,
        dummy_ent,
    ):
        # Arrange
        ent = dummy_ent
        mapping = ent.__dict__.copy()
        dummy_repo._to_mappings = mocker.MagicMock(return_value=[mapping])
        dummy_repo._bulk_insert_mappings = mocker.MagicMock()
        expected = [ent]

        # Act
        result = dummy_repo.create_many(ents=[ent])

        # Assert
        dummy_repo._to_mappings.assert_called_once_with(ents=[ent])
        dummy_repo._bulk_insert_mappings.assert_called_once_with(mappings=[mapping])
        assert result == expected


class TestBaseRPOCreateShould:
    def test_create_successfully(
        self,
        mocker: MockerFixture,
        dummy_repo,
        dummy_ent,
    ):
        # Arrange
        ent = dummy_ent
        dummy_repo.create_many = mocker.MagicMock(return_value=[ent])

        # Act
        dummy_repo.create(ent=ent)

        # Assert
        dummy_repo.create_many.assert_called_once_with(
            ents=[ent],
        )


class TestBaseRPORetrieve:
    def test_retrieve_successfully(self, mocker: MockerFixture, dummy_repo, dummy_ent):
        # Arrange
        dummy_repo._filter_by_keys = mocker.MagicMock(return_value=[dummy_ent])
        dummy_repo._to_ents = mocker.MagicMock(return_value=[dummy_ent])

        # Act
        result = dummy_repo.retrieve(key=dummy_ent.key)

        # Assert
        dummy_repo._filter_by_keys.assert_called_once_with(keys=[dummy_ent.key])
        dummy_repo._to_ents.assert_called_once_with(daos=[dummy_ent])
        assert result == dummy_ent


class TestBaseRPORetrieveMany:
    def test_retrieve_many(self, mocker: MockerFixture, dummy_repo, dummy_ent):
        # Arrange
        dummy_repo._filter_by_keys = mocker.MagicMock(return_value=[dummy_ent])
        dummy_repo._to_ents = mocker.MagicMock(return_value=[dummy_ent])

        # Act
        result = dummy_repo.retrieve_many(keys=[dummy_ent.key])

        # Assert
        dummy_repo._filter_by_keys.assert_called_once_with(keys=[dummy_ent.key])
        dummy_repo._to_ents.assert_called_once_with(daos=[dummy_ent])
        assert result == [dummy_ent]
