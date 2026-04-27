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
                    "job_id": job.company_code,
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





