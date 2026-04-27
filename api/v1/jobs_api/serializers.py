from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.jobs.models import Job
from django.utils import timezone
from datetime import datetime , time
from django.db.models import Q



class JobCreateSerializer(serializers.ModelSerializer):

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
            "actual_date",
            "deadline_date",
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

        request = self.context.get("request")
        user = request.user

        company_code = validated_data.get("company_code")

        # =========================
        # 🔥 COMPANY RESOLUTION
        # =========================

        jobs_with_code = Job.objects.filter(company_code=company_code)

        if not jobs_with_code.exists():
            raise serializers.ValidationError({
                "company_code": "Invalid company code"
            })

        job_source = jobs_with_code.first()

        validated_data["company"] = job_source.company
        validated_data["company_logo"] = job_source.company_logo
        validated_data["biography"] = job_source.biography

        # =========================
        # 🔥 DATE LOGIC (IMPORTANT FIX)
        # =========================
        now = timezone.now()

        actual_date = validated_data.get("actual_date")

        if actual_date:
            actual_date = datetime.combine(actual_date, now.time())
        else:
            actual_date = now

        deadline_date = validated_data.get("deadline_date")

        if deadline_date:
            deadline_date = datetime.combine(deadline_date, time(0 , 0))

        validated_data["actual_date"] = actual_date
        validated_data["deadline_date"] = deadline_date

        # =========================
        # 🔥 ACTIVE LOGIC
        # =========================
        if user.is_superuser or getattr(user, "is_super_staff", False):
            validated_data["is_active"] = True
        else:
            validated_data["is_active"] = False

        # =========================
        # 🔥 POSTED BY
        # =========================
        validated_data["posted_by"] = user

        # =========================
        # SAVE JOB
        # =========================
        return super().create(validated_data)


class JobSerializer(serializers.ModelSerializer):
    company_logo = serializers.SerializerMethodField()  # 👈 for output only

    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = [
            "posted_by",
            "public_id",
            "created_at",
            "updated_at",
            "is_active",
            "company_logo"  # 👈 muhimu
        ]

    def get_company_logo(self, obj):
        return obj.company_logo