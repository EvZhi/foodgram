from rest_framework.routers import DefaultRouter
from .apis import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
