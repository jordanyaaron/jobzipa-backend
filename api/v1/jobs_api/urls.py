from django.urls import path, include
from .views import(
    JobCreateView,
    JobListView
)

urlpatterns = [
    path("create/", JobCreateView.as_view(), name="create-job"),
    path("jobs/", JobListView.as_view(), name="get-jobs"),
]