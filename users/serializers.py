from common.serializers import ModelSerializer
from users import models


class UserSerializer(ModelSerializer):

    class Meta:
        model = models.User
        exclude = (
            "uuid",
            "password",
            "email",
        )
