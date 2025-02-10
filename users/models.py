import uuid
from common import constants
from cryptography.fernet import Fernet
from core.settings import KEY_ENCRYPTION
from users.managers import UserManager

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import password_validation
from django.utils import timezone
from django.db import models


class UserGender(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    name = models.CharField(verbose_name=("name"), max_length=120)
    code_name = models.CharField(max_length=30, verbose_name=("code name"), blank=True)

    class Meta:
        verbose_name = "user gender"

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    email = models.EmailField(verbose_name=("email"), unique=True, max_length=255)
    first_name = models.CharField(
        verbose_name=("first name"), max_length=80, blank=True
    )
    last_name = models.CharField(verbose_name=("last name"), max_length=80, blank=True)
    legal_id_type = models.CharField(
        verbose_name=("legal ID type"),
        max_length=3,
        choices=constants.ID_LEGAL_TYPES,
        blank=True,
        null=True,
    )
    legal_id = models.CharField(
        max_length=20, verbose_name=("legal ID"), null=True, blank=True
    )
    gender = models.ForeignKey("users.UserGender", on_delete=models.SET_NULL, null=True)
    birth_date = models.DateField(verbose_name=("birth date"), null=True)
    is_active = models.BooleanField(verbose_name=("is active?"), default=True)
    is_staff = models.BooleanField(verbose_name=("staff"), default=False)
    created_at = models.DateTimeField(
        verbose_name=("registered at"), auto_now_add=timezone.now
    )
    updated_at = models.DateTimeField(verbose_name=("updated at"), auto_now=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        cipher_suite = Fernet(KEY_ENCRYPTION)

        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

        if self.email is not None:
            self.email = self.email.lower()
