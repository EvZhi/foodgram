import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from ingredients.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из CSV файла'

    def create_ingredients(self, csv_reader):
        existing_ingredients = set(
            Ingredient.objects.values_list('name', 'measurement_unit')
        )
        ingredients_to_create = []
        added_count = 0

        for row in csv_reader:
            if len(row) < 2 or not row[0].strip() or not row[1].strip():
                continue

            name = row[0].strip()
            measurement_unit = row[1].strip()
            if (name, measurement_unit) not in existing_ingredients:
                ingredients_to_create.append(
                    Ingredient(name=name, measurement_unit=measurement_unit)
                )
                added_count += 1

        if ingredients_to_create:
            with transaction.atomic():
                Ingredient.objects.bulk_create(ingredients_to_create)

        self.stdout.write(f"Добавлено {added_count} новых ингредиентов.")

    def handle(self, *args, **kwargs):
        csv_file_path = settings.BASE_DIR.parent / 'data' / 'ingredients.csv'
        with open(csv_file_path, 'r', encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)  # Пропускаем заголовок (если есть)
            self.create_ingredients(csv_reader)
        self.stdout.write(self.style.SUCCESS('Все ингредиенты загружены!'))
