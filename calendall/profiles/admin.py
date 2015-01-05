from django.contrib import admin

from .models import CalendallUser


class CalendallUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "first_name", "last_name",
                    "is_superuser")
    readonly_fields = ("reset_token",)

admin.site.register(CalendallUser, CalendallUserAdmin)
