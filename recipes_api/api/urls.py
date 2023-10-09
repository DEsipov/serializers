from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, SmokeViewSet, RecipesViewSet

v1_router = DefaultRouter()


v1_router.register('ingredients', IngredientViewSet, basename='ingredients')
v1_router.register('smoke', SmokeViewSet, basename='smoke')
v1_router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
