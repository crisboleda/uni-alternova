from rest_framework import serializers


class ModelSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, source="uuid")

    class Meta:
        abstract = True
        exclude = ("uuid", "created_at", "updated_at")
