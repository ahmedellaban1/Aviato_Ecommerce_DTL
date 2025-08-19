from django.core.exceptions import ValidationError
import re

def validate_file_size(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError("File size must be under 5MB.")


def validate_password_strength(password):
    """
    Validates that the password meets required strength:
    - At least 8 characters
    - At least one lowercase letter
    - At least one uppercase letter
    - At least one digit
    - At least one special character
    """
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

    if not re.match(pattern, password):
        raise ValidationError(
            "Password must be at least 8 characters long and include at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character (@$!%*?&)."
        )
