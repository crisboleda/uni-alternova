from django.contrib import admin

from professors import models


@admin.register(models.Professor)
class ProfessorAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
