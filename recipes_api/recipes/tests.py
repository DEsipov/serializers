#!-*-coding:utf-8-*-
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.serializers import SimpleSmokeSerializer
from recipes.models import (Ingredient, Smoke, Tag, RecipeIngredient, Recipe,
                            Favorite)

User = get_user_model()


class ModelTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='admin', first_name='Anton')

        self.recipe = Recipe.objects.create(
            name='soup',
            author=self.user,
            text='some_text'
        )

        self.ingredient = Ingredient.objects.create(
            name='salt',
            measurement_unit='gr',
        )
        self.ingredient2 = Ingredient.objects.create(
            name='sugar',
            measurement_unit='gr',
        )

    def test_m2m(self):
        # Создание.
        self.tag = Tag.objects.create(name='black', slug='black')
        self.tag2 = Tag.objects.create(name='white', slug='white')

        # Добавление.
        self.recipe.tags.add(self.tag)
        self.recipe.tags.add(self.tag2)

        # Получение.
        res = self.recipe.tags.all()
        print(res)

        # Удаление.
        self.recipe.tags.remove(self.tag)
        print(res)

        # Очищение.
        self.recipe.tags.clear()
        print(res)

    def test_m2m_through(self):
        # Добавление.
        ingredient_recipe = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            amount=100,
        )
        # Еще добавление.
        self.recipe.ingredients.add(self.ingredient2)

        # Получение.
        res = self.recipe.ingredients.all()
        print(res)

        # Удаление.
        self.recipe.ingredients.remove(self.ingredient)
        print(res)

        # Очищение.
        self.recipe.ingredients.clear()
        print(res)
