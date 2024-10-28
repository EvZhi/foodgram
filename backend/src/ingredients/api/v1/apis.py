from rest_framework.viewsets import ReadOnlyModelViewSet
from ingredients.models import Ingredient
from ingredients.api.v1.serializers import IngridientSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngridientSerializer
