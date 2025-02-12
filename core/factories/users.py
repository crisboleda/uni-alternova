import factory
from factory.faker import Faker
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
