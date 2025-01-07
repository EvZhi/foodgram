from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from users.validators import validate_username_not_me


class User(AbstractUser):

    email = models.EmailField(
        verbose_name='Адрес эл. почты',
        max_length=254,
        unique=True,
        error_messages={
            'unique': 'Данный адрес уже используеться.'
        },
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.'
        },
        validators=[UnicodeUsernameValidator(), validate_username_not_me]
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150

    )

    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='users/',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    def __str__(self):
        return self.username
