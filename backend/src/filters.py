import django_filters
from django.contrib.auth import get_user_model

from ingredients.models import Ingredient
from recipes.models import Recipe
from tags.models import Tag

User = get_user_model()


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


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

    is_favorited = django_filters.CharFilter(method="filter_is_favorited")

    is_in_shopping_cart = django_filters.CharFilter(
        method="filter_is_in_shopping_cart"
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value == '1':
                return queryset.filter(favorites__user=self.request.user)
            else:
                return queryset.exclude(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value == '1':
                return queryset.filter(shopping_list__user=self.request.user).distinct()
            else:
                return queryset.exclude(shopping_list__user=self.request.user).distinct()
        return queryset
