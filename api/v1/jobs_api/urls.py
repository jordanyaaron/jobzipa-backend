from django.urls import path, include
from .views import(
    JobCreateView
)

urlpatterns = [
    path("create/", JobCreateView.as_view(), name="create-job"),
]