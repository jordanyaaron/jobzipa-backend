from django.contrib.auth import get_user_model
import uuid
import random
import string

User = get_user_model()



# username generator
def generate_username(first_name, last_name=None):
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
            if not User.objects.filter(username=variant).exists():
                return variant

        # If all variants taken, append random suffix
        while True:
            username_candidate = f"{base_username}_{generate_random_suffix(8)}"
            if not User.objects.filter(username=username_candidate).exists():
                return username_candidate