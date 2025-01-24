from django.core.management.base import BaseCommand

from ingredients.management.commands.import_ingredients import \
    Command as ImportIngredientsCommand
from recipes.management.commands.create_test_recipes import \
    Command as ImportRecipesCommand
from tags.management.commands.import_tags import Command as ImportTagsCommand
from users.management.commands.create_test_users import \
    Command as CreateTestUsersCommand


class Command(BaseCommand):
    help = 'Загрузка всех данных'

    def handle(self, *args, **kwargs):
        import_tags_command = ImportTagsCommand()
        import_tags_command.handle(*args, **kwargs)

        import_ingredients_command = ImportIngredientsCommand()
        import_ingredients_command.handle(*args, **kwargs)

        create_test_users_command = CreateTestUsersCommand()
        create_test_users_command.handle(*args, **kwargs)

        import_recipes_command = ImportRecipesCommand()
        import_recipes_command.handle(*args, **kwargs)

        self.stdout.write(self.style.SUCCESS('Все данные успешно загружены!'))
