from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from collections import OrderedDict
from .models import Todo


class SigninTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse((user is not None) and user.is_authenticated)


class TodoTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()
        self.todo = Todo(owner=self.user, title='Zakupy', description='chleb wino kobiety')
        self.todo.save()

    def tearDown(self):
        self.user.delete()

    def test_read_todo(self):
        self.assertEqual(self.todo.owner, self.user)
        self.assertEqual(self.todo.title, 'Zakupy')
        self.assertEqual(self.todo.description, 'chleb wino kobiety')

    def test_update_task_title(self):
        self.todo.title = 'Nowy tytuł'
        self.todo.save()
        self.assertEqual(self.todo.title, 'Nowy tytuł')

    def test_update_task_description(self):
        self.todo.description = 'Nowy opis'
        self.todo.save()
        self.assertEqual(self.todo.description, 'Nowy opis')


class TodoListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def tearDown(self):
        self.user.delete()

    def test_no_todos(self):
        response = self.client.get('/api/todos/')
        self.assertEqual(response.data, [])
