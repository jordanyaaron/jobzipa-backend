from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated , AllowAny
from datetime import datetime , time
from django.utils import timezone
from apps.jobs.models import Job
from django.db.models import Q

from .utils.storage import upload_logo_to_bucket
from .utils.generators import generate_company_code

from .serializers import (
    JobSerializer , JobCreateSerializer
)
from rest_framework.permissions import BasePermission

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff


class JobCreateMoreView(APIView):
    permission_classes = [IsStaffUser]
    def post(self, request):

        serializer = JobCreateSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            job = serializer.save()

            return Response(
                {
                    "message": "Job created successfully",
                    "job_id": job.public_id,
                    "company_code": job.company_code,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class JobCreateView(APIView):

    permission_classes = [IsStaffUser]

    def post(self, request):

        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():

            user = request.user
            logo_file = request.FILES.get("company_logo")

            logo_url = None

            # =========================
            # 🔥 HANDLE LOGO UPLOAD
            # =========================
            if logo_file:
                logo_url = upload_logo_to_bucket(logo_file)

            # =========================
            # 🔥 DATE LOGIC
            # =========================
            actual_date = serializer.validated_data.get("actual_date")
            deadline_date = serializer.validated_data.get("deadline_date")

            now = timezone.now()

            if actual_date:
                actual_date = datetime.combine(actual_date, now.time())
            else:
                actual_date = now

            if deadline_date:
                deadline_date = datetime.combine(deadline_date, time(18, 0))

            # =========================
            # 🔥 ACTIVE LOGIC
            # =========================
            if user.is_superuser or getattr(user, "is_super_staff", False):
                is_active = True
            else:
                is_active = False

            # =========================
            # 🔥 COMPANY CODE GENERATION
            # =========================
            company_name = serializer.validated_data.get("company")
            company_code = generate_company_code(company_name)

            # =========================
            # 🔥 REUSE COMPANY DATA (IF EXISTS)
            # =========================
            existing_job = Job.objects.filter(company_code=company_code).first()

            if existing_job:
                # reuse existing company data
                company_name = existing_job.company
                logo_url = existing_job.company_logo
                biography = existing_job.biography
            else:
                # use new data from request
                biography = serializer.validated_data.get("biography")

            # =========================
            # 🔥 SAVE JOB
            # =========================
            job = serializer.save(
                posted_by=user,
                company=company_name,
                company_logo=logo_url,
                biography=biography,
                company_code=company_code,
                is_active=is_active,
                actual_date=actual_date,
                deadline_date=deadline_date
            )

            return Response(
                {
                    "message": "Job posted successfully",
                    "job_id": job.public_id,
                    "company_code": company_code
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class JobFullUpdateView(APIView):

    permission_classes = [IsStaffUser]

    def put(self, request, public_id):

        try:
            job = Job.objects.get(public_id=public_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=404)

        serializer = JobSerializer(job, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = request.user
        now = timezone.now()

        old_job = job  # snapshot before update

        # =========================
        # LOGO
        # =========================
        logo_file = request.FILES.get("company_logo")

        if logo_file:
            logo_url = upload_logo_to_bucket(logo_file)
        else:
            logo_url = job.company_logo

        # =========================
        # COMPANY CODE
        # =========================
        if not job.company_code:
            company_code = generate_company_code(
                serializer.validated_data.get("company") or job.company
            )
        else:
            company_code = job.company_code

        # =========================
        # DATE LOGIC
        # =========================
        input_actual = serializer.validated_data.get("actual_date")
        input_deadline = serializer.validated_data.get("deadline_date")

        is_actual = False
        is_deadline = False

        if input_actual:
            if job.actual_date and input_actual == job.actual_date.date():
                actual_date = job.actual_date
            else:
                actual_date = datetime.combine(input_actual, now.time())
                is_actual = True
        else:
            actual_date = job.actual_date

        if input_deadline:
            if job.deadline_date and input_deadline == job.deadline_date.date():
                deadline_date = job.deadline_date
            else:
                deadline_date = datetime.combine(input_deadline, time(18, 0))
                is_deadline = True
        else:
            deadline_date = job.deadline_date

        # =========================
        # ACTIVE
        # =========================
        is_active = True if (
            user.is_superuser or getattr(user, "is_super_staff", False)
        ) else job.is_active

        # =========================
        # SAVE FIRST
        # =========================
        updated_job = serializer.save(
            actual_date=actual_date,
            deadline_date=deadline_date,
            company_logo=logo_url,
            is_active=is_active,
            company_code=company_code,
            posted_by=job.posted_by
        )

        # =========================
        # AUDIT LOG
        # =========================
        def serialize(v):
            return v.isoformat() if hasattr(v, "isoformat") else v

        TRACKED_FIELDS = [
            "title",
            "description",
            "description_summary",
            "company",
            "biography",
            "location",
            "tags",
            "job_type",
            "job_mode",
            "application_link",
            "company_logo",
            "company_code",
        ]

        changes = []

        for field in TRACKED_FIELDS:
            old = getattr(old_job, field)
            new = getattr(updated_job, field)

            if old != new:
                changes.append({
                    "field": field,
                    "old": serialize(old),
                    "new": serialize(new),
                })

        if is_actual:
            changes.append({
                "field": "actual_date",
                "old": serialize(old_job.actual_date),
                "new": serialize(actual_date),
            })

        if is_deadline:
            changes.append({
                "field": "deadline_date",
                "old": serialize(old_job.deadline_date),
                "new": serialize(deadline_date),
            })

        # =========================
        # SAVE EDIT INFO
        # =========================
        if changes:
            edit_entry = {
                "by": user.id,
                "at": now.isoformat(),
                "changes": changes
            }

            updated_job.edit_info = (old_job.edit_info or []) + [edit_entry]
            updated_job.save(update_fields=["edit_info"])

        return Response({
            "message": "Job fully updated successfully"
        }, status=200)

class JobListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("search", "").strip()

        jobs = Job.objects.filter(is_active=True)

        if query:
            jobs = jobs.filter(
                Q(title__icontains=query) |
                Q(company__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )

        # 👇 Send Jobs
        jobs = jobs.order_by("-actual_date")

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
class JobDetailView(RetrieveAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

    lookup_field = "public_id"





