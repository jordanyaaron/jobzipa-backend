from django.urls import path, include
from .views import(
    JobCreateView,
    JobListView,
    JobDetailView
)

urlpatterns = [
    path("create/", JobCreateView.as_view(), name="create-job"),
    path("create/more/", JobCreateView.as_view(), name="create-more"),
    path("get/", JobListView.as_view(), name="get-jobs"),
    path("<uuid:public_id>/", JobDetailView.as_view(), name="job-detail"),
]