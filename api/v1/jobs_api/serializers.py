from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.jobs.models import Job

class JobSerializer(serializers.ModelSerializer):
    company_logo = serializers.ImageField(
        write_only=True,
        required=False
    )
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = [
            "posted_by",
            "public_id",
            "created_at",
            "updated_at",
            "is_active",
        ]