from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated , AllowAny
from datetime import datetime, time
from django.utils import timezone
from apps.jobs.models import Job
from django.db.models import Q

from .utils.storage import upload_logo_to_bucket

from .serializers import (
    JobSerializer
)
from rest_framework.permissions import BasePermission

class IsStaffUser(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff



class JobCreateView(APIView):

    permission_classes = [IsStaffUser]

    def post(self, request):

        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():

            user = request.user
            logo_file = request.FILES.get("company_logo")

            logo_url = None

            if logo_file:
                logo_url = upload_logo_to_bucket(logo_file)


            actual_date = serializer.validated_data.get("actual_date")
            deadline_date = serializer.validated_data.get("deadline_date")

            if actual_date:
                actual_date = datetime.combine(actual_date, time(0,0))
            
            if not actual_date:
                actual_date = deadline_date = timezone.now()

            if deadline_date:
                deadline_date = datetime.combine(deadline_date, time(18,0))

            if user.is_superuser or getattr(user, "is_super_staff", False):
                is_active = True
            else:
                is_active = False

            job = serializer.save(
                posted_by=user,
                company_logo=logo_url,
                is_active=is_active,
                actual_date=actual_date,
                deadline_date=deadline_date
            )

            return Response(
                {
                    "message": "Job posted successfully",
                    "job_id": job.public_id,
                    "company_logo": logo_url
                },
                status=status.HTTP_201_CREATED
            )


        return Response(serializer.errors, status=400)




class JobListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get("search", "").strip()

        jobs = Job.objects.filter(is_active=True)

        if query:
            jobs = jobs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )

        # 👇 IMPORTANT: usiweke none()
        jobs = jobs.order_by("-actual_date")

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
class JobDetailView(RetrieveAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

    lookup_field = "public_id"





