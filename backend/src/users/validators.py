from django.core.exceptions import ValidationError


def validate_username_not_me(value):
    if value == 'me':
        raise ValidationError(
            f"Использовать имя '{value}' " "в качестве username запрещено."
        )
