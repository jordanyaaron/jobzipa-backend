from django.urls import path, include
from .views import(
    JobCreateView,
    JobListView,
    JobDetailView,
    JobCreateMoreView,
    JobFullUpdateView
)

urlpatterns = [
    path("create/", JobCreateView.as_view(), name="create-job"),
    path("create/more/", JobCreateMoreView.as_view(), name="create-more"),
    path("update/", JobFullUpdateView.as_view(), name="update-job"),
    path("get/", JobListView.as_view(), name="get-jobs"),
    path("<uuid:public_id>/", JobDetailView.as_view(), name="job-detail"),
]