from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        "pk",
        "role",
        "username",
        "email",
        "first_name",
        "last_name",
        "password",
    )
    search_fields = ("username",)
    list_filter = (
        "email",
        "username",
    )
    list_editable = (
        "role",
        "username",
    )
    empty_value_display = "-пусто-"


admin.site.register(CustomUser, CustomUserAdmin)
