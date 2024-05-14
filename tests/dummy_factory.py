import factory

from tests.dummy_dao import DummyDAO

class DummyFactory(factory.Factory):
    class Meta:
        model = DummyDAO

    key = factory.Faker("uuid4")
    created_at = factory.Faker("date_time_this_year")
    updated_at = factory.Faker("date_time_this_month")
    archived = False
    name = factory.Faker("name")
    age = factory.Faker("random_int", min=1, max=100)