#!-*-coding:utf-8-*-
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


User = get_user_model()


class TestCasePost(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='admin')
        self.other = User.objects.create_user(username='other')
        self.post = Post.objects.create(
            author=self.user,
            text='Hello',
        )
        self.client.force_login(user=self.user)

    def test_list(self):
        url = reverse('posts-list')

        resp = self.client.get(url)

        print(resp.data)

    def test_detail(self):
        url = reverse('posts-detail', kwargs={'pk': self.post.id})

        resp = self.client.get(url)

        print(resp.data)

    def test_create(self):
        url = reverse('posts-list')
        data = {
            'text': 'new_text',
            'author': self.other.pk,
        }

        resp = self.client.post(url, data=data)

        print(resp.data)
        print(Post.objects.count())
