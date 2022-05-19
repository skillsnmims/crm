from django.core.exceptions import ValidationError


def password_validator(value):
    if len(value) < 8:
        raise ValidationError("Password must have at least 8 characters!")
    elif value.isdigit():
        raise ValidationError("Password may not be numeric!")
    return True
