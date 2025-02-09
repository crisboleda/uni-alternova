from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(
        self,
        email,
        password,
        is_staff,
        is_superuser,
        is_active,
        **extra_fields
    ):
        """
        Creates and saves a User with the given username, email and password.
        """
        user = self.model(
            email=self.normalize_email(email).lower(),
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=timezone.now(),
            created_at=timezone.now(),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email=None, password=None, is_active=True, **extra_fields
    ):
        is_staff = extra_fields.pop('is_staff', False)
        is_superuser = extra_fields.pop('is_superuser', False)
        return self._create_user(
            email, password, is_staff, is_superuser, is_active, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email,
            password,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **extra_fields,
        )
