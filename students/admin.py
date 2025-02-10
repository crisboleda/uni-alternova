from django.contrib import admin

from students import models


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
