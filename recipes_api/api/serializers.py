# TODO

# Связанные поле. Related.

# Поля m2m.

# Получение kwargs и флильтр
from rest_framework import serializers

from recipes.models import (Ingredient, Smoke, Tag, RecipeIngredient, Recipe,
                            User, Favorite)


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
    # name = serializers.CharField(max_length=3)

    class Meta:
        model = Smoke
        # exclude = ('id', )
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    # Отдельная валидация, вне зависимости от модели.
    name = serializers.CharField(max_length=32)

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


####### Сериализатор внутри сериализатора
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'name', 'measurement_unit', 'id')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения списка рецептов."""
    ingredients = serializers.SerializerMethodField()
    # tags = serializers.PrimaryKeyRelatedField(many=True,
    #                                           queryset=Tag.objects.all())
    # tags = serializers.SlugRelatedField(many=True, slug_field='slug',
    #                                     queryset=Tag.objects.all())

    tags = TagSerializer(many=True)

    # PrimaryKeyRelatedField это по умолчанию.
    # Это по желанию.
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False)

    def get_ingredients(self, obj):
        qs = RecipeIngredient.objects.filter(recipe=obj).all()
        return RecipeIngredientSerializer(qs, many=True).data

    class Meta:
        model = Recipe
        fields = '__all__'
        # Можно указать поле, только для чтения.
        # read_only = ('author', )


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        # read_only=True,
    )
    user_slug = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        source='user',
        # read_only=True,
    )
    user_string = serializers.StringRelatedField(
        # queryset=User.objects.all(),
        source='user',
    )

    class Meta:
        model = Favorite
        fields = '__all__'
        # Можно указать поле, только для чтения.
        # read_only = ('user', 'user_slug')
        # read_only = ('user', )