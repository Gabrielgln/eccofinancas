from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class AuthTests(TestCase):
    #Teste de criação de usuário
    def test_create_user(self):
        user = User.objects.create_user(
            username = "test_user",
            email = "test_email",
            first_name = "test_first_name",
            password= "test_password"
        )

        self.assertEqual(user.username, "test_user")
        self.assertTrue(user.check_password("test_password"))
    #Teste de criação de usuário + autenticação do mesmo
    def test_authenticate(self):
        user = User.objects.create_user(
            username = "test_user",
            email = "test_email",
            first_name = "test_first_name",
            password= "test_password"
        )

        authenticate_user = authenticate(
            username = "test_user",
            password = "test_password"
        )

        self.assertIsNotNone(authenticate_user)

