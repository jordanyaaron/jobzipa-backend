from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.v1.auth_api.urls")),
    path("users/", include("api.v1.users_api.urls")),
    path("jobs/", include("api.v1.jobs_api.urls")),
]