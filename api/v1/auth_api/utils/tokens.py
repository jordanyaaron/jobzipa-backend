from django.contrib.auth.tokens import PasswordResetTokenGenerator

class InviteStaffTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{True}"


invite_staff_token = InviteStaffTokenGenerator()
