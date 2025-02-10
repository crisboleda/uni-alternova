import uuid
from django.db import models


class SubjectStatus(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    name = models.CharField(verbose_name=("name"), max_length=120)
    code_name = models.CharField(max_length=30, verbose_name=("code name"), blank=True)

    class Meta:
        verbose_name = "subject status"

    def __str__(self):
        return self.name


class Subject(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    required_subjects = models.ManyToManyField(
        "subjects.Subject", verbose_name=("required subjects"), blank=True
    )
    name = models.CharField(verbose_name=("subject name"), max_length=80, blank=True)
    description = models.CharField(
        verbose_name=("subject description"), max_length=120, blank=True
    )
    is_active = models.BooleanField(verbose_name=("is active?"), default=True)
    created_at = models.DateTimeField(verbose_name=("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=("updated at"), auto_now=True)

    def __str__(self):
        return self.name


class SubjectRegistration(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    subject = models.ForeignKey("subjects.Subject", on_delete=models.RESTRICT)
    student = models.ForeignKey("students.Student", on_delete=models.RESTRICT)
    professor = models.ForeignKey("professors.Professor", on_delete=models.RESTRICT)
    note = models.FloatField(verbose_name=("note"), default=0.0)
    status = models.ForeignKey("subjects.SubjectStatus", on_delete=models.RESTRICT)
    created_at = models.DateTimeField(verbose_name=("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=("updated at"), auto_now=True)
