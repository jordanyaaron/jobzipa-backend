from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class InviteStaffSerializer(serializers.Serializer):
    email = serializers.EmailField()

# 🔐 Staff Register Serializer
class CompleteStaffRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=True,
        allow_blank=False
    )

    last_name = serializers.CharField(
        required=False,     # optional
        allow_blank=True   
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False
    )

# 🔐 Register Staff Serializer
class StaffRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        return User.objects.create_staffuser(**validated_data)


# 🔑 Login Serializer (STAFF ONLY)
class StaffLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data["email"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_staff:
            raise serializers.ValidationError("Access denied. Staff only.")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_superuser": user.is_superuser,
                "is_staff": True,
            }
        }


