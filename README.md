##### Запуск

1. Склонировать репо 
git clone git@github.com:DEsipov/serializers.git

1. Создать вирт. окружение.

1. Обновить pip
python -m pip install --upgrade pip

1. Установить зависимости из requirements.txt
pip install -r requirements.txt

1. Активировать окружение.

1. Применить миграции 
./manage.py migrate

1. Создать админка
./manage.py createsuperuser

1. Запустить сервер
./manage.py runserver


#### Как изспользовать http-запросы pycharm.


###### Создать токен, см. тест api.tests.RecipeTestCase.setUpClass

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

user = User.objects.get()
token, _ = Token.objects.get_or_create(user=user)
print(token.key)
```

###### Подставить token.key в заголовк Token.
Authorization: Token 0c73436bd884a502b6ea710cace9a5e633e0358b



#### Полезные ссылки

Шпора 
https://docs.google.com/document/d/195C3crfvMDfxL7GSxoKYyj1Pfnfx8zyPoEtmMD8JZQE/edit#heading=h.oe06q2t0a6zt

Доки сериализаторы
https://www.django-rest-framework.org/api-guide/serializers/
