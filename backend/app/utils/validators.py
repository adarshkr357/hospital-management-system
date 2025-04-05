import re
from datetime import date
from typing import Tuple


def validate_email(email: str) -> bool:
    """
    Validate email format.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    """
    pattern = r"^\+?1?\d{9,15}$"
    return bool(re.match(pattern, phone))


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength.
    Returns (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"

    return True, "Password is strong"


def validate_date_format(date_str: str) -> bool:
    """
    Validate date string format (YYYY-MM-DD).
    """
    try:
        date.fromisoformat(date_str)
        return True
    except ValueError:
        return False


def sanitize_input(input_str: str) -> str:
    """
    Sanitize input string to prevent SQL injection and XSS.
    """
    # Remove special characters and HTML tags
    input_str = re.sub(r'[<>"/\'%;()&+]', "", input_str)
    return input_str.strip()


def validate_name(name: str) -> bool:
    """
    Validate person name format.
    """
    pattern = r"^[a-zA-Z\s\'-]{2,50}$"
    return bool(re.match(pattern, name))


def validate_blood_group(blood_group: str) -> bool:
    """
    Validate blood group format.
    """
    valid_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    return blood_group in valid_groups
