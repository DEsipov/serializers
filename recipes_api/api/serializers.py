# TODO

# Связанные поле. Related.

# Поля m2m.

# Получение kwargs и флильтр
from rest_framework import serializers

from recipes.models import Ingredient, Smoke


class SimpleSmokeSerializer(serializers.Serializer):
    """Обычный сериализатор для объекта, сырой, без заморочек."""
    name = serializers.CharField(max_length=32)
    count = serializers.IntegerField(required=False)

    def create(self, validated_data):
        """Meтод создания объекта из данных"""
        return Smoke(**validated_data)

    def update(self, instance, validated_data):
        # Метод обновления объекта.
        instance.name = validated_data.get('name', instance.name)
        instance.count = validated_data.get('count', instance.count)
        instance.save()
        return instance


class SmokeSerializer(serializers.ModelSerializer):
    """Сериазайзер для обычной модели."""
    # Какой формат здесь укажем, такой и будет в данных.
    count = serializers.CharField()

    class Meta:
        model = Smoke
        fields = '__all__'
        excludes = ('id', )


class IngredientSerializer(serializers.ModelSerializer):
    # Отдельная валидация, вне зависимости от модели.
    name = serializers.CharField(max_length=32, verbose_name='Название')

    class Meta:
        model = Ingredient
        fields = '__all__'

    def validate_name(self, value):
        """Валидация на уровене поля."""
        if value == 'sugar':
            raise serializers.ValidationError('sugar is evil')
        return value

    def validate(self, data):
        """Валидация на уровне объекта."""
        name = data.get('name')
        unit = data.get('measurement_unit')

        if name == 'salt' and not unit == 'km':
            raise serializers.ValidationError('Not Good!')
        return data


