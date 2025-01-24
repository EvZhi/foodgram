from faker import Faker

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = ('Создать базовых пользователей: '
            'суперпользователь, администратор и обычный пользователь')

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Создаём суперпользователя
        self.stdout.write("Создание суперпользователя...")
        User.objects.create_superuser(
            username='superuser',
            email='superuser@example.com',
            password='super12345',
            first_name='Super',
            last_name='User'
        )
        self.stdout.write(self.style.SUCCESS(
            "Суперпользователь создан: superuser@example.com / super12345"))

        # Создаём администратора
        self.stdout.write("Создание администратора...")
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin12345',
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        admin.is_staff = True  # Устанавливаем статус администратора
        admin.save()
        self.stdout.write(self.style.SUCCESS(
            "Администратор создан: admin@example.com / admin12345"))

        # Создаём обычного пользователя
        self.stdout.write("Создание обычного пользователя...")
        User.objects.create_user(
            username='user',
            email='user@example.com',
            password='user12345',
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        self.stdout.write(self.style.SUCCESS(
            "Обычный пользователь создан: user@example.com / user12345"))

        self.stdout.write(self.style.SUCCESS(
            "Все базовые пользователи успешно созданы."))
