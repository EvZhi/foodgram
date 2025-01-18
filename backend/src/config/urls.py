from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from ingredients.api.v1.urls import router as ingredients_router
from recipes.api.v1.urls import router as recipes_router
from services import redirection
from tags.api.v1.urls import router as tags_router
from users.api.v1.urls import router as users_router

router = DefaultRouter()
router.registry.extend(tags_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(ingredients_router.registry)
router.registry.extend(recipes_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/base_auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    path("s/<str:short_url>/", redirection, name="redirect_short_link"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += (path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),)
