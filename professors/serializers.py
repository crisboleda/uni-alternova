from common.serializers import ModelSerializer
from professors import models
from users.serializers import UserSerializer


class ProfessorSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Professor
        exclude = ("uuid",)
