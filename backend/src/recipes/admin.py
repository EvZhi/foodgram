from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from favorites.models import Favorite

from .models import Recipe, RecipeIngredient

EMPTY_MSG = '-пусто-'


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    # autocomplete_fields = ('ingredient',)
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
        "favorite_count",
        "get_tags",
    )
    search_fields = [
        "author__username",
        "name",
    ]
    list_filter = [
        "tags",
    ]
    inlines = [RecipeIngredientInline]
    fieldsets = (
        (None, {"fields": ("name", "author", "tags")}),
        ("Описание", {"fields": ("text", "cooking_time", "image")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "author",
                    "tags",
                    "text",
                    "cooking_time",
                    "ingredients",
                    "image",
                ),
            },
        ),
    )
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }

    @admin.display(description='В избранном')
    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    @admin.display(description='Теги')
    def get_tags(self, obj):
        return ", ".join(
            obj.tags.values_list('name', flat=True).order_by('name')
        )


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     inlines = (RecipeIngredientInline,)
#     filter_horizontal = ('tags',)
