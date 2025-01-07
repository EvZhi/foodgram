from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Список id тегов')
    image = models.ImageField('Изображение блюда', upload_to='recipes/images/')
    name = models.CharField('Название', max_length=256)
    text = models.TextField('Описание')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(1)
        ],
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()


class ShortLink(models.Model):
    recipe = models.OneToOneField(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        primary_key=True
    )
    short_link = models.CharField(
        'Короткая ссылка', blank=True, null=True, max_length=10, unique=True
    )
