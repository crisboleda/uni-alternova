
from django.contrib import admin
from subjects import models


@admin.register(models.SubjectStatus)
class SubjectStatusAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
