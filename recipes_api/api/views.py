from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.serializers import (IngredientSerializer, SmokeSerializer,
                             RecipeListSerializer, TagSerializer)
from recipes.models import Ingredient, Smoke, Recipe, Tag


class SmokeViewSet(ModelViewSet):
    serializer_class = SmokeSerializer
    queryset = Smoke.objects.all()


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    pagination_class = None
    http_method_names = ['get']

    def get_queryset(self):
        # Пример, как доставать параметры из url, и использовать их.
        qs = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name__istartswith=name)
        return qs.all()


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = [IsAuthenticated, ]


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, ]