from django.core.exceptions import ValidationError


def validate_username_not_me(value):
    forbidden_usernames = ('me',)
    if value.lower() in [name.lower() for name in forbidden_usernames]:
        raise ValidationError(
            ("Имя '%(value)s' запрещено для использования."),
            params={'value': value},
        )
