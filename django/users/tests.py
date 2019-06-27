from django.test import TestCase
from django.auth.models import User
from django.urls import reverse


class UserTests(TestCase):

    def create_user(self):
        self.testuser = User.objects.create(
            username='testuser',
            password='testuser',
        )
        super(UserTests, self).create_user()

    def test_created_user(self):
        self.assertEqual(self.testuser.username, 'testuser')
