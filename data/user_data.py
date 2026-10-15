import random
import string


def generate_unique_user() -> dict:
    email_suffix = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=10)
    )
    name_suffix = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=6)
    )
    return {
        "email": f"{email_suffix}@example.com",
        "password": "securePassword123",
        "name": f"User_{name_suffix}",
    }


REQUIRED_REGISTRATION_FIELDS = ["email", "password", "name"]

UPDATABLE_USER_FIELDS_IN_RESPONSE = [
    ("email", "updated_email@example.com"),
    ("name", "Updated Name"),
]

NEW_PASSWORD = "updatedSecurePassword456"

WRONG_EMAIL = "wrong@example.com"
WRONG_PASSWORD = "wrongPassword123"