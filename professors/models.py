import uuid

from django.db import models


class Professor(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        verbose_name=("created at"), auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=("updated at"), auto_now=True
    )
