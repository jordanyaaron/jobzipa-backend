from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import (
    LoginView , 
    InviteStaffView , CompleteStaffRegistrationView
)

urlpatterns = [
    path("staff/invite/", InviteStaffView.as_view(), name="staff_invite"),
    path("staff/register/", CompleteStaffRegistrationView.as_view(), name="staff_register"),
    path("tokens/refresh/", TokenRefreshView.as_view(), name="auth-tokens"),
    path("login/", LoginView.as_view(), name="staff_login"),
]