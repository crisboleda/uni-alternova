import factory
from subjects.models import Subject


class SubjectFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Subject
