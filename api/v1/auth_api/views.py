from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework.permissions import BasePermission


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

# serializers
from .serializers import (
    StaffRegisterSerializer, StaffLoginSerializer , 
    InviteStaffSerializer , 
    CompleteStaffRegistrationSerializer
)
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


# utils
from .utils.credentials import (
    generate_username
)

from .utils.tokens import (
    invite_staff_token
)

from .utils.mailing import (
    send_staff_invitation_email
)


User = get_user_model()



# variables
class InviteStaffView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request):
        serializer = InviteStaffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        username = generate_username("staff", "")
        # Check kama tayari yupo
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            if existing_user.is_active:
                return Response(
                    {"message": "User with this email {email} is active"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                # Delete unverified user so they can re-register
                existing_user.delete()


        user = User.objects.create(
            first_name="staff",
            last_name="",
            email=email,
            username=username,
            is_staff=True,
            is_active=False,
        )


        user.save()

        user = User.objects.filter(email=email).first()

        send_staff_invitation_email( user , request )

        return Response({"message": "Invitation sent successfully"})

class CompleteStaffRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")

        if not uid or not token:
            return Response(
                {"error": "Invalid link"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

        except Exception:
            return Response(
                {"error": "Invalid user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not invite_staff_token.check_token(user, token):
            return Response(
                {"error": "Token expired or invalid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CompleteStaffRegistrationSerializer(data=request.data)

        if serializer.is_valid():

            user.first_name = serializer.validated_data["first_name"]
            
            if "last_name" in serializer.validated_data:
                user.last_name = serializer.validated_data["last_name"]
            
            user.set_password(serializer.validated_data["password"])
            username = generate_username( user.first_name  , user.last_name  )
            user.username = username
            user.is_active = True

            user.save()

            return Response({
                "message": "Registration completed"
            })

        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔐 Only Superuser can register staff
class StaffRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:
            return Response(
                {"detail": "Only superuser can register staff."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = StaffRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Staff user created successfully."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔑 Staff Login
class StaffLoginView(APIView):
    permission_classes = [AllowAny]  # public endpoint

    def post(self, request):
        serializer = StaffLoginSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "first_name" : user.first_name,
                "last_name" : user.last_name ,
                "email": user.email,
                "username": user.username,
                "is_superuser": user.is_superuser,
                "is_admin": user.is_admin,
                "is_official": user.is_super_staff,
                "is_staff": user.is_staff,
            }
        })