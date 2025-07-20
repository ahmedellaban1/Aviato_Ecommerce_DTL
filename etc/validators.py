from django.core.exceptions import ValidationError

def validate_file_size(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError("File size must be under 5MB.")
