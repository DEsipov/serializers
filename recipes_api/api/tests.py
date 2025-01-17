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


class SmokeTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='admin')
        self.smoke = Smoke.objects.create(name='one', count=3, )

    def test_simple_serializer(self):
        serializer = SimpleSmokeSerializer(self.smoke)
        # Сериализация.
        print(serializer.data)

    def test_simple_serializer_create(self):
        data = {'name': 'some_name', 'count': 22}
        serializer = SimpleSmokeSerializer(data=data)
        is_valid = serializer.is_valid()
        # # Результат валидация,True или False
        print(is_valid)
        # # Здесь будут ошибки, при их наличии.
        print(serializer.errors)
        smoke = serializer.save()
        print(smoke)

    def test_simple_serializer_update(self):
        data = {'name': 'new_name'}
        serializer = SimpleSmokeSerializer(instance=self.smoke, data=data)
        is_valid = serializer.is_valid()
        print(is_valid)
        # Здесь будут ошибки.
        print(serializer.errors)
        serializer.save()
        print(serializer.data)

    def test_detail(self):
        url = reverse('smoke-detail', kwargs={'pk': self.smoke.id})
        print(url)
        # /api/v1/smoke/1/

        resp = self.client.get(url)

        print(resp.data)
        # {'id': 1, 'count': '3', 'name': 'one', 'created': '2023-10-09'}

    def test_list(self):
        url = reverse('smoke-list')
        print(url)
        # /api/v1/smoke/

        resp = self.client.get(url)

        print(resp.data)
        # [OrderedDict([('id', 1), ('name', 'one'), ('count', 3),
        # ('created', '2023-10-09')])]
        print(resp.data[0])
        print(resp.data[0].get('name'))

    def test_create(self):
        url = reverse('smoke-list')
        print(url)
        # /api/v1/smoke/

        data = {
            'name': 'new_text',
            'count': '77'
        }

        resp = self.client.post(url, data=data)

        print(resp.data)
        # {'id': 2, 'count': '77', 'name': 'new_text', 'created': '2023-10-09'}

    def test_update(self):
        url = reverse('smoke-detail', kwargs={'pk': self.smoke.id})
        print(url)
        # /api/v1/smoke/1/

        data = {
            'name': 'new_name',
            'count': '77777'
        }

        resp = self.client.patch(url, data=data,
                                 content_type='application/json')

        print(resp.data)
        # {'id': 2, 'count': '77', 'name': 'new_text', 'created': '2023-10-09'}


class TestCaseIngredient(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='admin')
        self.ingredient = Ingredient.objects.create(
            name='salt',
            measurement_unit='gr',
        )
        self.client.force_login(user=self.user)

    def test_list(self):
        url = reverse('ingredients-list')
        print(url)
        # /api/v1/ingredients/

        resp = self.client.get(url)

        print(resp.data)
        # [OrderedDict(
        # [('id', 1), ('name', 'salt'), ('measurement_unit', 'gr')])
        # ]


class RecipeTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Создаем клиента, с токеном.
        cls.admin = User.objects.create(username='lauren', email='l@l.ru')
        token, _ = Token.objects.get_or_create(user=cls.admin)

        # Авторизируем его.
        cls.client_admin = APIClient()
        cls.client_admin.force_authenticate(user=cls.admin,
                                            token=cls.admin.auth_token)

        # Тэги
        cls.tag = Tag.objects.create(name='обед', slug='dinner')

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='admin',
                                             first_name='Anton')
        self.ingredient = Ingredient.objects.create(
            # !!! Так делать фу, бяка, плохо !!! Только в целях демонстрации.
            id=1488,
            name='salt',
            measurement_unit='gr',
        )
        self.recipe = Recipe.objects.create(
            name='soup',
            author=self.user,
            text='some_text'
        )
        self.tag = Tag.objects.create(name='black', slug='black')
        self.tag2 = Tag.objects.create(name='white', slug='white')

        self.recipe.tags.add(self.tag)
        self.recipe.tags.add(self.tag2)

        self.ingredient_recipe = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            amount=100,
        )
        self.client.force_login(user=self.user)

    def test_list_auth_serializer(self):
        """Тест для наглядной работы сериалайзера."""
        url = reverse('recipes-list')

        resp = self.client_admin.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Ниже printЫ, чтобы посмотреть работу сериализаторов.
        # item = resp.data[0]

        # tags = item.get('tags')
        # print(tags)

        # ingredients = item.get('ingredients')
        # print(ingredients[0])

        # Здесь будет id объекта Ingredient.
        # print(ingredients[0].get('id'))
        # print(self.ingredient.id)

        # Автор.
        # print(item.get('author'))

    def test_list_not_auth(self):
        """Проверяем работу закрытого api для неавториз. пользователя."""
        url = reverse('recipes-list')

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_auth(self):
        """Проверяем работу закрытого api для авторизован. пользователя."""
        url = reverse('recipes-list')

        resp = self.client_admin.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        expected = resp.data[0].get('id')
        self.assertEqual(self.recipe.id, expected)

    def test_detail(self):
        """Инфа о конкретном объекте."""
        url = reverse('recipes-detail', args=(self.recipe.pk,))

        resp = self.client_admin.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.recipe.id, resp.data.get('id'))
        print(resp.data)

    def test_create_recipe(self):
        url = reverse('recipes-list')
        data = {
            "name": "Медовуха",
            "text": "Сварить",
            "tags": [self.tag.pk],
            "author": self.admin.pk,
        }

        resp = self.client_admin.post(url, data=data)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        print(resp.data)

    def test_update_recipe(self):
        """Тест обновления рецепта."""
        url = reverse('recipes-detail', args=(self.recipe.pk,))
        data = {
            "name": "Медовуха",
            "text": "Сварганить"
        }

        resp = self.client_admin.put(url, data=data)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data.get('name'), data['name'])
        print(resp.data)


class FavoriteTestCase(TestCase):

    def setUp(self) -> None:
        # Создаем клиента, с токеном.
        self.admin = User.objects.create(username='lauren',
                                         email='l@l.ru')
        token, _ = Token.objects.get_or_create(user=self.admin)

        # Авторизируем его.
        self.client_admin = APIClient()
        self.client_admin.force_authenticate(user=self.admin,
                                             token=self.admin.auth_token)

        self.client_auth = Client()
        self.recipe = Recipe.objects.create(
            name='soup',
            author=self.admin,
            text='some_text'
        )
        self.favorite = Favorite.objects.create(
            recipe=self.recipe,
            user=self.admin,
        )

    def test_list(self):
        url = reverse('favorites-list')
        print(url)
        # /api/v1/favorites/

        resp = self.client_admin.get(url)

        print(resp.data)
        print(resp.data[0]['user'])