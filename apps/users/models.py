from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid
import random
import string


def generate_random_suffix(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# =========================
# User Manager
# =========================
class UserManager(BaseUserManager):

    def generate_username(self, first_name, last_name=None):
        """Automatic username generator ensuring uniqueness"""
        base_username = first_name.lower()

        # Case 1: first + last name provided
        if last_name:
            base_username = f"{first_name.lower()}.{last_name.lower()}"
            # Try with underscore and hyphen variants if taken
            variants = [
                base_username,
                f"{first_name.lower()}_{last_name.lower()}",
                f"{first_name.lower()}-{last_name.lower()}",
            ]
        else:
            # Only first name
            variants = [base_username, f"_{base_username}"]

        for variant in variants:
            if not self.model.objects.filter(username=variant).exists():
                return variant

        # If all variants taken, append random suffix
        while True:
            username_candidate = f"{base_username}_{generate_random_suffix(8)}"
            if not self.model.objects.filter(username=username_candidate).exists():
                return username_candidate

    def create_user(self, email, first_name, last_name=None, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")

        email = self.normalize_email(email)
        if not username:
            username = self.generate_username(first_name, last_name)

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name or "",
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault("role", "STAFF")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, first_name, last_name, username, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault("role", "ADMIN")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_super_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, first_name, last_name, username, password, **extra_fields)


# =========================
# User Model
# =========================
class User(AbstractBaseUser, PermissionsMixin):

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        RECRUITER = "RECRUITER", "Recruiter"
        USER = "USER", "User"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.STAFF
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)  # kwa sasa wote ni staff
    is_super_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN