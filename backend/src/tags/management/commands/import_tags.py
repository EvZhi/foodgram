import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from tags.models import Tag


class Command(BaseCommand):

    help = 'Загрузка ингредиентов из csv файла'

    def create_tags(self, csv_reader):
        if not Tag.objects.exists():
            ingredients_to_create = [
                Tag(name=row[0], slug=row[1])
                for row in csv_reader
            ]
            Tag.objects.bulk_create(ingredients_to_create)

    def handle(self, *args, **kwargs):
        csv_file_path = settings.BASE_DIR.parent / 'data' / 'tags.csv'
        with open(csv_file_path, 'r', encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            self.create_tags(csv_reader)
            self.stdout.write(self.style.SUCCESS('Все теги загружены!'))
