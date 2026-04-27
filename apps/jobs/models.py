import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class Job(models.Model):

    id = models.BigAutoField(primary_key=True)

    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    title = models.CharField(max_length=255)

    company_logo = models.URLField(
        max_length=1000,
        blank=True,
        null=True
    )

    company = models.CharField(max_length=255)

    biography = models.TextField(blank=True, null=True)

    description = models.TextField()

        description_summary = models.TextField(
        blank=True,
        null=True,
        max_length=300
    )

    company_code = models.CharField(
        max_length=50,
        db_index=True,
        blank=True,
        null=True
    )

    location = models.JSONField(blank=True, null=True)

    tags = models.JSONField(default=list, blank=True)

    job_type = models.CharField(max_length=2)

    job_mode = models.CharField(max_length=2)

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='jobs'
    )

    edit_info = models.JSONField(default=list, blank=True)

    application_link = models.URLField(
        max_length=500,
        blank=True,
        null=True
    )

    actual_date = models.DateTimeField(blank=True, null=True)

    deadline_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if not self.actual_date:
            self.actual_date = timezone.now().date()

        super().save(*args, **kwargs)



    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "description_summary",
            "company_code",
            "location",
            "job_type",
            "job_mode",
            "application_link",
        ]

        read_only_fields = [
            "company",
            "company_logo",
            "biography",
            "posted_by",
            "public_id",
            "created_at",
            "updated_at",
            "is_active",
        ]

    def create(self, validated_data):
        company_code = validated_data.get("company_code")

        # 🔥 CHUKUA DATA KUTOKA DB
        try:
            company = Company.objects.get(code=company_code)
        except Company.DoesNotExist:
            raise serializers.ValidationError({
                "company_code": "Invalid company code"
            })

        # 🔥 MAP DATA
        validated_data["company"] = company.name
        validated_data["company_logo"] = company.logo
        validated_data["biography"] = company.biography

        return super().create(validated_data)