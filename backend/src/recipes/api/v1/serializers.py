from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from favorites.models import Favorite
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredient
from services import recipe_ingredient_bulk_create
from shopping_cart.models import ShoppingCart
from tags.api.v1.serializers import TagSerializer
from tags.models import Tag
from users.api.v1.serializers import CustomUserSerializer


class RecipieIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', "measurement_unit", 'amount')


class RecipeDownloadShoppingCartSerializer(serializers.Serializer):
    ingredient__name = serializers.CharField(read_only=True)
    ingredient__measurement_unit = serializers.CharField(read_only=True)
    total_amount = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'ingredient_name', 'ingredient__measurement_unit', 'total_amount'
        )


class RecipieSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=True
    )
    ingredients = RecipieIngredientSerializer(
        source='recipeingredient_set', many=True, required=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError("Нужно добавить ингредиенты.")
        ingredient_ids = set()
        for ingredient in value:
            ingredient_id = ingredient["ingredient"]["id"]
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    "Количество ингирдиента должно быть больше нуля."
                )
            if ingredient_id in ingredient_ids:
                raise serializers.ValidationError(
                    "Ингредиенты не должны повторяться."
                )
            ingredient_ids.add(ingredient_id)
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError("Ингредиент не существует.")
        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError('Нужно добавить тег.')
        tags = set()
        for tag in value:
            if tag in tags:
                raise serializers.ValidationError(
                    'Тэги не должны повторяться.'
                )
            tags.add(tag)
        return value

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError(
                "Нужно добавить изображение."
            )
        return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        tags_data = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)
        recipe_ingredient_bulk_create(recipe, ingredients_data)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set', None)
        tags_data = validated_data.pop('tags', None)

        self.validate_ingredients(ingredients_data)
        self.validate_tags(tags_data)

        recipe = super().update(instance, validated_data)

        if tags_data:
            recipe.tags.set(tags_data)

        if ingredients_data:
            instance.recipeingredient_set.all().delete()
            recipe_ingredient_bulk_create(recipe, ingredients_data)
        return instance

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user,
                                           recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ShoppingCart.objects.filter(user=request.user,
                                               recipe=obj).exists()
        return False

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return ret


class RecipeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('name', 'image', 'cooking_time')
