from django.utils import timezone


def default_deadline(days=30):
    return timezone.now().date() + timezone.timedelta(days=days)