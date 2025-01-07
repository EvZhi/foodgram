from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.html import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Персональная информация'), {
            'fields': (
                'first_name', 'last_name', 'email', 'avatar', 'preview_avatar'
            )
        }),
        (('Права'), {
            'fields': (
                'is_active', 'is_staff',
                'is_superuser', 'groups',
                'user_permissions'
            ),
        }),
        (('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('preview_avatar',)

    @admin.display(description='Превью')
    def preview_avatar(self, user: User):
        if user.avatar:
            return mark_safe(f"<img src='{user.avatar.url}' height=100>")
        return 'Без изображения'


admin.site.unregister(Group)
