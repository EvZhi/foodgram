import random

from faker import Faker

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class Command(BaseCommand):
    help = 'Создать 5 рецептов с рандомным текстом и именами.'

    def handle(self, *args, **kwargs):
        fake = Faker()
        # Создаём рецепты
        self.stdout.write("Создание рецептов...")
        users = User.objects.all()
        for i in range(1, 6):  # 5 рецептов
            author = random.choice(users)
            recipe_name = fake.sentence(nb_words=2)
            recipe = Recipe.objects.create(
                name=recipe_name,
                author=author,
                cooking_time=random.randint(10, 60),
                text=fake.text(),
            )
            tags = Tag.objects.all()
            if tags.exists():
                recipe.tags.add(random.choice([tag for tag in tags]))
            else:
                self.stdout.write(
                    'Тэги не обнаружены, загрузите их используя команду: '
                    '"python manage.py import_tags"'
                )
                break
            ingredients = Ingredient.objects.all()
            if ingredients.exists():
                recipe.ingredients.add(
                    random.choice(
                        [ingredient for ingredient in ingredients]),
                    through_defaults={'amount': random.randint(1, 10)}
                )
            else:
                self.stdout.write(
                    'Ингредиенты не обнаружены, '
                    'загрузите их используя команду: '
                    '"python manage.py import_ingredients"'
                )
                break
            self.stdout.write(f'Создан рецепт №{i}')
        recipes_count = Recipe.objects.count()
        if recipes_count == 5:
            self.stdout.write(self.style.SUCCESS(
                'Тестовые данные успешно созданы.'
            ))
        elif recipes_count > 5:
            self.stdout.write(self.style.SUCCESS(
                f'Тестовые данные успешно созданы. '
                f'На данный момент в базе {recipes_count} рецептов.'
            ))
        else:
            self.stdout.write(self.style.ERROR(
                'Тестовые данные не созданы.'
            ))
