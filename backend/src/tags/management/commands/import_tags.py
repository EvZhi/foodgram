import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from tags.models import Tag


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из csv файла'

    def create_tags(self, csv_reader):
        existing_slugs = set(Tag.objects.values_list('slug', flat=True))
        tags_to_create = []
        added_count = 0

        for row in csv_reader:
            if len(row) < 2 or not row[0].strip() or not row[1].strip():
                continue

            name = row[0].strip()
            slug = row[1].strip()
            if slug not in existing_slugs:
                tags_to_create.append(Tag(name=name, slug=slug))
                added_count += 1

        if tags_to_create:
            with transaction.atomic():
                Tag.objects.bulk_create(tags_to_create)     
        self.stdout.write(f"Добавлено {added_count} новых тегов.")

    def handle(self, *args, **kwargs):
        csv_file_path = settings.BASE_DIR.parent / 'data' / 'tags.csv'
        with open(csv_file_path, 'r', encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)  # Пропускаем заголовок (если есть)
            self.create_tags(csv_reader)
        self.stdout.write(self.style.SUCCESS('Все теги загружены!'))