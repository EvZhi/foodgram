import django_filters
from django.contrib.auth import get_user_model

from ingredients.models import Ingredient
from rest_framework.filters import SearchFilter
from recipes.models import Recipe
from tags.models import Tag

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)

# class IngredientFilter(SearchFilter):
#     search_param = 'name'


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        label='Автор'
    )

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        label='Теги',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        label='В корзине.',
        method="filter_is_in_shopping_cart"
    )
    is_favorited = django_filters.BooleanFilter(
        label='В избранных.',
        method="filter_is_favorited"
    )

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(in_shopping_cart__user=user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(favorites__user=user)
        return queryset


# class RecipeFilter(FilterSet):
#     tags = django_filters.ModelMultipleChoiceFilter(field_name='tags__slug',
#                                              to_field_name='slug',
#                                              queryset=Tag.objects.all())
#     is_favorited = filters.BooleanFilter(
#         method='is_favorited_filter')
#     is_in_shopping_cart = filters.BooleanFilter(
#         method='is_in_shopping_cart_filter')

#     class Meta:
#         model = Recipe
#         fields = ('tags', 'author',)

#     def is_favorited_filter(self, queryset, name, value):
#         user = self.request.user
#         if value and user.is_authenticated:
#             return queryset.filter(favorite_recipe__user=user)
#         return queryset

#     def is_in_shopping_cart_filter(self, queryset, name, value):
#         user = self.request.user
#         if value and user.is_authenticated:
#             return queryset.filter(shopping_recipe__user=user)
#         return queryset

