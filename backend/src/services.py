import shortuuid

from django.shortcuts import get_object_or_404, redirect
from recipes.models import RecipeIngredient, ShortLink

LENGTH_SHORT_LINK = 7


def recipe_ingredient_bulk_create(recipe, ingredients_data):
    recipe_ingredients_to_create = [
        RecipeIngredient(
            recipe=recipe,
            ingredient_id=ingredient_data["ingredient"]["id"],
            amount=ingredient_data['amount'])
        for ingredient_data in ingredients_data
    ]
    RecipeIngredient.objects.bulk_create(recipe_ingredients_to_create)


def get_or_create_short_link(recipe):
    if not hasattr(recipe, 'shortlink'):
        short_link = shortuuid.uuid()[:LENGTH_SHORT_LINK]
        ShortLink.objects.create(recipe=recipe, short_link=short_link)
        return short_link
    return recipe.shortlink.short_link


def redirection(request, short_url):
    """Перенаправляем пользователя по ссылке"""
    short_link = get_object_or_404(ShortLink, short_link=short_url)
    return redirect(f"/recipes/{short_link.recipe.id}")

# Оставил на память для себя
# def annotate_qs_is_favorited_field(obj, queryset):
#     subquery = Favorite.objects.filter(
#         user=obj.request.user,
#         recipe=OuterRef('pk')
#     )
#     queryset = queryset.annotate(is_favorited=Exists(subquery))
#     return queryset


# def annotate_qs_is_subscribed_field(obj, queryset):
#     subquery = Subscription.objects.filter(
#         user=obj.request.user,
#         subscription=OuterRef('pk')
#     )
#     queryset = queryset.annotate(is_subscribed=Exists(subquery))
#     return queryset


# def annotate_qs_is_in_shopping_cart(obj, queryset):
#     subquery = ShoppingCart.objects.filter(
#         user=obj.request.user,
#         recipe=OuterRef('pk')
#     )
#     queryset = queryset.annotate(is_in_shopping_cart=Exists(subquery))
#     return queryset
