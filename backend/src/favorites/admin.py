from django.contrib import admin

from .models import Favorite

EMPTY_MSG = '-пусто-'


@admin.register(Favorite)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'recipe'
    )
    empty_value_display = EMPTY_MSG
