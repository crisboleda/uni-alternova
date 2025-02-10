from common.serializers import ModelSerializer
from students import models
from users.serializers import UserSerializer


class StudentSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Student
        exclude = ("uuid",)
