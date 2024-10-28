from rest_framework.routers import DefaultRouter

from .apis import IngredientViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)