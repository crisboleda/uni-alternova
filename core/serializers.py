from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = None

        try:
            users = get_user_model().objects.all()
            for user_item in users:
                user = user_item if user_item.get_email() == email else None
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("Correo electrónico no encontrado")

        if not user:
            raise serializers.ValidationError("Correo electrónico no encontrado")

        if not user.check_password(password):
            raise serializers.ValidationError("Contraseña incorrecta")

        data = super().validate(attrs)
        return data
