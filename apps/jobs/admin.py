from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "company",
        "job_type",
        "job_mode",
        "is_active",
        "created_at",
    )

    list_filter = (
        "job_type",
        "job_mode",
        "is_active",
        "company_code",
        "created_at",
    )

    search_fields = (
        "title",
        "company",
        "description",
    )

    readonly_fields = (
        "id",
        "public_id",
        "created_at",
        "updated_at",
        "edit_info",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": (
                "title",
                "company",
                "company_logo",
                "biography",
                "description",
            )
        }),
        ("Job Details", {
            "fields": (
                "job_type",
                "job_mode",
                "location",
                "tags",
            )
        }),
        ("Application", {
            "fields": (
                "application_link",
            )
        }),
        ("Dates", {
            "fields": (
                "actual_date",
                "deadline_date",
                "created_at",
                "updated_at",
            )
        }),
        ("System", {
            "fields": (
                "id",
                "public_id",
                "posted_by",
                "is_active",
            )
        }),
    )