from django.contrib import admin

from users import models


@admin.register(models.UserGender)
class UserGenderAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
