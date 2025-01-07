from django.contrib import admin

from .models import ShoppingCart

EMPTY_MSG = '-пусто-'


@admin.register(ShoppingCart)
class SoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'recipe')
    empty_value_display = EMPTY_MSG
