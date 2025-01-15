import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import User


@receiver(pre_save, sender=User)
def delete_old_avatar(sender, instance, **kwargs):
    """Удаляем старый аватар, если он заменяется новым."""
    if instance.pk:
        try:
            old_avatar = User.objects.get(pk=instance.pk).avatar
            if old_avatar and old_avatar != instance.avatar:
                if os.path.isfile(old_avatar.path):
                    os.remove(old_avatar.path)
        except User.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def delete_avatar_on_user_delete(sender, instance, **kwargs):
    """Удаляем аватар при удалении пользователя."""
    if instance.avatar and os.path.isfile(instance.avatar.path):
        os.remove(instance.avatar.path)
