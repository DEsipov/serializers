# TODO

# Обычные поля, текcт, строка, число, время-дата, slug.

# Связанные поле. Related.

# Поля m2m.

# Валидация в сериализаторах.

# Получение kwargs и флильтр
from rest_framework import serializers

from recipes.models import Ingredient, Smoke


class SimpleSmokeSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()


class SmokeSerializer(serializers.ModelSerializer):
    """Сериазайзер для обычной модели."""
    # Какой формат здесь укажем, такой и будет в данных.
    count = serializers.CharField()

    class Meta:
        model = Smoke
        fields = '__all__'
        excludes = ('id', )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
