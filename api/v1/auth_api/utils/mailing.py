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
    message = f"""
        
        Hello!

        We are so exited to invite you to join our team at {settings.FRONTEND_WEB_APP_NAME} 🚀 please tap the link below to complete registresion. \n
        {complete_registrasion_url}

        if you didn't request invitation please ignore this email.
        thank you!
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False
    )

    