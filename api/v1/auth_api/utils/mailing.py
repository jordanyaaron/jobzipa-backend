from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .tokens import (
    invite_staff_token
)

def send_staff_invitation_email(user, request):
    token = invite_staff_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    complete_registrasion_url = f"{settings.FRONTEND_URL}complete-registration?uid={uid}&token={token}"

    subject = "Complete Registration"
    message = (
        f"Hello!\n\n"
        f"We are so excited to invite you to join our team at {settings.FRONTEND_WEB_APP_NAME} 🚀.\n"
        f"Please tap the link below to complete registration:\n"
        f"{complete_registrasion_url}\n\n"
        f"If you didn't request this invitation, please ignore this email.\n"
        f"Thank you!"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False
    )

    