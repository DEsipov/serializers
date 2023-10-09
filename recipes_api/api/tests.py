#!-*-coding:utf-8-*-
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from api.serializers import SimpleSmokeSerializer
from recipes.models import Ingredient, Smoke

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
        # Результат валидация,True или False
        print(is_valid)
        # Здесь будут ошибки, при их наличии.
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
