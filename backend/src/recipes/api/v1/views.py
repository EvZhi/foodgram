from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from favorites.models import Favorite
from filters import RecipeFilter
from paginations import CustomPagination
from permissions import IsAuthorOrReadOnly
from recipes.models import Recipe, RecipeIngredient
from renders import CSVShopingCartDataRenderer
from services import get_or_create_short_link
from shopping_cart.models import ShoppingCart

from .serializers import (RecipeDownloadShoppingCartSerializer,
                          RecipeMiniSerializer, RecipieSerializer)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by('-created_at')
    serializer_class = RecipieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == 'favorite':
            return RecipeMiniSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = qs.select_related('author').prefetch_related(
                'tags', 'ingredients',
                'shopping_list', 'favorites', 'recipeingredient_set',

            )
            return qs
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def handle_add_remove(self, request, pk, model):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        recipe = self.get_object()

        if request.method == "DELETE":
            try:
                item = model.objects.get(user=user, recipe=recipe)
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except model.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        _, created = model.objects.get_or_create(user=user, recipe=recipe)
        if created:
            serializer = RecipeMiniSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'],permission_classes=[IsAuthenticated])
    def favorite(self, request, pk, *args):
        return self.handle_add_remove(request, pk, Favorite)

    @action(detail=True, methods=["GET"], url_path="get-link")
    def get_short_link(self, request, pk=None):
        recipe = self.get_object()
        short_link = get_or_create_short_link(recipe)
        short_url = request.build_absolute_uri(f"/s/{short_link}")
        return Response({"short-link": short_url},
                        status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="shopping_cart",
        permission_classes=[IsAuthenticated]

    )
    def shopping_cart(self, request, pk=None):
        return self.handle_add_remove(request, pk, ShoppingCart)

    @action(
        detail=False,
        methods=["GET"],
        renderer_classes=[CSVShopingCartDataRenderer],
        url_path="download_shopping_cart",
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user).values_list(
            'recipe', flat=True
        )
        qs = (
            RecipeIngredient.objects.filter(recipe__in=shopping_cart)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total_amount=Sum('amount'))
            .order_by('ingredient__name')
        )
        file_name = f'Shopping_list.{request.accepted_renderer.format}'
        serializer = RecipeDownloadShoppingCartSerializer(qs, many=True)
        return Response(
            serializer.data,
            headers={
                'Content-Disposition': f'attachment; filename="{file_name}"'
            }
        )
