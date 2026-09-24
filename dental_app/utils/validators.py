"""Input validators — single copy shared by registration and user management."""
import re

PHONE_PATTERN = r"^09\d{9}$"          # Philippine mobile: 11 digits starting with 09
EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def validate_phone(phone_number: str) -> bool:
    return re.match(PHONE_PATTERN, phone_number) is not None


def validate_email(email: str) -> bool:
    return re.match(EMAIL_PATTERN, email) is not None
