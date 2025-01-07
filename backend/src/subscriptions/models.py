from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Подписчик, текущий пользователь',
        related_name='subscribers',
    )
    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='subscriptions',
    )

    def __str__(self):
        return f'{self.user.username} подписан на {self.subscription.username}'

    def clean(self):
        if self.user == self.subscription:
            raise ValidationError('Нельзя подписаться на самого себя.')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'subscription'),
                name='unique_subscriptions'
            ),
        ]
