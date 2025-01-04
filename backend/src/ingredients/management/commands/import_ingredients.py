import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from ingredients.models import Ingredient


class Command(BaseCommand):

    help = 'Загрузка ингредиентов из csv файла'

    def create_ingredients(self, csv_reader):
        if not Ingredient.objects.exists():
            ingredients_to_create = [
                Ingredient(name=row[0], measurement_unit=row[1])
                for row in csv_reader
            ]
            Ingredient.objects.bulk_create(ingredients_to_create)

    def handle(self, *args, **kwargs):
        csv_file_path = settings.BASE_DIR.parent / 'data' / 'ingredients.csv'
        with open(csv_file_path, 'r', encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            self.create_ingredients(csv_reader)
            self.stdout.write(self.style.SUCCESS('Все ингридиенты загружены!'))
