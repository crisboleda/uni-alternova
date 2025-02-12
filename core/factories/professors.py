import factory
from professors.models import Professor


class ProfessorFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Professor
