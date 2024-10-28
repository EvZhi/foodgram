from rest_framework.routers import DefaultRouter
from .apis import TagViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet)
