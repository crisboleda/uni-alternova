import factory
from students.models import Student
from core.factories.users import UserFactory


class StudentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Student
