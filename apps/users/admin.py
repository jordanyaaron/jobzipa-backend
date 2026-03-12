from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("-date_joined",)
    
    # Fields to display in the user list
    list_display = (
        "email",
        "username",
        "full_name",  # property from model
        "role",
        "is_staff",
        "is_active",
        "date_joined",
    )

    # Filters in the sidebar
    list_filter = (
        "role",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    # Searchable fields
    search_fields = (
        "email",
        "username",
        "first_name",
        "last_name",
    )

    # Fields that cannot be edited from admin
    readonly_fields = (
        "id",
        "date_joined",
        "last_login",
        "full_name",  # readonly property
    )

    # Sections in the edit user page
    fieldsets = (
        (None, {
            "fields": ("email", "username", "password")
        }),
        (_("Personal Info"), {
            "fields": ("first_name", "last_name")
        }),
        (_("Roles & Permissions"), {
            "fields": (
                "role",
                "is_active",
                "is_staff",
                "is_super_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        (_("Important Dates"), {
            "fields": ("last_login", "date_joined")
        }),
    )

    # Fields to show when adding a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",  # auto-generated username will still appear
                "first_name",
                "last_name",
                "role",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )